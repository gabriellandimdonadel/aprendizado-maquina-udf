<img src="assets/logo-udf.jpg" alt="UDF Centro Universitário" width="230">

**Profa. Kadidja Valéria | UDF**  
Ciência de Dados e Aprendizado de Máquina · Sistemas de Informação · 2026.2

# Questões de revisão — Registro individual

## Identificação

- Estudante ou equipe: **Gabriel Landim Donadel de Farias (registro individual)**
- Turma: **Sistemas de Informação — UDF, 2026.2**
- Data de realização: **25/11/2026**
- Integrantes e contribuições (se em equipe): **Não se aplica: registro individual. O laboratório citado foi feito em dupla com Rafael Batista Mota.**

Responda com suas palavras e apresente os cálculos quando solicitados. Os números dos exercícios manuais não são os resultados do laboratório.

## 1. Explique a diferença entre regra programada para bloquear uma palavra e modelo de spam treinado com exemplos.

**Resposta:** A regra é escrita por uma pessoa ("se contiver 'grátis', bloqueie"). Ela é transparente e previsível, mas rígida: bloqueia mensagens legítimas com a palavra e é driblada com "gr4tis". O modelo aprende sozinho, a partir de muitas mensagens já rotuladas como spam ou legítima, quais combinações de características indicam spam. Ele generaliza para casos que ninguém escreveu como regra, mas depende de rótulos de qualidade, erra de formas menos óbvias e precisa ser reavaliado quando o spam muda.

## 2. Por que codificar evadiu/permaneceu como 1/0 não transforma classificação em regressão?

**Resposta:** O que define a tarefa é o significado do alvo, não o tipo de número. 1 e 0 são só rótulos de duas categorias. Não existe "meio evadido" (0,5), e a distância entre 0 e 1 não mede quantidade. Por isso usamos métricas de classificação (acurácia, sensibilidade, matriz), e não MAE. Um classificador pode produzir uma estimativa entre 0 e 1, mas ela serve para ordenar ou decidir a classe.

## 3. Uma biblioteca quer estimar empréstimos e descobrir perfis. Que tarefas correspondem a cada pergunta?

**Resposta:** "Estimar empréstimos por semana" é **regressão** (supervisionada): o alvo é uma quantidade numérica conhecida no histórico, avaliada por MAE ou R². "Descobrir perfis de usuários" é **agrupamento** (não supervisionado): não há alvo nem categorias prévias, e o algoritmo forma grupos por semelhança, avaliados por silhueta e por utilidade para a gestão.

## 4. O que são atributo, alvo e unidade de análise no laboratório educacional?

**Resposta:** A **unidade de análise** é cada estudante fictício (uma linha). Os **atributos** são as informações conhecidas no momento da previsão (semana 4): `frequencia_sem4`, `nota_sem4` e `entregas_sem4`. O **alvo** é o que se quer prever: `evasao_fim_semestre` (0 = permaneceu, 1 = evadiu), conhecido só ao fim do semestre.

## 5. Por que calcular a mediana antes de dividir os dados pode invalidar a avaliação?

**Resposta:** Se a mediana usada para preencher os ausentes for calculada com todos os dados, ela incorpora valores do conjunto de teste. Isso é **vazamento de informação**: o modelo "vê" um pouco do teste durante a preparação, e o resultado fica otimista, sem representar dados realmente novos. O correto é aprender a mediana só no treino, dentro de um `Pipeline`, e aplicar o mesmo valor ao teste. Foi o que fizemos no laboratório.

## 6. Em uma matriz didática com TN=80, FP=5, FN=10, TP=5, calcule acurácia e sensibilidade. O resultado é suficiente para aprovar o modelo?

**Resposta:**
- Total = 80 + 5 + 10 + 5 = 100.
- **Acurácia** = (TN + TP) / total = (80 + 5) / 100 = **0,85**.
- **Sensibilidade** = TP / (TP + FN) = 5 / (5 + 10) = **0,333**.

**Não é suficiente.** Há 15 positivos em 100. Um modelo que sempre previsse negativo teria 85/100 = **0,85**, a mesma acurácia. O modelo encontra só 1 em cada 3 positivos e deixa 10 de fora. Antes de aprovar, é preciso comparar com a referência, considerar o custo dos falsos negativos e, se for o caso, ajustar o modelo ou o limiar.

## 7. Valores reais 100, 120, 140 e previsões 110, 115, 130. Calcule MAE e informe a unidade se o alvo for vendas em reais.

**Resposta:**
- Erros absolutos: |100 − 110| = 10; |120 − 115| = 5; |140 − 130| = 10.
- **MAE** = (10 + 5 + 10) / 3 = 25 / 3 ≈ **R$ 8,33**.

Em média, a previsão erra cerca de R$ 8,33 para mais ou para menos. A unidade é a mesma do alvo: reais.

## 8. Um R² de -0,2 significa “20% de acertos negativos”? Explique.

**Resposta:** Não. R² = 1 − SQ_erro / SQ_total compara o erro quadrático do modelo com o de prever sempre a média do conjunto avaliado. R² = −0,2 significa que o erro quadrático do modelo é 20% **maior** que o de simplesmente usar a média, ou seja, o modelo é pior que essa referência trivial. R² não é porcentagem de acertos: em regressão não há acerto ou erro binário.

## 9. Uma árvore tem acurácia 1,00 no treino e 0,65 na validação. Que hipótese investigar e como?

**Resposta:** A hipótese é **sobreajuste**: a árvore decorou o treino, inclusive o ruído, e não generaliza. Para investigar, uso validação cruzada no treino comparando configurações mais restritas (menor `max_depth`, maior `min_samples_leaf`) e observo se a lacuna treino−validação diminui e se a validação melhora. Também comparo com a referência e confiro se não há vazamento ou registros duplicados. No laboratório, a árvore sem limite e com folha 5 teve 0,868 no treino e 0,713 na validação, enquanto folhas maiores reduziram a lacuna para cerca de 0,05.

## 10. Por que escolher a profundidade pelo teste prejudica a estimativa final?

**Resposta:** Se testo várias profundidades no teste e escolho a melhor, o teste passa a fazer parte do ajuste. O valor obtido fica otimista, porque escolhi justamente a configuração que se deu bem *naqueles* 150 casos, inclusive por sorte. O teste deixa de ser "dado não visto". A escolha deve ser feita por validação no treino. Se eu precisar escolher de novo depois de ver o teste, preciso de um novo teste independente.

## 11. Baixa frequência associada à evasão demonstra causa? Proponha explicação alternativa.

**Resposta:** Não. Associação não é causa. Uma explicação alternativa: um estudante que começou a trabalhar à noite (causa comum) passa a faltar **e** acaba evadindo por falta de tempo ou de renda. Nesse caso, a baixa frequência é um sintoma, não a causa. Também pode haver causalidade reversa: quem já decidiu sair deixa de frequentar. Para afirmar causa, seria preciso um desenho experimental ou um estudo causal, não só correlação.

## 12. Um modelo sinaliza um estudante como possível evasão. Que ação responsável pode ser adotada?

**Resposta:** Uma pessoa da equipe de apoio revisa a sinalização e faz um **convite voluntário e sigiloso** para conversar, oferecendo monitoria, orientação sobre auxílios e flexibilização de prazos. Sem rótulo de "risco", sem punição e sem registro no histórico. O estudante pode recusar e contestar os dados, e o apoio continua aberto também a quem não foi sinalizado. A previsão é um indício para oferecer ajuda, não uma decisão sobre a pessoa.

## Fontes adicionais consultadas

**SCIKIT-LEARN. *Common pitfalls and recommended practices*. Disponível em: https://scikit-learn.org/stable/common_pitfalls.html. Acesso em: 25 nov. 2026. — CARVALHO, A. C. P. L. F. de; MENEZES, A. G.; BONIDIA, R. P. *Ciência de Dados: fundamentos e aplicações*. Rio de Janeiro: LTC. — Laboratório da disciplina ([notebooks/laboratorio-equipe.ipynb](notebooks/laboratorio-equipe.ipynb)). — Assistente de IA (Claude) usado para revisar a redação. Os cálculos foram conferidos manualmente.**

[Voltar ao início](README.md).
