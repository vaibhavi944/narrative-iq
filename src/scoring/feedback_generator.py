def generate_feedback(score_result, language="english"):
    """
    Generates user-friendly feedback and actionable tips based on scoring results.
    Calibrated for realistic and context-aware feedback.
    """

    # Step 1 - Extract data from score_result
    label = score_result["label"]
    reasons = score_result["reasons"]
    pacing_score = score_result["pacing"]["pacing_score"]
    repetition_data = score_result["repetition"]
    emotion_score = score_result["emotion"]["emotion_score"]
    combined_score = score_result["combined_score"]

    # Step 2 - Build a context-aware summary message based on label and reasons
    if label == "Strong":
        summary = "This section is strong. The pacing and word choice work together effectively to create a professional narrative tone."
    elif label == "Weak":
        if "Heavy repetition" in reasons:
            summary = "This paragraph feels repetitive, which distracts from the story. Focusing on word variety will help."
        elif "Prose is overly simplistic" in reasons:
            summary = "The writing here is a bit too simple. Adding complexity to your sentence structures will improve the rhythm."
        else:
            summary = "This section needs more development in its structure and emotional depth to keep readers engaged."
    else:
        # Moderate
        if "Repetitive wording" in reasons:
            summary = "The scene communicates clearly, but repetitive wording reduces narrative richness."
        else:
            summary = "This is a solid foundation, but there's room to improve the rhythmic flow and emotional resonance."

    # Step 3 - Build specific actionable tips based on individual scores
    tips = []

    # Pacing tips
    if pacing_score < 0.5:
        if pacing_score < 0.35:
            tips.append("Your sentences are very long and uniform. Try breaking them up with shorter punchy sentences to create rhythm.")
        else:
            tips.append("Your pacing feels slightly slow. Mix short and long sentences to create a natural reading flow.")

    # Repetition tips
    if repetition_data["repetition_score"] < 0.6:
        if repetition_data.get("repeated_starters"):
            tips.append(f"Several sentences start with the same word: {repetition_data['repeated_starters']}. Try varying your sentence openings.")
        if repetition_data.get("repeated_words"):
            tips.append(f"These words appear too frequently: {repetition_data['repeated_words']}. Replace some with synonyms.")
        if repetition_data.get("repeated_bigrams"):
            tips.append(f"This phrase repeats too often: {repetition_data['repeated_bigrams']}. Rephrase some occurrences.")

    # Emotion tips
    if emotion_score < 0.4:
        tips.append("Consider adding more sensory details or internal character thoughts to deepen the emotional impact.")

    # Default tip if nothing specific found
    if not tips and label != "Strong":
        tips.append("Try experimenting with more expressive imagery to elevate the prose.")
    elif not tips and label == "Strong":
        tips.append("Well-balanced prose. Maintain this level of variety in the rest of your chapter.")

    # Step 4 - Return dictionary with exact keys
    return {
        "label": label,
        "combined_score": combined_score,
        "summary": summary,
        "tips": tips
    }
