"""
Extração, normalização e validação das coleções do Cloud Firestore
da plataforma GastroMatch.

Fase 3 do CRISP-DM — Preparação dos Dados.

Entrada (dados/brutos/), exportada sem dados pessoais por scripts/exportar_gastromatch.py:
  * firestore_restaurantes.json: estabelecimentos com listas 'vibes' (até 3) e 'ocasioes';
  * firestore_avaliacoes.json: notas inteiras (1 a 5) para restaurantes e pratos;
  * firestore_menus.json: itens do cardápio por estabelecimento;
  * firestore_cupons.json / firestore_resgates.json: cupons e conversões (ativo -> usado).

Verificações (registradas em log_validacao.csv):
  1. notaMedia == somaNotas / totalAvaliacoes (consistência da transação do sistema);
  2. totalAvaliacoes == avaliações contadas na coleção 'avaliacoes';
  3. vibes, cozinha e faixaPreco dentro do vocabulário oficial (app/src/lib/catalogo.js);
  4. ausência de campos pessoais (LGPD) na base analítica;
  5. integridade referencial (restauranteId existente).

Uso:
    python src/extracao.py dados/brutos dados/processados
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# 1. Vocabulário oficial do GastroMatch (app/src/lib/catalogo.js)
#    Atenção: a experiência "Cafeteria" é gravada com esse id; "Cafeteria / Brunch" é só o rótulo da tela.
# ---------------------------------------------------------------------------
VIBES_CANONICAS = ["Romântica", "Alegre", "Tranquila", "Sofisticada", "Familiar", "Descontraída", "Noturna", "Cafeteria"]

COZINHAS_CANONICAS = [
    "Brasileira", "Nordestina", "Churrasco", "Frutos do Mar", "Italiana", "Pizzaria", "Japonesa", "Chinesa",
    "Tailandesa", "Indiana", "Árabe", "Francesa", "Portuguesa", "Mexicana", "Peruana", "Contemporânea",
    "Mediterrânea", "Vegetariana", "Hamburgueria", "Cafeteria",
]

CATEGORIAS_MENU = ["Entrada", "Prato Principal", "Sobremesa", "Bebida", "Acompanhamento"]

# Motor de recomendação (app/src/lib/recomendacao.js)
PESOS_RECOMENDACAO = {"cozinha": 40, "experiencia": 30, "local": 15, "preco": 15}
CORTE_MINIMO_SCORE = 30

CAMPOS_PESSOAIS = {"cpf", "cnpj", "email", "senha", "telefone", "whatsapp", "nome", "nomeResponsavel",
                   "usuarioNome", "usuarioEmail", "nomeExibicao", "endereco", "lat", "lng"}


def _chave(texto: str) -> str:
    """Remove acentos, espaços e pontuação para comparação normalizada."""
    if not isinstance(texto, str):
        return ""
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Z0-9]", "", sem_acento.upper())


_MAPA_VIBES = {_chave(v): v for v in VIBES_CANONICAS}
_MAPA_VIBES[_chave("Cafeteria / Brunch")] = "Cafeteria"
_MAPA_COZINHAS = {_chave(c): c for c in COZINHAS_CANONICAS}


def padronizar_vibe(nome: str) -> str | None:
    """Devolve o nome canônico da experiência (vibe) ou None se inválido."""
    return _MAPA_VIBES.get(_chave(nome))


def padronizar_cozinha(nome: str) -> str | None:
    """Devolve o nome canônico da cozinha ou None se fora do vocabulário."""
    return _MAPA_COZINHAS.get(_chave(nome))


# ---------------------------------------------------------------------------
# 2. Leitura das exportações JSON
# ---------------------------------------------------------------------------
def carregar_json(caminho: Path) -> list[dict]:
    """Lê uma coleção exportada do Cloud Firestore em JSON (lista ou dict por ID)."""
    if not caminho.exists():
        return []
    with open(caminho, encoding="utf-8") as f:
        conteudo = json.load(f)
    if isinstance(conteudo, list):
        return conteudo
    if isinstance(conteudo, dict):
        return [{**dados, "id": dados.get("id", doc_id)} for doc_id, dados in conteudo.items()]
    return []


@dataclass
class BaseExtraida:
    restaurantes: pd.DataFrame
    vibes_longa: pd.DataFrame
    avaliacoes: pd.DataFrame
    menus: pd.DataFrame
    resgates: pd.DataFrame
    log: list[dict] = field(default_factory=list)


def _registrar(log, entidade, rid, tipo, mensagem):
    log.append({"entidade": entidade, "id": rid, "tipo": tipo, "mensagem": mensagem})


# ---------------------------------------------------------------------------
# 3. Normalização, derivação e auditoria
# ---------------------------------------------------------------------------
def processar_colecoes(pasta_brutos: Path) -> BaseExtraida:
    log: list[dict] = []
    brutos = {c: carregar_json(pasta_brutos / f"firestore_{c}.json")
              for c in ["restaurantes", "avaliacoes", "menus", "cupons", "resgates"]}

    # LGPD: nenhum campo pessoal pode chegar à base analítica
    for colecao, docs in brutos.items():
        achados = sorted({k for d in docs for k in d} & CAMPOS_PESSOAIS)
        _registrar(log, colecao, "-", "ERRO_LGPD" if achados else "ok",
                   f"Campos pessoais encontrados: {achados}" if achados else "Nenhum campo pessoal na coleção")

    df_aval = pd.DataFrame(brutos["avaliacoes"])
    df_menu = pd.DataFrame(brutos["menus"])
    df_cup = pd.DataFrame(brutos["cupons"])
    df_resg = pd.DataFrame(brutos["resgates"])
    ids_rest = {d.get("id") for d in brutos["restaurantes"]}

    # Integridade referencial
    for nome, df in [("avaliacoes", df_aval), ("menus", df_menu), ("cupons", df_cup), ("resgates", df_resg)]:
        if not df.empty and "restauranteId" in df.columns:
            orfaos = int((~df["restauranteId"].isin(ids_rest)).sum())
            _registrar(log, nome, "-", "ERRO" if orfaos else "ok", f"{orfaos} registro(s) com restauranteId inexistente")

    # Domínio da nota
    if not df_aval.empty:
        fora = int((~df_aval["nota"].between(1, 5)).sum())
        _registrar(log, "avaliacoes", "-", "ERRO" if fora else "ok", f"{fora} nota(s) fora de 1–5")

    # Agregados por restaurante
    aval_rest = df_aval[df_aval["alvo"] == "restaurante"] if not df_aval.empty else df_aval
    contagem_aval = aval_rest.groupby("alvoId")["nota"].count().to_dict() if not aval_rest.empty else {}
    media_aval = aval_rest.groupby("alvoId")["nota"].mean().to_dict() if not aval_rest.empty else {}
    preco_medio = df_menu.groupby("restauranteId")["preco"].mean().round(2).to_dict() if not df_menu.empty else {}
    preco_mediano_principal = (df_menu[df_menu["categoria"] == "Prato Principal"].groupby("restauranteId")["preco"]
                               .median().round(2).to_dict() if not df_menu.empty else {})
    qtd_itens = df_menu.groupby("restauranteId")["preco"].count().to_dict() if not df_menu.empty else {}
    resg_total = df_resg.groupby("restauranteId").size().to_dict() if not df_resg.empty else {}
    resg_usados = (df_resg[df_resg["status"] == "usado"].groupby("restauranteId").size().to_dict()
                   if not df_resg.empty else {})

    if not df_menu.empty:
        fora_cat = int((~df_menu["categoria"].isin(CATEGORIAS_MENU)).sum())
        _registrar(log, "menus", "-", "aviso" if fora_cat else "ok", f"{fora_cat} prato(s) com categoria fora do padrão")
        fora_preco = int((~df_menu["preco"].between(0.01, 100000)).sum())
        _registrar(log, "menus", "-", "ERRO" if fora_preco else "ok", f"{fora_preco} preço(s) fora de R$ 0,01–100.000")

    linhas_rest, linhas_vibes = [], []
    div_media = div_total = 0
    for doc in brutos["restaurantes"]:
        rid = doc.get("id", "")
        nome = str(doc.get("nomeRestaurante", "")).strip()
        status = doc.get("status", "ativo")
        if status != "ativo":   # apenas estabelecimentos visíveis ao público
            _registrar(log, "restaurantes", rid, "info", f"'{nome}' ignorado (status='{status}')")
            continue

        cozinha = padronizar_cozinha(doc.get("cozinha", ""))
        if cozinha is None:
            _registrar(log, "restaurantes", rid, "aviso", f"Cozinha fora do vocabulário: '{doc.get('cozinha')}'")
            cozinha = str(doc.get("cozinha", "Não informada"))
        faixa = doc.get("faixaPreco")
        if faixa not in (1, 2, 3, 4):
            _registrar(log, "restaurantes", rid, "aviso", f"faixaPreco inválida: {faixa}")

        total = int(doc.get("totalAvaliacoes", 0) or 0)
        soma = float(doc.get("somaNotas", 0) or 0)
        media = float(doc.get("notaMedia", 0) or 0)
        if total > 0 and abs(media - soma / total) > 1e-4:   # verificação 1
            div_media += 1
            _registrar(log, "restaurantes", rid, "ERRO", f"notaMedia {media} ≠ somaNotas/total {soma / total:.4f}")
        if contagem_aval.get(rid, 0) != total:                 # verificação 2
            div_total += 1
            _registrar(log, "restaurantes", rid, "aviso",
                       f"Ficha informa {total} avaliações; coleção tem {contagem_aval.get(rid, 0)}")

        vibes = []
        for v in doc.get("vibes") or []:
            vc = padronizar_vibe(v)
            if vc and vc not in vibes:
                vibes.append(vc)
            elif not vc:
                _registrar(log, "restaurantes", rid, "aviso", f"Vibe fora do vocabulário: '{v}'")
        if len(vibes) > 3:
            _registrar(log, "restaurantes", rid, "aviso", f"{len(vibes)} vibes (máximo 3)")

        usados, resgatados = resg_usados.get(rid, 0), resg_total.get(rid, 0)
        registro = {
            "restaurante_id": rid,
            "nome_restaurante": nome,
            "cozinha": cozinha,
            "faixa_preco": faixa,
            "estado": doc.get("estado", ""),
            "cidade": doc.get("cidade", ""),
            "bairro": doc.get("bairro", ""),
            "destaque": bool(doc.get("destaque", False)),
            "qtd_vibes": len(vibes),
            "vibes_lista": "; ".join(vibes) if vibes else "sem_vibe_declarada",
            "qtd_ocasioes": len(doc.get("ocasioes") or []),
            "total_avaliacoes": total,
            "nota_media": round(media, 4) if total > 0 else None,   # NaN, não zero, quando não há avaliações
            "nota_media_recalculada": round(media_aval[rid], 4) if rid in media_aval else None,
            "qtd_itens_menu": qtd_itens.get(rid, 0),
            "preco_medio_cardapio": preco_medio.get(rid),
            "preco_mediano_principal": preco_mediano_principal.get(rid),
            "cupons_resgatados": resgatados,
            "cupons_usados": usados,
            "taxa_conversao_cupom": round(usados / resgatados, 4) if resgatados else None,
        }
        for v in VIBES_CANONICAS:   # one-hot das 8 experiências
            registro[f"vibe_{_chave(v).lower()}"] = int(v in vibes)
        for o in ["aniversario", "confraternizacao", "dia-dos-namorados", "dia-das-maes", "dia-dos-pais"]:
            registro[f"ocasiao_{o.replace('-', '_')}"] = int(o in (doc.get("ocasioes") or []))
        linhas_rest.append(registro)

        for v in vibes or ["sem_vibe_declarada"]:   # base longa: um registro por par restaurante × vibe
            linhas_vibes.append({k: registro[k] for k in ["restaurante_id", "nome_restaurante", "cozinha", "faixa_preco",
                                                          "cidade", "nota_media", "total_avaliacoes"]} | {"vibe": v})

    df_rest = pd.DataFrame(linhas_rest)
    _registrar(log, "restaurantes", "-", "ok" if div_media == 0 else "ERRO",
               f"Verificação 1 (notaMedia = somaNotas/total): {len(df_rest) - div_media}/{len(df_rest)} válidos")
    _registrar(log, "restaurantes", "-", "ok" if div_total == 0 else "aviso",
               f"Verificação 2 (totalAvaliacoes = avaliações contadas): {len(df_rest) - div_total}/{len(df_rest)} válidos")
    erros = sum(1 for item in log if item["tipo"].startswith("ERRO"))
    _registrar(log, "RESUMO", "-", "ok" if erros == 0 else "ERRO",
               f"{len(df_rest)} restaurantes ativos; {len(df_aval)} avaliações; {len(df_menu)} pratos; "
               f"{len(df_resg)} resgates; {erros} erro(s).")

    return BaseExtraida(df_rest, pd.DataFrame(linhas_vibes), df_aval, df_menu, df_resg, log)


DICIONARIO = [
    ("restaurante_id", "texto", "ID do restaurante no Firestore (UID da conta do restaurante)"),
    ("cozinha", "categoria", "Tipo de cozinha (20 opções oficiais)"),
    ("faixa_preco", "ordinal 1–4", "1 = até R$ 60/pessoa · 2 = R$ 60–120 · 3 = R$ 120–200 · 4 = acima de R$ 200"),
    ("estado / cidade / bairro", "categoria", "Localização declarada"),
    ("destaque", "booleano", "Destaque definido pelo suporte"),
    ("qtd_vibes", "inteiro 0–3", "Número de experiências declaradas"),
    ("vibe_*", "binário", "One-hot de cada uma das 8 experiências"),
    ("ocasiao_*", "binário", "One-hot das 5 ocasiões especiais"),
    ("total_avaliacoes", "inteiro", "Avaliações do restaurante (ficha pública)"),
    ("nota_media", "real 1–5", "Média das notas (vazio quando não há avaliações)"),
    ("nota_media_recalculada", "real 1–5", "Média recalculada a partir da coleção avaliacoes (auditoria)"),
    ("qtd_itens_menu", "inteiro", "Pratos cadastrados"),
    ("preco_medio_cardapio", "R$", "Preço médio de todos os pratos"),
    ("preco_mediano_principal", "R$", "Mediana dos pratos principais"),
    ("cupons_resgatados / cupons_usados", "inteiro", "Resgates de cupom e quantos foram validados no restaurante"),
    ("taxa_conversao_cupom", "proporção", "cupons_usados ÷ cupons_resgatados"),
]


# ---------------------------------------------------------------------------
# 4. Execução principal e exportação
# ---------------------------------------------------------------------------
def main(pasta_brutos: str | Path, pasta_saida: str | Path) -> BaseExtraida:
    dir_brutos, dir_saida = Path(pasta_brutos), Path(pasta_saida)
    dir_saida.mkdir(parents=True, exist_ok=True)

    r = processar_colecoes(dir_brutos)
    df_log = pd.DataFrame(r.log)
    resumo_aval = (r.avaliacoes.groupby(["alvo", "nota"]).size().unstack(fill_value=0)
                   if not r.avaliacoes.empty else pd.DataFrame())
    por_vibe = (r.vibes_longa.groupby("vibe").agg(restaurantes=("restaurante_id", "nunique"),
                                                  nota_media=("nota_media", "mean"),
                                                  avaliacoes=("total_avaliacoes", "sum")).round(3).reset_index())

    r.restaurantes.to_csv(dir_saida / "gastromatch_restaurantes.csv", index=False, encoding="utf-8-sig")
    r.vibes_longa.to_csv(dir_saida / "gastromatch_vibes_longa.csv", index=False, encoding="utf-8-sig")
    df_log.to_csv(dir_saida / "log_validacao.csv", index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(dir_saida / "gastromatch_analitico.xlsx", engine="openpyxl") as w:
        r.restaurantes.to_excel(w, sheet_name="restaurantes_consolidado", index=False)
        por_vibe.to_excel(w, sheet_name="por_experiencia", index=False)
        resumo_aval.to_excel(w, sheet_name="avaliacoes_resumo")
        df_log.to_excel(w, sheet_name="log_validacao", index=False)
        pd.DataFrame(DICIONARIO, columns=["atributo", "tipo", "descrição"]).to_excel(w, sheet_name="dicionario", index=False)

    resumo = df_log[df_log["entidade"].isin(["RESUMO"]) | df_log["tipo"].ne("info")]
    print(resumo[resumo["id"] == "-"].to_string(index=False))
    print(f"\n{len(r.restaurantes)} estabelecimentos consolidados -> {dir_saida / 'gastromatch_restaurantes.csv'}")
    return r


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "dados/brutos",
         sys.argv[2] if len(sys.argv) > 2 else "dados/processados")
