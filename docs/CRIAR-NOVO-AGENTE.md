# Como criar um novo agente

Antes de criar, pergunte: **o papel já existe?** Agentes duplicados geram dois donos para a mesma decisão e handoffs inúteis. Na criação desta equipe, propostas de "arquiteto", "CMO", "diretor de arte" e "UX/UI" foram descartadas porque NERD, MARKETEIRO e DESIGNER já cobriam o papel. Prefira ampliar o escopo de um agente existente quando a lacuna for pequena.

## 1. Defina o papel
| Pergunta | Exemplo |
| --- | --- |
| Que lacuna real ele cobre? | "ninguém escreve testes de regressão" |
| A quem responde? | `nerd` |
| O que **faz**? | roda testes, escreve testes, relatório |
| O que **não faz**? | não corrige código de produção, não faz parecer de segurança |
| Autonomia (A0–A3)? | A1 |
| Onde pode escrever? | arquivos de teste e handoffs |
| Quais ferramentas precisa, no mínimo? | Read, Grep, Glob, Bash, Edit, Write |
| Que entregável devolve? | relatório no modelo X |

## 2. Escreva o arquivo `agents/<slug>.md`
```markdown
---
name: <slug>
description: "<uma frase: o que faz, para quem, limites principais>"
model: sonnet
memory: user
permissionMode: default
tools: Read, Grep, Glob, Write
hooks:
  PreToolUse:
    - matcher: "Bash|Read|Edit|Write|Grep|Glob|NotebookEdit"
      hooks:
        - type: command
          command: "python3 \"$HOME/.claude/clt-team/hooks/guarda-segredos.py\" marketing"
---

# <NOME> — <subtítulo>
<Missão em 2 frases. A quem responde. O que não faz.>

## Antes de começar
1. Identifique projeto, entidade, classificação...
2. ...

## Regras
- ...

## Entregáveis
- ...

## QA antes de entregar
...

## Contexto e regras sempre válidas
<copie o bloco padrão do fim de qualquer agente existente>
```

Dicas:
- `description` é o que o Claude usa para decidir quando delegar: seja específico.
- `tools` em **lista fechada** para sub-agentes. Omitir `tools` = herda tudo da sessão (só para agentes principais de confiança).
- `model`: `opus` para decisões de alto impacto (produção, arquitetura, estratégia); `sonnet` para produção de texto e rotina; `haiku` para tarefas simples e baratas.
- Escolha o perfil do hook (`produto`, `qa`, `sre`, `marketing`) mais próximo ou crie um novo em `hooks/guarda-segredos.py` (função `_regras_escrita`) e acrescente casos ao `--teste`.

## 3. (Opcional) Crie o atalho `skills/<slug>/SKILL.md`
```markdown
---
name: <slug>
description: "<NOME>: <resumo>"
argument-hint: "[projeto e solicitação]"
context: fork
agent: <slug>
background: false
disable-model-invocation: true
---

<instrução curta>: $ARGUMENTS

Leia a base em `~/.claude/clt-team/` ... (copie o parágrafo de uma skill existente)
```

## 4. Integre à equipe
- Acrescente o agente em `docs/HIERARQUIA.md` (tabela e organograma).
- Se for sub-agente, cite-o na seção "Equipe do <CHEFE>" do agente a quem responde.
- Se deve entrar em `/equipe-toda`, atualize `skills/equipe/SKILL.md` e `skills/equipe-toda/SKILL.md`.
- Acrescente exemplos em `docs/GUIA-USO.md` e uma linha no `CHANGELOG.md`.

## 5. Teste
- `/agents` lista o novo agente sem erro de frontmatter.
- Um pedido simples devolve o handoff no formato do protocolo.
- Um pedido fora do escopo é recusado ou encaminhado.
- Uma tentativa proibida (ex.: `printenv`) é bloqueada pelo hook.
- `python3 hooks/guarda-segredos.py --teste` continua OK.
