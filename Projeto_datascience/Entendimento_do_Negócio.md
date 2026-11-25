# Fase 1 — Entendimento do Negócio (CRISP-DM)

## Projeto: Descoberta Gastronômica e Mercado de Alimentação Fora do Lar (GastroMatch)

**Pergunta de negócio:** Quais fatores (experiência/ambiente, tipo de cozinha, faixa de preço e localidade) mais influenciam a avaliação média e a recomendação de estabelecimentos gastronômicos, e como o mercado de bares e restaurantes se estrutura digitalmente no Brasil e no Distrito Federal?

**Recorte geográfico:** Distrito Federal e cidades atendidas na base do protótipo (Brasil).  
**Período de análise:** 2024 a 2026 (base operacional do protótipo e relatórios setoriais recentes).  
**Área de aplicação:** Ciência de Dados, Engenharia de Software e Hospitalidade Inteligente.

## 1. Problema de negócio

A escolha de um restaurante para uma refeição fora de casa não depende apenas do tipo de comida e do preço; atributos intangíveis como o ambiente físico (*vibe*), a iluminação, a acústica e a adequação à ocasião determinam a satisfação e a intenção de retorno do cliente. No Brasil, entretanto, a presença digital dos restaurantes está fortemente concentrada em aplicativos de delivery voltados ao consumo fora do salão, onde informações sobre a atmosfera do local aparecem dispersas em comentários e fotos não estruturadas.

Além de dificultar a decisão do consumidor (sobrecarga de escolha), essa dinâmica concentra a visibilidade digital em grandes redes ou estabelecimentos com alto orçamento publicitário, pressionando as margens de pequenos negócios locais. Compreender como os atributos estruturados de experiência se relacionam com a avaliação dos clientes e a pontuação de recomendação é essencial para orientar tanto consumidores quanto proprietários de restaurantes.

## 2. Objetivo do negócio

Analisar a estrutura da oferta gastronômica e o comportamento de avaliação na plataforma **GastroMatch**, identificando quais combinações de experiência (*vibe*), tipo de cozinha, faixa de preço e localidade geram maior compatibilidade e melhores notas médias, além de contextualizar o cenário digital do setor de alimentação fora do lar no Brasil e no DF.

## 3. Objetivo da Ciência de Dados

Utilizar a base de dados do protótipo GastroMatch (extraída do Cloud Firestore e planilhas de cardápio) e dados secundários do setor gastronômico para realizar análise exploratória e modelagem preditiva/descritiva que permitam:

- Quantificar a distribuição dos estabelecimentos por experiência (*vibe*), tipo de cozinha, faixa de preço e localidade;
- Analisar a correlação e o impacto dos atributos do estabelecimento sobre a nota média (`notaMedia`) e o volume de avaliações (`totalAvaliacoes`);
- Avaliar o comportamento do algoritmo de recomendação baseado em regras com pesos fixos (cozinha: 40, experiência: 30, local: 15, preço: 15) e agrupar perfis de restaurantes;
- Contrastar a oferta voltada à experiência no salão com os indicadores de dependência de aplicativos de delivery no Brasil (pesquisa ABRASEL).

## 4. Critérios de sucesso

O projeto será considerado bem-sucedido se:

1. Mapear e apresentar o perfil completo dos 188 estabelecimentos e 1.751 avaliações da base do GastroMatch, identificando os atributos predominantes;
2. Comparar estatisticamente as notas médias e o engajamento (avaliações e resgates de cupons) entre diferentes categorias de experiência e faixas de preço de forma verificável;
3. Produzir gráficos, matrizes de correlação e agrupamentos (*clusters*) claros, com indicação da fonte e dos parâmetros utilizados;
4. Explicar as limitações metodológicas dos dados (base de demonstração com registros fictícios e classificação autodeclarada pelos restaurantes).

## 5. Plano inicial do projeto

1. **Entendimento do negócio:** definir pergunta, objetivos, critérios de sucesso e contexto do setor gastronômico.
2. **Entendimento dos dados:** examinar as coleções do Cloud Firestore, o dicionário de dados do TCC e os relatórios setoriais (ABRASEL).
3. **Preparação dos dados:** extrair os registros das coleções (`restaurantes`, `avaliacoes`, `menus`, `cupons`, `resgates`), tratar listas (*arrays* de *vibes* e ocasiões) e validar a integridade referencial.
4. **Modelagem/análise:** calcular rankings, testar correlações entre atributos e notas, analisar o comportamento do score de recomendação e aplicar clusterização de estabelecimentos.
5. **Avaliação:** verificar se os resultados respondem à pergunta de negócio e validar a coerência das métricas frente à literatura da área.
6. **Apresentação/implantação:** consolidar o pipeline reprodutível, o plano de monitoramento para dados reais futuros e o relatório final.

## 6. Fontes de dados e restrições iniciais

**Fonte principal:** Base estruturada do protótipo **GastroMatch** (Cloud Firestore — coleções `restaurantes`, `avaliacoes`, `menus`, `promocoes`, `cupons` e `resgates`), contendo 188 restaurantes, 1.751 avaliações e cardápios importados via `.xlsx`.

**Fontes complementares:**
- **ABRASEL (2026):** Pesquisa com 1.710 empresários sobre digitalização e vendas por aplicativos de delivery no Brasil;
- **Literatura científica de referência:** Zanetta et al. (2024), Rathnasiri et al. (2025) e Raj; Eggers (2026) para fundamentação dos pesos e comportamento do consumidor.

**Limitações previstas:** Os dados da base GastroMatch provêm de um ambiente de demonstração com registros fictícios (sem validação em campo com usuários reais). Além disso, as categorias de experiência (*vibe*) são autodeclaradas pelo próprio estabelecimento no cadastro (limite de até 3 entre 8 opções), refletindo a percepção do proprietário, que pode divergir da percepção subjetiva de cada cliente.

## 7. Entregável da Fase 1

Este documento consolida o entendimento do problema de descoberta gastronômica baseada em experiência, a pergunta de negócio, os objetivos, os critérios de sucesso, as fontes previstas e o plano inicial de trabalho. **Os resultados estatísticos, a exploração das coleções e os modelos pertencem às fases seguintes do CRISP-DM.**
