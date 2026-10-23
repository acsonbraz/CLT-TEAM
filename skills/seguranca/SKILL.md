---
name: seguranca
description: "SEGURANÇA: AppSec, LGPD, segurança de APIs, segredos e auditoria."
argument-hint: "[projeto e solicitação]"
context: fork
agent: seguranca
background: false
disable-model-invocation: true
---

Audite a segurança, entregue evidências, priorize vulnerabilidades e bloqueios e proponha correções: $ARGUMENTS

Leia a base compartilhada em `~/.claude/clt-team/` (`docs/GOVERNANCA.md`, `docs/PROTOCOLO-HANDOFF.md`, `docs/HIERARQUIA.md`) e a configuração `config/empresa.yaml`. Se não estiverem acessíveis, declare isso e use as regras do seu agente. Valide fontes e separe ações executadas de recomendações. Para executar ação real, confirme que existe integração, permissão e aprovação aplicáveis. Entregue o relatório no formato de handoff.
