def compute_score(recall: float, hall_score: float, refused: bool, length_ratio: float) -> tuple[float, str, list]:
    """
    Score 0-100:
      - Recall de keywords:     hasta 60 puntos
      - Penalización alucinaciones: -20 por keyword prohibida encontrada
      - Penalización rechazo incorrecto: -30
      - Bonus longitud apropiada: hasta 10 puntos
    """
    issues = []
    score = recall * 60

    if hall_score > 0:
        penalty = min(hall_score * 40, 40)
        score -= penalty
        issues.append(f"⚠️  Posible alucinación ({hall_score * 100:.0f}% keywords prohibidas detectadas)")

    if refused:
        score -= 30
        issues.append("❌ Modelo rechazó responder (debería tener info en contexto)")

    # Bonus por longitud apropiada (no demasiado corta ni demasiado larga)
    if 0.3 <= length_ratio <= 3.0:
        score += 10
    elif length_ratio < 0.1:
        issues.append("⚠️  Respuesta demasiado corta")

    score = max(0, min(100, score))

    if score >= 80:
        verdict = "✅ CORRECTO"
    elif score >= 50:
        verdict = "⚠️  PARCIAL"
    elif score >= 20:
        verdict = "❌ INCORRECTO"
    else:
        verdict = "🚨 ALUCINACIÓN / FALLO CRÍTICO"

    return score, verdict, issues