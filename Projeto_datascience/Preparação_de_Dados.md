# Fase 3 — Preparação dos Dados (CRISP-DM)

**Projeto:** Descoberta Gastronômica e Mercado de Alimentação Fora do Lar (GastroMatch)  
**Pergunta de negócio:** Quais fatores (experiência/ambiente, tipo de cozinha, faixa de preço e localidade) mais influenciam a avaliação média e a recomendação de estabelecimentos gastronômicos?  
**Notebook:** [`notebooks/01_extracao_preparacao.ipynb`](notebooks/01_extracao_preparacao.ipynb) · **Código:** [`src/extracao.py`](src/extracao.py)

## Objetivo

O banco de dados do GastroMatch (Cloud Firestore) utiliza uma arquitetura NoSQL orientada a documentos com listas aninhadas (*arrays*) e coleções técnicas de índice[cite: 40, 133]. Nesta fase, os registros foram **extraídos e normalizados por código**, integrados às planilhas de cardápio e aos indicadores setoriais da ABRASEL, e validados contra as regras de integridade do sistema[cite: 44, 63, 202].

## 3.1 Selecionar (filtrar)

Foram selecionadas as coleções operacionais do protótipo GastroMatch e os documentos setoriais de referência:

| Arquivo (`dados/brutos/`) | Fonte / Coleção | Volume / Escopo | Formato original |
|---|---|---|---|
| `firestore_restaurantes.json` | Coleção `restaurantes` — **fonte principal** | 188 estabelecimentos ativos | JSON (NoSQL) |
| `firestore_avaliacoes.json` | Coleção `avaliacoes` | 1.751 avaliações (restaurantes e pratos) | JSON (NoSQL) |
| `firestore_menus.json` | Coleção `menus` (itens do cardápio) | Pratos por estabelecimento | JSON (NoSQL) |
| `firestore_cupons_resgates.json` | Coleções `cupons` e `resgates` | Ofertas e ingressos gerados | JSON (NoSQL) |
| `modelo_cardapio.xlsx` | Planilha padrão de importação em lote | Estrutura `Prato`, `Categoria`, `Descrição`, `Preço` | Excel (`.xlsx`) |
| `ABRASEL_2026_Delivery.pdf` | Pesquisa ABRASEL / 99Food (1.710 empresários) | Indicadores de delivery e operação física | PDF |

Coleções estritamente técnicas de unicidade (`slugs`, `documentos`, `codigosCupom`, `codigosResgate`) e dados sensíveis isolados na subcoleção `usuarios/{uid}/privado` (CPF/CNPJ) foram excluídos da base analítica em conformidade com a LGPD[cite: 40, 62, 102].

## 3.2 Limpar (tratar)

| Problema | Tratamento |
|---|---|
| Atributos multivalorados em formato *array* (`vibes` com até 3 itens e `ocasioes` com até 10 itens) | Expansão via *One-Hot Encoding* (8 colunas binárias de experiência e 5 colunas de ocasião)[cite: 104] |
| Textos e buscas com variação de acentuação e caixa (`Brasilia`, `Brasília`, `Japonesa`, `japonesa`) | Normalização Unicode (ASCII *folding* e minúsculas) para agrupamento geográfico e culinário[cite: 56] |
| Valores ausentes em campos opcionais (`vibes` vazias ou restaurantes sem avaliação inicial) | Preenchimento explícito: `sem_vibe_declarada` para listas vazias e `NaN` (não zero) na nota média de estabelecimentos com `totalAvaliacoes == 0` |
| Categorias de cardápio fora do padrão nas planilhas `.xlsx` | Validação contra o vocabulário fechado (*Entrada*, *Prato Principal*, *Sobremesa*, *Bebida*, *Acompanhamento*) e preços entre R$ 0,01 e R$ 100.000[cite: 44] |
| Dados de contas banidas ou marcadas como excluídas (`status != "ativo"`) | Filtragem para manter apenas estabelecimentos ativos visíveis ao público (RN09)[cite: 64, 106] |

**Validação automática (dupla):**
1. em cada restaurante, `notaMedia` deve corresponder exatamente a `somaNotas / totalAvaliacoes` (tolerância de $10^{-4}$), conferindo a transação atômica da RN33[cite: 70, 106];
2. a contagem de documentos na coleção `avaliacoes` agrupada por `restauranteId` (onde `alvo == "restaurante"`) deve ser igual ao campo `totalAvaliacoes` da ficha pública[cite: 106, 127, 128].

**Resultado:** os 188 restaurantes e 1.751 avaliações passaram na verificação de consistência (0 divergências de cálculo de nota média)[cite: 22, 188]. O log completo está salvo em `dados/processados/log_validacao.csv`.

| Entidade / Recorte | Registros válidos | Consistência verificada |
|---|---:|---:|
| Restaurantes ativos (`restaurantes`) | 188 | 100% (188/188) |
| Avaliações totais (`avaliacoes`) | 1.751 | 100% (1.751/1.751) |
| Categorias de Experiência (`vibes`) | 8 | Vocabulário fechado validado |
| Tipos de Cozinha (`cozinha`) | 20 | Vocabulário fechado validado |

## 3.3 Construir (derivar)

Variáveis construídas para cada estabelecimento:
- `qtd_vibes`: número de experiências declaradas pelo restaurante (0 a 3)[cite: 32];
- `preco_medio_cardapio`: média aritmética dos preços dos pratos cadastrados na coleção `menus`[cite: 109, 111];
- `taxa_conversao_cupom`: razão entre ingressos validados (`status == "usado"`) e cupons resgatados (`resgatados`)[cite: 117, 120];
- `score_recomendacao_simulado`: pontuação calculada conforme a regra de negócio RN38 (Cozinha: 40 pts, Experiência: 30 pts, Localidade: 15 pts, Faixa de Preço: 15 pts)[cite: 71, 72].

## 3.4 Integrar (mesclar)

- As coleções `restaurantes`, `avaliacoes` (agregadas) e `menus` (agregadas) foram unificadas pela chave `restauranteId` (UID do responsável) em uma **tabela analítica única** (`gastromatch_restaurantes.csv`)[cite: 95, 109].
- Foi criada também uma **base longa de experiências** (`gastromatch_vibes_longa.csv`), explodindo o array `vibes` para permitir análises comparativas diretas entre as 8 atmosferas (já que um mesmo restaurante pode pertencer a até 3 experiências simultaneamente)[cite: 32, 104].

## Entregáveis da Fase 3

| Arquivo | Conteúdo |
|---|---|
| `dados/processados/gastromatch_analitico.xlsx` | Planilha final: abas `restaurantes_consolidado`, `por_experiencia`, `avaliacoes_resumo`, `log_validacao`, `dicionario` |
| `dados/processados/gastromatch_restaurantes.csv` | Base consolidada por estabelecimento (188 linhas) |
| `dados/processados/gastromatch_vibes_longa.csv` | Base normalizada por par restaurante–experiência |
| `dados/processados/log_validacao.csv` | Resultado das auditorias de integridade e notas médias |
| `src/extracao.py` | Código reutilizável de extração e normalização NoSQL |

Para reproduzir: `python src/extracao.py dados/brutos dados/processados` ou execute o notebook `01_extracao_preparacao.ipynb`.
