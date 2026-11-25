<img src="assets/logo-udf.jpg" alt="UDF Centro Universitário" width="230">

**Profa. Kadidja Valéria | UDF**  
Ciência de Dados e Aprendizado de Máquina · Sistemas de Informação · 2026.2

# Aula 1 — Conceitos e classificação de problemas

## Identificação

- Estudante ou equipe: **Gabriel Landim Donadel de Farias e Rafael Batista Mota**
- Turma: **Sistemas de Informação — UDF, 2026.2**
- Data de realização: **25/11/2026**
- Integrantes e contribuições (se em equipe): **Gabriel: explicações conceituais (seção 1) e raciocínio crítico (seção 4). Rafael: quadro comparativo (seção 2). Os dois: classificação dos casos (seção 3) e revisão final.**

## Objetivos

Distinguir programação tradicional e Machine Learning, identificar atributos e alvo e diferenciar classificação, regressão e agrupamento.

## 1. Explicação com suas palavras

1. Como um modelo aprende com dados? **O algoritmo recebe muitos exemplos e ajusta parâmetros internos para reduzir o erro entre o que ele prevê e o que de fato aconteceu. Numa árvore de decisão, por exemplo, ele escolhe as perguntas ("frequência < 60%?") que melhor separam os exemplos. Aprender, aqui, é encontrar padrões nos dados de treino que continuem valendo em dados novos. Por isso a avaliação precisa usar dados que o modelo não viu.**
2. Qual diferença entre algoritmo e modelo? **O algoritmo é a receita de aprendizado: o procedimento genérico, como "árvore de decisão" ou "regressão linear". O modelo é o resultado de aplicar esse algoritmo a um conjunto de dados específico: a árvore já treinada, com suas perguntas e folhas, ou a reta com seus coeficientes. O mesmo algoritmo gera modelos diferentes em dados diferentes.**
3. Compare uma regra de bloqueio de palavra com um modelo de spam. **A regra é programação tradicional: uma pessoa escreve "se a mensagem tiver 'prêmio', bloqueie". Ela é fácil de entender, mas não se adapta: bloqueia mensagens legítimas com a palavra e deixa passar spam escrito "pr3mio". O modelo de spam aprende, com milhares de mensagens já rotuladas como spam ou legítima, quais combinações de palavras, remetentes e formatos indicam spam. Ele generaliza melhor, mas precisa de dados rotulados, erra de formas menos previsíveis e deve ser reavaliado quando o spam muda.**
4. Dê um exemplo de atributo e alvo e defina o momento da previsão. **No laboratório de evasão, os atributos são frequência, nota e entregas observadas até a 4ª semana, e o alvo é `evasao_fim_semestre` (0 = permaneceu, 1 = evadiu). O momento da previsão é o fim da semana 4. Só pode entrar no modelo o que já é conhecido nesse instante. A nota final, por exemplo, seria vazamento de informação, porque só existe depois.**

## 2. Quadro comparativo

| Critério | Supervisionado | Não supervisionado |
| --- | --- | --- |
| Presença de alvo no treino | Sim: cada exemplo tem a resposta conhecida (rótulo ou valor) | Não: não há resposta; só os atributos |
| Pergunta que pode responder | "Este caso vai evadir?", "Quantos empréstimos teremos?" | "Que grupos naturais existem?", "Que registros são atípicos?" |
| Tipo de saída | Classe (classificação) ou número (regressão) | Grupos, estruturas ou pontuação de anomalia |
| Tarefas e exemplo | Classificação: spam/legítima. Regressão: tempo de espera em minutos | Agrupamento: perfis de compra. Detecção de anomalias: operações atípicas |
| Dados necessários | Histórico com desfechos conhecidos e rotulados com qualidade | Atributos relevantes e comparáveis (escala, unidades); rótulos não são necessários |
| Forma de avaliação | Métricas num teste separado: acurácia, sensibilidade, matriz de confusão, MAE, R² | Coesão e separação (silhueta), estabilidade e utilidade avaliada por especialistas |
| Limitação | Depende de rótulos confiáveis e caros; aprende os vieses do histórico | Não há "resposta certa" para validar; os grupos podem não ter significado prático |

## 3. Situações-problema

Os casos são cenários didáticos. Escolha **pelo menos cinco** e justifique sua classificação pelo significado do alvo ou por sua ausência.

| Caso | Situação-problema |
| --- | --- |
| 1 Educação | Prever evadiu/permaneceu com histórico rotulado de turmas anteriores. |
| 2 Saúde | Estimar o tempo de espera em minutos a partir de registros de atendimento. |
| 3 Comércio | Descobrir perfis de compra sem categorias prévias de clientes. |
| 4 Finanças | Prever inadimplente/adimplente com contratos e desfechos conhecidos. |
| 5 Segurança digital | Distinguir spam/legítima com mensagens já revisadas. |
| 6 Comércio | Estimar o total de vendas em reais na próxima semana. |
| 7 Educação | Agrupar perfis de acesso ao ambiente virtual sem rótulo de evasão. |
| 8 Saúde | Classificar exames em categorias previamente definidas por especialistas. |

| Caso escolhido | Alvo ou ausência de alvo | Categoria, quantidade ou grupos? | Abordagem e justificativa | Dados necessários e limitação |
| --- | --- | --- | --- | --- |
| 1 Educação | Alvo: evadiu/permaneceu, conhecido nas turmas anteriores | Categoria (2 classes) | Supervisionado, **classificação**: o alvo é uma categoria e há histórico rotulado | Frequência, notas e entregas até o momento da previsão. Limitação: definição de evasão e mudanças entre turmas |
| 2 Saúde | Alvo: tempo de espera em minutos | Quantidade contínua | Supervisionado, **regressão**: o alvo é numérico e medido | Horário, fila, equipe e tipo de atendimento. Limitação: registros de horário incompletos e sazonalidade |
| 3 Comércio | Sem alvo: não há categorias prévias | Grupos | Não supervisionado, **agrupamento**: queremos descobrir perfis, não prever um rótulo | Frequência, valor e categorias compradas. Limitação: os grupos dependem dos atributos e da escala escolhidos |
| 4 Finanças | Alvo: inadimplente/adimplente, desfecho conhecido | Categoria (2 classes) | Supervisionado, **classificação** | Renda, histórico de pagamento e valor do contrato. Limitação: só há desfecho de quem recebeu crédito (viés de seleção) |
| 6 Comércio | Alvo: vendas em reais na próxima semana | Quantidade | Supervisionado, **regressão** (série temporal) | Vendas passadas, promoções e calendário. Limitação: a divisão treino/teste precisa respeitar a ordem do tempo; feriados atípicos |
| 7 Educação | Sem alvo: não há rótulo de evasão | Grupos | Não supervisionado, **agrupamento** de padrões de acesso | Logins, tempo e recursos usados no ambiente virtual. Limitação: um grupo "pouco ativo" não significa risco de evasão sem validação |

## 4. Raciocínio crítico

“Detectar fraude” define sozinho o tipo de aprendizado? Compare o uso de exemplos rotulados e a busca de operações atípicas sem rótulos. **Não. O que define o tipo de aprendizado é a existência e o uso do alvo, não o nome do problema. Se a empresa tem um histórico de operações confirmadas como fraude ou legítimas, pode treinar um classificador supervisionado. Ele aprende padrões de fraudes já conhecidas e é avaliado por sensibilidade e falsos positivos, mas tende a não reconhecer golpes novos. Sem rótulos, ou para captar golpes ainda não vistos, usa-se uma abordagem não supervisionada: detecção de anomalias que sinaliza operações muito diferentes do comportamento habitual. Ela encontra o que é atípico, mas atípico não é sinônimo de fraude, e cada alerta exige verificação humana. Na prática, as duas abordagens costumam ser combinadas.**

## Entrega

Salve este arquivo preenchido. Critérios: distinção conceitual, pertinência dos dados, justificativa e clareza. [Voltar ao início](README.md).
