# Guia de uso

## Três formas de chamar a equipe

| Forma | Quando usar | Exemplo |
| --- | --- | --- |
| **Atalho do agente** (`/socio`, `/nerd`...) | pedido para um especialista | `/nerd app-agenda planeje o módulo de lembretes` |
| **Pelo nome na conversa** | dentro de uma tarefa maior | "peça ao qa para testar a branch feat/lembretes" |
| **Reunião** (`/equipe`, `/equipe-toda`) | decisão que cruza áreas | `/equipe app-agenda vale lançar plano anual?` |

E uma quarta, para quem quer o SÓCIO lendo tudo:
```bash
claude --agent socio
```
A sessão inteira passa a ter o SÓCIO como agente principal: ele faz a triagem de cada pedido e delega. Isso não observa outras sessões.

## `/equipe` x `/equipe-toda`
- `/equipe <projeto> <objetivo>`: o SÓCIO escolhe 2 a 4 especialistas relevantes.
- `/equipe toda <projeto> <objetivo>` ou `/equipe-toda <projeto> <objetivo>`: os nove agentes principais. Mais caro em tokens.
- Sub-agentes só entram quando citados: `/equipe app-agenda qa e sre revisem a migração de lembretes`.

## Exemplos por equipe

### Direção
```
/socio Quais três iniciativas eu deveria pausar este trimestre? Use os projetos do empresa.yaml.
/equipe-toda app-agenda Discutam prioridades, riscos, verba, implementação e vídeos do lançamento.
```

### Engenharia (NERD + produto, qa, sre)
```
/nerd app-agenda Planeje o módulo de lembretes preservando contratos e estrutura de código.
Peça ao produto uma SPEC para "lembrete por e-mail 24h antes", com Gherkin e bordas.
Peça ao qa para rodar a suíte na branch feat/lembretes e testar idempotência do envio.
Peça ao sre um plano de release com rollback para a migração 0042.
```

### Segurança (SEGURANÇA + privacidade)
```
/seguranca app-agenda Revise isolamento entre clientes e o tratamento de segredos das integrações.
Peça à privacidade uma minuta de política de privacidade para o app-agenda, em comparação antes/depois.
```

### Design (DESIGNER + editor, ux-researcher, ux-writer)
```
/designer app-agenda auditar Encontre e unifique os design systems do painel e da landing.
Peça ao ux-researcher uma avaliação heurística da tela de cadastro rodando em localhost.
Peça ao ux-writer o catálogo de mensagens de erro do fluxo de pagamento.
/editor app-agenda Vídeo de 30 s para reels a partir do briefing do marketeiro.
```

### Marketing (MARKETEIRO + copywriter, seo, analista, crm)
```
/marketeiro app-agenda Estratégia de crescimento B2B com análise de concorrência.
Peça ao copywriter 15 títulos RSA e 4 descrições para a campanha de busca, com contagem.
Peça ao seo uma pauta de cluster sobre "agendamento online para clínicas".
Peça ao analista o plano de medição do funil de cadastro.
Peça ao crm a régua de fim de teste grátis (só desenho, sem envio).
```

### Mídia e finanças
```
/traficante app-agenda Otimize o Google Ads dentro do teto aprovado de janeiro.
/tesoureiro Separe assinaturas, APIs e anúncios por entidade e projeto, com o que falta comprovar.
```

### Orgânico
```
/social-media @perfil Rascunhe o calendário da próxima semana e conte as conversas sem resposta no direct.
```

## Como ler a resposta
Todo agente devolve o **handoff** (`docs/PROTOCOLO-HANDOFF.md`). Atenção a três campos:
- **ESTADO:** `observado` é fato verificado; `hipótese` e `não verificado` não são.
- **AÇÃO EXECUTADA:** o que realmente aconteceu. "nenhuma" é uma resposta válida e comum.
- **APROVAÇÃO REQUERIDA:** se for A3, nada acontece até você responder com a palavra de aprovação + código.

## Aprovar
Quando um agente pedir aprovação, ele mostra o código do pedido. Responda:
```
APROVO 7F3A
```
(ou a palavra que você configurou). Aprovação vale para aquele pedido, com aquele escopo e teto. Para recusar, basta não aprovar ou dizer o que mudar.

## Boas práticas
- Comece pedidos com o `id` do projeto: evita que o agente adivinhe a entidade.
- Prefira um agente certo a uma reunião: `/equipe-toda` custa ~9 vezes mais.
- Peça "só rascunho" quando quiser ver antes; os agentes já fazem isso por padrão em A1.
- Guarde decisões aprovadas em `registros/DECISOES.md`; os agentes consultam esse arquivo.
