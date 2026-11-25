# Fase 5 — Avaliação (CRISP-DM)

**Notebook:** [`notebooks/03_avaliacao.ipynb`](notebooks/03_avaliacao.ipynb) · **Resultado das verificações:** `dados/processados/avaliacao_verificacoes.csv`

O Guia CRISP-DM define o objetivo desta fase: avaliar os resultados **pelos critérios de sucesso da Fase 1** (o impacto real pesa mais que a precisão técnica) e decidir entre **implementar ou iterar**.

## 5.1 Os resultados respondem à pergunta?

**Sim, para a base analisada.** A resposta é diferente da hipótese inicial:

- **Avaliação média:** nenhum dos fatores (experiência, faixa de preço, cozinha, estado) muda a nota média de forma significativa no nível do restaurante (Kruskal-Wallis, p de 0,09 a 0,89). Isso é esperado numa base fictícia em que a nota é sorteada sem relação com esses atributos. A resposta definitiva exige dados reais.
- **Recomendação:**
  - A **cozinha** é o fator decisivo: pesa 40 pontos e filtra antes de pontuar. A **experiência** vem em seguida, com 30 pontos.
  - Declarar 3 experiências dá **1,54×** mais exposição que declarar 1, nas 500 buscas simuladas.
  - Como há muitos empates, a **nota média, usada só como desempate, é o atributo mais associado à exposição** (rho = 0,50).
- **Contexto de mercado:** a pesquisa ABRASEL/99Food (agosto de 2026, 1.710 empresários) indica que 86% dos estabelecimentos que fazem entregas recebem pedidos por aplicativos, que respondem por 58% das vendas por delivery. Isso reforça a lacuna que o GastroMatch explora: uma descoberta centrada no salão e na experiência.

## 5.2 Fidelidade dos dados e do processo (verificações automáticas)

| Verificação | Resultado | Evidência |
|---|---|---|
| Restaurantes ativos = 188 | ✔ | base consolidada |
| Avaliações extraídas = 1.751 (≥ 1.000 pedidas) | ✔ | `firestore_avaliacoes.json` |
| Log de extração sem erros | ✔ | 15/15 verificações "ok" |
| `notaMedia` = média recalculada das avaliações | ✔ | 188/188 |
| Vibes ≤ 3 e dentro das 8 oficiais; cozinhas dentro das 20 oficiais | ✔ | vocabulário de `catalogo.js` |
| Regra de pontuação reproduz casos calculados à mão; Python = JavaScript | ✔ | 100, 8 e 48 pontos; 500/500 buscas idênticas |
| Nenhum restaurante recomendado abaixo de 30 pontos | ✔ | menor score médio: 45,2 |
| Base analítica sem campos pessoais (LGPD) | ✔ | nenhum campo pessoal nas saídas |
| Testes unitários do sistema | ✔ | **67/67**, reexecutados em 25/11/2026 (`evidencias/testes-unitarios.txt`) |
| Testes no navegador | ✔ | **147 aprovados, 0 falhas** (`evidencias/resultados-navegador.txt`) |
| Desempenho em rede média < 3 s (RNF04) | ✔ | conteúdo principal: 1,32 s (início) e 1,94 s (catálogo), medição de 10/11/2026 |
| Desempenho em rede lenta < 3 s (RNF04) | **✘** | conteúdo principal: 4,79 s (início) e 2,33 s (catálogo); 1º restaurante: 4,68 s e 3,69 s |

Os **105 testes de regras do Firestore** estão declarados em `app/tests/regras.test.js`, mas não foram reexecutados nesta análise, porque exigem o emulador com Java 21.

## 5.3 Critérios de sucesso da Fase 1

| Critério | Situação | Evidência |
|---|---|---|
| 1. Mapear os 188 estabelecimentos e as 1.751 avaliações | **Atendido** | notebook 01; fig. 1 e 2 |
| 2. Comparar estatisticamente notas e engajamento entre experiências e faixas | **Atendido** | Kruskal-Wallis em dois níveis, Spearman e simulação de 500 buscas (Modelagem, fig. 3) |
| 3. Gráficos, correlações e clusters com fonte e parâmetros declarados | **Atendido** | fig. 1–4 com fonte; silhueta de k = 2 a 5 (0,195–0,224) declarada |
| 4. Explicar limitações (dados fictícios e autodeclaração) | **Atendido** | §5.4 |

## 5.4 Revisão do processo e limitações

1. **Base de demonstração fictícia.** Os 188 restaurantes e as 1.751 avaliações foram gerados pelo script de seed, com apenas 41 clientes avaliadores (cerca de 43 avaliações cada) e datas retroativas. Os testes mostram que o processo funciona, não como consumidores reais se comportam.
2. **Autodeclaração da experiência.** A vibe é informada pelo próprio restaurante e não é auditada. A associação com a faixa de preço existe, mas é fraca (\|rho\| ≤ 0,25).
3. **Pseudorreplicação.** Testar no nível da avaliação gerou falsos positivos (cozinha p ≈ 10⁻⁷ contra 0,30 no nível do restaurante). A unidade de análise correta é o restaurante.
4. **Sem conversão de reserva.** A reserva vai para o WhatsApp externo, então a base não sabe quantas visitas vieram da plataforma. Os únicos sinais de visita são os 27 cupons validados, todos com o mesmo instante na base fictícia.
5. **Catálogo esparso.** 47% das buscas simuladas caíram em "cozinha em outra cidade". Com dados reais, isso indicaria onde captar novos parceiros.
6. **Agrupamento fraco.** Silhueta ≤ 0,224: os clusters descrevem a base, mas não são segmentos robustos.
7. **Desempenho em rede lenta.** A página inicial fica acima da meta de 3 s (4,79 s).

## 5.5 Decisão: implementar ou iterar?

**Implementar** o *pipeline* analítico (exportação sem dados pessoais → `src/extracao.py` → notebooks 01–03) como módulo de inteligência do GastroMatch. Ele é reprodutível, passou em todas as verificações de integridade e já usa o esquema de produção.

**Iterar** antes de usar os resultados em decisões de negócio:

- rodar o *pipeline* sobre a **produção** (`thegastromatch`) quando houver volume real;
- registrar, sem dados pessoais, **filtros de busca, visualizações de perfil e cliques em "Reservar pelo WhatsApp"**;
- incluir a **validação colaborativa da experiência** (perguntar ao cliente se a vibe correspondeu à declarada);
- avaliar um desempate que não concentre a exposição só pela nota (por exemplo, considerar o número de avaliações);
- cruzar a distribuição geográfica com dados socioeconômicos das Regiões Administrativas do DF (IPEDF/PDAD) depois do início da operação comercial.
