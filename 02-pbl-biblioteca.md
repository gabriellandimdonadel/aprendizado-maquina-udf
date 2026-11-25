<img src="assets/logo-udf.jpg" alt="UDF Centro Universitário" width="230">

**Profa. Kadidja Valéria | UDF**  
Ciência de Dados e Aprendizado de Máquina · Sistemas de Informação · 2026.2

# PBL — Biblioteca em Foco

## Identificação

- Estudante ou equipe: **Gabriel Landim Donadel de Farias e Rafael Batista Mota**
- Turma: **Sistemas de Informação — UDF, 2026.2**
- Data de realização: **25/11/2026**
- Integrantes e contribuições (se em equipe): **Gabriel: delimitação do problema, perguntas de negócio e abordagem. Rafael: dados, atributos, privacidade e avaliação. Os dois: conclusão e síntese da apresentação.**

## Situação-problema

Uma biblioteca universitária enfrenta filas em horários específicos e baixa utilização de alguns serviços. A coordenação deseja melhorar o atendimento e planejar recursos. Este é um cenário didático.

**Público-alvo:** estudantes usuários, equipe de atendimento e gestão.

**Questão norteadora:** como os dados podem orientar o planejamento da biblioteca e a oferta de serviços sem identificar ou discriminar seus usuários?

## Investigação em equipe

1. Delimitem o problema e a decisão a apoiar.
2. Registrem o que já sabem e o que precisam investigar.
3. Formulem duas perguntas de negócio.
4. Definam a unidade de análise, os atributos e o alvo, quando houver.
5. Justifiquem a abordagem e indiquem se uma análise descritiva já seria suficiente.
6. Proponham avaliação, cuidados com os dados e limitações.

## Canvas da equipe

| Campo | Registro |
| --- | --- |
| Problema e decisão | Filas em alguns horários e serviços pouco usados (salas de estudo em grupo, apoio à pesquisa, empréstimo de notebooks). Decisão a apoiar: **como distribuir a escala de atendentes por faixa horária e quais serviços divulgar, ajustar ou remanejar** |
| Público-alvo | Estudantes usuários (atendimento mais rápido), equipe de atendimento (escala equilibrada) e gestão (alocação de recursos) |
| O que sabemos | As filas se concentram em certos horários, provavelmente nos intervalos entre aulas e perto das provas. Alguns serviços têm baixa procura. O sistema de empréstimos e as catracas já registram eventos com data e hora |
| O que precisamos investigar | Em que dias e horas exatamente a demanda passa da capacidade; se a baixa procura é falta de interesse ou de divulgação, horário ou localização; quanto tempo dura cada atendimento |
| Pergunta de negócio 1 | **Quantos atendimentos por hora a biblioteca terá em cada dia da semana nas próximas semanas, para dimensionar a escala?** |
| Pergunta de negócio 2 | **Quais serviços têm uso abaixo do esperado, em quais períodos, e o que os usuários dizem que os faria usar?** |
| Unidade de análise e período | Pergunta 1: **faixa de uma hora** de funcionamento (dia × hora), nos últimos 2 semestres. Pergunta 2: **serviço × semana** no mesmo período |
| Atributos, unidades e origem pretendida | Dia da semana, hora, semana do semestre (indica período de provas), feriado (sim/não): calendário acadêmico. Empréstimos e devoluções por hora (contagem): sistema da biblioteca. Entradas por hora (contagem): catracas. Reservas de salas (contagem): sistema de reservas. Tempo de atendimento (minutos): amostra cronometrada |
| Alvo e momento em que será conhecido, ou ausência de alvo | Pergunta 1: **alvo numérico**, a quantidade de atendimentos na faixa horária, conhecida ao fim de cada hora. A previsão é feita na sexta-feira para a semana seguinte. Pergunta 2: **sem alvo**, análise descritiva do uso por serviço |
| Abordagem e justificativa | Começar pela **análise descritiva** (mapa de calor dia × hora, médias por semana do semestre). Ela provavelmente já basta para montar a escala. Se o padrão variar muito ao longo do semestre, usar uma **regressão** (atendimentos por hora a partir de dia, hora e semana), avaliada com divisão temporal. Pergunta 2: descritiva, complementada por questionário |
| Alternativa sem ML | Tabela de médias de atendimentos por dia × hora do semestre anterior, com acréscimo nas semanas de prova. É simples, explicável e serve como **referência** que qualquer modelo precisa superar |
| Como avaliar a proposta | Previsão: MAE em atendimentos/hora nas últimas semanas (treino nas anteriores), comparado com a média histórica. Negócio: tempo médio de espera e tamanho máximo da fila antes e depois da nova escala, além da satisfação dos usuários |
| Privacidade e limitações | Usar só **contagens agregadas por hora**, sem matrícula ou nome. Os registros de empréstimo são pseudonimizados e descartados depois da agregação. Não cruzar com curso ou perfil de quem usa, para não discriminar. Limitações: mudanças de calendário, eventos atípicos (greves, feriados prolongados) e serviços novos sem histórico |

## Registro de colaboração

| Integrante | Papel | Contribuição |
| --- | --- | --- |
| Gabriel Landim Donadel de Farias | Problema e abordagem | Delimitação, perguntas de negócio, escolha entre análise descritiva e regressão |
| Rafael Batista Mota | Dados e responsabilidade | Atributos e fontes, plano de avaliação, cuidados de privacidade |

## Conclusão da equipe

**Proposta:** montar um painel descritivo de demanda por dia × hora, alimentado por contagens agregadas do sistema de empréstimos e das catracas, para redistribuir a escala de atendimento. Uma regressão de demanda só entra se superar, em MAE, a referência das médias históricas numa avaliação temporal. Para os serviços pouco usados, combinar dados de uso com um questionário curto antes de decidir cortes ou mudanças.

**Dúvida ainda aberta:** a baixa utilização de alguns serviços é falta de interesse ou de divulgação e acesso? Os dados de uso sozinhos não respondem; é preciso ouvir os usuários.

**Feedback recebido e melhoria realizada:** a primeira versão propunha ML direto. Revisamos para começar pela análise descritiva e usar as médias históricas como referência, porque o problema pode ser resolvido sem um modelo complexo.

## Entrega

Canvas preenchido e síntese para apresentação de dois minutos. Avaliar coerência da pergunta, dados, abordagem, responsabilidade e colaboração. [Voltar ao início](README.md).
