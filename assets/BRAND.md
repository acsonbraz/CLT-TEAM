# CLT-TEAM: identidade visual

Identidade original, neutra e técnica. Não usa elementos de nenhuma outra marca. O símbolo é uma árvore de três níveis (sócio no topo, equipes abaixo), em referência ao organograma.

## Paleta

| Papel | Hex | Uso |
|---|---|---|
| Grafite (ink) | `#111827` | Texto, fundo do símbolo e do banner |
| Papel | `#FFFFFF` | Fundo de diagramas |
| Névoa | `#F9FAFB` | Texto e traço sobre fundo escuro |
| Acento (menta) | `#2DD4BF` | Hífen do wordmark e nó do topo, só sobre grafite |
| Acento escuro | `#0F766E` | Nó do topo sobre fundo claro |

## Cores por equipe

| Equipe | Hex | Agentes |
|---|---|---|
| Liderança | `#374151` | socio |
| Engenharia | `#4338CA` | nerd, produto, qa, sre |
| Segurança | `#BE123C` | seguranca, privacidade |
| Design | `#7E22CE` | designer, editor, ux-researcher, ux-writer |
| Marketing | `#0F766E` | marketeiro, copywriter, seo, analista, crm, traficante |
| Finanças | `#15803D` | tesoureiro |
| Social | `#0369A1` | social-media |

Todas as cores de equipe têm contraste mínimo de 5:1 com branco (ícones brancos sobre o bloco colorido). Aprovação humana usa âmbar escuro `#92400E` sobre `#FFFBEB`, com borda tracejada: o estado nunca depende só da cor.

## Tipografia

Somente fontes de sistema, sem arquivos externos.
- Texto: `-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif` (peso 600 a 800 em títulos).
- Código e rótulos técnicos: `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`.

## Uso do logo

- `logo.svg`: fundo claro. `logo-dark.svg`: fundo escuro. `logo-mark.svg`: avatar e favicon (quadrado).
- `banner.svg` (1280x640): social preview do GitHub e topo do README. Para o social preview, exporte PNG.
- Área de respiro: metade da altura do símbolo em todos os lados. Tamanho mínimo do símbolo: 24 px.
- Não girar, distorcer, recolorir fora da paleta nem trocar o hífen por outro caractere.

## Ícones

`icons/<slug>.svg`, 64x64, bloco arredondado na cor da equipe e glifo branco com traço de 3,5 e pontas arredondadas. Cada ícone tem `<title>` e `aria-label`.

## Acessibilidade (WCAG 2.2 AA)

- Texto normal: contraste mínimo 4,5:1; texto grande e elementos gráficos: 3:1.
- Grafite sobre branco: cerca de 17:1. Névoa sobre grafite: cerca de 16:1.
- Nunca usar cor como único indicador (legendas e rótulos de texto acompanham as cores).
- Todo SVG traz `role="img"`, `aria-label` e `<title>`. No README, use sempre texto alternativo.
- Sem animação nos arquivos.
