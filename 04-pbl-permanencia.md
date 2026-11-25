<img src="assets/logo-udf.jpg" alt="UDF Centro Universitário" width="230">

**Profa. Kadidja Valéria | UDF**  
Ciência de Dados e Aprendizado de Máquina · Sistemas de Informação · 2026.2

# PBL integrador — Apoio à Permanência

## Identificação

- Estudante ou equipe: **Gabriel Landim Donadel de Farias e Rafael Batista Mota**
- Turma: **Sistemas de Informação — UDF, 2026.2**
- Data de realização: **25/11/2026**
- Integrantes e contribuições (se em equipe): **Gabriel: delimitação, abordagem e avaliação (seções 1, 4 e 5). Rafael: dados, limites e proteção (seções 3 e 6). Os dois: perguntas de negócio, recomendações e apresentação.**

## Contexto

Uma instituição quer compreender sinais associados à evasão e oferecer apoio antes do fim do semestre. Público-alvo: estudantes matriculados e equipe de apoio acadêmico. O cenário é didático e a prática usa dados sintéticos.

**Questão norteadora:** como identificar situações que merecem atenção e oferecer apoio, reconhecendo erros do modelo e dificuldades que os dados não capturam?

## Proposta da equipe

### 1. Delimitação

- Problema e público: **Estudantes que abandonam o curso costumam dar sinais nas primeiras semanas (faltas, notas baixas, atividades não entregues), mas a equipe de apoio acadêmico só fica sabendo quando já é tarde. Público: estudantes matriculados (beneficiários) e equipe de apoio acadêmico (usuária).**
- Decisão que o resultado pode apoiar: **A quem a equipe de apoio deve oferecer primeiro um convite voluntário de conversa ou monitoria na semana 5, considerando que ela tem tempo limitado.**
- Definição de evasão, unidade e horizonte: **Evasão é não renovar a matrícula nem concluir a disciplina até o fim do semestre, sem trancamento formal. Unidade: estudante × semestre. Previsão na semana 4, com horizonte até o fim do semestre.**

### 2. Perguntas de negócio

1. **Quais estudantes, pelos sinais observados até a semana 4, têm maior chance de evadir e devem receber primeiro o convite de apoio?**
2. **Quantos estudantes que evadiram o modelo deixa de sinalizar (falsos negativos), e como garantir que eles também tenham acesso ao apoio?**

### 3. Dados necessários

| Dado | Papel no projeto | Disponível quando? | Origem pretendida | Necessidade e risco |
| --- | --- | --- | --- | --- |
| Frequência até a semana 4 (%) | Atributo | Semana 4 | Diário de classe | Necessário. Risco: registro irregular por docente |
| Nota parcial até a semana 4 (0–10) | Atributo | Semana 4, com ausentes | Ambiente virtual / diário | Necessário. Risco: notas faltantes (5% na simulação) e critérios diferentes entre disciplinas |
| Entregas até a semana 4 (contagem) | Atributo | Semana 4 | Ambiente virtual | Necessário. Risco: atividades diferentes por disciplina |
| Evasão ao fim do semestre (0/1) | Alvo | Só ao fim do semestre | Secretaria acadêmica | Necessário para treinar e avaliar. Risco: definição ambígua (trancamento, transferência) |
| Curso, turno e forma de ingresso | Auditoria de equidade (não entra no modelo) | Matrícula | Sistema acadêmico | Só para medir erros por grupo. Risco: discriminação se usado para decidir |
| Trabalho, saúde, renda, transporte | Não usado | — | — | Dados sensíveis, que o modelo não captura. São tratados na conversa humana, não coletados |

Diferencie dados usados na simulação e dados que seriam necessários para uma investigação real: **A simulação usou só 3 atributos sintéticos (frequência, nota e entregas) e um alvo sorteado por uma função conhecida, com 600 registros. Uma investigação real exigiria registros históricos de vários semestres, com definição oficial de evasão, autorização e base legal (LGPD), dados de grupos para auditoria, divisão temporal (treinar em semestres passados e testar no seguinte) e a participação de estudantes e da equipe de apoio na definição do uso.**

### 4. Abordagem e algoritmo

- Classificação, regressão ou outra formulação, com justificativa: **Classificação binária supervisionada: o alvo é uma categoria (evadiu ou permaneceu) com histórico rotulado. Codificar como 1/0 não a torna regressão. Usamos a estimativa de cada folha só para ordenar quem recebe o convite primeiro.**
- Algoritmo introdutório escolhido: **Árvore de decisão com imputação pela mediana num `Pipeline` (`max_depth=5`, `min_samples_leaf=10`), escolhida por validação cruzada no treino. É interpretável: a equipe de apoio entende as regras.**
- Referência simples: **`DummyClassifier` com a classe mais frequente (sempre "permaneceu"), com acurácia de 0,593 no teste e sensibilidade 0. Alternativa sem ML: convidar quem tem frequência abaixo de 75%.**

### 5. Avaliação

- Preparação, divisão e validação: **Divisão estratificada 75/25 (450 de treino e 150 de teste), semente 42. Imputação aprendida só no treino, dentro do `Pipeline`. Validação cruzada estratificada em 5 partes para escolher a profundidade. Teste usado uma única vez.**
- Métricas e razão da escolha: **Sensibilidade da classe 1 (o pior erro é deixar de convidar quem vai evadir), matriz de confusão (mostra os tipos de erro) e acurácia, sempre comparadas com a referência. A acurácia sozinha enganaria em turmas com pouca evasão.**
- Resultados efetivamente calculados e link da evidência: **Acurácia no teste de 0,78 (referência: 0,593); sensibilidade de 0,689 (42/61); validação cruzada de 0,722 ± 0,039. Matriz: TN = 75, FP = 14, FN = 19, TP = 42. Evidência: [notebooks/laboratorio-equipe.ipynb](notebooks/laboratorio-equipe.ipynb) e [03-aula2-laboratorio.md](03-aula2-laboratorio.md).**
- Erros relevantes e consequências: **19 falsos negativos: estudantes que evadiram e não seriam convidados, o erro mais grave. 14 falsos positivos: convites desnecessários, de custo baixo se o contato for acolhedor. Num uso real, valeria baixar o limiar para trocar falsos negativos por falsos positivos.**

### 6. Limites e proteção

- Por que os resultados não demonstram causalidade? **O modelo encontra associações: estudantes com nota baixa evadem mais na simulação. A nota baixa pode ser consequência da mesma causa da evasão (trabalho, problemas financeiros, saúde), e não a causa. Melhorar a nota à força não garante a permanência. Além disso, nos dados sintéticos as relações foram definidas por uma função escolhida pela professora.**
- Por que dados sintéticos não validam uso institucional? **Eles mostram só que o método funciona. As associações, a proporção de evasão (41%), o ruído e a ausência de grupos foram inventados. Uma instituição real tem outra população, outras definições e mudanças ao longo do tempo. Seria preciso avaliar com dados reais, em divisão temporal e com auditoria por grupos, antes de qualquer uso.**
- Que grupos podem ser mal representados? Como investigar isso com evidências apropriadas? **Estudantes do noturno ou que trabalham (menos entregas no ambiente virtual por falta de tempo, não de interesse), ingressantes por transferência, pessoas com deficiência e cursos com poucos alunos. Para investigar, com dados reais e autorização, medir sensibilidade e taxa de falsos positivos separadamente por curso, turno e forma de ingresso. Também ouvir estudantes desses grupos sobre como os sinais são registrados.**
- Como minimizar dados, restringir acesso e definir retenção? **Usar só os 3 sinais acadêmicos necessários, sem nome no conjunto de modelagem (ID pseudonimizado). Só a equipe de apoio acessa a lista de convites, e docentes não veem a pontuação. As previsões são apagadas ao fim do semestre, e só métricas agregadas são guardadas para reavaliar o modelo.**
- Como garantir revisão humana e contestação? **Toda sinalização passa por uma pessoa da equipe de apoio antes do contato. O estudante pode saber que foi sinalizado, recusar o convite sem consequência e pedir correção dos dados. O modelo nunca gera bloqueio, punição ou registro no histórico.**

### 7. Recomendações de apoio

- Ação voluntária proposta: **Na semana 5, convite individual e sigiloso para uma conversa com a equipe de apoio, com oferta de monitoria, plano de estudos, orientação sobre auxílios e flexibilização de prazos. A ordem dos convites segue a estimativa do modelo, revisada por uma pessoa.**
- Como acolher estudantes não sinalizados pelo modelo: **O apoio fica aberto a todos: divulgação geral em sala e no ambiente virtual, possibilidade de autoencaminhamento e indicação por docentes. Assim os 19 falsos negativos (31% dos que evadiram, no teste) não ficam sem acesso.**
- O que precisa ser verificado antes de aplicação real: **Desempenho em dados reais e em divisão temporal; sensibilidade e falsos positivos por grupo; definição oficial de evasão; base legal e consentimento (LGPD); capacidade da equipe de atender os convites; e um piloto acompanhado, comparando permanência com e sem o programa.**

Previsões não são certezas. Priorize apoio e revisão humana, sem punições ou decisões automáticas prejudiciais.

## Apresentação de cinco minutos

| Tempo | Conteúdo | Responsável |
| --- | --- | --- |
| 1 minuto | Problema e dados | Rafael Batista Mota |
| 2 minutos | Método e resultados | Gabriel Landim Donadel de Farias |
| 1 minuto | Limitações | Rafael Batista Mota |
| 1 minuto | Recomendações de apoio | Gabriel Landim Donadel de Farias |

## Contribuições

| Integrante | Contribuição verificável |
| --- | --- |
| Gabriel Landim Donadel de Farias | Seções 1, 4, 5 e 7; execução e interpretação do [notebook](notebooks/laboratorio-equipe.ipynb) |
| Rafael Batista Mota | Seções 2, 3 e 6; tabela de dados e plano de proteção (minimização, acesso, retenção e contestação) |

[Voltar ao início](README.md).
