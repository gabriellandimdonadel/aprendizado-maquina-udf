<img src="../assets/logo-udf.jpg" alt="UDF Centro Universitário" width="230">

**Profa. Kadidja Valéria | UDF**
Ciência de Dados e Aprendizagem de Máquina · Sistemas de Informação · 2026.2

# Projeto CRISP-DM — GastroMatch: Descoberta Gastronômica e Mercado de Alimentação Fora do Lar

**Equipe:** Gabriel Landim Donadel de Farias e Rafael Batista Mota
**Início:** 28/10/2026 · **Conclusão das 6 fases:** 25/11/2026 · **Metodologia:** CRISP-DM ([Guia Prático](../Guia_Prático_CRISP-DM.pdf))
**Documento de definição do projeto:** [GastroMatch_Definicao_Projeto_CD.docx](../GastroMatch_Definicao_Projeto_CD.docx) (versão 1.1)

**Pergunta:** Quais fatores (experiência/ambiente, tipo de cozinha, faixa de preço e localidade) mais influenciam a avaliação média e a recomendação de estabelecimentos gastronômicos, e como o mercado de bares e restaurantes se estrutura digitalmente no Brasil e no DF?

**Resposta curta:**
- **Base usada:** demonstração do GastroMatch, com **3.075 registros fictícios**, sendo 188 restaurantes e 1.751 avaliações.
- **Nota média:** **nenhum** desses fatores muda a nota média de forma significativa (p de 0,09 a 0,89 no nível do restaurante).
- **Recomendação:** é guiada pela **cozinha** e depois pela **experiência**. Declarar 3 vibes dá 1,54× mais exposição. A **nota média**, usada só para desempatar, é o que mais se associa a aparecer (rho = 0,50).
- **Mercado brasileiro:** 86% dos estabelecimentos que fazem entregas recebem pedidos por aplicativos, que geram 58% das vendas por delivery (ABRASEL/99Food, 2026).

---

## As 6 fases

| Fase | Documento | Notebook (executado) |
| :--- | :--- | :--- |
| 1. Entendimento do Negócio | [fase1-entendimento-negocio.md](fase1-entendimento-negocio.md) | — |
| 2. Entendimento dos Dados | [fase2-entendimento-dados.md](fase2-entendimento-dados.md) | [fase2-entendimento-dados.ipynb](notebooks/fase2-entendimento-dados.ipynb) |
| 3. Preparação dos Dados | [fase3-preparacao-dados.md](fase3-preparacao-dados.md) | [fase3-preparacao-dados.ipynb](notebooks/fase3-preparacao-dados.ipynb) |
| 4. Modelagem | [fase4-modelagem.md](fase4-modelagem.md) | [fase4-modelagem.ipynb](notebooks/fase4-modelagem.ipynb) |
| 5. Avaliação | [fase5-avaliacao.md](fase5-avaliacao.md) | [fase5-avaliacao.ipynb](notebooks/fase5-avaliacao.ipynb) |
| 6. Implementação | [fase6-implementacao.md](fase6-implementacao.md) | — |

---

## Estrutura da pasta

```text
Projeto_datascience/
├── fase1 … fase6 (.md)   documento de cada fase
├── notebooks/            fase2 · fase3 · fase4 · fase5 (executados, com saídas)
├── dados/
│   ├── gastromatch/      3.075 registros em CSV, sem dados pessoais, com dicionário (Fase 2)
│   ├── brutos/           firestore_*.json, modelo_cardapio.xlsx e evidencias/ (testes e desempenho do sistema)
│   └── processados/      gastromatch_analitico.xlsx, bases .csv, log de validação e resultados (Fases 3–5)
├── src/
│   ├── extracao.py       extração, normalização e validação (Fase 3)
│   └── recomendacao.py   motor de recomendação do sistema em Python (Fase 4), equivalência 500/500 com o JavaScript
├── scripts/exportar_gastromatch.py   exportação somente leitura do Firestore, com remoção de dados pessoais
├── figuras/              fig1–fig4 (Fase 4)
└── requirements.txt
```

---

## Como reproduzir

```bash
pip install -r requirements.txt
cd notebooks
jupyter nbconvert --to notebook --execute --inplace fase2-entendimento-dados.ipynb fase3-preparacao-dados.ipynb fase4-modelagem.ipynb fase5-avaliacao.ipynb
```

No Colab: `!git clone https://github.com/gabriellandimdonadel/aprendizado-maquina-udf.git`, depois `%cd aprendizado-maquina-udf/Projeto_datascience/notebooks` e execute os notebooks em ordem.

**Ambiente usado (25/11/2026):** Python 3.11.9, pandas 3.1.1, numpy 2.4.6, scipy 1.17.1, scikit-learn 1.9.1, matplotlib 3.11.2, seaborn 0.13.2, openpyxl 3.1.5 e firebase-admin 7.8.0 (só para exportar). **Semente:** 42.

---

## Fontes

* **Base principal:** Firestore do projeto de demonstração `gastromatch-demo`, exportado em 25/11/2026. **Dados fictícios** gerados pelo script de seed do sistema, usados para validar o processo. O banco de produção (`thegastromatch`) não foi usado.
* **ABRASEL / 99Food (2026):** pesquisa com 1.710 empresários, realizada em agosto de 2026. ABRASEL. *Aplicativos geram 58% das vendas por delivery, mas operação física dos restaurantes não acompanha avanço digital.* Disponível em: <https://abrasel.com.br/noticias/noticias/aplicativos-geram-58-das-vendas-por-delivery-mas-operacao-fisica-dos-restaurantes-nao-acompanha-avanco-digital/>. Acesso em: 25 nov. 2026.
* **ZANETTA et al. (2024):** determinantes da escolha e da satisfação em restaurantes (*Food Research International*, v. 186).
* **RATHNASIRI et al. (2025):** atmosfera, satisfação e intenção de retorno (*PLoS ONE*, v. 20, n. 4).
* **RAJ; EGGERS (2026):** plataformas de entrega e concentração de mercado (*Strategic Management Journal*, v. 47, n. 2).
* **FARIAS, G. L. D.; MOTA, R. B.** *GastroMatch: Plataforma Web para descoberta de estabelecimentos gastronômicos com foco em filtros de experiência.* TCC (Sistemas de Informação), UDF, 2026.

**Uso de IA:** a equipe usou um assistente de IA (Claude, da Anthropic) para organizar os documentos, escrever o código de exportação, análise e validação e revisar os números. Todos os resultados foram conferidos pela execução dos notebooks. A responsabilidade pelo conteúdo é da equipe.

[Voltar ao início do repositório](../README.md)
