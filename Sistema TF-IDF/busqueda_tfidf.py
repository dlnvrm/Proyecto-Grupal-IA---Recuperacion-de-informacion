# busqueda_tfidf.py
#
# Búsqueda en texto libre usando TF‑IDF + similitud del coseno

from pathlib import Path
import sys

import numpy as np
from facetas_consulta import bonificacion_por_facetas

RAIZ_REPOSITORIO = Path(__file__).resolve().parents[1]
if str(RAIZ_REPOSITORIO) not in sys.path:
    sys.path.insert(0, str(RAIZ_REPOSITORIO))

from common.procesado import preprocesar_texto


def buscar_tfidf(consulta, vectorizador, matriz_tfidf, ids_documentos):
    """
    Devuelve una lista de (doc_id, score) ordenada por similitud.
    """

    # Preprocesar la consulta igual que los documentos
    consulta_proc = preprocesar_texto(consulta)

    # Vectorizar la consulta
    vector_q = vectorizador.transform([consulta_proc])

    # Calcular similitud del coseno
    # cos = (A·B) / (|A||B|)
    numerador = matriz_tfidf.dot(vector_q.T).toarray().ravel()
    norma_docs = np.linalg.norm(matriz_tfidf.toarray(), axis=1)
    norma_q = np.linalg.norm(vector_q.toarray())

    # Evitar división por cero
    similitudes = numerador / (norma_docs * norma_q + 1e-10)

    bonificaciones = np.array(
        [bonificacion_por_facetas(consulta, doc_id) for doc_id in ids_documentos],
        dtype=float,
    )
    similitudes = similitudes + bonificaciones

    # Ordenar de mayor a menor
    ranking = sorted(
        zip(ids_documentos, similitudes),
        key=lambda x: x[1],
        reverse=True
    )

    return ranking
