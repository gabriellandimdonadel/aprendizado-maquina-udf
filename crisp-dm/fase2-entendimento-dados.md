<img src="../assets/logo-udf.jpg" alt="UDF Centro Universitário" width="230">

**Profa. Kadidja Valéria | UDF**
Ciência de Dados e Aprendizado de Máquina · Sistemas de Informação · 2026.2

# CRISP-DM · Fase 2 — Entendimento dos Dados (GastroMatch)

- Equipe: Gabriel Landim Donadel de Farias e Rafael Batista Mota
- Data: 04/11/2026
- Sistema analisado: versão final em React + Firebase (repositório `TCC---Sistema-de-Informacao`)
- Notebook: [gastromatch-fase2-entendimento-dados.ipynb](../notebooks/gastromatch-fase2-entendimento-dados.ipynb) (abrir no Colab)

> **Objetivo da fase (Guia):** acessar, quantificar e qualificar a matéria-prima disponível para evitar falhas imprevistas na modelagem.

## 1. Coleta dos dados iniciais

### 1.1 Onde estão os dados

| Ambiente | Projeto Firebase | Conteúdo | Serve para conclusões? |
| --- | --- | --- | --- |
| Local | `demo-gastromatch` (emulador) | Fictício, gerado pelo `seed-emulator.mjs` | Não |
| Demonstração (Netlify) | `gastromatch-demo` | Fictício: 188 restaurantes em 26 cidades, cerca de 1.750 avaliações | Não, só para testar o notebook |
| Produção | `thegastromatch` | Cadastros reais | **Sim** |

O seed usa sorteio com semente fixa. Analisar esses dados só "redescobre" as regras do próprio script (a nota é sorteada em torno de uma "qualidade" que o script escolhe). Por isso, os resultados do projeto devem vir da **produção**.

### 1.2 Inventário das coleções (levantado em `firestore.rules` e `app/src/services`)

| Coleção | Campos principais | Uso na análise |
| --- | --- | --- |
| `usuarios` (restaurante) | cozinha, **vibes** (até 3), **ocasioes**, **faixaPreco** (1 a 4), estado, cidade, bairro, lat/lng, horários, status, destaque | Perfil de oferta |
| `usuarios` (cliente) | nome, telefone, status, criadoEm | Só contagem e data de cadastro |
| `usuarios/{uid}/privado` | CPF/CNPJ | **Não é lido** (só o dono tem acesso) |
| `menus` | restauranteId, categoria, titulo, **preco** (número) | Preço real por restaurante |
| `promocoes` | titulo, prato, valorPromocional (texto), diasValidos, horários | Oferta de promoções |
| `cupons` | desconto, validade, **limiteTotal**, **resgatados** | Engajamento |
| `eventos` | titulo, inicio, fim, tipoEvento | Oferta de eventos |
| `salvos` | usuarioId, promocaoId/eventoId, restauranteId, dataResgate | Interesse |
| `resgates` | cupomId, usuarioId, restauranteId, **status (ativo → usado)**, criadoEm, **usadoEm** | Interesse e **visita confirmada** (QR validado no restaurante) |
| `avaliacoes` | alvo (restaurante/prato), **nota 1–5**, comentario, criadoEm | Satisfação |

**O sistema não guarda:**
- **Reservas.** O botão "Reservar mesa" abre o WhatsApp, e o agendamento acontece fora da plataforma.
- **Buscas e filtros aplicados.** Os filtros ficam só no endereço da página e nada é gravado.
- **Visitas ao perfil do restaurante.**

## 2. Descrição (quantidade e tipos)

| Item | Registro |
| --- | --- |
| Volume por coleção (produção) | PREENCHER com a saída da seção 2 do notebook |
| Clientes e restaurantes reais ativos | PREENCHER |
| Período coberto | PREENCHER |
| Formato | Documentos JSON (NoSQL) → DataFrames pandas |
| Códigos/categorias | Lista oficial de 8 experiências e 20 cozinhas (`app/src/lib/catalogo.js`); faixa de preço de 1 a 4 ($ a $$$$); status ativo/banido/excluido |
| Tipos misturados | `valorPromocional` e `desconto` são texto ("R$ 29,90", "10%"); `menus.preco` é número |

## 3. Exploração (gráficos e hipóteses iniciais)

Gráficos no notebook:
- **Oferta:** restaurantes por cozinha, por experiência e por faixa de preço.
- **Demanda:** distribuição das notas, nota média por experiência, funil cupom resgatado → usado.
- **Mapa de calor** dos cupons usados por dia × hora.

Hipóteses que surgiram:
- O **cupom validado por QR** (`status = "usado"`) é o melhor indicador de visita real disponível e pode substituir "reserva" em P2, P3 e H2.
- **Oferta ≠ demanda:** saber quantos restaurantes são "Românticos" não diz quantos clientes procuram esse tipo de lugar.

## 4. Verificação de qualidade

O sistema final já valida muita coisa nas regras do Firestore: tipos, tamanho dos textos, nota de 1 a 5, um resgate por cliente e por cupom, CPF/CNPJ protegidos. Os pontos que sobram para a Fase 3:

| Ponto de atenção | Por que importa |
| --- | --- |
| Contas com status `banido`/`excluido` | Precisam ser filtradas antes de qualquer contagem |
| Restaurantes sem vibe, sem bairro ou sem cardápio | Não aparecem nos filtros e distorcem as comparações |
| `valorPromocional` e `desconto` como texto | Precisam ser convertidos em número |
| Restaurantes com poucas avaliações | A média fica instável (com 1 nota 5, a média é 5,0) |
| Nome/e-mail do cliente repetido em `salvos`, `resgates` e `avaliacoes` | LGPD: o notebook remove e pseudonimiza esses campos |
| Perfis antigos com CPF/CNPJ fora de `privado` | O README pede migração antes da produção |

Contagens: PREENCHER com a tabela da seção 4 do notebook rodado na produção.

## 5. Os dados respondem às perguntas de negócio?

| Pergunta / hipótese | Disponível? | Como responder |
| --- | --- | --- |
| P1 culinárias e vibes mais buscadas | Parcial | Oferta cadastrada + demanda indireta (salvos, resgates, avaliações). Não há log de buscas. |
| P2 perfil com maior conversão | Proxy | Trocar "visita → reserva" por "cupom resgatado → usado", por vibe, faixa de preço, bairro e nota |
| P3 dias e horários de maior demanda | Proxy | `resgates.usadoEm` (momento em que o cliente estava no restaurante) |
| P4 avaliações × culinária/vibe | **Sim** | `avaliacoes` × `vibes`/`cozinha` do restaurante |
| P5 promoções e eventos com mais engajamento | **Sim** | `salvos` por promoção/evento; `resgatados ÷ limiteTotal` por cupom |
| H1 vibe é mais filtrada que culinária | Não | Exige gravar os filtros aplicados |
| H2 nota > 4,5 e preço intermediário concentram reservas | Proxy | Usar cupons usados no lugar de reservas |
| H3 promoções agendadas geram mais reservas | Parcial | Só cupons têm data de início (`validadeInicio`); promoções não têm |

## 6. Conclusão e retorno à Fase 1

1. O sistema final **tem os dados centrais do projeto**: vibe, faixa de preço, localização, avaliações e cupons validados. P4 e P5 podem ser respondidas diretamente, e P2 e P3 por proxy.
2. **Lacunas:** reservas (WhatsApp) e buscas não são registradas. A H1 fica sem teste, e a P1 só pode ser respondida pela oferta.
3. **Volume real:** PREENCHER. Se a produção tiver poucos usuários reais, a análise fica descritiva, com essa limitação declarada. Uma coleta curta com colegas e parceiros pode ajudar, desde que seja informada como amostra de conveniência.
4. **Ajustes na Fase 1** (CRISP-DM é cíclico): atualizar o documento de definição (§3.1, §3.3 e §8 descrevem a versão antiga do sistema). Avaliar se o sistema passa a gravar, sem dados pessoais, (a) os filtros aplicados e (b) o clique em "Reservar pelo WhatsApp".

[← Fase 1](fase1-entendimento-negocio.md) · [Voltar ao início](../README.md)
