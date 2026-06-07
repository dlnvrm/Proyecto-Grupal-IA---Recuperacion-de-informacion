# main_tfidf.py
#
# Sistema de Recuperación en Texto Libre (TF‑IDF + Coseno)
# Modo interactivo: permite escribir consultas y ver resultados con nombres.

import json
from pathlib import Path
from indexacion import construir_indice
from busqueda import buscar
from evaluacion import evaluar 

# Mapa ID → Nombre del director
DIRECTORES = {
    "1.txt": "Pedro Almodóvar",          "2.txt": "Luis Buñuel",
    "3.txt": "Alejandro Amenábar",        "4.txt": "Álex de la Iglesia",
    "5.txt": "Fernando Trueba",           "6.txt": "Icíar Bollaín",
    "7.txt": "Carlos Saura",              "8.txt": "Víctor Erice",
    "9.txt": "Bigas Luna",               "10.txt": "Juan Antonio Bayona",
    "11.txt": "Julio Médem",             "12.txt": "Isabel Coixet",
    "13.txt": "Emilio Martínez-Lázaro",  "14.txt": "Fernando León de Aranoa",
    "15.txt": "Montxo Armendáriz",       "16.txt": "Steven Spielberg",
    "17.txt": "Martin Scorsese",         "18.txt": "Stanley Kubrick",
    "19.txt": "Francis Ford Coppola",    "20.txt": "Quentin Tarantino",
    "21.txt": "Christopher Nolan",       "22.txt": "Alfred Hitchcock",
    "23.txt": "Orson Welles",            "24.txt": "Billy Wilder",
    "25.txt": "Woody Allen",             "26.txt": "Tim Burton",
    "27.txt": "David Lynch",             "28.txt": "Ridley Scott",
    "29.txt": "James Cameron",           "30.txt": "Clint Eastwood",
    "31.txt": "Oliver Stone",            "32.txt": "Spike Lee",
    "33.txt": "Wes Anderson",            "34.txt": "David Fincher",
    "35.txt": "Sofia Coppola",           "36.txt": "Guillermo del Toro",
    "37.txt": "Alfonso Cuarón",          "38.txt": "Alejandro González Iñárritu",
    "39.txt": "Fernando Meirelles",      "40.txt": "Paolo Sorrentino",
    "41.txt": "Lars von Trier",          "42.txt": "Michael Haneke",
    "43.txt": "Yorgos Lanthimos",        "44.txt": "Pedro Costa",
    "45.txt": "Ken Loach",              "46.txt": "Jean-Luc Godard",
    "47.txt": "François Truffaut",      "48.txt": "Federico Fellini",
    "49.txt": "Ingmar Bergman",         "50.txt": "Akira Kurosawa",
    "51.txt": "Hayao Miyazaki",         "52.txt": "Isao Takahata",
    "53.txt": "Makoto Shinkai",         "54.txt": "Satoshi Kon",
    "55.txt": "Bong Joon-ho",           "56.txt": "Park Chan-wook",
    "57.txt": "Kim Ki-duk",             "58.txt": "Takashi Miike",
    "59.txt": "John Carpenter",         "60.txt": "Wes Craven",
    "61.txt": "George A. Romero",       "62.txt": "James Wan",
    "63.txt": "Denis Villeneuve",       "64.txt": "Paul Thomas Anderson",
    "65.txt": "Robert Eggers",          "66.txt": "Greta Gerwig",
    "67.txt": "Chloé Zhao",             "68.txt": "Jane Campion",
    "69.txt": "Kathryn Bigelow",        "70.txt": "Sergio Leone",
}


def modo_interactivo(vectorizador, matriz_tfidf, ids, map_global):
    print("\n" + "=" * 62)
    print("   SISTEMA TF‑IDF — Consultas en Texto Libre")
    print("=" * 62)
    print("Escribe una consulta en lenguaje natural.")
    print("Ejemplos:")
    print("  directores de animación")
    print("  cine de terror japonés")
    print("  ganadores del óscar")
    print()
    print("Escribe 'salir' para terminar.")
    print("=" * 62 + "\n")

    while True:
        consulta = input("Consulta: ").strip()
        if consulta.lower() == "salir":
            print("Hasta luego.")
            break
        if not consulta:
            continue

        ranking = buscar(consulta, vectorizador, matriz_tfidf, ids)

        print("\nResultados:")
        for doc, score in ranking[:10]:
            nombre = DIRECTORES.get(doc, "Desconocido")
            print(f"  {doc:>6}  →  {nombre:<25}  (similitud = {score:.4f})")
        
        print(f"\nMAP del sistema: {map_global:.4f}\n")

        print()


def main():
    print("Calculando MAP global del sistema...")
    resultados = evaluar()
    map_global = resultados["_promedios"]["map"]

    print("Construyendo índice TF‑IDF...")
    vectorizador, matriz_tfidf, ids = construir_indice()

    modo_interactivo(vectorizador, matriz_tfidf, ids, map_global)


if __name__ == "__main__":
    main()
