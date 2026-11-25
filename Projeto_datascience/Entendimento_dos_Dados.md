# Fase 2 — Entendimento dos Dados (CRISP-DM)

**Projeto:** Descoberta Gastronômica e Mercado de Alimentação Fora do Lar (GastroMatch)  
**Pergunta de negócio:** Quais fatores (experiência/ambiente, tipo de cozinha, faixa de preço e localidade) mais influenciam a avaliação média e a recomendação de estabelecimentos gastronômicos?  
**Recorte dos dados:** Base do protótipo GastroMatch (2026) e indicadores setoriais (2024–2026).

## 2.1 Coleta inicial dos dados

Foram reunidas três fontes principais para compor o estudo:

| Fonte / Documento | Conteúdo | Utilização no projeto |
|---|---|---|
| Base Cloud Firestore — GastroMatch | Coleções NoSQL (`restaurantes`, `avaliacoes`, `menus`, `promocoes`, `cupons`, `resgates`) exportadas em JSON/CSV | **Fonte principal** |
| Planilhas de Cardápio (`.xlsx`) | Arquivos modelo de importação em lote (`Prato`, `Categoria`, `Descrição`, `Preço`) | Análise de ticket médio e estrutura de menu |
| Pesquisa ABRASEL / 99Food (2026) | Levantamento com 1.710 empresários de bares e restaurantes sobre delivery e operação física | Contextualização de mercado |

Os relatórios setoriais externos fornecem o panorama macroeconômico da digitalização no setor, enquanto as coleções extraídas do GastroMatch permitem analisar em nível granular o cruzamento entre atributos de experiência, preços e avaliações.

## 2.2 Descrição dos dados

| Característica | Descrição |
|---|---|
| Fonte | Banco de dados Cloud Firestore (protótipo GastroMatch) e Dicionário de Dados (TCC II) |
| Cobertura geográfica | Cidades brasileiras cadastradas na base, com foco no Distrito Federal (ex.: Lago Sul, Asa Sul, Asa Norte, Águas Claras) |
| Cobertura temporal | Dados consolidados da versão de demonstração (novembro de 2026) |
| Unidade de análise | Estabelecimento gastronômico (`restaurantes/{uid}`) e avaliação individual (`avaliacoes/{alvoId_uid}`) |
| Variáveis principais | `vibes` (até 3 experiências entre 8 opções), `cozinha` (20 tipos), `faixaPreco` (1 a 4), `notaMedia` (0 a 5), `totalAvaliacoes` |
| Variáveis derivadas | Score de recomendação (0 a 100 pontos), preço médio do cardápio, taxa de conversão/validação de cupons |
| Outras dimensões disponíveis | Ocasiões atendidas (`ocasioes`), horário de funcionamento, pratos do cardápio (`menus`) e status de destaque |
| Formato dos arquivos recebidos | Documentos JSON (exportação NoSQL), planilhas `.xlsx` (cardápios) e relatórios em PDF |

**Observação:** A base principal é orientada a documentos (NoSQL). Diferente de bancos relacionais, atributos como `vibes` e `ocasioes` são armazenados como listas (*arrays*) dentro do documento do restaurante, exigindo normalização (*one-hot encoding* ou explosão de linhas) na etapa de preparação.

## 2.3 Exploração inicial dos dados

### Volumetria das principais entidades da base GastroMatch

| Entidade / Coleção | Quantidade de registros | Observação |
|---|---:|---|
| Restaurantes (`restaurantes`) | 188 | Estabelecimentos ativos na base de demonstração |
| Avaliações (`avaliacoes`) | 1.751 | Notas inteiras de 1 a 5 estrelas para restaurantes e pratos |
| Usuários (`usuarios`) | 229 | Contas de clientes e responsáveis por restaurantes |
| Promoções ativas (`promocoes`) | 32 | Ofertas com vigência programada |
| Eventos (`eventos`) | 22 | Eventos próprios de restaurantes e super eventos da plataforma |

### Taxonomia de atributos estruturados (Vocabulário Fechado)

- **Experiências (`vibes` — até 3 por restaurante):** *Romântica*, *Alegre*, *Tranquila*, *Sofisticada*, *Familiar*, *Descontraída*, *Noturna* e *Cafeteria / Brunch*.
- **Tipos de cozinha (`cozinha` — 20 opções):** *Brasileira*, *Italiana*, *Japonesa*, *Churrasco*, *Frutos do Mar*, *Pizzaria*, *Vegetariana*, entre outras.
- **Faixas de preço (`faixaPreco` — escala 1 a 4):**
  - `$` (1): até R$ 60 por pessoa;
  - `$$` (2): de R$ 60 a R$ 120 por pessoa;
  - `$$$` (3): de R$ 120 a R$ 200 por pessoa;
  - `$$$$` (4): acima de R$ 200 por pessoa.
- **Categorias de cardápio (`menus`):** *Entrada*, *Prato Principal*, *Sobremesa*, *Bebida* e *Acompanhamento*.

### Indicadores setoriais complementares (ABRASEL, 2026)

- **Adesão a aplicativos:** 86% dos estabelecimentos que realizam entregas recebem pedidos via plataformas digitais de delivery.
- **Dependência de receita:** Os aplicativos respondem, em média, por 58% das vendas na modalidade delivery.
- **Lacuna de descoberta:** As grandes plataformas priorizam o consumo fora do salão e a ordenação por engajamento/anúncios, sem filtros nativos para a atmosfera física do estabelecimento.

## 2.4 Verificação da qualidade dos dados

| Aspecto | Avaliação inicial |
|---|---|
| Procedência | Base estruturada do TCC II (GastroMatch) com regras de integridade aplicadas pelo Firestore Security Rules |
| Cobertura de atributos | Campos obrigatórios (`nomeRestaurante`, `cozinha`, `faixaPreco`, `estado`, `cidade`, `notaMedia`) 100% preenchidos |
| Consistência matemática | A `notaMedia` é calculada via transação atômica (`somaNotas ÷ totalAvaliacoes`), garantindo consistência entre coleções |
| Valores ausentes / opcionais | Campos como `vibes`, `ocasioes` e `descricao` podem estar vazios em cadastros incompletos; coordenadas (`lat`, `lng`) existem apenas na base de demonstração |
| Privacidade (LGPD) | Dados sensíveis (CPF, CNPJ, e-mail e telefone pessoal) estão isolados na subcoleção `privado` e não compõem a base analítica |
| Limitações | Base composta por dados fictícios de demonstração; ausência de histórico longitudinal de cliques ou reservas confirmadas (reservas ocorrem via WhatsApp externo) |

**Cuidados de interpretação:** Como a base atual utiliza 188 restaurantes e 1.751 avaliações geradas para validação funcional do protótipo, os padrões encontrados refletem a modelagem e a distribuição sintética do sistema, servindo como prova de conceito metodológica até a ingestão de dados de operação comercial real.

## 2.5 Conclusão do entendimento dos dados

A estrutura de dados do GastroMatch é altamente adequada para análises quantitativas e modelagem, pois transforma percepções subjetivas de ambiente ("vibe") em variáveis categóricas estruturadas e auditáveis. A presença de 188 restaurantes e 1.751 avaliações permite testar correlações entre faixa de preço, experiência e nota média, além de simular cenários do motor de recomendação.

Para a Fase 3 (Preparação dos Dados), será necessário extrair os documentos JSON do Firestore, desmembrar os vetores de `vibes` e `ocasioes` em colunas binárias e cruzar a tabela de restaurantes com as métricas agregadas de cardápio (`menus`) e avaliações (`avaliacoes`).

## 2.6 Entregáveis da Fase 2

1. **Relatório de entendimento dos dados:** fontes, dicionário resumido das coleções, taxonomia de atributos e avaliação de qualidade (este documento).
2. **Base estruturada inicial:** extração das coleções `restaurantes` (188 registros) e `avaliacoes` (1.751 registros) pronta para limpeza e transformação.
3. **Mapeamento de variáveis derivadas:** definição das métricas de preço médio por prato, densidade de *vibes* e pontuação de compatibilidade.

## 2.7 Fontes complementares incorporadas (atualização)

Além da base principal do Firestore, foram incorporados os registros de **testes automatizados e desempenho** (`resultados-navegador.txt` e `desempenho-publicado-versao-nova.json`) e o modelo oficial de **planilha de importação de cardápios** (`.xlsx`), permitindo validar tanto o comportamento dos dados de negócio quanto a eficiência computacional das consultas paginadas (lotes de 24 documentos, exibidos de 12 em 12).

## Referências documentais

- FARIAS, Gabriel Landim Donadel de; MOTA, Rafael Batista. *GastroMatch: Plataforma Web para descoberta de estabelecimentos gastronômicos com foco em filtros de experiência*. TCC (Bacharelado em Sistemas de Informação) — UDF, Brasília, 2026.
- ABRASEL. *Aplicativos geram 58% das vendas por delivery, mas operação física dos restaurantes não acompanha avanço digital*. 2026.
- ZANETTA, Luis D'Avoglio et al. *How does the consumer choose a restaurant? An overview of the determinants of consumer satisfaction*. Food Research International, v. 186, 2024.
