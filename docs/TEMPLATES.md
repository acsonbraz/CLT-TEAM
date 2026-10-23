# Modelos de entregáveis

Copie o bloco do entregável e preencha. Exemplos sempre com dados fictícios.

## SPEC (produto)
```
# SPEC <projeto> — <título>   (status: rascunho | aprovada pelo proprietário em <data>)
Projeto / entidade / classificação: ...
Problema e evidência: ... (fonte; observado | hipótese)
Métrica de sucesso: ... (como medir; se não houver instrumentação, dizer)
Histórias:
  H1 Como <papel>, quero <ação>, para <resultado>.
Critérios de aceite (Gherkin):
  Cenário: <caminho feliz>
    Dado ... Quando ... Então ...
  Cenário: <borda: vazio, duplicado, sem permissão, outra empresa/unidade,
            valor limite, falha de integração, repetição/idempotência>
Regras de negócio: RN1 ... (fonte: código/arquivo/decisão)
Fora de escopo: ...
Perguntas ao proprietário: ...
Impacto: contratos, e-mails, preços, termos, dados existentes, outros sistemas
Custo variável: sim/não (para TESOUREIRO)
Sensível para SEGURANÇA: sim/não, por quê
```
Checklist: todo critério é testável (nada de "rápido", "intuitivo"); há cenário de permissão negada e de outra empresa/unidade quando multiempresa; regras com fonte; fora de escopo explícito; perguntas não viram suposição; tamanho proporcional.

## Relatório de QA (qa)
```
# QA <projeto> — <branch>@<commit>   veredito: aprovado | aprovado com ressalvas | reprovado
Ambiente: local | staging | produção (smoke de leitura)   Data/hora:
Comandos executados e resultado real:
  npm run check  ->  OK (N testes) | FALHOU (trecho do erro, sem segredos)
Critérios de aceite:
  H1/Cenário 1 ... PASSOU | FALHOU | NÃO TESTADO (motivo)
Defeitos:
  QA-1 [crítico|alto|médio|baixo] Título
    Passos para reproduzir: 1. ... 2. ...
    Esperado: ...   Obtido: ...
    Evidência: log/screenshot/arquivo de teste (caminho)
    Suspeita de causa (opcional): arquivo:linha
Regressão: áreas verificadas e não verificadas
Testes adicionados: caminhos
Encaminhado à SEGURANÇA: suspeitas (sem detalhes exploráveis)
```

## Plano de release (sre)
```
# PLANO DE RELEASE <projeto> — <commit>   risco: baixo | médio | alto   aprovação A3: sim/não
Pré-condições: testes (comando + resultado), QA (link), SEGURANÇA (link ou "não aplicável"),
               backup (data, onde, restauração testada sim/não)
Migrações: arquivo -> efeito -> reversível? -> trava? -> duração estimada -> ordem (expand/contract)
Ação em massa: consulta de dry-run, contagem, amostra anonimizada, aprovação
Passos de deploy: 1. ... (quem executa)
Verificação pós-deploy: o que olhar, por quanto tempo, limites que disparam rollback
Rollback: passos, tempo estimado, perda de dados possível
Comunicação: quem avisar
```

## Verificação pós-deploy (sre)
```
# VERIFICAÇÃO PÓS-DEPLOY <projeto> — <deployment>   resultado: estável | degradado | rollback recomendado
Janela observada: das HH:MM às HH:MM
Erros HTTP 5xx, latência, reinícios, erros de log novos (sem PII): antes x depois
Fluxos críticos conferidos (smoke de leitura): ...
Pendências e alertas a criar
```

## Runbook (sre, no repositório)
```
# RUNBOOK <sistema>   (docs/RUNBOOK.md)
Serviços e dependências · como verificar saúde · onde ficam os logs · deploy e rollback ·
backup e restauração · incidentes conhecidos e correção · aprovadores (papéis, sem contatos pessoais)
```

## Especificação de tela (designer → nerd, qa)
```
# TELA <projeto> — <fluxo>
Fluxo passo a passo: 1. ... 2. ...
Wireframe: texto ou HTML usando SÓ tokens/componentes do design system do projeto
Estados: carregando | vazio | erro | sem permissão | sucesso
Responsivo (mobile-first): breakpoints e o que muda
Acessibilidade: foco, labels, contraste, alvos de toque, movimento reduzido
Textos: tabela do ux-writer (ou pendente)
O que o QA confere visualmente: ...
```

## Ficha de direção de arte (designer → editor)
```
# DIREÇÃO DE ARTE <projeto> — <peça/campanha>
Projeto / entidade / canal / objetivo / duração; brand kit (caminho, versão, status de aprovação)
Conceito (até 3 frases) · referências verificadas · proibições estéticas
Paleta: background, foreground, primary, accent, legenda, gradientes permitidos; contraste
Tipografia: famílias (licença verificada), pesos, hierarquia, tracking/leading, legibilidade no celular
Geometria: grid, margens, safe areas, cantos e curvas, espessura de linha, posição do logo
Motion: entrada, permanência, saída, easing, duração, amplitude, direção, delays, relação com áudio
Storyboard: timecode | imagem/vídeo | texto exato aprovado | elemento visual | movimento | SFX | CTA
Formatos: 9:16 · 4:5 · 1:1 · 16:9; fps, resolução, codec
QA: legibilidade, cortes, consistência, licenças, ortografia, safe areas, contraste, evidência de render
```

## Brief de landing page (copywriter)
```
Objetivo · métrica · ICP · promessa verificável
Hero (≤10 palavras) + sub (≤25) + CTA
Problema · 3 passos · provas reais · FAQ/objeções · preço ou contato · CTA final
Evento a medir · pedido ao DESIGNER
```

## Régua de CRM (crm)
| id | gatilho (evento + atraso) | saída | canal | remetente | assunto (≤50) | preheader (40–90) | corpo | CTA + UTM | variáveis | base legal | descadastro | variante |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Auditoria heurística (ux-researcher)
| tela | heurística | problema | severidade 0–4 | evidência | sugestão |
| --- | --- | --- | --- | --- | --- |

## Tabela de microcopy (ux-writer)
| tela | elemento | texto | limite / contagem | estado | observação técnica |
| --- | --- | --- | --- | --- | --- |
