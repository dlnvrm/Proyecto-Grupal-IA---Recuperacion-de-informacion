# evaluacion.py

import json
from pathlib import Path
from typing import List, Dict, Tuple

from busqueda import buscar

RUTA_RELEVANCIAS = Path("datos/relevancias.json")

def cargar_relevancias() -> Dict[str, Dict[str, List[str]]]:
    """
    Carga el fichero JSON con las necesidades de información
    y los documentos relevantes.
    """
    with open(RUTA_RELEVANCIAS, "r", encoding="utf-8") as f:
        datos = json.load(f)
    return datos

def average_precision(
    ranking: List[Tuple[str, float]],
    relevantes: List[str]
) -> float:
    """
    Calcula la Average Precision (AP) para una consulta.
    ranking: lista de (id_doc, similitud) ordenada.
    relevantes: lista de ids relevantes.
    """
    relevantes = set(relevantes)
    if not relevantes:
        return 0.0

    num_relevantes_encontrados = 0
    sum_precision = 0.0

    for i, (doc_id, _) in enumerate(ranking, start=1):
        if doc_id in relevantes:
            num_relevantes_encontrados += 1
            precision_en_i = num_relevantes_encontrados / i
            sum_precision += precision_en_i

    if num_relevantes_encontrados == 0:
        return 0.0

    return sum_precision / len(relevantes)

def mean_average_precision(
    vectorizador,
    matriz_tfidf,
    ids_documentos: List[str]
) -> float:
    """
    Calcula el MAP sobre todas las necesidades de información
    definidas en el fichero relevancias.json.
    """
    datos = cargar_relevancias()
    APs = []

    for consulta, info in datos.items():
        relevantes = info["relevantes"]
        ranking = buscar(consulta, vectorizador, matriz_tfidf, ids_documentos)
        ap = average_precision(ranking, relevantes)
        APs.append(ap)

    if not APs:
        return 0.0

    return sum(APs) / len(APs)

def evaluar():
    """
    Calcula el MAP global del sistema TF‑IDF.
    Devuelve un diccionario con el MAP promedio.
    """
    from indexacion import construir_indice
    vectorizador, matriz_tfidf, ids_documentos = construir_indice()

    map_global = mean_average_precision(vectorizador, matriz_tfidf, ids_documentos)

    return {
        "_promedios": {
            "map": map_global
        }
    }

