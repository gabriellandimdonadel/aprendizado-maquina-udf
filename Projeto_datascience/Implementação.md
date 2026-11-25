# Fase 6 — Implementação (CRISP-DM)

O guia CRISP-DM pede quatro entregáveis nesta fase: plano de implementação, plano de monitoramento, relatório final e revisão do projeto.

## 6.1 Plano de implementação (arquitetura)

O projeto estrutura-se como um **pipeline reprodutível de análise de dados** acoplado à arquitetura do GastroMatch. Para atualizar os indicadores com novos restaurantes, avaliações ou planilhas de cardápio, basta exportar o snapshot do Cloud Firestore e executar os notebooks em sequência:

```text
 Cloud Firestore / Planilhas (.xlsx)
            │
            ▼
 dados/brutos/*.json ──► src/extracao.py ──► dados/processados/gastromatch_analitico.xlsx / .csv
                         (normalização de        │
                          arrays e validação)    ▼
                                     notebooks/02_modelagem.ipynb ──► figuras/*.png
                                                 │                    resultado_modelagem_*.csv
                                                 ▼
                                     notebooks/03_avaliacao.ipynb ──► avaliacao_verificacoes.csv
