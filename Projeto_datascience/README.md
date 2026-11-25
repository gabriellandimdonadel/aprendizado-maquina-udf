# Projeto de Ciência de Dados — Descoberta Gastronômica e Mercado de Alimentação Fora do Lar (GastroMatch)

**Disciplina:** Ciência de Dados e Aprendizagem de Máquina · UDF · 2026.2
**Docente:** Profa. Kadidja Valéria
**Equipe:** Gabriel Landim Donadel de Farias e Rafael Batista Mota
**Início:** 28/10/2026 · **Metodologia:** CRISP-DM (guia IBM)

**Pergunta:** Quais fatores (experiência/ambiente, tipo de cozinha, faixa de preço e localidade) mais influenciam a avaliação média e a recomendação de estabelecimentos gastronômicos, e como o mercado de bares e restaurantes se estrutura digitalmente no Brasil e no DF?

**Resposta curta:**
- **Base usada:** demonstração do GastroMatch, com dados **fictícios**: 3.075 registros, sendo 188 restaurantes e 1.751 avaliações.
- **Nota média:** **nenhum** dos fatores muda a nota média de forma significativa (Kruskal-Wallis no nível do restaurante, p de 0,09 a 0,89).
- **Recomendação:** é guiada pela **cozinha** (filtra e pesa 40) e pela **experiência** (30). Declarar 3 vibes dá 1,54× mais exposição. A **nota média**, usada só como desempate, é o atributo mais associado a aparecer (rho = 0,50).
- **Mercado brasileiro:** 86% dos estabelecimentos que fazem entregas recebem pedidos por aplicativos, que geram 58% das vendas por delivery (ABRASEL/99Food, 2026). Isso evidencia a concentração digital fora do salão.

---

## Fases do CRISP-DM

| Fase | Documento | Notebook |
| :--- | :--- | :--- |
| 1. Entendimento do Negócio | [`Entendimento_do_Negócio.md`](Entendimento_do_Negócio.md) | — |
| 2. Entendimento dos Dados | [`Entendimento_dos_Dados.md`](Entendimento_dos_Dados.md) | [`../notebooks/gastromatch-fase2-entendimento-dados.ipynb`](../notebooks/gastromatch-fase2-entendimento-dados.ipynb) |
| 3. Preparação dos Dados | [`Preparação_de_Dados.md`](Preparação_de_Dados.md) | [`notebooks/01_extracao_preparacao.ipynb`](notebooks/01_extracao_preparacao.ipynb) |
| 4. Modelagem | [`Modelagem.md`](Modelagem.md) | [`notebooks/02_modelagem.ipynb`](notebooks/02_modelagem.ipynb) |
| 5. Avaliação | [`Avaliação.md`](Avaliação.md) | [`notebooks/03_avaliacao.ipynb`](notebooks/03_avaliacao.ipynb) |
| 6. Implementação | [`Implementação.md`](Implementação.md) | — |

Todos os notebooks estão **executados**, com as saídas salvas.

---

## Estrutura

```text
Projeto_datascience/
├── dados/
│   ├── brutos/          firestore_*.json (exportação sem dados pessoais), modelo_cardapio.xlsx, evidencias/ (testes e desempenho do sistema)
│   └── processados/     gastromatch_analitico.xlsx, bases .csv, log_validacao.csv, resultados da modelagem e da avaliação
├── src/
│   ├── extracao.py      extração, normalização (vocabulário oficial) e validação dos dados do Firestore
│   └── recomendacao.py  motor de recomendação do sistema traduzido de app/src/lib/recomendacao.js (equivalência 500/500)
├── notebooks/           01 preparação · 02 modelagem · 03 avaliação (executados)
├── figuras/             fig1–fig4 gerados pela modelagem
└── *.md                 documentação de cada fase
```

A exportação do Firestore é feita por [`../scripts/exportar_gastromatch.py`](../scripts/exportar_gastromatch.py), somente leitura. A chave de conta de serviço **nunca** entra no repositório.

---

## Reprodução

```bash
pip install -r requirements.txt
cd notebooks
jupyter nbconvert --to notebook --execute --inplace 01_extracao_preparacao.ipynb 02_modelagem.ipynb 03_avaliacao.ipynb
```

No Colab: `!git clone https://github.com/gabriellandimdonadel/aprendizado-maquina-udf.git`, depois `%cd aprendizado-maquina-udf/Projeto_datascience/notebooks` e execute os notebooks em ordem.

**Ambiente usado (25/11/2026):** Python 3.11.9, pandas 3.1.1, numpy 2.4.6, scipy 1.17.1, scikit-learn 1.9.1, matplotlib 3.11.2, seaborn 0.13.2, openpyxl 3.1.5 e firebase-admin 7.8.0 (só para exportar). **Semente aleatória:** 42.

---

## Fontes

* **Base principal (GastroMatch):** Firestore do projeto de demonstração `gastromatch-demo`, exportado em 25/11/2026. São 188 restaurantes, 1.751 avaliações, 748 pratos, 29 cupons e 66 resgates, com atributos de experiência (8 categorias), cozinha (20 tipos), faixa de preço (1 a 4) e notas médias. **Dados fictícios** gerados pelo script de seed do sistema, usados para validar o processo.
* **ABRASEL / 99Food (2026):** pesquisa com 1.710 empresários do setor de alimentação fora do lar, realizada em agosto de 2026: 86% dos estabelecimentos que fazem entregas recebem pedidos por aplicativos; os aplicativos geram, em média, 58% das vendas por delivery. ABRASEL. *Aplicativos geram 58% das vendas por delivery, mas operação física dos restaurantes não acompanha avanço digital.* Disponível em: <https://abrasel.com.br/noticias/noticias/aplicativos-geram-58-das-vendas-por-delivery-mas-operacao-fisica-dos-restaurantes-nao-acompanha-avanco-digital/>.
* **ZANETTA et al. (2024):** revisão sobre os determinantes da escolha e da satisfação em restaurantes (*Food Research International*, v. 186).
* **RATHNASIRI et al. (2025):** influência da atmosfera e do ambiente físico na satisfação e na intenção de retorno (*PLoS ONE*, v. 20, n. 4).
* **RAJ; EGGERS (2026):** impacto das plataformas digitais de entrega na concentração de mercado (*Strategic Management Journal*, v. 47, n. 2).
* **Referências complementares (para cruzamento futuro com dados reais do DF):** IBGE (Pesquisa Anual de Serviços) e Portal de Dados Abertos do DF / IPEDF.

> As referências acadêmicas acima foram mantidas da versão original da equipe e não foram conferidas nesta revisão. A fonte ABRASEL foi conferida no site da associação em 25/11/2026.
