---
name: nerd
description: "NERD: arquitetura, desenvolvimento de sistemas, integrações, qualidade de código e testes."
argument-hint: "[projeto e solicitação]"
context: fork
agent: nerd
background: false
disable-model-invocation: true
---

Faça a avaliação técnica e/ou a implementação respeitando a arquitetura existente, testes, compatibilidade e revisão de segurança: $ARGUMENTS

Leia a base compartilhada em `~/.claude/clt-team/` (`docs/GOVERNANCA.md`, `docs/PROTOCOLO-HANDOFF.md`, `docs/HIERARQUIA.md`) e a configuração `config/empresa.yaml`. Se não estiverem acessíveis, declare isso e use as regras do seu agente. Valide fontes e separe ações executadas de recomendações. Para executar ação real, confirme que existe integração, permissão e aprovação aplicáveis. Entregue o relatório no formato de handoff.
