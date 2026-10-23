# Protocolo de colaboração e handoff

## Como os agentes conversam
**Modo padrão (econômico).** A sessão principal (ou o SÓCIO) recebe o pedido, escolhe só os agentes relevantes e os chama em paralelo, quando independentes, ou em sequência, quando um depende do outro. Recebe os relatórios, sintetiza e repassa ao próximo o que ele precisa. Subagentes não têm sala de mensagens persistente: a coordenação passa pela sessão principal e pelos arquivos de handoff.

**Modo reunião (experimental, opcional).** Com Agent Teams habilitado no Claude Code, a sessão líder monta um time com os mesmos tipos de `agents/*.md`, distribui tarefas e permite mensagens diretas entre participantes. Use só em decisões complexas: reunião consome muitos tokens e pode perder continuidade ao retomar a sessão.

**Regra de ouro:** nenhum agente diz que consultou outro sem que a consulta tenha acontecido.

## Roteamento sugerido
| Pedido | Participantes | Ordem |
| --- | --- | --- |
| Nova campanha de produto comercial | socio, marketeiro, tesoureiro, traficante, designer, editor | estratégia → verba → campanha/briefing → guidelines da marca → criativo → validação |
| Novos anúncios e otimização | traficante (+ tesoureiro se mexer em verba) | verba autorizada → execução → relatório |
| Vídeo de campanha | marketeiro, designer, editor (+ traficante se pago) | briefing → identidade vigente → ficha de direção de arte → montagem → preview → QA visual → export |
| Decisão de produto ou preço | socio, marketeiro, tesoureiro | hipóteses → economia → decisão |
| Feature ou refactor | nerd, seguranca (+ designer se UI) | impacto/arquitetura → tokens/componentes → implementação → testes/auditoria |
| Auditoria e consolidação visual | designer, nerd (+ socio se mudar marca) | fontes → conflitos → sistema canônico → proposta → testes visuais |
| Integração com API externa | nerd, seguranca, tesoureiro | escopo/limites → riscos → custos → execução |
| Incidente de segurança | seguranca (líder), nerd, sre; socio notificado | conter → preservar evidência → corrigir → verificar → comunicar |
| Sistema interno da operação | nerd, seguranca (+ socio/tesoureiro se custo) | foco operacional, **nunca** venda como SaaS |
| Instagram orgânico | social-media, designer, editor, marketeiro | pauta → peça/vídeo → legenda → pedido de aprovação → publicação → métricas |

## Formato de handoff (obrigatório)
Todo agente entrega:

```
PROJETO: <id> (<interno|comercial>) — entidade: <id da entidade>
OBJETIVO: ...
ESTADO: observado | estimado | hipótese | não verificado
DADOS/BASE: <fontes, identificadores, períodos>
AÇÃO EXECUTADA: <o quê, onde, resultado comprovado> (ou "nenhuma")
RECOMENDAÇÃO: ...
RISCOS/BLOQUEIOS: ...
CUSTO E ENVELOPE: <estimativa; dentro de envelope aprovado? sim/não>
DEPENDÊNCIAS: <agentes que precisam agir + mensagem resumida>
APROVAÇÃO REQUERIDA: <sim/não + motivo + nível A0–A3>
PRÓXIMO PASSO: ...
```

## Arquivos de registro
| Arquivo | Conteúdo | Regra |
| --- | --- | --- |
| `config/empresa.yaml` | entidades, projetos, marcas, tetos, aprovadores | editado só pelo proprietário |
| `registros/DECISOES.md` | decisões aprovadas com data e justificativa | nunca inventar decisão |
| `registros/handoffs/` | um arquivo por transição: `AAAA-MM-DD_<projeto>_<agente>_<assunto>.md` | evitar escrita concorrente no mesmo arquivo |

Se a sessão não tiver acesso a `~/.claude/clt-team/`, o orquestrador injeta o conteúdo relevante no prompt de delegação.

## Integrações de registro (opcional)
Se você tiver um servidor MCP próprio para handoffs e decisões (banco, planilha, gestor de tarefas), acrescente as ferramentas dele à lista `tools` dos sub-agentes. O formato do handoff continua o mesmo. Ver `docs/GUIA-CONFIGURACAO.md`.
