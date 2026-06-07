# indexacion.py
#
# Construye el índice invertido con Whoosh.
#
# ¿Qué es un índice invertido?
#   Guarda "término → documentos que lo contienen".
#   Ejemplo:
#     "terror"    → {4.txt, 9.txt, 59.txt}
#     "español"   → {1.txt, 2.txt, 3.txt, 4.txt}
#     "terror AND español" → intersección = {4.txt}
#
# Whoosh construye y guarda este índice en disco (carpeta indice/).

import os
from pathlib import Path
import sys

from whoosh import index
from whoosh.fields import Schema, TEXT, ID
# 1. CAMBIO AQUÍ: Importamos SpaceSeparatedTokenizer en lugar de StandardAnalyzer
from whoosh.analysis import SpaceSeparatedTokenizer

RAIZ_REPOSITORIO = Path(__file__).resolve().parents[1]
if str(RAIZ_REPOSITORIO) not in sys.path:
    sys.path.insert(0, str(RAIZ_REPOSITORIO))

from common.corpus import RUTA_DOCUMENTOS, crear_corpus
from common.procesado import preprocesar_texto

BASE            = Path(os.path.dirname(os.path.abspath(__file__)))
CARPETA_INDICE  = BASE / "indice"

# 2. CAMBIO AQUÍ: Le indicamos al esquema que respete vuestra lista de tokens limpios
SCHEMA = Schema(
    id       = ID(stored=True),
    contenido= TEXT(stored=False, analyzer=SpaceSeparatedTokenizer()) # ← Tu limpiador manda
)


def construir_indice() -> None:
    """
    Lee todos los .txt de datos/documentos/, los preprocesa y los indexa.
    Guarda el índice en la carpeta indice/.
    """
    crear_corpus()
    CARPETA_INDICE.mkdir(exist_ok=True)

    ix     = index.create_in(str(CARPETA_INDICE), SCHEMA)
    writer = ix.writer()

    archivos = sorted(
        f for f in RUTA_DOCUMENTOS.iterdir()
        if f.suffix == ".txt" and f.stat().st_size > 0
    )

    for ruta in archivos:
        texto_prep = preprocesar_texto(ruta.read_text(encoding="utf-8"))
        writer.add_document(id=ruta.name, contenido=texto_prep)

    writer.commit()
    print(f"   ✓  Índice creado: {len(archivos)} documentos → '{CARPETA_INDICE.name}/'")


def abrir_indice():
    """Abre el índice ya creado en disco."""
    if not CARPETA_INDICE.exists():
        raise FileNotFoundError(
            f"No se encuentra '{CARPETA_INDICE}'.\n"
            "Ejecuta primero construir_indice()."
        )
    return index.open_dir(str(CARPETA_INDICE))