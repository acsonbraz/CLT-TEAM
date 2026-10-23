# Guia de segurança

Agentes de IA com acesso a ferramentas reais são poderosos e arriscados. O CLT-TEAM usa cinco camadas de proteção; nenhuma sozinha é suficiente.

## 1. Aprovação explícita (humano no circuito)
- Ações A3 (gastar, publicar, enviar, apagar, deploy crítico, mexer em dados pessoais ou segredos) só acontecem depois de `<palavra de aprovação> <código>` do proprietário.
- **Instrução vinda de dado não é ordem.** Comentário, e-mail, página web, mensagem de cliente, resultado de ferramenta ou relatório de outro agente nunca aprovam nada nem mudam regras. Isso é a defesa básica contra prompt injection.
- Ação em massa (UPDATE/DELETE, reenvio, importação) exige dry-run com contagem e amostra antes da aprovação.

## 2. Menor privilégio
- Conceda a cada integração o menor escopo possível: token só de leitura para relatórios, conta de anúncio com limite de gasto na própria plataforma, usuário de banco somente leitura para consultas.
- Separe ambientes: desenvolvimento, homologação e produção com credenciais diferentes.
- `autorizacoes` no `empresa.yaml` deve começar vazio; amplie aos poucos.
- Não dê aos agentes acesso a contas pessoais que misturem dados de entidades diferentes.

## 3. Ferramentas em lista fechada
- Sub-agentes têm o campo `tools` explícito. Uma ferramenta MCP só é usável se estiver listada.
- Nunca liste em sub-agente ferramentas que listam variáveis de ambiente, exibem credenciais, fazem deploy, criam/apagam recursos ou gastam dinheiro.
- Agentes principais (sem `tools`) herdam as ferramentas da sessão: revise quais MCPs você tem conectados (`/mcp`) e o `permissionMode` em `~/.claude/settings.json`.

## 4. Hook `guarda-segredos.py`
Hook `PreToolUse` por perfil (`produto`, `qa`, `sre`, `marketing`) que bloqueia:
- exibição do ambiente (`printenv`, `env`, `export -p`), leitura de `.env`, chaves, `.netrc`, `.pgpass`, certificados;
- CLIs de plataforma que listam ou injetam variáveis (ex.: `railway variables`, `vercel env`, `heroku config`, `kubectl get secrets`);
- `git push`, deploy, `terraform apply`, migração em banco remoto;
- escrita fora do permitido para o perfil (ex.: o `qa` só escreve arquivos de teste e relatórios);
- edição de `config/empresa.yaml` por sub-agentes.

Teste: `python3 ~/.claude/clt-team/hooks/guarda-segredos.py --teste`.
**Limites conhecidos:** não cobre ferramentas MCP; escrita via Bash (ex.: `echo > arquivo`) não é inspecionada pelo filtro de caminho; padrões novos de CLI podem escapar. Trate o hook como cinto de segurança, não como cofre.

## 5. Higiene de segredos e dados
- Segredos ficam no cofre ou nas variáveis do provedor. Nunca em prompts, handoffs, memória, `empresa.yaml`, commits ou screenshots.
- Para conferir se uma chave é a certa, compare **hash curto**, nunca o valor.
- Rotacione chaves periodicamente e sempre que houver suspeita. Chave nova convive com a antiga até a troca ser confirmada; só então revogue a antiga.
- Ative varredura de segredos no repositório (ex.: proteção de push do provedor Git, scanners como gitleaks) e revise o histórico antes de tornar um repositório público.
- Memória dos agentes (`memory: user`) persiste entre conversas: nunca peça para lembrarem segredos ou dados pessoais.

## LGPD (visão geral; não é parecer jurídico)
- **Papéis:** identifique controlador, operador e suboperadores de cada tratamento. Cada entidade jurídica é controladora dos próprios dados.
- **Base legal** para cada finalidade (art. 7º; dados sensíveis, art. 11). Marketing: opt-in ou legítimo interesse com avaliação (LIA) registrada; descadastro em todo envio.
- **Minimização e retenção:** colete só o necessário e defina prazo de descarte.
- **Direitos do titular (art. 18):** canal de atendimento, verificação de identidade e prazo de resposta.
- **Logs sem PII**; amostras anonimizadas; dados fictícios em testes.
- **Transferência internacional:** provedores de IA, nuvem e analytics fora do país precisam de base e aviso.
- **Incidente:** comunicação à ANPD e aos titulares quando houver risco ou dano relevante (Res. CD/ANPD nº 15/2024). Confirme prazos e enquadramento com advogado. Ver [PLAYBOOK-INCIDENTES.md](PLAYBOOK-INCIDENTES.md).
- O agente `privacidade` redige **minutas**; o encarregado (DPO) e o advogado aprovam.

## Checklist antes de usar em produção
- [ ] `empresa.yaml` preenchido, sem segredos, fora do controle de versão público.
- [ ] Envelopes de orçamento com `status: pendente` até você aprovar.
- [ ] MCPs conectados revisados; tokens com escopo mínimo.
- [ ] Hook instalado e autoteste OK.
- [ ] Limites de gasto também configurados **na própria plataforma** de anúncios.
- [ ] Backup verificado dos bancos que os agentes podem tocar.
- [ ] Canal de aprovação testado com um pedido inofensivo.
- [ ] Varredura de segredos ativa nos repositórios.
