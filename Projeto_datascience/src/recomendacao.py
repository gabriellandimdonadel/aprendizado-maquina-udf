"""Motor de recomendação do GastroMatch portado de app/src/lib/recomendacao.js (mesmas regras e pesos).

Usado na Fase 4 para simular buscas e medir como os pesos fixos (40/30/15/15) e o corte de 30
pontos afetam quais restaurantes aparecem. A versão em JavaScript continua sendo a referência.
"""
from __future__ import annotations

import math

PESOS = {"cozinha": 40, "experiencia": 30, "local": 15, "preco": 15}
PONTUACAO_MINIMA = 30


def avaliar(r: dict, pref: dict) -> int:
    """Pontuação 0–100 de um restaurante para uma preferência (função avaliar do JS)."""
    pontos = 0.0
    # 1. Cozinha
    if pref.get("cozinha"):
        if r["cozinha"] == pref["cozinha"]:
            pontos += PESOS["cozinha"]
    else:
        pontos += PESOS["cozinha"] / 2
    # 2. Experiência: proporcional às experiências pedidas que o restaurante oferece
    pedidas = pref.get("experiencias") or []
    if pedidas:
        comuns = [e for e in pedidas if e in r["experiencias"]]
        pontos += PESOS["experiencia"] * len(comuns) / len(pedidas)
    else:
        pontos += PESOS["experiencia"] / 2
    # 3. Local: mesmo bairro vale tudo; outro bairro vale metade; sem bairro pedido vale tudo
    if pref.get("bairro"):
        pontos += PESOS["local"] if r["bairro"] == pref["bairro"] else PESOS["local"] / 2
    else:
        pontos += PESOS["local"]
    # 4. Preço: faixa exata vale tudo; vizinha vale um terço
    if pref.get("preco") and r.get("faixaPreco"):
        dif = abs(r["faixaPreco"] - pref["preco"])
        pontos += PESOS["preco"] if dif == 0 else PESOS["preco"] / 3 if dif == 1 else 0
    else:
        pontos += PESOS["preco"]
    return math.floor(pontos + 0.5)   # igual ao Math.round do JS (,5 sobe; o round() do Python iria para o par)


def _ordenar(lista, pref):
    av = [(r, avaliar(r, pref)) for r in lista]
    av = [x for x in av if x[1] >= PONTUACAO_MINIMA]
    return sorted(av, key=lambda x: (-x[1], -(x[0].get("notaMedia") or 0)))


def recomendar(restaurantes: list[dict], pref: dict, limite: int = 5):
    """Retorna (itens, situacao) como recomendarComSituacao do JS (sem geolocalização)."""
    na_cidade = [r for r in restaurantes if r["cidade"] == pref["cidade"]] if pref.get("cidade") else restaurantes
    if pref.get("cozinha"):
        mesma = [r for r in na_cidade if r["cozinha"] == pref["cozinha"]]
        if mesma:
            return _ordenar(mesma, pref)[:limite], "normal"
        outras = [r for r in restaurantes if r["cozinha"] == pref["cozinha"]]
        if pref.get("cidade") and outras:
            return _ordenar(outras, {**pref, "cidade": "", "bairro": ""})[:limite], "cozinha-em-outra-cidade"
        itens = _ordenar(na_cidade, {**pref, "cozinha": ""})[:limite]
        return itens, "sem-cozinha" if itens else "vazio"
    itens = _ordenar(na_cidade, pref)[:limite]
    return itens, "normal" if itens else "vazio"
