from functools import lru_cache
from pathlib import Path
import re
import unicodedata


RUTA_DOCUMENTOS = Path(__file__).resolve().parent / "datos" / "documentos"


FACETAS = {
    "mexico": {
        "consulta": ("mexican", "mexicano", "mexicana", "mexicanos", "mexicanas"),
        "documento": ("mexicano", "mexicana", "mexicanos", "mexicanas", "nacionalizado mexicano", "nacionalizada mexicana", "cine mexicano"),
        "peso": 0.35,
    },
    "espana": {
        "consulta": ("espanol", "espanola", "espanoles", "espanolas", "espana"),
        "documento": ("espanol", "espanola", "espanoles", "espanolas", "cine espanol"),
        "peso": 0.32,
    },
    "estados_unidos": {
        "consulta": ("estadounidense", "estadounidenses", "americano", "americana", "americanos", "americanas", "norteamericano", "norteamericana"),
        "documento": ("estadounidense", "estadounidenses", "americano", "americana", "americanos", "americanas", "de estados unidos"),
        "peso": 0.30,
    },
    "japon": {
        "consulta": ("japones", "japonesa", "japoneses", "japonesas", "japon"),
        "documento": ("japones", "japonesa", "japoneses", "japonesas", "cine japones", "anime"),
        "peso": 0.32,
    },
    "corea": {
        "consulta": ("coreano", "coreana", "coreanos", "coreanas", "corea"),
        "documento": ("coreano", "coreana", "coreanos", "coreanas", "corea del sur", "cine coreano"),
        "peso": 0.32,
    },
    "francia": {
        "consulta": ("frances", "francesa", "franceses", "francesas", "francia"),
        "documento": ("frances", "francesa", "franceses", "francesas", "cine frances"),
        "peso": 0.28,
    },
    "italia": {
        "consulta": ("italiano", "italiana", "italianos", "italianas", "italia"),
        "documento": ("italiano", "italiana", "italianos", "italianas", "cine italiano"),
        "peso": 0.28,
    },
    "reino_unido": {
        "consulta": ("britanico", "britanica", "britanicos", "britanicas", "ingles", "inglesa", "inglaterra", "reino unido"),
        "documento": ("britanico", "britanica", "britanicos", "britanicas", "ingles", "inglesa", "inglaterra", "reino unido"),
        "peso": 0.28,
    },
    "latinoamerica": {
        "consulta": ("latinoamericano", "latinoamericana", "latinoamericanos", "latinoamericanas", "latinoamerica"),
        "documento": (
            "mexicano", "mexicana", "mexicanos", "mexicanas",
            "chileno", "chilena", "chilenos", "chilenas",
            "argentino", "argentina", "argentinos", "argentinas",
            "brasileno", "brasilena", "brasilenos", "brasilenas",
            "colombiano", "colombiana", "colombianos", "colombianas",
            "peruano", "peruana", "peruanos", "peruanas",
            "uruguayo", "uruguaya", "uruguayos", "uruguayas",
            "venezolano", "venezolana", "venezolanos", "venezolanas",
        ),
        "peso": 0.20,
    },
    "europa": {
        "consulta": ("europeo", "europea", "europeos", "europeas", "europa"),
        "documento": (
            "espanol", "espanola", "espanoles", "espanolas",
            "frances", "francesa", "franceses", "francesas",
            "italiano", "italiana", "italianos", "italianas",
            "britanico", "britanica", "britanicos", "britanicas",
            "ingles", "inglesa", "ingleses", "inglesas",
            "danes", "danesa", "daneses", "danesas",
            "austriaco", "austriaca", "austriacos", "austriacas",
            "griego", "griega", "griegos", "griegas",
            "portugues", "portuguesa", "portugueses", "portuguesas",
            "aleman", "alemana", "alemanes", "alemanas",
            "sueco", "sueca", "suecos", "suecas",
            "noruego", "noruega", "noruegos", "noruegas",
            "irlandes", "irlandesa", "irlandeses", "irlandesas",
            "finlandes", "finlandesa", "finlandeses", "finlandesas",
            "holandes", "holandesa", "holandeses", "holandesas",
            "belga", "belgas",
            "suizo", "suiza", "suizos", "suizas",
        ),
        "peso": 0.18,
    },
    "terror": {
        "consulta": ("terror", "horror", "suspense"),
        "documento": ("terror", "horror", "suspense", "slasher"),
        "peso": 0.12,
    },
    "animacion": {
        "consulta": ("animacion", "animacion japonesa", "anime", "dibujos animados"),
        "documento": ("animacion", "anime", "dibujos animados", "studio ghibli"),
        "peso": 0.10,
    },
    "thriller": {
        "consulta": ("thriller", "suspense", "psicologico"),
        "documento": ("thriller", "suspense", "psicologico"),
        "peso": 0.08,
    },
}


def _normalizar(texto: str) -> str:
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


@lru_cache(maxsize=256)
def leer_documento_normalizado(doc_id: str) -> str:
    ruta = RUTA_DOCUMENTOS / doc_id
    with open(ruta, "r", encoding="utf-8") as archivo:
        return _normalizar(archivo.read())


def extraer_facetas(consulta: str) -> list[str]:
    consulta_normalizada = _normalizar(consulta)
    facetas = []

    for nombre, definicion in FACETAS.items():
        if any(patron in consulta_normalizada for patron in definicion["consulta"]):
            facetas.append(nombre)

    return facetas


def bonificacion_por_facetas(consulta: str, doc_id: str) -> float:
    facetas = extraer_facetas(consulta)
    if not facetas:
        return 0.0

    documento = leer_documento_normalizado(doc_id)[:260]
    bonificacion = 0.0

    for nombre in facetas:
        definicion = FACETAS[nombre]
        if any(patron in documento for patron in definicion["documento"]):
            bonificacion += definicion["peso"]

    return bonificacion