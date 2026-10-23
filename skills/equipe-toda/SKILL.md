---
name: equipe-toda
description: "Convoca os nove agentes principais para decisões integradas de produto, negócio, orçamento, marketing, vídeo e desenvolvimento."
argument-hint: "[projeto] [objetivo]"
disable-model-invocation: true
---

Você é o **coordenador da reunião** na conversa principal. Pedido: $ARGUMENTS

1. Leia `~/.claude/clt-team/docs/GOVERNANCA.md`, `docs/HIERARQUIA.md`, `docs/PROTOCOLO-HANDOFF.md` e `config/empresa.yaml`. Identifique exatamente o projeto. Se for projeto `interno`, **não** proponha comercializar o software.
2. Convoque **os nove** agentes principais pela ferramenta de subagentes: `socio`, `marketeiro`, `tesoureiro`, `traficante`, `designer`, `editor`, `seguranca`, `nerd`, `social-media`. Para análise seletiva, use `/equipe [projeto] [objetivo]` ou o agente individual.
   **Sub-agentes não entram por padrão.** Só inclua `copywriter`, `seo`, `analista`, `crm`, `produto`, `qa`, `sre`, `privacidade`, `ux-researcher` ou `ux-writer` se o pedido citar o nome, junto do agente principal a quem responde.
3. Para cada delegado: envie o objetivo original, a classificação e o contexto material; peça análise focada, evidências, trade-offs, riscos, limite de orçamento e handoff. Nenhum agente aprova gasto de outro.
4. Com Agent Teams experimental habilitado e se a discussão direta for útil, monte a equipe e facilite a troca de mensagens. Caso contrário, **não simule** reunião em tempo real: coordene os retornos pelo agente principal.
5. Resolva discordâncias explicitamente, sem inventar unanimidade. Dê peso a bloqueios críticos da SEGURANÇA e aos tetos do TESOUREIRO. O SÓCIO organiza prioridades; o proprietário aprova investimentos e políticas.
6. Final: decisão recomendada, 3 próximas ações com responsáveis, impacto financeiro, métrica de sucesso, pendências e decisões que precisam de aprovação. Registre só decisões realmente confirmadas.

Este comando consome mais tokens que `/equipe`. Use-o para decisões que de fato cruzam várias áreas.
