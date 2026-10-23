#!/usr/bin/env python3
"""guarda-segredos: hook PreToolUse do Claude Code para os sub-agentes do CLT-TEAM.

Bloqueia, por perfil, comandos e acessos que exibem segredos/ambiente ou que
alteram producao, e restringe onde cada perfil pode escrever.

Cobre Bash (comando) e Read/Edit/Write/Grep/Glob/NotebookEdit (caminho).
Nao cobre ferramentas MCP: para elas, use a lista fechada `tools` do agente.

Uso no frontmatter do agente:
  hooks:
    PreToolUse:
      - matcher: "Bash|Read|Edit|Write|Grep|Glob|NotebookEdit"
        hooks:
          - type: command
            command: "python3 \"$HOME/.claude/clt-team/hooks/guarda-segredos.py\" <perfil>"

Perfis: produto | qa | sre | marketing.
Saida 2 = bloqueia (a mensagem em stderr volta ao agente). Saida 0 = libera.

Pasta de handoffs: por padrao ~/.claude/clt-team/registros/handoffs/.
Para usar outra, defina CLT_TEAM_HANDOFFS com o caminho absoluto.

Autoteste: python3 guarda-segredos.py --teste

Este hook e uma barreira extra, nao uma garantia. Ele nao substitui o
principio do menor privilegio, a revisao humana nem os limites escritos
nos prompts dos agentes.
"""
import json
import os
import re
import sys

# Valem para todos os perfis: exibir segredos ou ambiente.
SEGREDOS = [
    (r"\brailway\s+(variables|vars|variable)\b", "listar variaveis da plataforma"),
    (r"\brailway\s+(run|shell|connect)\b", "comando que injeta variaveis no processo"),
    (r"\bheroku\s+(config|run)\b", "listar/injetar variaveis da plataforma"),
    (r"\b(fly|flyctl)\s+secrets\b", "segredos da plataforma"),
    (r"\b(vercel|netlify)\s+env\b", "variaveis da plataforma"),
    (r"\bkubectl\s+get\s+secrets?\b", "segredos do Kubernetes"),
    (r"\bprintenv\b", "printenv exibe o ambiente"),
    (r"(^|[;&|(]\s*|\bxargs\s+|\bsudo\s+)env\s*($|[;&|>)])", "env sem comando exibe o ambiente"),
    (r"(^|[;&|]\s*)(set|export(\s+-p)?|declare\s+-p?x?)\s*($|[;&|>])", "set/export/declare exibem o ambiente"),
    (r"/proc/[^\s]*/environ", "leitura de environ"),
    (r"(^|[\s/'\"=])\.env(?!\.(example|sample|template)\b)(\.[\w.-]+)?($|[\s'\";|&)])", "arquivo .env"),
    (r"\bgh\s+(secret|variable)\b", "segredos/variaveis do GitHub"),
    (r"\bsecurity\s+(find|dump)-", "Keychain do macOS"),
    (r"\b(aws|gcloud|az)\s+.*\b(credentials|get-secret-value|print-access-token|keyvault\s+secret)\b", "credenciais de nuvem"),
    (r"\bcat\s+[^|;&]*(\.netrc|\.npmrc|\.pgpass|credentials|id_rsa|id_ed25519|\.pem)\b", "arquivo de credencial"),
    (r"\b(echo|printf)\b[^|;&]*\$\{?[A-Z0-9_]*(TOKEN|SECRET|KEY|PASSWORD|PASS|DATABASE_URL|DSN|PEPPER|SALT)", "exibir variavel sensivel"),
]

# Valem para todos: mudancas de producao ou de repositorio remoto.
# Quem executa essas acoes e o agente principal (NERD/sessao principal) com aprovacao.
PRODUCAO = [
    (r"\bgit\s+push\b", "push e feito pela sessao principal"),
    (r"\brailway\s+(up|redeploy|down|delete|domain|volume|add|environment|service|link|unlink|init|login|logout)\b", "alteracao na plataforma"),
    (r"\b(vercel|netlify)\s+(deploy|--prod|promote|rollback|remove)\b", "deploy na plataforma"),
    (r"\b(fly|flyctl)\s+(deploy|scale|destroy|apps\s+destroy)\b", "deploy na plataforma"),
    (r"\bkubectl\s+(apply|delete|scale|rollout|edit|patch)\b", "alteracao no cluster"),
    (r"\bterraform\s+(apply|destroy)\b", "alteracao de infraestrutura"),
    (r"\bgh\s+(pr\s+merge|release|workflow\s+run|repo\s+(delete|edit))\b", "alteracao no GitHub"),
    (r"\b(prisma\s+migrate\s+deploy|drizzle-kit\s+push)\b", "migracao em banco remoto"),
]

# Perfis sem acesso algum a CLIs de plataforma.
SEM_PLATAFORMA = [
    (r"\b(railway|heroku|flyctl|fly|vercel|netlify|kubectl|terraform)\b", "este perfil nao usa CLI de plataforma"),
]

# sre: dentro de um shell remoto, so leitura (SELECT) e sem ambiente.
SRE_SSH = [
    (r"\b(railway\s+ssh|ssh)\b.*\b(insert|update|delete|drop|alter|truncate|create|grant|revoke|copy)\b", "shell remoto: apenas SELECT"),
    (r"\b(railway\s+ssh|ssh)\b.*\b(env|printenv|export|set)\b", "shell remoto: nao exibir ambiente"),
]


def regras(perfil):
    r = SEGREDOS + PRODUCAO
    if perfil in ("produto", "qa", "marketing"):
        r = r + SEM_PLATAFORMA
    if perfil == "sre":
        r = r + SRE_SSH
    return r


def verificar(comando, perfil):
    for padrao, motivo in regras(perfil):
        if re.search(padrao, comando, re.IGNORECASE | re.MULTILINE):
            return motivo
    return None


ARQUIVO_SENSIVEL = re.compile(
    r"(^|/)(\.env(?!\.(example|sample|template)$)(\.[\w.-]+)?|\.netrc|\.npmrc|\.pgpass|id_rsa|id_ed25519"
    r"|[^/]*\.pem|[^/]*\.pfx|[^/]*\.p12|[^/]*\.key|credentials(\.json)?|empresa\.yaml)$",
    re.IGNORECASE,
)


def verificar_arquivo(dados):
    entrada = dados.get("tool_input") or {}
    for campo in ("file_path", "path", "notebook_path"):
        caminho = entrada.get(campo)
        if caminho and ARQUIVO_SENSIVEL.search(str(caminho).rstrip("/")):
            # config/empresa.yaml pode ser lido, nunca editado pelos sub-agentes.
            if str(caminho).endswith("empresa.yaml") and dados.get("tool_name") in ("Read", "Grep", "Glob"):
                continue
            return f"arquivo sensivel ({str(caminho).rsplit('/', 1)[-1]})"
    padrao = str(entrada.get("glob") or entrada.get("pattern") or "")
    if dados.get("tool_name") in ("Glob", "Grep") and re.search(r"\.env(?!\.(example|sample|template))", padrao):
        return "busca em arquivos .env"
    return None


def _handoffs():
    extra = os.environ.get("CLT_TEAM_HANDOFFS", "").rstrip("/")
    base = r"/\.claude/clt-team/registros/handoffs/|/private/tmp/|/tmp/|/scratchpad/"
    if extra:
        base += "|^" + re.escape(extra) + "/"
    return base


def _regras_escrita():
    h = _handoffs()
    return {
        # qa: so arquivos de teste e relatorio (codigo de producao e do NERD).
        "qa": re.compile(
            h + r"|(^|/)(tests?|__tests__|spec|specs|e2e|playwright|cypress|fixtures)/"
            r"|\.(test|spec|e2e)\.[cm]?[jt]sx?$|_test\.(py|go)$|(^|/)test_[^/]+\.py$"
            r"|(^|/)playwright\.config\.[cm]?[jt]s$|(^|/)vitest\.config\.[cm]?[jt]s$",
            re.IGNORECASE,
        ),
        "produto": re.compile(h + r"|/docs/specs/[^/]+\.md$", re.IGNORECASE),
        "sre": re.compile(h + r"|/docs/RUNBOOK\.md$|/docs/runbooks?/[^/]+\.md$", re.IGNORECASE),
        # marketing: rascunhos de texto, nunca codigo ou configuracao.
        "marketing": re.compile(r"\.(md|mdx|txt|csv)$", re.IGNORECASE),
    }


def verificar_escrita(dados, perfil):
    if dados.get("tool_name") not in ("Edit", "Write", "NotebookEdit", "MultiEdit"):
        return None
    regra = _regras_escrita().get(perfil)
    if regra is None:
        return None
    entrada = dados.get("tool_input") or {}
    caminho = str(entrada.get("file_path") or entrada.get("notebook_path") or "")
    if not regra.search(caminho):
        return f"escrita fora do permitido para {perfil} ({caminho.rsplit('/', 1)[-1]})"
    return None


def teste():
    total = 0
    falhas = 0
    comandos = [
        ("railway variables --service api", "sre", True),
        ("railway logs --service api", "sre", False),
        ("railway logs --service api", "qa", True),
        ("vercel env pull", "sre", True),
        ("kubectl get secrets", "sre", True),
        ("kubectl get pods", "sre", False),
        ("printenv", "qa", True),
        ("env", "sre", True),
        ("env NODE_ENV=test npm test", "qa", False),
        ("cat .env", "qa", True),
        ("cat .env.example", "qa", False),
        ("cat .env.local", "qa", True),
        ("ls src/env.ts", "qa", False),
        ("npm run test", "qa", False),
        ("git push origin main", "qa", True),
        ("git log -5", "produto", False),
        ("export -p", "sre", True),
        ("export FOO=1 && npm test", "qa", False),
        ("echo $DATABASE_URL", "sre", True),
        ("railway ssh -s api 'psql -c \"select count(*) from pedidos\"'", "sre", False),
        ("railway ssh -s api 'psql -c \"delete from pedidos\"'", "sre", True),
        ("railway ssh -s api printenv", "sre", True),
        ("railway up", "sre", True),
        ("terraform apply", "sre", True),
        ("docker run --rm -e POSTGRES_PASSWORD=ci postgres:16", "qa", False),
    ]
    for cmd, perfil, esperado in comandos:
        total += 1
        if (verificar(cmd, perfil) is not None) != esperado:
            falhas += 1
            print(f"FALHA [{perfil}] {cmd!r}: esperado bloqueio={esperado}")
    arquivos = [
        ({"tool_name": "Read", "tool_input": {"file_path": "/home/dev/app/.env"}}, True),
        ({"tool_name": "Read", "tool_input": {"file_path": "/home/dev/app/.env.production"}}, True),
        ({"tool_name": "Read", "tool_input": {"file_path": "/home/dev/app/.env.example"}}, False),
        ({"tool_name": "Read", "tool_input": {"file_path": "/home/dev/app/src/env.ts"}}, False),
        ({"tool_name": "Read", "tool_input": {"file_path": "/home/dev/certificado.pfx"}}, True),
        ({"tool_name": "Read", "tool_input": {"file_path": "/home/dev/.claude/clt-team/config/empresa.yaml"}}, False),
        ({"tool_name": "Edit", "tool_input": {"file_path": "/home/dev/.claude/clt-team/config/empresa.yaml"}}, True),
        ({"tool_name": "Grep", "tool_input": {"pattern": "KEY", "glob": "**/.env*"}}, True),
        ({"tool_name": "Edit", "tool_input": {"file_path": "/home/dev/app/tests/a.test.ts"}}, False),
    ]
    for dados, esperado in arquivos:
        total += 1
        if (verificar_arquivo(dados) is not None) != esperado:
            falhas += 1
            print(f"FALHA arquivo {dados}: esperado bloqueio={esperado}")
    escritas = [
        ("qa", "/home/dev/app/src/server/pedidos.ts", True),
        ("qa", "/home/dev/app/src/server/pedidos.test.ts", False),
        ("qa", "/home/dev/app/tests/estoque.spec.ts", False),
        ("qa", "/home/dev/.claude/clt-team/registros/handoffs/2026-01-01_app_qa_x.md", False),
        ("produto", "/home/dev/app/docs/specs/blog.md", False),
        ("produto", "/home/dev/app/server/index.js", True),
        ("sre", "/home/dev/app/docs/RUNBOOK.md", False),
        ("sre", "/home/dev/app/migrations/1.sql", True),
        ("marketing", "/home/dev/site/blog/posts/artigo.md", False),
        ("marketing", "/home/dev/site/index.html", True),
    ]
    for perfil, caminho, esperado in escritas:
        total += 1
        obtido = verificar_escrita({"tool_name": "Write", "tool_input": {"file_path": caminho}}, perfil) is not None
        if obtido != esperado:
            falhas += 1
            print(f"FALHA escrita [{perfil}] {caminho}: esperado bloqueio={esperado}")
    print(f"{total - falhas}/{total} casos OK")
    return 1 if falhas else 0


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--teste":
        sys.exit(teste())
    perfil = sys.argv[1] if len(sys.argv) > 1 else "qa"
    try:
        dados = json.load(sys.stdin)
    except Exception:
        # Entrada ilegivel: nao bloqueia, para nao travar a sessao.
        sys.exit(0)
    if dados.get("tool_name") == "Bash":
        comando = (dados.get("tool_input") or {}).get("command") or ""
        motivo = verificar(comando, perfil)
    else:
        motivo = verificar_arquivo(dados) or verificar_escrita(dados, perfil)
    if motivo:
        print(
            f"Bloqueado pelo guarda-segredos ({perfil}): {motivo}. "
            "Segredos nunca sao exibidos e mudancas de producao sao executadas pela "
            "sessao principal com aprovacao. Registre o pedido no handoff em vez de contornar.",
            file=sys.stderr,
        )
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
