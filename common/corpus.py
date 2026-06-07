from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json


BASE = Path(__file__).resolve().parent
RUTA_DOCUMENTOS = BASE / "datos" / "documentos"

DIRECTORES = [
    "Pedro_Almodóvar",
    "Luis_Buñuel",
    "Alejandro_Amenábar",
    "Álex_de_la_Iglesia",
    "Fernando_Trueba",
    "Icíar_Bollaín",
    "Carlos_Saura",
    "Víctor_Erice",
    "Bigas_Luna",
    "Juan_Antonio_Bayona",
    "Julio_Médem",
    "Isabel_Coixet",
    "Emilio_Martínez-Lázaro",
    "Fernando_León_de_Aranoa",
    "Montxo_Armendáriz",
    "Steven_Spielberg",
    "Martin_Scorsese",
    "Stanley_Kubrick",
    "Francis_Ford_Coppola",
    "Quentin_Tarantino",
    "Christopher_Nolan",
    "Alfred_Hitchcock",
    "Orson_Welles",
    "Billy_Wilder",
    "Woody_Allen",
    "Tim_Burton",
    "David_Lynch",
    "Ridley_Scott",
    "James_Cameron",
    "Clint_Eastwood",
    "Oliver_Stone",
    "Spike_Lee",
    "Wes_Anderson",
    "David_Fincher",
    "Sofia_Coppola",
    "Guillermo_del_Toro",
    "Alfonso_Cuarón",
    "Alejandro_González_Iñárritu",
    "Fernando_Meirelles",
    "Paolo_Sorrentino",
    "Lars_von_Trier",
    "Michael_Haneke",
    "Yorgos_Lanthimos",
    "Pedro_Costa",
    "Ken_Loach",
    "Jean-Luc_Godard",
    "François_Truffaut",
    "Federico_Fellini",
    "Ingmar_Bergman",
    "Akira_Kurosawa",
    "Hayao_Miyazaki",
    "Isao_Takahata",
    "Makoto_Shinkai",
    "Satoshi_Kon",
    "Bong_Joon-ho",
    "Park_Chan-wook",
    "Kim_Ki-duk",
    "Takashi_Miike",
    "John_Carpenter",
    "Wes_Craven",
    "George_A._Romero",
    "James_Wan",
    "Denis_Villeneuve",
    "Paul_Thomas_Anderson",
    "Robert_Eggers",
    "Greta_Gerwig",
    "Chloé_Zhao",
    "Jane_Campion",
    "Kathryn_Bigelow",
    "Sergio_Leone",
]


def asegurar_directorio_documentos() -> None:
    RUTA_DOCUMENTOS.mkdir(parents=True, exist_ok=True)


def corpus_completo() -> bool:
    asegurar_directorio_documentos()
    for indice in range(1, len(DIRECTORES) + 1):
        if not (RUTA_DOCUMENTOS / f"{indice}.txt").exists():
            return False
    return True


def crear_corpus(force: bool = False) -> None:
    """
    Descarga los extractos de Wikipedia y los guarda como 1.txt, 2.txt, ...
    dentro de common/datos/documentos.
    """
    asegurar_directorio_documentos()

    if not force and corpus_completo():
        return

    for indice, nombre in enumerate(DIRECTORES, start=1):
        url = "https://es.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "prop": "extracts",
            "explaintext": True,
            "format": "json",
            "titles": nombre,
        }

        headers = {"User-Agent": "Sofia-IR-Project/1.0 (sofia@example.com)"}
        query = urlencode(params)
        request = Request(f"{url}?{query}", headers=headers)
        with urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))

        page = next(iter(data["query"]["pages"].values()))
        texto = page.get("extract", "")

        ruta = RUTA_DOCUMENTOS / f"{indice}.txt"
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(texto)
