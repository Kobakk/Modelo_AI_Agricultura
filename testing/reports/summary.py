import json
from models.eval_result import EvalResult
def print_summary(results: list[EvalResult]):
    scores      = [r.score for r in results]
    latencias   = [r.latency_s for r in results]
    recalls     = [r.keyword_recall for r in results]
    hall_scores = [r.hallucination_score for r in results]

    correctos  = sum(1 for r in results if r.score >= 80)
    parciales  = sum(1 for r in results if 50 <= r.score < 80)
    fallidos   = sum(1 for r in results if r.score < 50)
    alucinados = sum(1 for r in results if r.hallucination_score > 0)
    rechazados = sum(1 for r in results if r.refused_to_answer)

    avg_score   = sum(scores) / len(scores)
    avg_latency = sum(latencias) / len(latencias)
    avg_recall  = sum(recalls) / len(recalls)
    avg_hall    = sum(hall_scores) / len(hall_scores)

    # Calificación global
    if avg_score >= 80:
        calificacion = "🟢 SISTEMA FIABLE"
    elif avg_score >= 60:
        calificacion = "🟡 SISTEMA FUNCIONAL — mejoras recomendadas"
    elif avg_score >= 40:
        calificacion = "🟠 SISTEMA DÉBIL — revisar retrieval y prompt"
    else:
        calificacion = "🔴 SISTEMA NO FIABLE — rediseño necesario"

    print("\n" + "=" * 65)
    print("  RESUMEN DE EVALUACIÓN")
    print("=" * 65)
    print(f"  Score medio:          {avg_score:.1f} / 100")
    print(f"  Keyword Recall medio: {avg_recall*100:.1f}%")
    print(f"  Tasa de alucinación:  {avg_hall*100:.1f}%")
    print(f"  Latencia media:       {avg_latency:.1f}s / pregunta")
    print(f"")
    print(f"  ✅ Correctos  (≥80): {correctos}/{len(results)}")
    print(f"  ⚠️  Parciales (50-79): {parciales}/{len(results)}")
    print(f"  ❌ Fallidos   (<50):  {fallidos}/{len(results)}")
    print(f"  🚨 Con alucinación:   {alucinados}/{len(results)}")
    print(f"  🚫 Rechazó responder: {rechazados}/{len(results)}")
    print(f"")
    print(f"  VEREDICTO: {calificacion}")
    print("=" * 65)

    # Tabla por categoría
    print("\n  DETALLE POR PREGUNTA:")
    print(f"  {'ID':<5} {'Score':>6} {'Recall':>7} {'Aluc.':>6} {'Lat.':>5}  Veredicto")
    print(f"  {'-'*5} {'-'*6} {'-'*7} {'-'*6} {'-'*5}  {'-'*20}")
    for r in results:
        print(f"  {r.id:<5} {r.score:>5.0f}  {r.keyword_recall*100:>6.0f}%  "
              f"{r.hallucination_score*100:>5.0f}%  {r.latency_s:>4.1f}s  {r.verdict}")


def export_results_json(results: list[EvalResult], path: str = "rag_eval_results.json"):
    """Exporta los resultados a JSON para análisis posterior."""
    data = []
    for r in results:
        data.append({
            "id": r.id,
            "categoria": r.categoria,
            "pregunta": r.pregunta,
            "respuesta_modelo": r.respuesta_modelo,
            "respuesta_esperada": r.respuesta_esperada,
            "metricas": {
                "score": round(r.score, 2),
                "keyword_recall": round(r.keyword_recall, 3),
                "hallucination_score": round(r.hallucination_score, 3),
                "refused_to_answer": r.refused_to_answer,
                "latency_s": round(r.latency_s, 2),
            },
            "verdict": r.verdict,
            "issues": r.issues,
        })
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Resultados exportados a {path}")