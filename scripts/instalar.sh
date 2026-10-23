#!/usr/bin/env bash
# Instalador do CLT-TEAM para o Claude Code.
#
# Uso:
#   ./scripts/instalar.sh                 # instala para o usuário (~/.claude)
#   ./scripts/instalar.sh --projeto DIR   # agentes e skills em DIR/.claude
#   ./scripts/instalar.sh --simular       # mostra o que faria, sem copiar
#   ./scripts/instalar.sh --sem-skills    # só agentes e base
#
# A base compartilhada (docs, config, hooks, registros) vai sempre para
# ~/.claude/clt-team/, porque os hooks e prompts apontam para esse caminho.
# Arquivos existentes com o mesmo nome são copiados para uma pasta de backup
# antes de serem substituídos. config/empresa.yaml e registros/ nunca são
# sobrescritos.
set -euo pipefail

ORIGEM="$(cd "$(dirname "$0")/.." && pwd)"
DESTINO_BASE="$HOME/.claude/clt-team"
DESTINO_CLAUDE="$HOME/.claude"
SIMULAR=0
SKILLS=1

while [ $# -gt 0 ]; do
  case "$1" in
    --projeto) DESTINO_CLAUDE="$(cd "$2" && pwd)/.claude"; shift 2 ;;
    --simular) SIMULAR=1; shift ;;
    --sem-skills) SKILLS=0; shift ;;
    -h|--help) sed -n '2,16p' "$0"; exit 0 ;;
    *) echo "Opção desconhecida: $1" >&2; exit 1 ;;
  esac
done

BACKUP="$HOME/.claude/clt-team-backup-$(date +%Y%m%d-%H%M%S)"

copiar() { # origem destino
  local de="$1" para="$2"
  if [ -e "$para" ] && ! cmp -s "$de" "$para"; then
    echo "  backup: $para"
    if [ "$SIMULAR" -eq 0 ]; then
      mkdir -p "$BACKUP/$(dirname "${para#$HOME/}")"
      cp -p "$para" "$BACKUP/${para#$HOME/}"
    fi
  fi
  echo "  copia : ${para/#$HOME/~}"
  if [ "$SIMULAR" -eq 0 ]; then
    mkdir -p "$(dirname "$para")"
    cp "$de" "$para"
  fi
}

echo "Agentes -> ${DESTINO_CLAUDE/#$HOME/~}/agents"
for f in "$ORIGEM"/agents/*.md; do
  copiar "$f" "$DESTINO_CLAUDE/agents/$(basename "$f")"
done

if [ "$SKILLS" -eq 1 ]; then
  echo "Skills -> ${DESTINO_CLAUDE/#$HOME/~}/skills"
  for d in "$ORIGEM"/skills/*/; do
    nome="$(basename "$d")"
    copiar "$d/SKILL.md" "$DESTINO_CLAUDE/skills/$nome/SKILL.md"
  done
fi

echo "Base -> ~/.claude/clt-team"
for f in "$ORIGEM"/docs/*.md; do
  copiar "$f" "$DESTINO_BASE/docs/$(basename "$f")"
done
copiar "$ORIGEM/hooks/guarda-segredos.py" "$DESTINO_BASE/hooks/guarda-segredos.py"
copiar "$ORIGEM/config/empresa.example.yaml" "$DESTINO_BASE/config/empresa.example.yaml"
if [ ! -e "$DESTINO_BASE/config/empresa.yaml" ]; then
  copiar "$ORIGEM/config/empresa.example.yaml" "$DESTINO_BASE/config/empresa.yaml"
  echo "  -> preencha ~/.claude/clt-team/config/empresa.yaml (docs/GUIA-CONFIGURACAO.md)"
else
  echo "  mantido: ~/.claude/clt-team/config/empresa.yaml (já existe)"
fi
if [ ! -e "$DESTINO_BASE/registros/DECISOES.md" ]; then
  copiar "$ORIGEM/registros/DECISOES.example.md" "$DESTINO_BASE/registros/DECISOES.md"
fi
[ "$SIMULAR" -eq 0 ] && mkdir -p "$DESTINO_BASE/registros/handoffs"

if [ "$SIMULAR" -eq 0 ]; then
  chmod +x "$DESTINO_BASE/hooks/guarda-segredos.py"
  echo "Autoteste do hook:"
  python3 "$DESTINO_BASE/hooks/guarda-segredos.py" --teste
  [ -d "$BACKUP" ] && echo "Backup dos arquivos substituídos: ${BACKUP/#$HOME/~}"
else
  echo "(simulação: nada foi copiado)"
fi
echo "Pronto. Abra o Claude Code e rode /agents para conferir a equipe."
