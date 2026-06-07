# indexacion.py

import os
from pathlib import Path
import sys
from typing import List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer

RAIZ_REPOSITORIO = Path(__file__).resolve().parents[1]
if str(RAIZ_REPOSITORIO) not in sys.path:
    sys.path.insert(0, str(RAIZ_REPOSITORIO))

from common.corpus import RUTA_DOCUMENTOS, crear_corpus
from common.procesado import preprocesar_texto

def cargar_documentos() -> Tuple[List[str], List[str]]:
    """
    Lee todos los documentos de la carpeta y devuelve:
    - lista_textos: lista de textos originales
    - lista_ids: lista de IDs (por ejemplo, nombres de archivo)
    """
    textos = []
    ids = []

    for nombre in sorted(os.listdir(RUTA_DOCUMENTOS)):
        ruta = RUTA_DOCUMENTOS / nombre
        if ruta.is_file() and nombre.endswith(".txt"):
            with open(ruta, "r", encoding="utf-8") as f:
                texto = f.read()
            textos.append(texto)
            ids.append(nombre)  # puedes usar solo el número si quieres

    return textos, ids

def construir_indice():
    """
    Carga documentos, los preprocesa y construye el vectorizador TF-IDF.
    Devuelve:
    - vectorizador: objeto TfidfVectorizer ya entrenado
    - matriz_tfidf: matriz documentos × términos
    - ids_documentos: lista de IDs de documentos
    """
    crear_corpus()
    textos, ids = cargar_documentos()
    textos_preprocesados = [preprocesar_texto(t) for t in textos]

    vectorizador = TfidfVectorizer()
    matriz_tfidf = vectorizador.fit_transform(textos_preprocesados)

    return vectorizador, matriz_tfidf, ids
