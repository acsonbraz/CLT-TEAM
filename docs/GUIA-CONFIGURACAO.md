# Guia de configuração

Toda informação específica da sua empresa fica em **um único arquivo**: `~/.claude/clt-team/config/empresa.yaml`. Os agentes são genéricos; é esse arquivo que diz a eles quem é quem.

> **Nunca coloque segredos aqui.** Senhas, tokens, chaves de API, cartões e dados pessoais de clientes ficam fora do arquivo (cofre, variáveis de ambiente do seu provedor). O `.gitignore` deste repositório ignora `config/empresa.yaml` para você não publicar por engano a configuração real.

## Passo a passo

### 1. Proprietário e aprovação
```yaml
proprietario:
  nome_exibicao: "o proprietário"
aprovacao:
  palavra: "APROVO"
  canal: "sessao"
```
- `palavra`: o que você escreve para autorizar ações A3. Os agentes esperam `<palavra> <código>` (ex.: `APROVO 7F3A`). Pode trocar por `AUTORIZO`, `OK-PUBLICAR` etc.
- `canal`: onde a aprovação chega. `sessao` = na própria conversa do Claude Code. `whatsapp`, `slack` ou `email` só funcionam se você tiver uma integração (MCP ou webhook) que crie pedidos e devolva a resposta.
- `aprovadores`: papéis que podem aprovar cada tipo de ação. Use papéis ou nomes de exibição, nunca e-mail ou telefone.

### 2. Entidades jurídicas
Uma entrada por CNPJ. Se você tem uma empresa de tecnologia e uma loja, são duas entidades, mesmo com o mesmo sócio.
```yaml
entidades:
  - id: tech
    razao_social: "{{RAZAO_SOCIAL_1}}"
    cnpj: "{{CNPJ_1}}"
    tipo: tecnologia
    centro_de_custo: "TEC"
```
Os agentes usam o `id` para separar custos, contas de anúncio, dados e marcas.

### 3. Projetos
```yaml
projetos:
  - id: app-agenda
    nome: "Agenda"
    entidade: tech
    classificacao: comercial   # comercial | interno
    estado: mvp
    marca: agenda
    push_faz_deploy: true
```
- `comercial`: pode ser vendido; MARKETEIRO e TRAFICANTE trabalham aquisição.
- `interno`: ferramenta da sua operação (ERP, PDV, RH, chat). Os agentes nunca sugerem vendê-la sem decisão sua.
- `push_faz_deploy: true` avisa NERD e SRE de que push na main publica sozinho, e que portanto exige mais cuidado.
- `nao_confundir`: pares de projetos com nomes parecidos.

### 4. Marcas
```yaml
marcas:
  - id: agenda
    entidade: tech
    grafia_oficial: "Agenda"
    design_system: "app-agenda/docs/DESIGN_SYSTEM.md"
    estado_design_system: nao_auditado
    voz: "literal, frases curtas, sem metáforas"
    proibicoes: ["prometer resultado garantido", "falar de lucro do cliente"]
```
`voz` e `proibicoes` são lidas por COPYWRITER, UX WRITER, SEO, CRM e SOCIAL-MEDIA. Coloque aqui as regras de comunicação da sua marca (o que nunca dizer, como grafar o nome, tom de emojis).

### 5. Orçamentos (envelopes)
```yaml
orcamentos:
  - projeto: app-agenda
    canal: google_ads
    periodo: "2026-01"
    teto: 0            # ou "pendente"
    status: pendente   # pendente | aprovado | encerrado
```
**Sem `status: aprovado` e teto numérico, TRAFICANTE e TESOUREIRO só preparam rascunho.** `entidade_pagadora` só é preenchida com fatura ou extrato que comprovem quem paga.

### 6. Autorizações permanentes
```yaml
autorizacoes:
  commit_push_automatico: [app-agenda]
  deploy_automatico: []
  leitura_producao:
    - projeto: app-agenda
      modo: logs
      via: mcp_plataforma
```
Deixe vazio para que os agentes perguntem sempre. Conceda o mínimo necessário.

### 7. Ferramentas
- `skill_video`: nome da skill de edição de vídeo que você já usa (o EDITOR a consulta e nunca a altera).
- `envio_marketing` e `envio_transacional`: ferramentas aprovadas. Vazio = o CRM só desenha réguas.
- `analytics_comportamental`: ferramentas de mapa de calor/gravação que o UX RESEARCHER pode **ler**.
- `plataforma_deploy`: onde seus sistemas rodam (ajuda SRE a escolher comandos de leitura).

## Integrações (MCP)
Os agentes principais não têm lista `tools`, então herdam as ferramentas da sua sessão. Os sub-agentes têm **lista fechada**: só usam o que está listado.

| Agente | MCP opcional já listado | Como trocar |
| --- | --- | --- |
| `qa`, `ux-researcher` | `mcp__claude-in-chrome__*` (extensão Claude in Chrome) | remova da lista se não usar |
| `sre` | `mcp__railway__*` só de leitura (exemplo) | troque pelas ferramentas **de leitura** do MCP da sua plataforma |
| `analista` | nenhum | acrescente ferramentas **de leitura** de anúncios/analytics |
| demais | nenhum | acrescente seu MCP de handoffs, se tiver |

Para descobrir o nome exato das ferramentas de um MCP, rode `/mcp` no Claude Code. Regra: em sub-agente, nunca liste ferramenta que **escreve, gasta, publica, apaga, faz deploy ou mostra variáveis/credenciais**.

## Ajustar um agente
Edite o `.md` em `~/.claude/agents/`. Mudanças comuns:
- `model:` (`opus`, `sonnet`, `haiku`) para equilibrar custo e qualidade;
- regras extras do seu setor (ex.: saúde, educação, finanças) na seção de regras;
- remover um agente que você não usa (apague o arquivo e a skill correspondente).

Para criar um novo: [CRIAR-NOVO-AGENTE.md](CRIAR-NOVO-AGENTE.md).
