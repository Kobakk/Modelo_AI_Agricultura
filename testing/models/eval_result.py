from dataclasses import dataclass, field

@dataclass
class EvalResult:
    id: str
    categoria: str
    pregunta: str
    respuesta_modelo: str
    respuesta_esperada: str

    # Métricas calculadas
    keyword_recall: float = 0.0  # % keywords_obligatorias encontradas
    hallucination_score: float = 0.0  # % keywords_prohibidas encontradas (malo)
    length_ratio: float = 0.0  # longitud respuesta vs esperada
    refused_to_answer: bool = False  # dijo "no tengo información"
    latency_s: float = 0.0

    # Score final
    score: float = 0.0
    verdict: str = ""
    issues: list = field(default_factory=list)





