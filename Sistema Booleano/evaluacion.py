# evaluacion.py
#
# Calcula Precisión y Recall del sistema booleano.
#
# ─────────────────────────────────────────────────────────────────
# MÉTRICAS:
#
#   Precisión = Relevantes recuperados / Total recuperados
#   → De lo que el sistema devuelve, ¿cuánto es realmente útil?
#
#   Recall    = Relevantes recuperados / Total relevantes
#   → De todo lo útil que existe, ¿cuánto encontró el sistema?
# ─────────────────────────────────────────────────────────────────
#
# Necesita el fichero: datos/relevancias.json
# Formato:
# {
#   "directores españoles de terror": {
#     "consulta_booleana": "español AND terror",
#     "relevantes": ["4.txt", "9.txt"]
#   }, ...
# }

import json
from pathlib import Path
from typing import Dict, Tuple

from busqueda import buscar

RUTA_RELEVANCIAS = Path("datos/relevancias.json")


def cargar_relevancias() -> dict:
    with open(RUTA_RELEVANCIAS, "r", encoding="utf-8") as f:
        return json.load(f)


def calcular_precision_recall(recuperados: list, relevantes: list) -> Tuple[float, float]:
    rec = set(recuperados)
    rel = set(relevantes)
    vp  = rec & rel  # verdaderos positivos

    precision = len(vp) / len(rec) if rec else 0.0
    recall    = len(vp) / len(rel) if rel else 0.0
    return precision, recall


def evaluar() -> Dict:
    """
    Evalúa el sistema booleano sobre las 20 necesidades de información.
    Devuelve un dict con los resultados por necesidad y los promedios finales.
    """
    datos      = cargar_relevancias()
    resultados = {}
    precisiones, recalls = [], []

    print(f"\n{'Necesidad':<46} {'P':>6}  {'R':>6}  {'VP':>4}  {'Rec':>4}  {'Rel':>4}")
    print("─" * 76)

    for necesidad, info in datos.items():
        # Compatibilidad: aceptar dos formatos de relevancias.json
        # - formato antiguo: contiene 'consulta_booleana' y 'relevantes'
        # - formato simplificado: solo contiene 'relevantes'
        if "consulta_booleana" in info:
            consulta = info["consulta_booleana"]
        else:
            # Derivar una consulta booleana sencilla a partir del texto
            # de la necesidad: tomar palabras relevantes (>2) y unir con AND.
            import re
            tokens = re.findall(r"[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]+", necesidad.lower())
            tokens = [t for t in tokens if len(t) > 2]
            consulta = " AND ".join(tokens) if tokens else necesidad
        relevantes = info["relevantes"]

        recuperados = buscar(consulta)
        p, r        = calcular_precision_recall(recuperados, relevantes)

        precisiones.append(p)
        recalls.append(r)

        vp = len(set(recuperados) & set(relevantes))
        print(f"{necesidad[:45]:<46} {p:>6.3f}  {r:>6.3f}  "
              f"{vp:>4}  {len(recuperados):>4}  {len(relevantes):>4}")

        resultados[necesidad] = {
            "consulta_booleana":    consulta,
            "recuperados":          recuperados,
            "verdaderos_positivos": vp,
            "precision":            round(p, 4),
            "recall":               round(r, 4),
        }

    p_media = sum(precisiones) / len(precisiones) if precisiones else 0.0
    r_medio = sum(recalls)     / len(recalls)     if recalls     else 0.0

    print("─" * 76)
    print(f"{'PROMEDIO':<46} {p_media:>6.3f}  {r_medio:>6.3f}")

    resultados["_promedios"] = {
        "precision_media": round(p_media, 4),
        "recall_medio":    round(r_medio, 4),
    }
    return resultados
