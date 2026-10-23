# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/); versões seguem [SemVer](https://semver.org/lang/pt-BR/).

## [1.0.0] — 2026-10-23
### Adicionado
- 9 agentes principais: `socio`, `nerd`, `seguranca`, `designer`, `editor`, `marketeiro`, `traficante`, `tesoureiro`, `social-media`.
- 10 sub-agentes: `copywriter`, `seo`, `analista`, `crm` (marketing); `produto`, `qa`, `sre` (engenharia); `privacidade` (segurança); `ux-researcher`, `ux-writer` (design).
- Skills `/equipe`, `/equipe-toda` e atalhos por agente principal.
- Hook `guarda-segredos.py` com perfis `produto`, `qa`, `sre` e `marketing`, e autoteste.
- `config/empresa.example.yaml` com entidades, projetos, marcas, orçamentos, aprovadores e autorizações.
- Documentação: governança, hierarquia, protocolo de handoff, modelos, design systems, guias de instalação, configuração, uso e segurança, playbook de incidentes, criação de agentes e FAQ.
- Instalador `scripts/instalar.sh` com simulação e backup.
