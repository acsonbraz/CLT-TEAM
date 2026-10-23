# Playbook de resposta a incidentes

**Dono do processo:** SEGURANÇA. **Apoio técnico:** NERD e SRE. **Minutas de comunicação:** PRIVACIDADE. **Aprovação e envio de qualquer comunicação externa:** proprietário, com advogado.

> Não é parecer jurídico. Prazos e enquadramentos legais citados aqui devem ser confirmados com advogado em cada caso.

**Regras de sempre**
- Nunca cole segredo, token, cookie, dump ou dado pessoal no registro do incidente, em handoffs, memórias, commits ou mensagens. Confira chaves por **hash curto**.
- Contenha **sem derrubar** o serviço sempre que possível: chave nova convive com a antiga → atualize os consumidores → confirme → só então revogue a antiga.
- Preserve evidência antes de limpar.
- Um responsável por incidente (SEGURANÇA); decisões A3 com o proprietário.

## Severidade
| Nível | Exemplo | Resposta |
| --- | --- | --- |
| **SEV1** | dado pessoal ou financeiro exposto publicamente; credencial de produção vazada e possivelmente usada; sistema de pagamento comprometido | imediata; proprietário avisado na hora |
| **SEV2** | credencial vazada sem indício de uso; acesso indevido limitado; indisponibilidade prolongada de sistema crítico | no mesmo dia |
| **SEV3** | vulnerabilidade sem exploração; erro de configuração sem exposição comprovada | planejada, com prazo |

## Fluxo geral
| Fase | O que fazer | Quem |
| --- | --- | --- |
| **0. Abrir** | Registrar a hora em que se soube (marco de prazos legais), fonte do alerta, sistemas e entidades possivelmente afetados, severidade inicial. Abrir `registros/handoffs/AAAA-MM-DD_<projeto>_incidente_<assunto>.md`. | quem detectou → SEGURANÇA |
| **1. Conter** | Parar o vazamento sem destruir evidência: rotacionar/revogar credencial, encerrar sessões, bloquear conta, desligar recurso exposto, feature flag, regra de firewall. Ação destrutiva ou com queda é A3. | SEGURANÇA decide; NERD/sessão principal executa |
| **2. Preservar evidência** | Antes de limpar: exportar logs do período (aplicação, plataforma, provedores), lista de deploys e commits, hashes das chaves antigas, capturas sem PII. Guardar fora do repositório, com acesso restrito e data de descarte. | SRE + NERD |
| **3. Avaliar** | Escopo: o que vazou, desde quando, quem acessou, quantos titulares, quais categorias de dado, quais entidades. Dado pessoal envolvido? Risco ou dano relevante aos titulares? | SEGURANÇA + PRIVACIDADE |
| **4. Erradicar** | Corrigir a causa raiz (código, configuração, permissão), remover acesso indevido, limpar segredo do histórico se aplicável, atualizar dependências. Teste de regressão. | NERD; QA verifica |
| **5. Recuperar** | Restabelecer serviço e dados a partir de fonte confiável; monitorar reincidência por período definido. | SRE + NERD |
| **6. Comunicar** | Conforme a avaliação: ANPD, titulares, controladores (se você for operador), clientes, parceiros, provedores. Minutas pela PRIVACIDADE; decisão e envio pelo proprietário com advogado. | proprietário |
| **7. Aprender** | Pós-mortem sem culpados: linha do tempo, causa raiz, o que funcionou, o que falhou, ações com dono e prazo. Atualizar este playbook. | SEGURANÇA |

## Comunicação legal (Brasil, LGPD)
- Incidente com dado pessoal que possa causar **risco ou dano relevante** aos titulares deve ser comunicado à ANPD e aos titulares (art. 48 da LGPD; Res. CD/ANPD nº 15/2024, que fixa prazo em dias úteis a partir do conhecimento). **Confirme prazo e enquadramento com advogado.**
- Quem comunica é o **controlador**. Se você é operador (ex.: fornecedor SaaS processando dados de clientes), avise o controlador sem demora e apoie com informações.
- Conteúdo mínimo da comunicação: natureza dos dados, titulares envolvidos, medidas de segurança usadas, riscos, motivo de eventual demora, medidas tomadas para reverter ou mitigar, contato do encarregado.
- Guarde o registro do incidente (inclusive dos não comunicados) pelo prazo que o advogado indicar.

## Playbooks específicos

### A. Credencial ou segredo vazado (chave de API, senha de banco, token)
1. Identifique o segredo por nome e hash curto, nunca pelo valor.
2. Gere a credencial nova; configure nos consumidores; confirme funcionamento; **revogue a antiga**.
3. Verifique nos logs do provedor se a antiga foi usada depois do vazamento.
4. Se esteve em repositório: considere-a comprometida mesmo após remover o commit; avalie limpeza do histórico e o cache de forks/espelhos.
5. Procure o mesmo segredo reutilizado em outros sistemas.

### B. Vazamento de variáveis de ambiente / configuração da plataforma
1. Liste **por nome** as variáveis expostas e classifique: segredo, identificador, configuração.
2. Rotacione todos os segredos da lista, priorizando pagamento, banco, e-mail/SMS, provedores de IA e autenticação.
3. Valores derivados de um segredo (pepper/salt de hash, chaves de criptografia de dados) exigem plano de migração antes da troca: trocar sem migrar pode invalidar dados.
4. Revise quem e o que tinha acesso ao painel/CLI (tokens de CI, integrações, agentes) e reduza.

### C. Acesso indevido a dados entre clientes/entidades (falha de isolamento)
1. Contenha: desative a rota/feature afetada ou aplique a regra de autorização faltante.
2. Determine pelos logs quais registros foram lidos por quem.
3. Escreva teste de isolamento que reproduza a falha e comprove a correção.
4. Avalie comunicação como incidente de dado pessoal.

### D. Conta de anúncio, rede social ou e-mail comprometida
1. Troque a senha, revogue sessões e apps conectados, ative MFA.
2. Pause campanhas e conteúdos publicados pelo invasor; registre gasto indevido para contestação.
3. Avise a plataforma pelo canal oficial; avise o TESOUREIRO.
4. Publicação pública de correção só com aprovação do proprietário.

### E. Agente de IA executou ação indevida (prompt injection ou erro)
1. Interrompa a sessão; revogue o token/integração usado.
2. Liste as ações executadas (logs da ferramenta, histórico da sessão) e desfaça as reversíveis.
3. Identifique a origem da instrução (conteúdo externo, arquivo, resposta de ferramenta).
4. Endureça: retire a ferramenta da lista `tools`, exija aprovação, acrescente regra ao hook, reduza escopo do token.

### F. Indisponibilidade ou perda de dados
1. Declare a janela e o impacto; comunique a operação interna.
2. Restaure do último backup íntegro em ambiente separado antes de produção, quando possível.
3. Registre RPO/RTO observados e ajuste a rotina de backup e o teste de restauração.

## Modelo de registro do incidente
```
# INCIDENTE <projeto> — <assunto>   severidade: SEV1|SEV2|SEV3   estado: aberto|contido|resolvido
Soube em: AAAA-MM-DD HH:MM (fuso)   Fonte do alerta:
Entidades/sistemas afetados:
Dados pessoais envolvidos: sim/não/a confirmar — categorias (sem dados reais):
Linha do tempo: HH:MM — evento (sem segredos)
Contenção: ação → quem executou → resultado
Evidências preservadas: o quê, onde (fora do repositório), descarte em
Avaliação de risco aos titulares: ... (PRIVACIDADE + advogado)
Comunicações: ANPD (sim/não, data), titulares, controladores, parceiros — aprovadas por
Correção da causa raiz: commit/PR, teste de regressão
Ações de aprendizado: ação — dono — prazo
```
