# Projeto de Ciência de Dados — Descoberta Gastronômica e Mercado de Alimentação Fora do Lar (GastroMatch)

**Disciplina:** Ciência de Dados e Aprendizagem de Máquina · UDF · 2026.2  
**Docente:** Profa. Kadidja Valéria  
**Início:** 28/10/2026  
**Metodologia:** CRISP-DM — guia IBM  

**Pergunta:** Quais fatores (experiência/ambiente, tipo de cozinha, faixa de preço e localidade) mais influenciam a avaliação média e a recomendação de estabelecimentos gastronômicos, e como o mercado de bares e restaurantes se estrutura digitalmente no Brasil e no DF?

**Resposta curta:** Na base do protótipo GastroMatch (188 estabelecimentos cadastrados e 1.751 avaliações), o algoritmo de compatibilidade prioriza tipo de cozinha (peso 40) e experiência do ambiente (peso 30) sobre localidade (15) e faixa de preço (15). No cenário real brasileiro, 86% dos estabelecimentos com entrega dependem de aplicativos de delivery — que respondem por 58% dessas vendas —, evidenciando a concentração digital fora do salão.

---

## Fases do CRISP-DM

| Fase | Documento | Notebook |
| :--- | :--- | :--- |
| 1. Entendimento do Negócio | `Entendimento_do_Negócio.md` | — |
| 2. Entendimento dos Dados | `Entendimento_dos_Dados.md` | — |
| 3. Preparação dos Dados | `Preparação_de_Dados.md` | `01_extracao_preparacao.ipynb` |
| 4. Modelagem | `Modelagem.md` | `02_modelagem.ipynb` |
| 5. Avaliação | `Avaliação.md` | `03_avaliacao.ipynb` |
| 6. Implementação | `Implementação.md` | — |

---

## Estrutura

```text
Projeto_de_Ciência_de_Dados/
├── dados/
│   ├── brutos/          exportações JSON/CSV do Cloud Firestore (restaurantes, avaliações, menus) e relatórios setoriais
│   └── processados/     bases tratadas (.xlsx/.csv), matrizes de atributos e resultados de score
├── src/extracao.py      extração, limpeza e normalização dos dados do Firestore e planilhas .xlsx
├── notebooks/           01 preparação · 02 modelagem · 03 avaliação (executados)
├── figuras/             gráficos gerados pela análise exploratória e modelagem
└── *.md                 documentação de cada fase
```

---

## Reprodução

```bash
pip install -r requirements.txt
cd notebooks
jupyter nbconvert --to notebook --execute --inplace 01_extracao_preparacao.ipynb 02_modelagem.ipynb 03_avaliacao.ipynb
```

**Ambiente usado:** Python 3.13, pandas 3.0, numpy 2.2, scikit-learn 1.9, matplotlib 3.11, seaborn 0.13, firebase-admin 6.7. **Semente aleatória:** 42.

---

## Fontes

* **Base principal do TCC (GastroMatch):** Dados estruturados do protótipo (188 restaurantes, 1.751 avaliações e cardápios em `.xlsx` / Cloud Firestore), incluindo atributos de *vibe*/experiência (8 categorias), culinária (20 tipos), faixa de preço (1 a 4) e notas médias.
* **ABRASEL — Associação Brasileira de Bares e Restaurantes (2026):** Pesquisa com 1.710 empresários sobre digitalização do setor, delivery (86% de adesão; 58% das vendas) e operação física (*Aplicativos geram 58% das vendas por delivery, mas operação física dos restaurantes não acompanha avanço digital*).
* **ZANETTA et al. (2024):** Revisão sistemática de 111 estudos sobre atributos determinantes na escolha e satisfação em restaurantes — comida, serviço, preço/valor e ambiente (*Food Research International*, v. 186).
* **RATHNASIRI et al. (2025):** Estudo empírico sobre a influência da atmosfera e do ambiente físico na satisfação e intenção de retorno dos clientes (*PLoS ONE*, v. 20, n. 4).
* **RAJ; EGGERS (2026):** Análise sobre o impacto das plataformas digitais de entrega na concentração de mercado e fechamento de restaurantes locais (*Strategic Management Journal*, v. 47, n. 2).
* **Referências complementares (dados públicos externos, caso queira cruzar com indicadores reais do DF):** IBGE (Pesquisa Anual de Serviços — Serviços de Alimentação) e Portal de Dados Abertos do DF / IPEDF (distribuição empresarial e perfil socioeconômico por Região Administrativa).
