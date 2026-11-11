<img src="../assets/logo-udf.jpg" alt="UDF Centro Universitário" width="230">

**Profa. Kadidja Valéria | UDF**
Ciência de Dados e Aprendizado de Máquina · Sistemas de Informação · 2026.2

# CRISP-DM · Fase 1 — Entendimento do Negócio (GastroMatch)

- Equipe: Gabriel Landim Donadel de Farias e Rafael Batista Mota
- Data: 04/11/2026
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
| Dados existentes | Coleções `usuarios` (restaurantes com vibes, faixa de preço e localização), `menus`, `promocoes`, `cupons`, `eventos`, `salvos`, `resgates` e `avaliacoes`. O detalhamento está na [Fase 2](fase2-entendimento-dados.md). |
| Restrições | Prazo até dez/2026; pouco volume de dados; sem Firebase Functions; nenhum integrante especialista em dados. |
| Riscos principais | Pouco volume nas coleções novas (probabilidade alta, impacto alto); atraso na implementação das coleções; dificuldade para montar o dashboard; desalinhamento com o orientador. |
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
| 1. Negócio | Este documento + validação com a professora/orientador | 04/11/2026 |
| 2. Dados | Exportar o Firestore, inventariar campos e verificar qualidade ([notebook](../notebooks/gastromatch-fase2-entendimento-dados.ipynb)) | 04/11/2026 |
| 3. Preparação | Remover dados pessoais, padronizar preço/desconto/culinária, juntar coleções por `restauranteId` | Nov/2026 |
| 4. Modelagem | Análises descritivas P1–P5; regressão logística opcional em P2 | Dez/2026 |
| 5. Avaliação | Conferir as respostas contra os critérios de sucesso de negócio; testar o painel com parceiros | Dez/2026 |
| 6. Implementação | Dashboard para parceiros e relatório final para a banca | Dez/2026 |

## 5. Pontos de atenção encontrados na revisão

Estes pontos não invalidam o documento. São ajustes para conversar com a professora:

1. **O escopo exclui ML, mas a P2 cita regressão logística**, que é um modelo de aprendizado supervisionado. Sugestão: deixar explícito que a regressão logística é opcional e só entra se houver volume de reservas.
2. **Faltava um critério de sucesso de negócio.** Com o sistema final, um candidato natural é a taxa de cupons resgatados que viram visita (QR validado). Os critérios da seção 11 medem o projeto acadêmico, não o impacto para o parceiro. O Guia CRISP-DM diz para medir impacto real, não só precisão técnica. A sugestão está no item 1 acima.
3. **O documento descreve a versão antiga do sistema.** As seções §3.1, §3.3 e §8 citam a coleção `restaurantes` e dizem que avaliações e reservas "serão implementadas". No sistema final, avaliações, resgates, vibes e faixa de preço já existem, e as reservas acontecem pelo WhatsApp. Também é preciso dizer qual banco é real (produção) e qual é fictício (demonstração).
4. **Duas perguntas dependem de dados que o sistema não grava** (filtros aplicados e reservas). A Fase 2 mostra isso em detalhe. É o "retorno" previsto no ciclo CRISP-DM: os dados obrigam a revisar o negócio.

[Ir para a Fase 2 →](fase2-entendimento-dados.md) · [Voltar ao início](../README.md)
