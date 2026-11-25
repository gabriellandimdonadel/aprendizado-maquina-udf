<img src="../assets/logo-udf.jpg" alt="UDF Centro Universitário" width="230">

**Profa. Kadidja Valéria | UDF**
Ciência de Dados e Aprendizado de Máquina · Sistemas de Informação · 2026.2

# CRISP-DM · Fase 1 — Entendimento do Negócio (GastroMatch)

- Equipe: Gabriel Landim Donadel de Farias e Rafael Batista Mota
- Data: 04/11/2026 (revisada em 25/11/2026, depois da Fase 2)
- Documento-base: [GastroMatch_Definicao_Projeto_CD.docx](../GastroMatch_Definicao_Projeto_CD.docx). Esta página organiza esse documento no checklist da Fase 1 do Guia CRISP-DM.

> **Objetivo da fase (Guia):** traduzir o problema de negócio em metas técnicas viáveis antes de investir recursos computacionais.

## 1. Objetivos de negócio e critérios de sucesso

| Item | Registro |
| --- | --- |
| Problema | Quem procura restaurante não encontra filtros por experiência (vibe/ambiente). Restaurantes locais têm pouca visibilidade porque as plataformas grandes favorecem quem paga publicidade. |
| Objetivo de negócio | Ajudar os restaurantes parceiros a decidir posicionamento, cardápio, promoções e horários com base nas preferências dos usuários. Ajudar os clientes a escolher restaurantes mais adequados ao que esperam. |
| Critério de sucesso **de negócio** | Ao menos 2 parceiros conseguem usar o painel sem ajuda e declaram que mudariam alguma decisão com base nele. Sugestão a validar com a professora: aumentar a taxa de **salvamento/resgate** de cupons e promoções dos parceiros que aplicarem as recomendações. |
| Critério de sucesso **do projeto** | As 5 perguntas de negócio respondidas. Pelo menos 90% dos registros sem dados críticos ausentes. As 3 hipóteses testadas com método explícito. Nota ≥ 8,0 na banca (seção 11 do documento). |

## 2. Avaliação da situação

| Aspecto | Registro |
| --- | --- |
| Recursos | Dupla de desenvolvedores; sistema final em React + Firebase (produção `thegastromatch`, demonstração `gastromatch-demo` com dados fictícios); Python/Colab; GitHub. |
| Dados existentes | Coleções `restaurantes` (vibes, faixa de preço, localização, nota média), `usuarios`, `menus`, `promocoes`, `cupons`, `eventos`, `salvos`, `resgates` e `avaliacoes`. Base analisada: demonstração, com **3.075 registros** e 1.751 avaliações (fictícios). Detalhes na [Fase 2](fase2-entendimento-dados.md). |
| Restrições | Prazo até dez/2026; pouco volume de dados; sem Firebase Functions; nenhum integrante especialista em dados. |
| Riscos principais | Pouco volume real em produção (probabilidade alta, impacto alto); usar dados fictícios como se fossem reais (mitigação: declarar a condição em todo resultado); atraso na implementação das coleções; dificuldade para montar o dashboard; desalinhamento com o orientador. |
| Custo × benefício | **Custo:** horas da equipe e ferramentas gratuitas (Colab, Firebase Spark, Looker Studio). **Benefício:** dados que comprovam o diferencial do TCC (filtro por experiência) e um painel com valor para o parceiro. O custo é baixo, mas o benefício só aparece se os dados de comportamento forem coletados (ver Fase 2). |
| Requisito legal | LGPD. O cadastro guarda nome, e-mail e telefone; CPF/CNPJ ficam numa subcoleção privada que a análise não lê. A análise usa apenas dados agregados e pseudonimizados. |

## 3. Metas técnicas de mineração de dados

Cada pergunta de negócio vira uma tarefa técnica.

| Pergunta de negócio | Meta técnica | Tipo de análise |
| --- | --- | --- |
| P1. Quais culinárias e vibes geram mais buscas e reservas? | Contar a frequência de filtros aplicados e de reservas por categoria | Descritiva (ranking) |
| P2. Qual perfil de restaurante converte mais visitas em reservas? | Taxa "cupom resgatado → usado" por vibe, faixa de preço, bairro e nota (reservas vão pelo WhatsApp); regressão logística como extensão | Descritiva / diagnóstica; supervisionada (classificação) se houver volume |
| P3. Em que dias e horários há mais reservas? | Volume de cupons validados (`usadoEm`) por dia da semana × hora | Descritiva (série temporal, mapa de calor) |
| P4. As avaliações variam com culinária ou vibe? | Média e dispersão das notas por grupo; correlação | Descritiva / diagnóstica |
| P5. Quais promoções e eventos geram mais engajamento? | Salvamentos por item ofertado (`salvos` ÷ itens publicados) | Descritiva (comparação de taxas) |

Critério técnico mínimo: toda tabela e gráfico do relatório deve sair do notebook versionado no GitHub, com a data de exportação dos dados registrada.

## 4. Plano de projeto

| Etapa CRISP-DM | Atividades | Prazo |
| --- | --- | --- |
| 1. Negócio | Este documento + validação com a professora/orientador | **Concluída em 04/11/2026**, revisada em 25/11 |
| 2. Dados | Exportar o Firestore, inventariar campos e verificar qualidade ([notebook](notebooks/fase2-entendimento-dados.ipynb)) | **Concluída em 25/11/2026** |
| 3. Preparação | Remover dados pessoais, padronizar preço/desconto/culinária, juntar coleções por `restauranteId` | **Concluída em 25/11/2026** ([Fase 3](fase3-preparacao-dados.md)) |
| 4. Modelagem | Testes estatísticos, simulação do motor de recomendação e agrupamento | **Concluída em 25/11/2026** ([Fase 4](fase4-modelagem.md)) |
| 5. Avaliação | Conferir os resultados contra os critérios de sucesso | **Concluída em 25/11/2026** ([Fase 5](fase5-avaliacao.md)) |
| 6. Implementação | Plano de implementação e de monitoramento, relatório final e revisão | **Concluída em 25/11/2026** ([Fase 6](fase6-implementacao.md)) |

## 5. Pontos de atenção encontrados na revisão

Estes pontos não invalidam o documento. São ajustes para conversar com a professora:

1. **O escopo exclui ML, mas a P2 cita regressão logística**, que é um modelo de aprendizado supervisionado. Sugestão: deixar explícito que a regressão logística é opcional e só entra se houver volume de reservas.
2. **Faltava um critério de sucesso de negócio.** Com o sistema final, um candidato natural é a taxa de cupons resgatados que viram visita (QR validado). Os critérios da seção 11 medem o projeto acadêmico, não o impacto para o parceiro. O Guia CRISP-DM diz para medir impacto real, não só precisão técnica. A sugestão está no item 1 acima.
3. **O documento descrevia uma versão antiga do sistema.** Ele dizia que avaliações e reservas "serão implementadas". No sistema final, avaliações, resgates, vibes e faixa de preço já existem, e as reservas acontecem pelo WhatsApp. **Corrigido na versão 1.1 do Word** (§3.1, §3.3, §8 e §16), que agora diz qual banco é real (produção) e qual é fictício (demonstração).
4. **Duas perguntas dependem de dados que o sistema não grava** (filtros aplicados e reservas). A Fase 2 mostra isso em detalhe. É o "retorno" previsto no ciclo CRISP-DM: os dados obrigam a revisar o negócio.

## 6. Revisão depois da Fase 2 (retorno do ciclo)

| Decisão | Motivo |
| --- | --- |
| P4 (avaliações × vibe/culinária) passa a ser a pergunta principal das próximas fases | É a única com dados diretos (1.213 avaliações de restaurante) |
| P1, P2, P3 e H1 dependem de nova coleta | O sistema não grava buscas nem reservas, e os usos de cupom da base têm um único instante |
| Nova meta técnica: comparar a faixa declarada com o preço do cardápio | 24% dos pratos principais de restaurantes "$" passam de R$ 60 |
| Conclusões só com dados de produção | A base de demonstração é fictícia, com 41 clientes que fizeram cerca de 43 avaliações cada |

## 7. Pergunta central da análise (usada nas fases 3 a 6)

Depois da revisão do §6, a análise das próximas fases foi concentrada numa pergunta respondível com os dados disponíveis. Ela une a P4 (avaliações × culinária/vibe) ao funcionamento da recomendação:

> **Quais fatores (experiência/ambiente, tipo de cozinha, faixa de preço e localidade) mais influenciam a avaliação média e a recomendação de estabelecimentos gastronômicos, e como o mercado de bares e restaurantes se estrutura digitalmente no Brasil e no DF?**

**Problema.** A escolha de um restaurante não depende só do tipo de comida e do preço. Atributos intangíveis, como o ambiente (*vibe*), a iluminação, a acústica e a adequação à ocasião, pesam na satisfação e na intenção de retorno. No Brasil, a presença digital dos restaurantes se concentra em aplicativos de delivery, voltados ao consumo fora do salão. Neles, a atmosfera do local aparece só dispersa em comentários e fotos. Isso dificulta a decisão do consumidor e concentra a visibilidade em quem tem mais orçamento publicitário.

**Objetivos de Ciência de Dados:**
- Quantificar a distribuição dos estabelecimentos por experiência, cozinha, faixa de preço e localidade.
- Testar se esses atributos se relacionam com a nota média (`notaMedia`) e com o volume de avaliações.
- Avaliar o motor de recomendação por regras (cozinha 40, experiência 30, local 15, preço 15; corte mínimo de 30 pontos) e agrupar perfis de restaurantes.
- Contrastar a proposta centrada no salão com a dependência de aplicativos de delivery no Brasil (pesquisa ABRASEL/99Food, 2026).

**Critérios de sucesso da análise** (verificados na [Fase 5](fase5-avaliacao.md)):
1. Mapear o perfil dos 188 estabelecimentos e das 1.751 avaliações da base, identificando os atributos predominantes.
2. Comparar estatisticamente as notas e o engajamento entre experiências e faixas de preço, de forma verificável.
3. Produzir gráficos, correlações e agrupamentos claros, com fonte e parâmetros declarados.
4. Explicar as limitações (base de demonstração fictícia; experiência autodeclarada pelo restaurante).

**Fontes complementares:**
- ABRASEL/99Food (agosto de 2026, 1.710 empresários): 86% dos estabelecimentos que fazem entregas recebem pedidos por aplicativos, que geram 58% das vendas por delivery.
- Literatura sobre os determinantes da satisfação em restaurantes: Zanetta et al., 2024; Rathnasiri et al., 2025; Raj e Eggers, 2026.

[Ir para a Fase 2 →](fase2-entendimento-dados.md) · [Índice do projeto](README.md)
