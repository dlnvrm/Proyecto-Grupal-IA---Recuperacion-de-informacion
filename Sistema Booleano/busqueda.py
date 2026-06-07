# busqueda.py
#
# Función de búsqueda booleana usando el índice Whoosh.
#
# Sintaxis soportada (operadores en MAYÚSCULAS):
#   AND  → ambos términos deben aparecer      "espanol AND terror"
#   OR   → al menos uno debe aparecer         "animacion OR anime"
#   NOT  → el término NO debe aparecer        "coreano NOT comedia"
#   ()   → agrupar condiciones                "oscar AND (espanol OR mexicano)"

import re
import unicodedata
from typing import List
from whoosh.qparser import QueryParser

from indexacion import abrir_indice


def _quitar_acentos(texto: str) -> str:
    """Elimina tildes y diacríticos: español → espanol, animación → animacion."""
    texto = unicodedata.normalize('NFD', texto)
    return ''.join(c for c in texto if unicodedata.category(c) != 'Mn')


def normalizar_consulta_booleana(consulta: str) -> str:
    """
    Normaliza los términos de la consulta para que coincidan con los tokens
    del índice (que fueron preprocesados con quitar_acentos + lower).
    Los operadores AND/OR/NOT y los paréntesis se conservan intactos.
    """
    tokens = re.findall(r'\(|\)|\bAND\b|\bOR\b|\bNOT\b|[^\s()]+', consulta, flags=re.IGNORECASE)
    normalizados = []
    for token in tokens:
        token_upper = token.upper()
        if token_upper in {'AND', 'OR', 'NOT'}:
            normalizados.append(token_upper)
        elif token in {'(', ')'}:
            normalizados.append(token)
        else:
            # Aplicar EXACTAMENTE la misma normalización que common/procesado.py:
            # 1. minúsculas  2. quitar acentos
            normalizados.append(_quitar_acentos(token.lower()))
    return ' '.join(normalizados)


def buscar(consulta: str) -> List[str]:
    """
    Ejecuta una consulta booleana y devuelve la lista de IDs de documentos
    que cumplen la condición.

    Parámetros:
        consulta : cadena con la consulta booleana (acentos opcionales)
                   Ejemplos:
                     "español AND terror"   o   "espanol AND terror"
                     "animación OR anime"   o   "animacion OR anime"
                     "coreano NOT comedia"
                     "oscar AND (español OR mexicano)"

    Retorna:
        Lista de nombres de archivo encontrados, ej: ["1.txt", "3.txt"]
        Lista vacía si no hay resultados.
    """
    ix = abrir_indice()
    consulta_norm = normalizar_consulta_booleana(consulta)

    with ix.searcher() as searcher:
        parser     = QueryParser('contenido', ix.schema)
        query      = parser.parse(consulta_norm)
        hits       = searcher.search(query, limit=None)
        resultados = [hit['id'] for hit in hits]

    return resultados
