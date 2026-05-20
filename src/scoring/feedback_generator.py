def generate_feedback(score_result, language="english"):
    """
    Generates user-friendly feedback and actionable tips based on scoring results.
    """

    # Step 1 - Extract data from score_result
    label = score_result["label"]
    reasons = score_result["reasons"]
    pacing_score = score_result["pacing"]["pacing_score"]
    repetition_data = score_result["repetition"]
    emotion_score = score_result["emotion"]["emotion_score"]
    combined_score = score_result["combined_score"]

    # Step 2 - Build a friendly summary message based on label
    if label == "Strong":
        summary = "This section reads well. Your pacing, word choice, and emotional tone are working together effectively."
    elif label == "Moderate":
        summary = "This section has a solid foundation but has some areas that could be tightened to keep readers engaged."
    else:  # label == "Weak"
        summary = "This section may cause readers to lose interest. Consider the specific suggestions below."

    # Step 3 - Build specific actionable tips based on individual scores
    tips = []

    # Pacing tips
    if pacing_score < 0.5:
        if pacing_score < 0.35:
            tips.append("Your sentences are very long and uniform. Try breaking them up with shorter punchy sentences to create rhythm.")
        else:
            tips.append("Your pacing feels slightly slow. Mix short and long sentences to create a natural reading flow.")

    # Repetition tips
    if repetition_data["repetition_score"] < 0.5:
        if repetition_data.get("repeated_starters"):
            tips.append(f"Several sentences start with the same word: {repetition_data['repeated_starters']}. Try varying your sentence openings.")
        if repetition_data.get("repeated_words"):
            tips.append(f"These words appear too frequently: {repetition_data['repeated_words']}. Replace some with synonyms.")
        if repetition_data.get("repeated_bigrams"):
            tips.append(f"This phrase repeats too often: {repetition_data['repeated_bigrams']}. Rephrase some occurrences.")

    # Emotion tips
    if emotion_score < 0.3:
        tips.append("This paragraph feels emotionally flat. Add a sensory detail, inner thought, or emotional reaction to give it life.")

    # Default tip if nothing specific found
    if not tips:
        tips.append("No major issues found. Keep writing.")

    # Step 4 - Return dictionary with exact keys
    return {
        "label": label,
        "combined_score": combined_score,
        "summary": summary,
        "tips": tips
    }
