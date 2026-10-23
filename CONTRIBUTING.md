# Como contribuir

Obrigado por querer melhorar o CLT-TEAM.

## Princípios
1. **Genérico primeiro.** Nada de nomes de empresas, marcas, pessoas, CNPJs, e-mails, telefones, domínios, IDs de contas ou valores reais. Use placeholders `{{ASSIM}}` e documente-os em `config/empresa.example.yaml`.
2. **Sem duplicar papéis.** Antes de propor um agente novo, leia [docs/CRIAR-NOVO-AGENTE.md](docs/CRIAR-NOVO-AGENTE.md) e explique por que um agente existente não cobre a lacuna.
3. **Segurança não regride.** Nenhuma mudança pode remover aprovação A3, ampliar a lista `tools` de sub-agentes com ferramentas de escrita/gasto/deploy ou enfraquecer o hook sem justificativa e teste.
4. **Português do Brasil** nos prompts e docs. Traduções vão em pastas separadas (ex.: `i18n/en/`).

## Fluxo
1. Abra uma issue descrevendo o problema ou a proposta.
2. Faça um fork e uma branch (`feat/...`, `fix/...`, `docs/...`).
3. Rode antes do PR:
   ```bash
   python3 hooks/guarda-segredos.py --teste
   bash -n scripts/instalar.sh
   ./scripts/instalar.sh --simular
   ```
4. Faça a varredura de vazamento (ajuste os termos à sua realidade):
   ```bash
   grep -rnE '[0-9]{2}\.[0-9]{3}\.[0-9]{3}/[0-9]{4}-[0-9]{2}' . --exclude-dir=.git   # CNPJ
   grep -rnE '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}' . --exclude-dir=.git     # e-mail
   grep -rnE '(sk-|ghp_|gho_|AKIA|eyJ)[A-Za-z0-9]' . --exclude-dir=.git           # tokens
   grep -rnE '/Users/|/home/[a-z]+/' . --exclude-dir=.git                         # caminhos pessoais
   ```
5. Atualize `CHANGELOG.md` e, se mudou comportamento, os guias em `docs/`.
6. Abra o PR explicando motivação, o que muda para quem já usa e como testou.

## Padrões dos agentes
- Frontmatter válido (`name`, `description`, `model`; `tools` em lista fechada para sub-agentes).
- Seções: missão, antes de começar, regras, entregáveis, QA, bloco "Contexto e regras sempre válidas".
- Retorno no formato de [docs/PROTOCOLO-HANDOFF.md](docs/PROTOCOLO-HANDOFF.md).

## Conduta
Seja respeitoso e objetivo. Críticas ao código, nunca às pessoas.
