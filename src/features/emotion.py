from textblob import TextBlob

def get_emotion_score(paragraph, language="english"):
    """
    Evaluates the emotional intensity and polarity of a paragraph.
    For English, uses TextBlob sentiment analysis.
    For Hindi and Marathi, uses a keyword-based approach.
    """
    
    polarity = 0.0
    emotion_intensity = 0.0

    # Step 1 - For English: Use TextBlob for sentiment polarity
    if language.lower() == "english":
        blob = TextBlob(paragraph)
        polarity = float(blob.sentiment.polarity)
        # Convert polarity to intensity by taking absolute value
        # (strongly negative or strongly positive both indicate high emotion)
        emotion_intensity = abs(polarity)

    # Step 2 - For Hindi and Marathi: Simple keyword-based intensity
    elif language.lower() in ["hindi", "marathi"]:
        hindi_emotion_words = ["प्यार", "नफरत", "डर", "खुशी", "दुख", "गुस्सा", "रोना", "हंसना", "तकलीफ", "मोहब्बत", "खौफ", "उम्मीद", "दर्द", "जिंदगी", "मौत"]
        marathi_emotion_words = ["प्रेम", "राग", "भीती", "आनंद", "दुःख", "रडणे", "हसणे", "वेदना", "आशा", "मृत्यू", "जीवन", "क्रोध", "काळजी", "स्वप्न", "एकटेपणा"]
        
        # Select appropriate lexicon
        emotion_lexicon = hindi_emotion_words if language.lower() == "hindi" else marathi_emotion_words
        
        # Count occurrences of emotion words in the paragraph
        emotion_word_count = 0
        for word in emotion_lexicon:
            if word in paragraph:
                emotion_word_count += 1
        
        # Calculate intensity: 3 or more words = 1.0 (capped at 1.0)
        emotion_intensity = min(1.0, emotion_word_count / 3.0)
        # Polarity remains 0.0 for keyword method as it's intensity-focused
        polarity = 0.0

    # Step 3 - Calculate final emotion score
    # Directly uses intensity as the score representing emotional richness
    emotion_score = float(emotion_intensity)

    # Step 4 - Return dictionary with exact keys
    return {
        "polarity": round(polarity, 2),
        "emotion_intensity": round(emotion_intensity, 2),
        "emotion_score": round(emotion_score, 2)
    }
