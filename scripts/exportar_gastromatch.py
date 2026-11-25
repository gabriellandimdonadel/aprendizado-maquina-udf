"""Exporta o Firestore do GastroMatch para CSVs sem dados pessoais (CRISP-DM, Fase 2).

Uso:
    python scripts/exportar_gastromatch.py --chave <chave-de-conta-de-servico.json>
    python scripts/exportar_gastromatch.py --json <exportacao-bruta.json>

- Somente leitura: o script nunca grava no Firebase.
- A chave fica FORA do repositório (nunca faça commit dela).
- Remove nome, e-mail, telefone, WhatsApp, endereço, coordenadas e fotos; os IDs de
  clientes viram pseudônimos (hash). CPF/CNPJ ficam em subcoleções privadas e não são lidos.
- Saída: dados/gastromatch/*.csv
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


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--chave"); g.add_argument("--json")
    a = ap.parse_args()
    bruto = ler_firestore(a.chave) if a.chave else json.load(open(a.json, encoding="utf-8"))
    os.makedirs(SAIDA, exist_ok=True)

    clientes = {d["id"] for d in bruto.get("usuarios", []) if d.get("tipo") != "restaurante"}
    for c in COLECOES:
        df = pd.DataFrame(bruto.get(c, []))
        if df.empty:
            continue
        df = df[[k for k in MANTER[c] if k in df.columns]].copy()
        if c == "usuarios":
            df.loc[df["id"].isin(clientes), "id"] = df.loc[df["id"].isin(clientes), "id"].map(pseudo)
        if "usuarioId" in df.columns:
            df["usuarioId"] = df["usuarioId"].map(pseudo)
        if c in ("avaliacoes", "resgates"):   # o ID do documento contém o uid do cliente
            df["id"] = [f"{c[:3]}_{i:05d}" for i in range(len(df))]
        for col in df.columns:   # listas viram texto separado por "|"
            if df[col].map(lambda v: isinstance(v, list)).any():
                df[col] = df[col].map(lambda v: "|".join(map(str, v)) if isinstance(v, list) else v)
        df.to_csv(os.path.join(SAIDA, f"{c}.csv"), index=False, encoding="utf-8")
        print(f"{c:13s} {len(df):5d} linhas  {df.shape[1]:2d} colunas")


if __name__ == "__main__":
    main()
