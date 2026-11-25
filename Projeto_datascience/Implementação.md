# Fase 6 — Implementação (CRISP-DM)

O Guia CRISP-DM pede quatro entregáveis nesta fase: plano de implementação, plano de monitoramento, relatório final e revisão do projeto.

## 6.1 Plano de implementação (arquitetura)

O projeto é um **pipeline reprodutível de análise de dados** acoplado à arquitetura do GastroMatch. Para atualizar os indicadores, basta exportar o Firestore e executar os notebooks em sequência:

```text
 Cloud Firestore (somente leitura, chave de conta de serviço fora do Git)
            │  scripts/exportar_gastromatch.py --chave <chave.json> --json-destino Projeto_datascience/dados/brutos
            ▼     (remove nome, e-mail, telefone, endereço, coordenadas e fotos; pseudonimiza clientes)
 dados/brutos/firestore_*.json ──► src/extracao.py ──► dados/processados/gastromatch_analitico.xlsx / *.csv
                                   (vocabulário oficial,    │   log_validacao.csv
                                    validações, one-hot)    ▼
                     notebooks/02_modelagem.ipynb ──► figuras/fig1–fig4.png
                       (src/recomendacao.py =             resultado_modelagem_gastromatch.csv
                        motor do sistema em Python)       │
                                                          ▼
                     notebooks/03_avaliacao.ipynb ──► avaliacao_verificacoes.csv
```

| Etapa | Quem | Quando |
|---|---|---|
| Exportar o Firestore de **produção** (`thegastromatch`) | Gabriel (dono da chave) | Mensalmente, ou após cada lote de novos parceiros |
| Rodar `01` → `02` → `03` | Rafael | Logo após a exportação |
| Revisar as verificações (`avaliacao_verificacoes.csv`) e publicar os indicadores no painel do restaurante | Equipe | Se todas as verificações passarem |

Comando de reprodução (a partir de `Projeto_datascience/`):

```bash
pip install -r requirements.txt
cd notebooks
jupyter nbconvert --to notebook --execute --inplace 01_extracao_preparacao.ipynb 02_modelagem.ipynb 03_avaliacao.ipynb
```

## 6.2 Plano de monitoramento

| O que monitorar | Indicador | Gatilho de ação |
|---|---|---|
| Integridade da base | Erros em `log_validacao.csv`; verificações 1 e 2 (notaMedia e totalAvaliacoes) | Qualquer erro → corrigir antes de publicar indicadores |
| Volume real | Avaliações e clientes **reais** em produção | ≥ 1.000 avaliações reais de ≥ 100 clientes → refazer os testes da Fase 4 (substituem os resultados da base fictícia) |
| Mudança na regra de recomendação | Equivalência `recomendacao.py` × `recomendacao.js` | Qualquer alteração no JS → atualizar o Python e repetir a comparação das 500 buscas |
| Vocabulário | Vibes e cozinhas fora de `catalogo.js` | Nova categoria no sistema → atualizar `src/extracao.py` |
| Concentração da exposição | Correlação aparições × nota; % de buscas em "cozinha em outra cidade" | rho > 0,5 ou > 40% → revisar o desempate e a captação de parceiros por cidade |
| Obsolescência do modelo | Silhueta do K-means; p-valores dos testes | Recalcular a cada exportação; não usar clusters com silhueta < 0,25 como segmentos |
| LGPD | Campos pessoais nas saídas | Qualquer ocorrência → bloquear a publicação |

## 6.3 Relatório final

**Pergunta:** quais fatores mais influenciam a avaliação média e a recomendação de estabelecimentos gastronômicos?

**Resposta (base de demonstração, dados fictícios, 3.075 registros):**

1. **Nenhum fator explica a nota média.** Experiência, faixa de preço, cozinha e estado não têm efeito significativo no nível do restaurante (p de 0,09 a 0,89).
2. **A recomendação é guiada pela cozinha**, que filtra e pesa 40 pontos, e depois pela **experiência** (30 pontos). Declarar 3 vibes dá 1,54× mais exposição que 1.
3. **A nota média, usada só como desempate, é o atributo mais associado à exposição** (rho = 0,50).
4. O cadastro é **coerente**: a faixa acompanha o preço do cardápio (rho ≈ 0,7). As experiências Sofisticada e Romântica aparecem mais nas faixas altas, mas a associação é fraca.
5. O catálogo é **esparso por cidade**: 47% das buscas não encontram a cozinha na cidade pedida.
6. **Mercado:** 86% dos estabelecimentos que fazem entregas recebem pedidos por aplicativos, que geram 58% das vendas por delivery (ABRASEL/99Food, 2026). O GastroMatch ocupa o espaço da descoberta do salão.

Detalhes: [Modelagem](Modelagem.md) e [Avaliação](Avaliação.md). Base e dicionário: `dados/processados/gastromatch_analitico.xlsx`.

## 6.4 Revisão do projeto (lições aprendidas)

| O que funcionou | O que mudar na próxima iteração |
|---|---|
| Exportação somente leitura com remoção de dados pessoais desde o início | Usar a **produção** assim que houver volume real |
| Validação cruzada dos campos calculados do sistema (188/188) | Registrar no sistema os eventos que faltam: buscas, visualizações e cliques no WhatsApp |
| Tradução do motor de recomendação com prova de equivalência (500/500) | Manter `recomendacao.py` sincronizado com o JS (monitoramento §6.2) |
| Testes no nível certo (restaurante), que evitaram falsos positivos | Definir a unidade de análise **antes** de testar |
| Corrigir o código e os documentos quando os números reais contradisseram o esperado: silhueta 0,22 em vez de 0,48; 1,54× em vez de 2,4×; correlações fracas, e não fortes | Só escrever resultados depois de executar os notebooks |
