from src.features.pacing import get_pacing_score
from src.features.repetition import get_repetition_score
from src.features.emotion import get_emotion_score

def score_paragraph(paragraph, language="english"):
    """
    Analyzes a paragraph by aggregating pacing, repetition, and emotion scores.
    Calibrated for stricter evaluation.
    """

    # Step 1 - Call feature functions
    pacing_result = get_pacing_score(paragraph, language=language)
    repetition_result = get_repetition_score(paragraph, language=language)
    emotion_result = get_emotion_score(paragraph, language=language)

    # Step 2 - Extract individual scores
    pacing_score = pacing_result.get("pacing_score", 0.0)
    repetition_score = repetition_result.get("repetition_score", 0.0)
    emotion_score = emotion_result.get("emotion_score", 0.0)

    # Step 3 - Calibrated Weighting (Cleanliness & Structure > Sentiment)
    # Applied to all languages for consistent quality standard
    weights = {
        "pacing": 0.45,
        "repetition": 0.40,
        "emotion": 0.15
    }

    combined_score = (pacing_score * weights["pacing"]) + \
                     (repetition_score * weights["repetition"]) + \
                     (emotion_score * weights["emotion"])

    # Step 4 - Penalty Logic
    reasons = []

    # A. Repetition Penalty
    if repetition_score < 0.5:
        combined_score -= 0.10  # Additional penalty for heavy repetition
        reasons.append("Heavy repetition weakens readability")

    # B. Simplicity Penalty (Pacing refinement)
    avg_len = pacing_result.get("avg_sentence_length", 0)
    variance = pacing_result.get("variance", 0)
    if avg_len < 10 and variance < 5:
        combined_score -= 0.05
        reasons.append("Prose is overly simplistic or choppy")

    # Ensure score stays in [0, 1]
    combined_score = max(0.0, min(1.0, combined_score))

    # Step 5 - Tightened Thresholds
    if combined_score >= 0.75:
        label = "Strong"
    elif combined_score >= 0.50:
        label = "Moderate"
    else:
        label = "Weak"

    # Step 6 - Descriptive Reasons
    if pacing_score < 0.5 and "Prose is overly simplistic" not in reasons:
        reasons.append("Pacing is monotonous or lacks rhythmic variety")
    if repetition_score < 0.7 and "Heavy repetition" not in reasons:
        reasons.append("Repetitive wording reduces narrative richness")
    if emotion_score < 0.3:
        reasons.append("Emotional depth appears limited")
    
    if not reasons and label == "Strong":
        reasons.append("Well-balanced prose with good rhythm and clarity")

    return {
        "paragraph": paragraph,
        "language": language,
        "pacing": pacing_result,
        "repetition": repetition_result,
        "emotion": emotion_result,
        "combined_score": round(float(combined_score), 2),
        "label": label,
        "reasons": reasons
    }
