# Design systems e direção de arte

**Dono do processo:** DESIGNER. **Implementação:** NERD. **Audiovisual:** EDITOR. **Aprovação de identidade:** proprietário, assessorado pelo SÓCIO.

## Objetivo
Ter um registro dos design systems do portfólio e **uma fonte da verdade por marca/projeto** (app, site, painel, landing, vídeo). Consolidar sistemas fragmentados dentro do MESMO projeto, sem mesclar identidades de marcas diferentes. Primitivas de acessibilidade e componentes neutros podem ser compartilhados.

## Descoberta
1. Consulte `marcas` em `config/empresa.yaml` e os repositórios autorizados. Sem acesso, não afirme que auditou.
2. Procure documentação oficial, `tailwind.config`, CSS e CSS variables, `tokens.*`, brandbook, logos, componentes, Storybook, Figma (se conectado), páginas em produção e decisões aprovadas.
3. Registre por projeto e superfície: caminho/URL, branch/commit, estado (`verificado`, `parcialmente_verificado`, `nao_auditado`, `ausente`), data, responsável, conflitos e ação sugerida.
4. Divergência: vale a versão aprovada mais recente com uso comprovado; mantenha changelog e critério de obsolescência. Nunca copie a paleta de outra marca por suposição.
5. Sem design system: audite a UI atual, proponha tokens semânticos, componentes e guidelines em `DESIGN_SYSTEM.md` no repositório e revise com o proprietário antes de trocar identidade aprovada.

## Contrato mínimo por projeto
- **Marca:** nome e grafia, logo e variações, paleta e significado dos tokens, contraste, tipografia licenciada, ícones, voz.
- **Tokens:** cores primitivas e semânticas, escala tipográfica, espaçamento, grid, breakpoints, z-index, raio, sombras, opacidade, motion, dark/light se aplicável.
- **Componentes:** botões, campos, busca, filtros, modal, toast, tooltip, navegação, tabelas, cards, gráficos, badges, alertas, estados de carregando/vazio/erro.
- **Telas:** responsividade, hierarquia, densidade, recuperação de erro, feedback de ação, animação com propósito.
- **Marketing e vídeo:** 1:1, 4:5, 9:16, 16:9; safe areas; uso do logo; legendas; motion.
- **Governança:** dono, fontes verificadas, semver, revisão por PR, checklist visual, baseline de screenshots quando possível, guia de migração, changelog.

## Maturidade
`nao_auditado` → `auditado` → `em_consolidacao` → `proposta_em_revisao` → `aprovado` → `implementado` → `monitorado`.
Estado de descoberta e estado de aprovação são campos separados. Documentação criada por IA sem decisão do proprietário **não** é branding oficial.

## Vocabulário de direção de arte
| Disciplina | Conceitos | O que especificar |
| --- | --- | --- |
| Composição | grid, alinhamento óptico, equilíbrio, hierarquia, contraste, Gestalt, espaço negativo, ritmo | hierarquia 1º/2º/3º nível, margens, densidade, ordem de leitura |
| Formas e curvas | primitivas, formas orgânicas e geométricas, raios, tangências, curvas de Bézier, continuidade G0/G1/G2 | proporções, raios, pesos, curvaturas, consistência de cantos |
| Símbolos | semiótica, pictograma, logotipo, monograma, área de respiro, stroke vs fill, grid de ícones | peso de traço, área de proteção, tamanho mínimo, variações aprovadas |
| Tipografia | classificações, variable fonts, optical size, kerning, tracking, leading, x-height, pareamento | família/licença, pesos, tamanhos, espaçamentos, regras de legenda |
| Cor | HEX/HSL/OKLCH, harmonias (análoga, complementar, triádica, monocromática), gradiente, contraste | paleta oficial ou proposta, papéis de tokens, contraste por fundo |
| Estilo | minimalista, editorial, corporativo, flat, 2D/3D, textura, sombra, profundidade | elementos permitidos/proibidos e intensidade |
| Motion | keyframes, timing, easing, cubic-bezier, antecipação, overshoot, parallax, tipografia cinética | duração, atraso, amplitude, origem, curva, relação com áudio, movimento reduzido |
| Produção | SVG, raster, resolução, aspect ratio, safe areas, alpha, sRGB/Rec.709 | formatos, dimensões, exportação e QA |

Regras: explique termos técnicos quando necessário, sem despejar jargão em resposta curta; use valores quantitativos quando houver base e marque como **proposta** quando não houver. Nunca invente fontes, direitos de uso, normas publicitárias ou aprovação visual.

### Exemplo de tradução de pedido impreciso
**Pedido:** "Logo menos larga, curvas mais suaves, animação perceptível, sem glow exagerado."
**Resposta técnica:** reduzir a relação largura/altura mantendo área de respiro; ajustar pontos de controle das curvas de Bézier com continuidade visual; deslocamento/rotação discretos por keyframes com easing documentado; animar fundo e grafismos sem alterar a marca; nenhum glow não solicitado. Valores exatos medidos no material real e aprovados antes de alterar o logo oficial.

## Ciclo DESIGNER + EDITOR
**briefing → ficha de direção de arte (`docs/TEMPLATES.md`) → montagem → preview → QA visual do DESIGNER → correções e export do EDITOR.**
Com brand kit validado e sem decisão visual nova, o EDITOR executa sozinho.
