"""Exporta o Firestore do GastroMatch para CSVs sem dados pessoais (CRISP-DM, Fase 2).

Uso:
    python scripts/exportar_gastromatch.py --chave <chave-de-conta-de-servico.json>
    python scripts/exportar_gastromatch.py --json <exportacao-bruta.json>

- Somente leitura: o script nunca grava no Firebase.
- A chave fica FORA do repositório (nunca faça commit dela).
- Remove nome, e-mail, telefone, WhatsApp, endereço, coordenadas e fotos; os IDs de
  clientes viram pseudônimos (hash). CPF/CNPJ ficam em subcoleções privadas e não são lidos.
- Saída: dados/gastromatch/*.csv (e, com --json-destino, firestore_<colecao>.json)
"""
import argparse, datetime, hashlib, json, os
import pandas as pd

SAIDA = os.path.join(os.path.dirname(__file__), "..", "dados", "gastromatch")
COLECOES = ["usuarios", "restaurantes", "avaliacoes", "menus", "cupons", "resgates", "promocoes", "eventos", "salvos", "favoritos"]

# campos mantidos por coleção (tudo o que não está aqui é descartado)
MANTER = {
    "usuarios": ["id", "tipo", "status", "criadoEm"],
    "restaurantes": ["id", "slug", "nomeRestaurante", "cozinha", "vibes", "ocasioes", "faixaPreco", "estado", "cidade", "bairro",
                     "status", "destaque", "notaMedia", "totalAvaliacoes", "somaNotas", "diasSemana", "inicioSemana", "fimSemana",
                     "diasFim", "inicioFds", "fimFds", "criadoEm"],
    "avaliacoes": ["id", "alvo", "alvoId", "restauranteId", "usuarioId", "nota", "comentario", "tituloPrato", "criadoEm", "atualizadoEm"],
    "menus": ["id", "restauranteId", "cozinha", "categoria", "titulo", "preco", "criadoEm"],
    "cupons": ["id", "restauranteId", "codigo", "desconto", "validadeInicio", "validadeFim", "horaInicio", "horaFim", "diasValidos",
               "limiteTotal", "resgatados", "promocaoId", "criadoEm"],
    "resgates": ["id", "cupomId", "usuarioId", "restauranteId", "desconto", "status", "criadoEm", "usadoEm", "validadeFim"],
    "promocoes": ["id", "restauranteId", "cozinha", "titulo", "prato", "valorPromocional", "evento", "diasValidos", "horaInicio",
                  "horaFim", "inicio", "fim", "criadoEm", "encerradaEm"],
    "eventos": ["id", "restauranteId", "cozinha", "titulo", "inicio", "fim", "diasValidos", "horaInicio", "horaFim", "tipoEvento",
                "vibes", "criadoEm"],
    "salvos": ["id", "usuarioId", "promocaoId", "eventoId", "restauranteId", "dataResgate"],
    "favoritos": ["id", "usuarioId", "restauranteId", "criadoEm"],
}


def pseudo(uid):
    return "u_" + hashlib.sha256(str(uid).encode()).hexdigest()[:12] if uid else uid


def ler_firestore(chave):
    import firebase_admin
    from firebase_admin import credentials, firestore
    firebase_admin.initialize_app(credentials.Certificate(chave))
    db = firestore.client()

    def conv(v):
        if isinstance(v, datetime.datetime): return v.isoformat()
        if isinstance(v, dict): return {k: conv(x) for k, x in v.items()}
        if isinstance(v, list): return [conv(x) for x in v]
        return v
    return {c: [{"id": d.id, **conv(d.to_dict())} for d in db.collection(c).stream()] for c in COLECOES}


def sanitizar(c, docs, clientes):
    """Mantém só os campos permitidos, pseudonimiza clientes e preserva listas."""
    saida = []
    for i, d in enumerate(docs):
        x = {k: d[k] for k in MANTER[c] if k in d}
        if c == "usuarios" and x.get("id") in clientes:
            x["id"] = pseudo(x["id"])
        if "usuarioId" in x:
            x["usuarioId"] = pseudo(x["usuarioId"])
        if c in ("avaliacoes", "resgates"):   # o ID do documento contém o uid do cliente
            x["id"] = f"{c[:3]}_{i:05d}"
        saida.append(x)
    return saida


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--chave"); g.add_argument("--json")
    ap.add_argument("--json-destino", help="também grava firestore_<colecao>.json (listas preservadas) nesta pasta")
    a = ap.parse_args()
    bruto = ler_firestore(a.chave) if a.chave else json.load(open(a.json, encoding="utf-8"))
    os.makedirs(SAIDA, exist_ok=True)
    if a.json_destino:
        os.makedirs(a.json_destino, exist_ok=True)

    clientes = {d["id"] for d in bruto.get("usuarios", []) if d.get("tipo") != "restaurante"}
    for c in COLECOES:
        docs = sanitizar(c, bruto.get(c, []), clientes)
        if not docs:
            continue
        if a.json_destino:
            with open(os.path.join(a.json_destino, f"firestore_{c}.json"), "w", encoding="utf-8") as f:
                json.dump(docs, f, ensure_ascii=False, indent=1)
        df = pd.DataFrame(docs)
        df = df[[k for k in MANTER[c] if k in df.columns]]   # ordem estável das colunas
        for col in df.columns:   # listas viram texto separado por "|"
            if df[col].map(lambda v: isinstance(v, list)).any():
                df[col] = df[col].map(lambda v: "|".join(map(str, v)) if isinstance(v, list) else v)
        df.to_csv(os.path.join(SAIDA, f"{c}.csv"), index=False, encoding="utf-8")
        print(f"{c:13s} {len(df):5d} linhas  {df.shape[1]:2d} colunas")


if __name__ == "__main__":
    main()
