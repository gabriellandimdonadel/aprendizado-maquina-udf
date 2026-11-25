<img src="../assets/logo-udf.jpg" alt="UDF Centro Universitário" width="230">

**Profa. Kadidja Valéria | UDF**
Ciência de Dados e Aprendizado de Máquina · Sistemas de Informação · 2026.2

# CRISP-DM · Fase 2 — Entendimento dos Dados (GastroMatch)

- Equipe: Gabriel Landim Donadel de Farias e Rafael Batista Mota
- Data: 25/11/2026
- Notebook executado: [gastromatch-fase2-entendimento-dados.ipynb](../notebooks/gastromatch-fase2-entendimento-dados.ipynb). Ele abre no Colab e baixa os dados do próprio GitHub.
- Dados: [dados/gastromatch/](../dados/gastromatch/) · Dicionário: [dados/gastromatch/README.md](../dados/gastromatch/README.md) · Exportação: [scripts/exportar_gastromatch.py](../scripts/exportar_gastromatch.py)

> **Objetivo da fase (Guia):** acessar, quantificar e qualificar a matéria-prima disponível para evitar falhas imprevistas na modelagem.

## 1. Coleta dos dados iniciais

| Item | Registro |
| --- | --- |
| Fonte | Firestore do projeto **`gastromatch-demo`**, o banco do site de demonstração publicado no Netlify |
| Data da exportação | 25/11/2026, somente leitura, com `scripts/exportar_gastromatch.py` |
| Condição dos dados | **Fictícios.** O banco é povoado pelo script `seed-emulator.mjs` do sistema (restaurantes, clientes e avaliações inventados, sorteio com semente fixa). É o mesmo esquema da produção. |
| Por que esta base | Ela atende à volumetria pedida (mais de 1.000 registros) e tem o mesmo esquema da produção. O banco de produção (`thegastromatch`) não foi usado. |
| Proteção de dados | Removidos nome, e-mail, telefone, WhatsApp, endereço, coordenadas e fotos. IDs de clientes pseudonimizados por hash. CPF/CNPJ ficam em subcoleção privada e não são lidos. |
| Fora da base | Reservas (feitas pelo WhatsApp) e registro de buscas e filtros: o sistema não grava esses dados. |

## 2. Descrição (quantidade, tipos e códigos)

| Coleção | Registros | Atributos | Conteúdo |
| --- | ---: | ---: | --- |
| `avaliacoes` | **1.751** | 10 | Nota 1–5, comentário, alvo (1.213 de restaurante, 538 de prato) |
| `menus` | 748 | 7 | Categoria, prato, preço (R$ 7,20 a R$ 384,00; mediana R$ 43,60) |
| `usuarios` | 232 | 4 | 188 restaurantes, 43 clientes, 1 admin (todos ativos) |
| `restaurantes` | 188 | 22 | Cozinha (20), vibes (8), ocasiões, faixa de preço 1–4, 26 cidades em 12 estados, notaMedia |
| `resgates` | 66 | 9 | Cupom resgatado, status ativo/usado |
| `promocoes` | 35 | 14 | Promoções com início e fim |
| `cupons` | 29 | 13 | Desconto, limite, resgatados |
| `eventos` | 22 | 12 | Eventos dos restaurantes e da plataforma |
| `favoritos` / `salvos` | 3 / 1 | — | Interações |
| **Total** | **3.075** | | |

- **Período das avaliações:** 19/03/2026 a 14/11/2026.
- **Tipos:** nota e faixa de preço são inteiros; preço é decimal; datas em ISO 8601 (UTC); listas (vibes, ocasiões, dias) aparecem como texto separado por `|`.
- **Tipos inadequados:** `desconto` ("15%", "Sobremesa grátis", "R$ 50 de desconto") e `valorPromocional` ("R$ 219,90") estão em texto.

## 3. Exploração (resultados calculados)

| Análise | Resultado |
| --- | --- |
| Oferta | Mais restaurantes Japoneses (20), Italianos (18) e Brasileiros (15). Vibes mais marcadas: Familiar (70), Tranquila (66), Descontraída (63). Faixas: $ 45 · $$ 57 · $$$ 46 · $$$$ 40. |
| Distribuição das notas | Nota 2: 67 · nota 3: 425 · nota 4: 768 · nota 5: 491. Média 3,96, desvio-padrão 0,82. Não há nota 1. |
| Nota por experiência | De 3,92 (Cafeteria) a 4,03 (Sofisticada). Os intervalos de confiança de 95% se sobrepõem. |
| Nota por faixa de preço | De 3,94 ($$) a 3,99 ($$$). Os intervalos se sobrepõem. |
| Preço × faixa | Mediana do prato principal: $ R$ 46 · $$ R$ 68 · $$$ R$ 96 · $$$$ R$ 131. Mas **24% dos pratos principais de restaurantes "$" passam de R$ 60**. |
| Cupons | 66 resgates, 27 usados no restaurante (**41%**). |

**Interpretação:** a vibe e a faixa de preço não mostram efeito sobre a nota nesta base. Isso é esperado, porque o seed sorteia a nota em torno de uma "qualidade" independente da vibe. Os padrões refletem o script gerador, não o comportamento de consumidores.

**Hipóteses que surgiram:**
- A faixa de preço declarada pode divergir do cardápio. Na Fase 3, vale derivar uma faixa a partir dos preços.
- O uso do cupom (QR validado) é o único sinal de visita real e pode substituir a reserva quando houver volume.

## 4. Verificação de qualidade

**O que está correto:** os campos calculados batem com os dados brutos (`notaMedia`, `totalAvaliacoes`, contador de resgates). Não há chaves duplicadas (uma avaliação por cliente e alvo), valores fora do domínio, registros órfãos nem preço ≤ 0. As regras do Firestore funcionam.

| Problema | Ocorrências | Consequência |
| --- | ---: | --- |
| Avaliações com data **anterior** ao cadastro do restaurante | 1.750 (99,9%) | As datas de cadastro não servem para análise temporal (datas retroativas do seed) |
| Todos os restaurantes cadastrados no mesmo dia (14/11/2026) | 188 (100%) | Idem |
| Os 27 usos de cupom têm o **mesmo instante** (sexta, 18h) | 27 (100%) | A P3 (dias e horários) não pode ser analisada |
| Apenas **41 clientes** fizeram as 1.751 avaliações (cerca de 43 cada) | — | Concentração irreal: a base não representa consumidores |
| Restaurantes sem avaliação / com ≤ 3 avaliações | 11 / 36 | Médias instáveis: exigir um mínimo de avaliações |
| Avaliações sem comentário | 493 (28%) | Limita a análise de texto |
| Cupons sem horário informado | 29 (100%) | Campo não preenchido |
| `desconto` não percentual · `valorPromocional` em texto | 2 · 35 | Converter na Fase 3 |
| Prato principal de restaurante "$" acima de R$ 60 | 21 (24%) | Faixa declarada × cardápio |

## 5. Os dados respondem às perguntas de negócio?

| Pergunta / hipótese | Disponível? | Evidência |
| --- | --- | --- |
| P1 culinárias e vibes mais buscadas | Parcial | Só a oferta (429 marcações de vibe). Não há log de buscas. |
| P2 perfil com maior conversão | Proxy fraco | 66 resgates e 27 usos: pouco volume por perfil |
| P3 dias e horários de maior demanda | Não nesta base | Os 27 usos têm o mesmo instante |
| P4 avaliações × culinária/vibe | **Sim** | 1.213 avaliações de restaurante com vibe e cozinha |
| P5 promoções e eventos com mais engajamento | Parcial | 35 promoções e 1 salvamento; 66 resgates de cupom |
| H1 vibe é mais filtrada que culinária | Não | Filtros não são registrados |
| H2 nota > 4,5 e preço intermediário concentram reservas | Proxy fraco | Não há reservas |
| H3 promoções agendadas geram mais reservas | Parcial | Não há reservas para comparar |

## 6. Conclusão e retorno à Fase 1

1. **A base tem volume e estrutura suficientes** (3.075 registros, 1.751 avaliações) para montar e testar todo o processo: exportação segura, limpeza e análise. As regras do sistema garantem boa integridade.
2. **Ela não permite conclusões sobre consumidores.** É fictícia, tem 41 clientes com cerca de 43 avaliações cada, datas retroativas e usos de cupom num único instante. Qualquer "resultado" seria só o reflexo do script gerador.
3. **Só a P4 tem dados diretos.** As perguntas sobre demanda (P1, P2, P3, H1, H2) dependem de dados que o sistema não grava.
4. **Ajustes na Fase 1** (o ciclo CRISP-DM):
   - Atualizar o documento de definição com a base usada e as lacunas. Já feito na versão 1.1.
   - Gravar, sem dados pessoais, os **filtros aplicados** (coleção `buscas`) e o **clique em "Reservar pelo WhatsApp"**.
   - Analisar a **produção** quando houver volume real, e usar esta base apenas para validar o processo.

[← Fase 1](fase1-entendimento-negocio.md) · [Voltar ao início](../README.md)
