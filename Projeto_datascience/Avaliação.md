# Fase 5 — Avaliação (CRISP-DM)

**Notebook:** [`notebooks/03_avaliacao.ipynb`](notebooks/03_avaliacao.ipynb) · **Resultado das verificações:** `dados/processados/avaliacao_verificacoes.csv`

O guia CRISP-DM define o objetivo desta fase: avaliar os resultados **pelos critérios de sucesso da Fase 1** (aderência ao problema de negócio > complexidade algorítmica) e decidir entre **implementar ou iterar**.

## 5.1 Os resultados respondem à pergunta?

**Sim.** A análise demonstrou que a combinação de **tipo de cozinha (peso 40)** e **experiência do ambiente (peso 30)** governa 70% da pontuação de compatibilidade no GastroMatch, permitindo que a atmosfera física funcione como critério objetivo de descoberta sem depender de histórico comportamental prévio[cite: 22, 71, 72]. Além disso, verificou-se que estabelecimentos com perfil completo (3 *vibes* cadastradas e cardápio estruturado) ampliam significativamente sua elegibilidade nas recomendações, enquanto no mercado externo (ABRASEL, 2026) a dependência de aplicativos de delivery atinge 86% dos estabelecimentos com entrega (58% do faturamento dessa modalidade)[cite: 21].

A resposta é **consistente e auditável**: todas as regras de pontuação, cálculos de média e validações de integridade foram reproduzidos em código e confrontados com os testes automatizados do sistema (67 unitários, 105 de regras do banco e 147 no navegador aprovados)[cite: 49].

## 5.2 Fidelidade dos dados (verificações automáticas)

| Verificação | Resultado |
|---|---|
| Total de restaurantes ativos na base = 188 (conforme delimitação do TCC)[cite: 22] | ✔ 0 divergências |
| Total de avaliações extraídas = 1.751 (conforme evidência do painel de suporte)[cite: 188] | ✔ 0 divergências |
| Consistência matemática (`notaMedia == somaNotas / totalAvaliacoes`) em 100% dos registros[cite: 106] | ✔ 188/188 válidos |
| Vocabulário fechado respeitado (`vibes` ≤ 3 entre 8 opções; `cozinha` entre 20 opções)[cite: 104] | ✔ 100% conformidade |
| Corte mínimo de recomendação (RN38 ≥ 30 pontos) aplicado corretamente nas simulações[cite: 71, 72] | ✔ validado |
| Ausência de dados pessoais sensíveis (CPF/CNPJ/e-mail) na base analítica (LGPD)[cite: 62, 102] | ✔ 100% anônimo |
| Desempenho de consulta paginada em conexão média (< 3,0 s conforme RNF04)[cite: 61, 196] | ✔ 1,32 s (Inicial) / 1,94 s (Catálogo) |

## 5.3 Critérios de sucesso da Fase 1

| Critério | Situação | Evidência |
|---|---|---|
| 1. Mapear os 188 estabelecimentos e 1.751 avaliações da base | **Atendido** | Base consolidada e distribuição por *vibe* e cozinha (Modelagem, fig. 1 e 2)[cite: 22, 188] |
| 2. Comparar notas médias e engajamento entre categorias de experiência e preço | **Atendido** | Testes de correlação e análise por cluster (Modelagem, fig. 3 e 4) |
| 3. Gráficos e tabelas claros, com fonte e parâmetros declarados | **Atendido** | Figuras com fonte GastroMatch/ABRASEL; dicionário de dados completo[cite: 96] |
| 4. Explicar limitações metodológicas (dados fictícios e autodeclaração) | **Atendido** | Seção 5.4 abaixo |

## 5.4 Revisão do processo e limitações

1. **Base de demonstração com dados fictícios:** Os 188 restaurantes e 1.751 avaliações foram gerados para validação funcional do protótipo[cite: 22, 188]. Embora demonstrem a viabilidade técnica e analítica da modelagem, os padrões estatísticos não representam o comportamento real de consumidores do Distrito Federal.
2. **Viés de autodeclaração da experiência (*vibe*):** A classificação do ambiente é informada exclusivamente pelo próprio restaurante no cadastro e não passa por auditoria[cite: 22, 32]. Como a percepção de atmosfera é subjetiva, um ambiente declarado como "Tranquilo" pode divergir da experiência real do cliente[cite: 32].
3. **Ausência de métricas de conversão de reserva:** Como a reserva é redirecionada para o WhatsApp externo do estabelecimento (RN19), a base de dados não captura quantas visitas foram efetivamente concretizadas a partir da descoberta na plataforma[cite: 67, 91].
4. **Escalabilidade das consultas analíticas:** Algumas telas da aplicação ainda carregam uma lista resumida de restaurantes por sessão[cite: 41, 199]; em cenário comercial com milhares de estabelecimentos, a extração e o motor de busca exigirão indexação dedicada[cite: 41, 200].
5. **Desempenho em conexões lentas:** Nos testes publicados, o carregamento em rede lenta (1,6 Mbit/s) levou entre 3,69 s e 4,79 s, não atingindo a meta de 3 segundos estabelecida no RNF04 para esse cenário específico[cite: 196].

## 5.5 Decisão: implementar ou iterar?

**Implementar** o pipeline analítico como módulo de inteligência de negócio do GastroMatch, pois a estrutura de dados e as validações estão íntegras. **Iterar** em uma segunda rodada (alinhada aos Trabalhos Futuros do TCC) para:

- incorporar a **validação colaborativa da experiência** nas avaliações (perguntando ao cliente se a *vibe* encontrada correspondeu à declarada pelo restaurante)[cite: 200];
- implementar o **painel de métricas reais** para os estabelecimentos (visualizações de página, favoritos, cliques no WhatsApp e taxa de validação de cupons)[cite: 200];
- cruzar a distribuição geográfica dos restaurantes com dados socioeconômicos reais das Regiões Administrativas do DF (IPEDF / PDAD) após o início da operação comercial.
