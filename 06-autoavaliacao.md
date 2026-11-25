<img src="assets/logo-udf.jpg" alt="UDF Centro Universitário" width="230">

**Profa. Kadidja Valéria | UDF**  
Ciência de Dados e Aprendizado de Máquina · Sistemas de Informação · 2026.2

# Autoavaliação e conferência da entrega

## Identificação

- Estudante ou equipe: **Gabriel Landim Donadel de Farias (autoavaliação individual), em equipe com Rafael Batista Mota**
- Turma: **Sistemas de Informação — UDF, 2026.2**
- Data de realização: **25/11/2026**
- Integrantes e contribuições (se em equipe): **Gabriel: execução dos notebooks, experimentos de classificação, Fases 1, 2 e 4 do CRISP-DM. Rafael: regressão, dados e proteção, documentação das Fases 3, 5 e 6. Os dois: PBLs, revisão e apresentação.**

## Checklist

- [x] Diferenciei IA, Ciência de Dados e ML com um exemplo.
- [x] Completei o quadro supervisionado/não supervisionado.
- [x] Justifiquei pelo menos cinco situações-problema.
- [x] Registrei a investigação da biblioteca.
- [x] Identifiquei atributos, alvo, unidade e momento da previsão.
- [x] Executei e documentei a prática em Python ou Orange.
- [x] Escolhi configurações usando treino/validação.
- [x] Mantive o teste fora do ajuste e da seleção.
- [x] Interpretei acurácia, matriz, MAE e R².
- [x] Comparei com uma referência e discuti erros.
- [x] Registrei limitações, dados sintéticos, privacidade e vieses.
- [x] Formulei recomendações de apoio com revisão humana.
- [x] Respondi às questões individuais.
- [x] Conferi os links e os arquivos de evidências.
- [x] Substituí os campos PREENCHER ou justifiquei os não aplicáveis.

**Exemplo (IA × Ciência de Dados × ML):** IA é o campo amplo de sistemas que realizam tarefas "inteligentes", como o assistente de conversa do GastroMatch. Ciência de Dados é o processo de transformar dados em decisões, como o projeto CRISP-DM que analisou 1.751 avaliações. ML é a parte que aprende padrões a partir de exemplos, como a árvore de decisão do laboratório, que aprendeu a prever evasão com 450 registros de treino.

## Reflexão individual

- O que aprendi e consigo explicar: **A diferença entre treino, validação e teste, e por que o teste só pode ser usado uma vez. Por que a acurácia sozinha engana (95% de acurácia com sensibilidade zero). Como ler uma matriz de confusão e pensar no custo de cada erro. No projeto CRISP-DM, aprendi que a unidade de análise muda a conclusão: no nível da avaliação a cozinha parecia significativa, mas no nível do restaurante não era.**
- Qual foi minha principal dificuldade: **Separar associação de causalidade e não confiar em resultados "bonitos" sem conferir. Alguns números iniciais do projeto (silhueta de 0,48, "2,4× mais exposição") não se sustentaram quando os notebooks foram executados de verdade (0,22 e 1,54×).**
- Qual evidência mostra meu avanço: **O [notebook do laboratório](notebooks/laboratorio-equipe.ipynb), com os experimentos de `min_samples_leaf` e de retirada de atributos, e o projeto [CRISP-DM](crisp-dm/README.md) nas 6 fases, com notebooks executados e verificações automáticas (log com 0 erros, equivalência 500/500 do motor de recomendação).**
- Como contribuí com a equipe: **Executei os notebooks e os experimentos de classificação, fiz a exportação segura dos dados do GastroMatch (sem dados pessoais) e redigi as Fases 1, 2 e 4. Também revisei a coerência dos números entre os documentos.**
- O que preciso revisar: **Métricas para classes desbalanceadas além da sensibilidade (precisão, F1, curva ROC), ajuste de limiar de decisão e validação temporal em dados reais.**
- Ferramentas de apoio utilizadas, incluindo IA quando houver, e como verifiquei as respostas: **Python (pandas, scikit-learn, scipy), Jupyter e Google Colab, Git/GitHub e o livro da disciplina. Usei um assistente de IA (Claude, da Anthropic) para organizar os documentos, escrever partes do código de análise e revisar a redação. Verifiquei executando todos os notebooks do zero, refazendo à mão os cálculos (acurácia 117/150 = 0,78; MAE = 25/3) e comparando os números dos documentos com as saídas. Quando houve divergência, mantive o valor calculado. A responsabilidade pelo conteúdo é minha e da equipe.**

## Critérios de avaliação

Escala sugerida do material: nível 3 consistente, 2 adequado com lacunas, 1 parcial, 0 ausente/incoerente. Nota do critério = peso × nível/3. A professora pode ajustar a aplicação.

| Critério | Peso aula 1 | Peso aula 2/PBL |
| --- | --- | --- |
| Problema e conceitos | 3,0 | 2,0 |
| Dados e justificativa | 2,0 | 2,0 |
| Método e avaliação | 1,0 | 3,0 |
| Interpretação e responsabilidade | 2,0 | 2,0 |
| Clareza e colaboração | 2,0 | 1,0 |
| Total | 10,0 | 10,0 |

Na aula 1, método corresponde à avaliação proposta. Na aula 2, inclui execução e interpretação. A maior acurácia isolada não assegura a melhor avaliação da atividade.

## Fontes de apoio

- SCIKIT-LEARN. *User Guide*. https://scikit-learn.org/stable/user_guide.html.
- SCIKIT-LEARN. *Common pitfalls and recommended practices*. https://scikit-learn.org/stable/common_pitfalls.html.
- ORANGE DATA MINING. *Test and Score*. https://orangedatamining.com/widget-catalog/evaluate/testandscore/.

Referências indicadas no material didático do módulo, consultadas em 14 out. 2026. Registre a data da sua própria consulta quando utilizar novas fontes.

[Voltar ao início](README.md).
