# Guia de instalação

## Requisitos
- [Claude Code](https://docs.claude.com/en/docs/claude-code) instalado e autenticado.
- Python 3.8+ (para o hook `guarda-segredos.py`; só biblioteca padrão).
- Bash (macOS ou Linux; no Windows, use WSL ou copie os arquivos manualmente).

## Opção 1 — instalador (recomendado)
```bash
git clone <url-do-seu-fork>/clt-team.git
cd clt-team
./scripts/instalar.sh --simular     # confere o que será copiado
./scripts/instalar.sh               # instala para o seu usuário
```

O instalador:
1. copia `agents/*.md` para `~/.claude/agents/` e `skills/*/SKILL.md` para `~/.claude/skills/`;
2. copia a base compartilhada para `~/.claude/clt-team/` (`docs/`, `hooks/`, `config/empresa.example.yaml`);
3. cria `~/.claude/clt-team/config/empresa.yaml` a partir do exemplo **só se ainda não existir**;
4. cria `~/.claude/clt-team/registros/` (decisões e handoffs) sem sobrescrever o que já existe;
5. faz backup de qualquer arquivo com o mesmo nome antes de substituí-lo (`~/.claude/clt-team-backup-<data>/`);
6. roda o autoteste do hook.

### Instalar só em um projeto
```bash
./scripts/instalar.sh --projeto /caminho/do/projeto
```
Agentes e skills vão para `/caminho/do/projeto/.claude/`; a base continua em `~/.claude/clt-team/`, porque os prompts e hooks apontam para lá.

### Sem as skills de atalho
```bash
./scripts/instalar.sh --sem-skills
```
Os agentes continuam acessíveis por nome ("use o nerd para..."); só os atalhos `/nerd`, `/socio` etc. deixam de existir. `/equipe` e `/equipe-toda` também são skills.

## Opção 2 — cópia manual
```bash
mkdir -p ~/.claude/agents ~/.claude/skills ~/.claude/clt-team/{docs,hooks,config,registros/handoffs}
cp agents/*.md ~/.claude/agents/
cp -R skills/* ~/.claude/skills/
cp docs/*.md ~/.claude/clt-team/docs/
cp hooks/guarda-segredos.py ~/.claude/clt-team/hooks/ && chmod +x ~/.claude/clt-team/hooks/guarda-segredos.py
cp config/empresa.example.yaml ~/.claude/clt-team/config/empresa.yaml
cp registros/DECISOES.example.md ~/.claude/clt-team/registros/DECISOES.md
```

## Conferir
```bash
python3 ~/.claude/clt-team/hooks/guarda-segredos.py --teste   # deve terminar com "N/N casos OK"
```
No Claude Code, rode `/agents` e confira os 19 agentes. Depois, `/socio teste: quem é você e o que precisa saber da minha empresa?`.

## Próximo passo
Preencha `~/.claude/clt-team/config/empresa.yaml`: [GUIA-CONFIGURACAO.md](GUIA-CONFIGURACAO.md).

## Atualizar
`git pull` no repositório e rode o instalador de novo. Seu `empresa.yaml` e seus `registros/` são preservados; agentes alterados por você vão para o backup antes de serem substituídos (reaplique suas mudanças ou mantenha um fork).

## Desinstalar
```bash
cd ~/.claude/agents && rm -f socio.md nerd.md seguranca.md designer.md editor.md marketeiro.md traficante.md tesoureiro.md social-media.md copywriter.md seo.md analista.md crm.md produto.md qa.md sre.md privacidade.md ux-researcher.md ux-writer.md
cd ~/.claude/skills && rm -rf equipe equipe-toda socio nerd seguranca designer editor marketeiro traficante tesoureiro social-media
# a base fica em ~/.claude/clt-team (apague se não quiser manter seus registros)
```
Se o instalador substituiu agentes ou skills que você já tinha, restaure o backup mais recente:
```bash
ULTIMO=$(ls -d ~/.claude/clt-team-backup-* 2>/dev/null | tail -1)
[ -n "$ULTIMO" ] && cp -Rp "$ULTIMO/.claude/." ~/.claude/
```
Confira antes de apagar se nenhum desses nomes pertence a outro agente ou skill seu.
