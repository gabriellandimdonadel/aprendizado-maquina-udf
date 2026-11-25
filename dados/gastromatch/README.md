# Dados do GastroMatch: dicionário

**Condição:** dados **fictícios** do projeto de demonstração `gastromatch-demo`, povoado pelo script `seed-emulator.mjs` do sistema. Não representam pessoas nem restaurantes reais.
**Exportação:** 25/11/2026, somente leitura, com [`scripts/exportar_gastromatch.py`](../../scripts/exportar_gastromatch.py). Nome, e-mail, telefone, WhatsApp, endereço, coordenadas e fotos foram removidos. `usuarioId` é um pseudônimo (hash). Listas estão separadas por `|`. Datas em ISO 8601 (UTC).

| Arquivo | Linhas | Unidade | Atributos |
| --- | ---: | --- | --- |
| `avaliacoes.csv` | 1.751 | uma avaliação | `alvo` (restaurante/prato), `alvoId`, `restauranteId`, `usuarioId`, `nota` (1–5), `comentario`, `tituloPrato` (só em prato), `criadoEm`, `atualizadoEm` |
| `menus.csv` | 748 | um prato | `restauranteId`, `cozinha`, `categoria`, `titulo`, `preco` (R$), `criadoEm` |
| `usuarios.csv` | 232 | uma conta | `id`, `tipo` (cliente/restaurante/admin), `status`, `criadoEm` |
| `restaurantes.csv` | 188 | um restaurante | `slug`, `nomeRestaurante`, `cozinha`, `vibes` (até 3), `ocasioes`, `faixaPreco` (1 = até R$ 60/pessoa · 2 = R$ 60–120 · 3 = R$ 120–200 · 4 = acima de R$ 200), `estado`, `cidade`, `bairro`, `status`, `destaque`, `notaMedia`, `totalAvaliacoes`, `somaNotas`, horários, `criadoEm` |
| `resgates.csv` | 66 | um cupom resgatado | `cupomId`, `usuarioId`, `restauranteId`, `desconto`, `status` (ativo/usado), `criadoEm`, `usadoEm`, `validadeFim` |
| `promocoes.csv` | 35 | uma promoção | `restauranteId`, `titulo`, `prato`, `valorPromocional` (texto), dias e horários, `inicio`, `fim` |
| `cupons.csv` | 29 | um cupom | `restauranteId`, `codigo`, `desconto` (texto), validade, `limiteTotal`, `resgatados` |
| `eventos.csv` | 22 | um evento | `restauranteId`, `titulo`, `inicio`, `fim`, `tipoEvento`, `vibes` |
| `favoritos.csv` · `salvos.csv` | 3 · 1 | uma interação | `usuarioId`, `restauranteId`, ids do item, data |

Chaves: `restauranteId` → `restaurantes.id`; `avaliacoes.alvoId` → `restaurantes.id` (alvo = restaurante) ou `menus.id` (alvo = prato); `resgates.cupomId` → `cupons.id`.
