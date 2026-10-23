# Perguntas frequentes

**O que é o CLT-TEAM?**
Um modelo de equipe de agentes para o Claude Code: 9 agentes principais e 10 sub-agentes, com governança, protocolo de handoff, níveis de autonomia e proteções. É um template para você adaptar à sua empresa.

**Por que "CLT"?**
É uma brincadeira com a "equipe contratada" brasileira: papéis definidos, hierarquia, escopo do que cada um faz e não faz. Nenhum agente substitui funcionário, contador, advogado ou encarregado de dados.

**Por que o gestor de tráfego se chama TRAFICANTE?**
Gíria bem-humorada para "gestor de tráfego pago". Se preferir, renomeie: troque `name:` no agente, o nome da pasta da skill e as menções em `docs/` e nas skills `equipe`/`equipe-toda`.

**Os agentes vão gastar dinheiro ou publicar sozinhos?**
Não por padrão. Gasto, publicação, envio e deploy crítico são A3: exigem sua aprovação explícita (`APROVO <código>`, palavra configurável). Sem orçamento aprovado no `empresa.yaml`, TRAFICANTE e TESOUREIRO só fazem rascunho. Ainda assim, configure limites também nas próprias plataformas.

**Preciso de todas as integrações (MCP)?**
Não. Sem integrações, os agentes planejam, escrevem, revisam código local e entregam rascunhos e checklists. Cada integração que você conecta amplia o que eles podem executar, dentro das regras.

**Funciona com uma empresa só?**
Sim. Cadastre uma entidade e quantos projetos quiser. A separação por entidade só faz diferença quando você tem mais de um CNPJ, mas não atrapalha com um.

**O que é projeto `interno` x `comercial`?**
`comercial` é algo que você vende (SaaS, app, serviço). `interno` é ferramenta da sua operação (ERP, PDV, RH, chat). Os agentes nunca sugerem vender um sistema interno sem decisão sua, e não usam a marca ou os dados de um no outro.

**Por que os sub-agentes não entram em `/equipe-toda`?**
Economia de tokens e foco. Chame pelo nome quando precisar: "peça ao qa...", ou `/equipe projeto qa e sre revisem...`.

**Quanto custa usar?**
Depende do seu plano do Claude e do volume. `/equipe-toda` chama nove agentes e custa bem mais que um atalho individual. Os agentes de texto usam `sonnet` por padrão; troque o `model:` se quiser economizar ou ganhar qualidade.

**O hook `guarda-segredos.py` me protege de tudo?**
Não. Ele bloqueia padrões comuns de exposição de segredos e de alteração de produção nos sub-agentes, mas não cobre ferramentas MCP nem toda escrita via shell. Ver [GUIA-SEGURANCA.md](GUIA-SEGURANCA.md).

**Posso usar em inglês?**
Os prompts estão em português do Brasil e citam LGPD. Para outro idioma/país, traduza os agentes e troque as referências legais (ex.: GDPR). Contribuições com traduções são bem-vindas.

**Onde ficam as memórias dos agentes?**
O campo `memory: user` usa a memória persistente do Claude Code, por usuário. Nunca peça para guardarem segredos ou dados pessoais. Remova o campo se não quiser memória.

**Agent Teams é obrigatório?**
Não. É um recurso experimental do Claude Code para conversa direta entre agentes. Sem ele, a sessão principal coordena os retornos, que é o modo padrão e mais econômico.

**Posso publicar minha versão configurada?**
Publique só o que é genérico. `config/empresa.yaml` e `registros/` estão no `.gitignore` justamente para não irem a um repositório público. Antes de publicar, faça uma varredura por nomes, CNPJs, e-mails, telefones, IDs de contas e tokens.

**Como contribuir?**
Ver [CONTRIBUTING.md](../CONTRIBUTING.md).
