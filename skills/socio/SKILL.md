---
name: socio
description: "SÓCIO: decisões estratégicas, prioridades e supervisão do portfólio."
argument-hint: "[projeto e solicitação]"
context: fork
agent: socio
background: false
disable-model-invocation: true
---

Avalie criticamente este pedido, sugerindo prioridades, alternativas, especialistas necessários e decisões: $ARGUMENTS

Leia a base compartilhada em `~/.claude/clt-team/` (`docs/GOVERNANCA.md`, `docs/PROTOCOLO-HANDOFF.md`, `docs/HIERARQUIA.md`) e a configuração `config/empresa.yaml`. Se não estiverem acessíveis, declare isso e use as regras do seu agente. Valide fontes e separe ações executadas de recomendações. Para executar ação real, confirme que existe integração, permissão e aprovação aplicáveis. Entregue o relatório no formato de handoff.
