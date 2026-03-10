import json
from models.eval_result   import EvalResult
from data.ground_truth    import GROUND_TRUTH
from metrics.keyword_metrics import keyword_recall, hallucination_check, refusal_check
from metrics.scoring      import compute_score
from reports.summary      import print_summary, export_results_json

MODELO_ID = "gemma3_4b"

with open(f"data/results/eval_{MODELO_ID}.json", encoding="utf-8") as f:
    raw = {r["id"]: r for r in json.load(f)}

results = []
for gt in GROUND_TRUTH:
    respuesta = raw[gt["id"]]["respuesta_modelo"]
    latencia  = raw[gt["id"]]["latencia_s"]

    recall, _, kw_miss        = keyword_recall(respuesta, gt["keywords_obligatorias"])
    hall_score, hallucinations = hallucination_check(respuesta, gt["keywords_prohibidas"])
    refused                   = refusal_check(respuesta)
    length_ratio              = len(respuesta) / max(len(gt["respuesta_esperada"]), 1)
    score, verdict, issues    = compute_score(recall, hall_score, refused, length_ratio)

    results.append(EvalResult(
        id=gt["id"],
        categoria=gt["categoria"],
        pregunta=gt["pregunta"],
        respuesta_modelo=respuesta,
        respuesta_esperada=gt["respuesta_esperada"],
        keyword_recall=recall,
        hallucination_score=hall_score,
        length_ratio=length_ratio,
        refused_to_answer=refused,
        latency_s=latencia,
        score=score,
        verdict=verdict,
        issues=issues,
    ))

print_summary(results)
export_results_json(results, f"data/results/eval_{MODELO_ID}_scored.json")