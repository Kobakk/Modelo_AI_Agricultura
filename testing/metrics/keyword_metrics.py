def normalize(text: str) -> str:
    """Minúsculas, sin tildes, sin puntuación para comparación robusta."""
    text = text.lower()
    replacements = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ü": "u", "ñ": "n"}
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


def keyword_recall(respuesta: str, keywords: list) -> tuple[float, list, list]:
    """Devuelve (recall, encontradas, no_encontradas)."""
    r = normalize(respuesta)
    encontradas = [kw for kw in keywords if normalize(kw) in r]
    no_encontradas = [kw for kw in keywords if normalize(kw) not in r]
    recall = len(encontradas) / len(keywords) if keywords else 1.0
    return recall, encontradas, no_encontradas


def hallucination_check(respuesta: str, keywords_prohibidas: list) -> tuple[float, list]:
    """Detecta keywords que NO deberían aparecer. Retorna (score, hallucinations)."""
    r = normalize(respuesta)
    hallucinations = [kw for kw in keywords_prohibidas if normalize(kw) in r]
    score = len(hallucinations) / len(keywords_prohibidas) if keywords_prohibidas else 0.0
    return score, hallucinations


def refusal_check(respuesta: str) -> bool:
    """Detecta si el modelo dijo que no tenía información."""
    frases_rechazo = [
        "no tengo información", "no tengo suficiente", "no encuentro",
        "no se menciona", "no aparece", "no está en el contexto",
        "no puedo responder", "fuera de mi conocimiento",
        "el documento no", "no se indica"
    ]
    r = normalize(respuesta)
    return any(normalize(f) in r for f in frases_rechazo)