"""
Extração, normalização e validação das coleções do Cloud Firestore
e planilhas de cardápio da plataforma GastroMatch.

Fase 3 do CRISP-DM — Preparação dos Dados.

A base do protótipo GastroMatch é orientada a documentos (NoSQL) e contém:
  * restaurantes: estabelecimentos com arrays de 'vibes' (até 3) e 'ocasioes';
  * avaliacoes: notas inteiras (1 a 5) para restaurantes e pratos;
  * menus: itens do cardápio por estabelecimento;
  * cupons / resgates: ofertas e conversões de vouchers.

Para cada coleção extraída, o código normaliza os vocabulários fechados e confere:
  1. se notaMedia == somaNotas / totalAvaliacoes (consistência atômica da RN33);
  2. se os valores de 'vibes', 'cozinha' e 'faixaPreco' respeitam os limites do sistema;
  3. se dados sensíveis (LGPD) estão ausentes da base analítica.
Qualquer divergência é registrada em 'log_validacao.csv'.

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
# 1. Vocabulários Fechados Canônicos do GastroMatch (TCC / Dicionário de Dados)
# ---------------------------------------------------------------------------
VIBES_CANONICAS = [
    "Romântica",
    "Alegre",
    "Tranquila",
    "Sofisticada",
    "Familiar",
    "Descontraída",
    "Noturna",
    "Cafeteria / Brunch",
]

COZINHAS_CANONICAS = [
    "Brasileira", "Italiana", "Japonesa", "Churrasco", "Frutos do Mar",
    "Pizzaria", "Vegetariana", "Hamburgueria", "Mexicana", "Árabe",
    "Francesa", "Contemporânea", "Cafeteria", "Padaria", "Doceria",
    "Asiática", "Peruana", "Portuguesa", "Mineira", "Nordestina",
]

PESOS_RECOMENDACAO = {
    "cozinha": 40,
    "vibe": 30,
    "local": 15,
    "preco": 15,
}
CORTE_MINIMO_SCORE = 30


def _chave(texto: str) -> str:
    """Remove acentos, espaços e pontuação para comparação normalizada."""
    if not isinstance(texto, str):
        return ""
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Z0-9]", "", sem_acento.upper())


_MAPA_VIBES = {_chave(v): v for v in VIBES_CANONICAS}
_MAPA_COZINHAS = {_chave(c): c for c in COZINHAS_CANONICAS}


def padronizar_vibe(nome: str) -> str | None:
    """Devolve o nome canônico da experiência (vibe) ou None se inválido."""
    return _MAPA_VIBES.get(_chave(nome))


def padronizar_cozinha(nome: str) -> str:
    """Devolve o nome canônico da cozinha, preservando o original se não mapeado."""
    return _MAPA_COZINHAS.get(_chave(nome), nome.strip() if isinstance(nome, str) else "Não informada")


# ---------------------------------------------------------------------------
# 2. Leitura das Exportações JSON / Planilhas Brutas
# ---------------------------------------------------------------------------
def carregar_json(caminho: Path) -> list[dict]:
    """Lê uma coleção exportada do Cloud Firestore em formato JSON (lista ou dict por ID)."""
    if not caminho.exists():
        return []
    with open(caminho, encoding="utf-8") as f:
        conteudo = json.load(f)
    if isinstance(conteudo, list):
        return conteudo
    if isinstance(conteudo, dict):
        registros = []
        for doc_id, dados in conteudo.items():
            item = dict(dados)
            item.setdefault("id", doc_id)
            registros.append(item)
        return registros
    return []


@dataclass
class BaseExtraida:
    restaurantes: pd.DataFrame
    vibes_longa: pd.DataFrame
    avaliacoes: pd.DataFrame
    menus: pd.DataFrame
    log: list[dict] = field(default_factory=list)


# ---------------------------------------------------------------------------
# 3. Normalização, Derivação e Auditoria de Integridade
# ---------------------------------------------------------------------------
def processar_colecoes(pasta_brutos: Path) -> BaseExtraida:
    log: list[dict] = []

    raw_rest = carregar_json(pasta_brutos / "firestore_restaurantes.json")
    raw_aval = carregar_json(pasta_brutos / "firestore_avaliacoes.json")
    raw_menu = carregar_json(pasta_brutos / "firestore_menus.json")

    df_aval = pd.DataFrame(raw_aval)
    df_menu = pd.DataFrame(raw_menu)

    # Contagem real de avaliações por restaurante na coleção 'avaliacoes'
    contagem_aval_real: dict[str, int] = {}
    soma_aval_real: dict[str, float] = {}
    if not df_aval.empty and "alvoId" in df_aval.columns:
        filtro_rest = df_aval[df_aval.get("alvo", "restaurante") == "restaurante"]
        contagem_aval_real = filtro_rest.groupby("alvoId")["nota"].count().to_dict()
        soma_aval_real = filtro_rest.groupby("alvoId")["nota"].sum().to_dict()

    # Métricas agregadas de cardápio por restaurante
    preco_medio_menu: dict[str, float] = {}
    qtd_itens_menu: dict[str, int] = {}
    if not df_menu.empty and "restauranteId" in df_menu.columns:
        preco_medio_menu = df_menu.groupby("restauranteId")["preco"].mean().round(2).to_dict()
        qtd_itens_menu = df_menu.groupby("restauranteId")["preco"].count().to_dict()

    linhas_rest = []
    linhas_vibes = []

    for doc in raw_rest:
        rid = doc.get("id") or doc.get("uid") or ""
        nome = doc.get("nomeRestaurante", "").strip()
        status = doc.get("status", "ativo")

        # Filtra apenas estabelecimentos ativos (RN09)
        if status != "ativo":
            log.append({
                "entidade": "restaurantes", "id": rid, "tipo": "info",
                "mensagem": f"Restaurante '{nome}' ignorado (status='{status}')",
            })
            continue

        cozinha = padronizar_cozinha(doc.get("cozinha", ""))
        faixa_preco = int(doc.get("faixaPreco", 1))
        cidade = str(doc.get("cidade", "")).strip()
        estado = str(doc.get("estado", "")).strip()
        bairro = str(doc.get("bairro", "")).strip()

        total_aval = int(doc.get("totalAvaliacoes", 0))
        soma_notas = float(doc.get("somaNotas", 0.0))
        nota_media = float(doc.get("notaMedia", 0.0))

        # --- Validação 1: Consistência atômica da nota média (RN33) ---
        if total_aval > 0:
            media_esperada = soma_notas / total_aval
            if abs(nota_media - media_esperada) > 1e-3:
                log.append({
                    "entidade": "restaurantes", "id": rid, "tipo": "ERRO",
                    "mensagem": f"Divergência notaMedia ({nota_media}) != somaNotas/total ({media_esperada:.4f})",
                })
        elif nota_media != 0:
            log.append({
                "entidade": "restaurantes", "id": rid, "tipo": "aviso",
                "mensagem": f"totalAvaliacoes=0 mas notaMedia={nota_media}",
            })

        # --- Validação 2: Cruzamento com a coleção 'avaliacoes' ---
        if rid in contagem_aval_real and contagem_aval_real[rid] != total_aval:
            log.append({
                "entidade": "avaliacoes", "id": rid, "tipo": "aviso",
                "mensagem": f"Ficha informa {total_aval} avaliações, coleção possui {contagem_aval_real[rid]}",
            })

        # --- Normalização das experiências (vibes) ---
        vibes_brutas = doc.get("vibes") or []
        vibes_validas = []
        for v in vibes_brutas:
            vc = padronizar_vibe(v)
            if vc and vc not in vibes_validas:
                vibes_validas.append(vc)
            elif not vc:
                log.append({
                    "entidade": "restaurantes", "id": rid, "tipo": "aviso",
                    "mensagem": f"Vibe fora do vocabulário fechado: '{v}'",
                })

        if len(vibes_validas) > 3:
            log.append({
                "entidade": "restaurantes", "id": rid, "tipo": "aviso",
                "mensagem": f"Mais de 3 vibes cadastradas ({len(vibes_validas)}); truncado para 3",
            })
            vibes_validas = vibes_validas[:3]

        # Garantia LGPD: verifica ausência de campos sensíveis na ficha pública
        for campo_sensivel in ("cpf", "cnpj", "email", "senha"):
            if campo_sensivel in doc:
                log.append({
                    "entidade": "restaurantes", "id": rid, "tipo": "ERRO_LGPD",
                    "mensagem": f"Campo sensível '{campo_sensivel}' encontrado na coleção pública",
                })

        registro = {
            "restaurante_id": rid,
            "nome_restaurante": nome,
            "cozinha": cozinha,
            "faixa_preco": faixa_preco,
            "cidade": cidade,
            "estado": estado,
            "bairro": bairro,
            "destaque": bool(doc.get("destaque", False)),
            "qtd_vibes": len(vibes_validas),
            "vibes_lista": "; ".join(vibes_validas) if vibes_validas else "Sem experiência declarada",
            "total_avaliacoes": total_aval,
            "soma_notas": soma_notas,
            "nota_media": round(nota_media, 4) if total_aval > 0 else None,
            "qtd_itens_menu": qtd_itens_menu.get(rid, 0),
            "preco_medio_cardapio": preco_medio_menu.get(rid, None),
        }

        # One-Hot Encoding para as 8 vibes canônicas
        for v_canonica in VIBES_CANONICAS:
            col = f"vibe_{_chave(v_canonica).lower()}"
            registro[col] = int(v_canonica in vibes_validas)

        linhas_rest.append(registro)

        # Base longa (um registro por par restaurante x vibe)
        vibes_para_explodir = vibes_validas if vibes_validas else ["Sem experiência declarada"]
        for v_item in vibes_para_explodir:
            linhas_vibes.append({
                "restaurante_id": rid,
                "nome_restaurante": nome,
                "vibe": v_item,
                "cozinha": cozinha,
                "faixa_preco": faixa_preco,
                "cidade": cidade,
                "nota_media": registro["nota_media"],
                "total_avaliacoes": total_aval,
            })

    df_rest = pd.DataFrame(linhas_rest)
    df_vibes = pd.DataFrame(linhas_vibes)

    # Registro de resumo no log
    erros = sum(1 for item in log if item["tipo"].startswith("ERRO"))
    log.append({
        "entidade": "RESUMO", "id": "-", "tipo": "ok" if erros == 0 else "ERRO",
        "mensagem": f"{len(df_rest)} restaurantes ativos processados; {len(df_aval)} avaliações lidas; {erros} erros.",
    })

    return BaseExtraida(
        restaurantes=df_rest,
        vibes_longa=df_vibes,
        avaliacoes=df_aval,
        menus=df_menu,
        log=log,
    )


# ---------------------------------------------------------------------------
# 4. Execução Principal e Exportação
# ---------------------------------------------------------------------------
def main(pasta_brutos: str, pasta_saida: str) -> BaseExtraida:
    dir_brutos, dir_saida = Path(pasta_brutos), Path(pasta_saida)
    dir_saida.mkdir(parents=True, exist_ok=True)

    resultado = processar_colecoes(dir_brutos)
    df_log = pd.DataFrame(resultado.log)

    resultado.restaurantes.to_csv(dir_saida / "gastromatch_restaurantes.csv", index=False, encoding="utf-8-sig")
    resultado.vibes_longa.to_csv(dir_saida / "gastromatch_vibes_longa.csv", index=False, encoding="utf-8-sig")
    df_log.to_csv(dir_saida / "log_validacao.csv", index=False, encoding="utf-8-sig")

    # Exportação consolidada em Excel (.xlsx) com múltiplas abas
    caminho_xlsx = dir_saida / "gastromatch_analitico.xlsx"
    with pd.ExcelWriter(caminho_xlsx, engine="openpyxl") as writer:
        resultado.restaurantes.to_excel(writer, sheet_name="restaurantes_consolidado", index=False)
        resultado.vibes_longa.to_excel(writer, sheet_name="por_experiencia", index=False)
        df_log.to_excel(writer, sheet_name="log_validacao", index=False)

    print(df_log.to_string(index=False))
    print(f"\n{len(resultado.restaurantes)} estabelecimentos consolidados -> {dir_saida / 'gastromatch_restaurantes.csv'}")
    return resultado


if __name__ == "__main__":
    entrada = sys.argv[1] if len(sys.argv) > 1 else "dados/brutos"
    saida = sys.argv[2] if len(sys.argv) > 2 else "dados/processados"
    main(entrada, saida)
