import re
import unicodedata
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

STOPWORDS_ES = set(stopwords.words('spanish'))
STEMMER_ES = SnowballStemmer('spanish')

def quitar_acentos(texto: str) -> str:
    texto = unicodedata.normalize('NFD', texto)
    return ''.join(ch for ch in texto if unicodedata.category(ch) != 'Mn')

def normalizar(texto: str, quitar_acentos_flag: bool = True) -> str:
    texto = texto.lower()
    if quitar_acentos_flag:
        texto = quitar_acentos(texto)
    texto = re.sub(r'[^a-z0-9áéíóúüñ]+', ' ', texto)
    return re.sub(r'\s+', ' ', texto).strip()

def tokenizar(texto: str, language: str = 'spanish') -> list[str]:
    return word_tokenize(texto, language=language)

def filtrar_tokens(tokens: list[str],
                   stopwords_set: set = STOPWORDS_ES,
                   min_len: int = 3,
                   keep_numbers: bool = False) -> list[str]:
    out = []
    for t in tokens:
        if not keep_numbers and t.isdigit():
            continue
        if t in stopwords_set:
            continue
        if len(t) < min_len:
            continue
        out.append(t)
    return out

def aplicar_stemming(tokens: list[str]) -> list[str]:
    return [STEMMER_ES.stem(t) for t in tokens]

def preprocesar_texto(texto: str,
                      quitar_acentos_flag: bool = True,
                      min_len: int = 3,
                      keep_numbers: bool = False,
                      apply_stemming: bool = False,
                      return_tokens: bool = False) -> str | list[str]:
    texto = normalizar(texto, quitar_acentos_flag)
    tokens = tokenizar(texto)
    tokens = filtrar_tokens(tokens, STOPWORDS_ES, min_len, keep_numbers)
    if apply_stemming:
        tokens = aplicar_stemming(tokens)
    if return_tokens:
        return tokens
    return " ".join(tokens)
