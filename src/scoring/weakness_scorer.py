from src.features.pacing import get_pacing_score
from src.features.repetition import get_repetition_score
from src.features.emotion import get_emotion_score

def score_paragraph(paragraph, language="english"):
    """
    Analyzes a paragraph by aggregating pacing, repetition, and emotion scores.
    """

    # Step 1 - Import and call all three feature functions
    pacing_result = get_pacing_score(paragraph, language=language)
    repetition_result = get_repetition_score(paragraph, language=language)
    emotion_result = get_emotion_score(paragraph, language=language)

    # Step 2 - Extract individual scores
    pacing_score = pacing_result.get("pacing_score", 0.0)
    repetition_score = repetition_result.get("repetition_score", 0.0)
    emotion_score = emotion_result.get("emotion_score", 0.0)

    # Step 3 - Calculate weighted combined score
    # Pacing: 0.4, Repetition: 0.35, Emotion: 0.25
    combined_score = (pacing_score * 0.4) + (repetition_score * 0.35) + (emotion_score * 0.25)

    # Step 4 - Assign label based on combined score
    if combined_score >= 0.60:
        label = "Strong"
    elif combined_score >= 0.40:
        label = "Moderate"
    else:
        label = "Weak"

    # Step 5 - Build reasons list in plain English
    reasons = []
    if pacing_score < 0.5:
        reasons.append("Pacing is slow or monotonous")
    if repetition_score < 0.5:
        reasons.append("Too much repetition detected")
    if emotion_score < 0.2:
        reasons.append("Paragraph feels emotionally flat")
    
    if not reasons and label == "Strong":
        reasons.append("Well balanced paragraph")

    # Step 6 - Return dictionary with exact keys
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
