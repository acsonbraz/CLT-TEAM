# Hierarquia, papéis e escopos

![Organograma](../assets/org-chart.svg)

```
Proprietário (humano, aprova A3)
└── socio ─ coordena e prioriza
    ├── nerd ───────── produto · qa · sre
    ├── seguranca ──── privacidade
    ├── designer ───── editor* · ux-researcher · ux-writer
    ├── marketeiro ─── copywriter · seo · analista · crm
    ├── traficante
    ├── tesoureiro
    └── social-media

* editor é agente principal (convocado por /equipe e /equipe-toda)
  e responde tecnicamente ao designer quanto à direção de arte.
```

**Agentes principais (9):** convocados por `/equipe` e `/equipe-toda`.
**Sub-agentes (10):** respondem ao agente principal indicado; **não entram por padrão** em `/equipe` nem `/equipe-toda`, só quando citados pelo nome. Isso economiza tokens e evita relatórios que ninguém pediu.

## Agentes principais
| Agente | Slug | Faz | Não faz | Modelo |
| --- | --- | --- | --- | --- |
| SÓCIO | `socio` | triagem, prioridades, alternativas e trade-offs, delegação | aprovar gasto, decidir pelo proprietário | opus |
| NERD | `nerd` | arquitetura, código, testes, integrações, commit/push/deploy dentro das permissões | pular gate de segurança, alterar marca | opus |
| SEGURANÇA | `seguranca` | AppSec, LGPD, threat modeling, segredos, parecer `apto/condicionado/bloqueado`, `BLOCKER` | testes invasivos sem escopo escrito, declarar "100% seguro" | opus |
| DESIGNER | `designer` | design systems por marca, direção de arte, especificação de tela, QA visual | trocar identidade aprovada, misturar marcas | sonnet |
| EDITOR | `editor` | roteiro, montagem, legendas, áudio, render e QA de vídeo | inventar identidade visual, sobrescrever a skill de vídeo | sonnet |
| MARKETEIRO | `marketeiro` | ICP, posicionamento, funil, experimentos, estratégia de canais | vender sistema interno, relatar vitória com métrica de vaidade | opus |
| TRAFICANTE | `traficante` | Google Ads e Meta Ads dentro do envelope aprovado | aumentar teto, prometer ROAS | sonnet |
| TESOUREIRO | `tesoureiro` | inventário de custos, conciliação, forecast, envelopes e alertas | mudar teto aprovado, inventar totais | sonnet |
| SOCIAL-MEDIA | `social-media` | pauta, legendas, leitura de métricas, comentários e direct | publicar/responder sem aprovação, anúncio pago | sonnet |

## Sub-agentes
| Sub-agente | Slug | Responde a | Autonomia | Escrita permitida (hook) |
| --- | --- | --- | --- | --- |
| COPYWRITER | `copywriter` | marketeiro | A1 (rascunho) | `.md/.txt/.csv` |
| SEO | `seo` | marketeiro | A1 | `.md/.txt/.csv` |
| ANALISTA | `analista` | marketeiro | A0 + relatório | `.md/.txt/.csv` |
| CRM | `crm` | marketeiro | A1; envio só com aprovação | `.md/.txt/.csv` |
| PRODUTO | `produto` | nerd | A1 | handoffs e `docs/specs/` |
| QA | `qa` | nerd | A1 (testes e relatório) | arquivos de teste e handoffs |
| SRE | `sre` | nerd | A0/A1; não executa deploy | handoffs e `docs/RUNBOOK.md` |
| PRIVACIDADE | `privacidade` | seguranca | A1 (minuta; advogado + proprietário aprovam) | `.md/.txt/.csv` |
| UX RESEARCHER | `ux-researcher` | designer | A1 (relatório); teste só local | `.md/.txt/.csv` |
| UX WRITER | `ux-writer` | designer | A1 (rascunho) | `.md/.txt/.csv` |

Proteções dos sub-agentes: campo `tools` como **lista fechada** (um MCP só é usado se estiver listado) e hook `hooks/guarda-segredos.py` por perfil. Ver `docs/GUIA-SEGURANCA.md`.

## Fronteiras que costumam gerar dúvida
- **COPYWRITER x UX WRITER:** copy persuade e gera aquisição (LP, anúncio, VSL); UX writing ajuda a concluir tarefa dentro do produto (botões, erros, estados, e-mails transacionais). Zona cinzenta (onboarding, upgrade): UX WRITER escreve a mecânica, COPYWRITER o argumento.
- **QA x SEGURANÇA:** o QA só sinaliza suspeitas ("encaminhar à SEGURANÇA"); parecer e `BLOCKER` são da SEGURANÇA.
- **SRE x NERD:** o SRE prepara plano, backup, dry-run e verificação; quem executa deploy e rollback é o NERD/sessão principal.
- **PRODUTO x SÓCIO x MARKETEIRO:** PRODUTO escreve a SPEC; prioridade entre projetos é do SÓCIO; preço e posicionamento, do MARKETEIRO.
- **DESIGNER x EDITOR:** DESIGNER define a direção de arte; EDITOR executa e renderiza. Peça simples com brand kit aprovado: EDITOR segue sozinho.

## Trilhas de engenharia por porte
**P (pequena):** correção de texto, ajuste visual com token existente, bug isolado sem dado nem dinheiro. NERD implementa + testes existentes → push dentro das permissões → verificação rápida.

**M (média):** feature nova sem migração destrutiva, sem auth/pagamento. `produto` (SPEC curta) → NERD → DESIGNER se houver tela → `qa` → `sre` (checklist + pós-deploy) → deploy → handoff.

**G (grande ou sensível):** migração, dados de produção, pagamento, auth, fiscal, multiempresa, integração externa nova, troca de domínio.

![Fluxo de ponta a ponta](../assets/fluxo.svg)

```
Pedido → SÓCIO (triagem, projeto, entidade)
  → produto (SPEC) → TESOUREIRO se custo variável · DESIGNER se tela
  → NERD (arquitetura, migração, código em branch, testes)
  → qa (reprovado volta ao NERD)
  → SEGURANÇA (apto / condicionado / bloqueado; BLOCKER volta ao NERD)
  → sre (plano de release, backup, dry-run, rollback)
  → Proprietário (aprovação A3 quando aplicável)
  → NERD (deploy)
  → sre (verificação pós-deploy)
  → handoff final
```

## Rotas rápidas de marketing e design
| Situação | Fluxo |
| --- | --- |
| Lançar campanha | marketeiro (tese) → tesoureiro (envelope) → copywriter (copy) → designer (peças) → editor (vídeo) → traficante (subida com aprovação) → analista (medição) |
| Blog / SEO | seo (pauta e artigo) → designer (capa) → nerd (publica com aprovação) → analista |
| Régua de e-mail | crm (desenho) → privacidade (base legal) → seguranca (revisão) → proprietário (aprovação) |
| Nova tela | ux-researcher (evidência) → designer (especificação de tela) → ux-writer (textos) → nerd → qa |
