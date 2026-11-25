# Fase 3 — Preparação dos Dados (CRISP-DM)

**Projeto:** Descoberta Gastronômica e Mercado de Alimentação Fora do Lar (GastroMatch)
**Pergunta de negócio:** Quais fatores (experiência/ambiente, tipo de cozinha, faixa de preço e localidade) mais influenciam a avaliação média e a recomendação de estabelecimentos gastronômicos?
**Notebook:** [`notebooks/fase3-preparacao-dados.ipynb`](notebooks/fase3-preparacao-dados.ipynb) · **Código:** [`src/extracao.py`](src/extracao.py)

## Objetivo

O banco do GastroMatch (Cloud Firestore) é NoSQL, orientado a documentos, com listas aninhadas (*arrays*) e coleções técnicas de índice. Nesta fase os registros foram **extraídos sem dados pessoais, normalizados por código, integrados e validados** contra as regras do próprio sistema.

## 3.1 Selecionar (filtrar)

Exportação somente leitura do banco de demonstração `gastromatch-demo` em **25/11/2026**, feita com `scripts/exportar_gastromatch.py`. Os dados são **fictícios**, gerados pelo script de seed do sistema.

| Arquivo (`dados/brutos/`) | Coleção | Registros | Uso |
|---|---|---:|---|
| `firestore_restaurantes.json` | `restaurantes`, **fonte principal** | 188 | Perfil dos estabelecimentos |
| `firestore_avaliacoes.json` | `avaliacoes` | 1.751 | Notas de restaurantes (1.213) e pratos (538) |
| `firestore_menus.json` | `menus` | 748 | Preço e categoria dos pratos |
| `firestore_cupons.json` · `firestore_resgates.json` | `cupons` · `resgates` | 29 · 66 | Conversão de cupom (ativo → usado) |
| `firestore_usuarios.json`, `promocoes`, `eventos`, `salvos`, `favoritos` | demais coleções | 232 · 35 · 22 · 1 · 3 | Contexto (fora da base analítica) |
| `modelo_cardapio.xlsx` | Planilha-modelo de importação em lote | 3 pratos | Validação das regras de cardápio |
| `evidencias/` | Testes e medição de desempenho do sistema | — | Usados na Fase 5 |

**Total exportado: 3.075 registros.** Coleções técnicas de unicidade (`slugs`, `documentos`, `codigosCupom`, `codigosResgate`, `admins`) e a subcoleção privada `usuarios/{uid}/privado` (CPF/CNPJ) **não foram exportadas**. Nome, e-mail, telefone, WhatsApp, endereço, coordenadas e fotos foram removidos, e os IDs de clientes viraram pseudônimos (LGPD).

O relatório setorial da ABRASEL entra só como referência textual, com a fonte citada no README. Os números dele não fazem parte da base analítica.

## 3.2 Limpar (tratar)

| Problema | Tratamento |
|---|---|
| Atributos multivalorados (`vibes` com até 3 itens, `ocasioes` com até 10) | *One-hot encoding*: 8 colunas `vibe_*` e 5 colunas `ocasiao_*`, além da base longa |
| Grafia, acento e caixa (`Japonesa` × `japonesa`) | Comparação por chave normalizada (sem acento, maiúsculas) contra o **vocabulário oficial** (`app/src/lib/catalogo.js`) |
| Experiência gravada como `Cafeteria`, mas exibida como "Cafeteria / Brunch" | O código anterior esperava o rótulo da tela e marcaria as 30 ocorrências como inválidas. Corrigido para o id gravado |
| Lista de cozinhas do código anterior diferente da do sistema (tinha Padaria e Mineira, faltavam Chinesa e Tailandesa) | Substituída pela lista oficial de 20 cozinhas |
| Restaurantes sem avaliação (`totalAvaliacoes == 0`) | `nota_media` vazia (NaN), nunca zero: 11 casos |
| Contas não ativas (`status != "ativo"`) | Filtradas (nenhuma nesta base) |
| Cardápio | Categoria dentro de Entrada / Prato Principal / Sobremesa / Bebida / Acompanhamento e preço entre R$ 0,01 e R$ 100.000 |

**Validação automática** (`dados/processados/log_validacao.csv`):

| Verificação | Resultado |
|---|---:|
| 1. `notaMedia == somaNotas ÷ totalAvaliacoes` (tolerância 10⁻⁴) | **188/188** |
| 2. `totalAvaliacoes` == avaliações contadas na coleção `avaliacoes` | **188/188** |
| Notas fora de 1–5 · preços fora do intervalo · categorias fora do padrão | 0 · 0 · 0 |
| Registros com `restauranteId` inexistente (avaliações, menus, cupons, resgates) | 0 |
| Campos pessoais na base analítica | 0 |
| Vibes e cozinhas fora do vocabulário oficial | 0 |
| **Erros no log** | **0** (15 verificações "ok") |

A planilha-modelo `modelo_cardapio.xlsx` (Bruschetta, Risoto, Petit gâteau) também passa nas regras de categoria e de preço.

## 3.3 Construir (derivar)

| Variável | Definição | Resumo (188 restaurantes) |
|---|---|---|
| `qtd_vibes` | Experiências declaradas (0–3) | 1: 34 · 2: 67 · 3: 87 |
| `preco_medio_cardapio` | Média dos preços dos pratos do restaurante | Média de R$ 59,45 entre restaurantes |
| `preco_mediano_principal` | Mediana dos pratos principais | Comparação com a faixa declarada |
| `taxa_conversao_cupom` | Cupons usados ÷ cupons resgatados | 23 restaurantes com resgate; média de 34% (66 resgates, 27 usados) |
| `nota_media_recalculada` | Média recalculada a partir de `avaliacoes` | Auditoria da verificação 1 |
| `vibe_*`, `ocasiao_*` | *One-hot* | 8 + 5 colunas |

O **score de recomendação** não é derivado aqui. Ele é simulado na Fase 4 com o motor do sistema traduzido para Python (`src/recomendacao.py`).

## 3.4 Integrar (mesclar)

- `restaurantes`, `avaliacoes` (agregadas), `menus` (agregados) e `resgates` (agregados) foram unidos pela chave `restauranteId` numa **tabela analítica única**: `gastromatch_restaurantes.csv`, com 188 linhas e 33 colunas.
- **Base longa de experiências** (`gastromatch_vibes_longa.csv`, 429 linhas): uma linha por par restaurante × vibe, porque um restaurante pode ter até 3.

## Entregáveis da Fase 3

| Arquivo | Conteúdo |
|---|---|
| `dados/processados/gastromatch_analitico.xlsx` | Abas `restaurantes_consolidado`, `por_experiencia`, `avaliacoes_resumo`, `log_validacao` e `dicionario` |
| `dados/processados/gastromatch_restaurantes.csv` | Base consolidada por estabelecimento (188 linhas) |
| `dados/processados/gastromatch_vibes_longa.csv` | Base por par restaurante × experiência (429 linhas) |
| `dados/processados/log_validacao.csv` | Resultado das verificações de integridade |
| `src/extracao.py` | Código reutilizável de extração, normalização e validação |

Para reproduzir: `python src/extracao.py dados/brutos dados/processados` ou execute o notebook `fase3-preparacao-dados.ipynb`.
