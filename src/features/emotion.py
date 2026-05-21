import os
import json
import time
from transformers import pipeline

# =========================================================
# NarrativeIQ - Local Multilingual Emotion Analysis
# =========================================================
# Model: cardiffnlp/twitter-xlm-roberta-base-sentiment
# Purpose:
# Provides local, high-speed multilingual sentiment analysis
# for English, Hindi, and Marathi stories.
# Eliminates Groq API dependency and rate limits.
# =========================================================

print("Initializing local emotion analysis pipeline...")
MODEL_ID = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

try:
    # Initialize globally for performance
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model=MODEL_ID,
        tokenizer=MODEL_ID
    )
    print(f"Model '{MODEL_ID}' loaded successfully.")
except Exception as e:
    print(f"Error loading local model: {e}")
    sentiment_pipeline = None

def get_emotion_score(paragraph, language="english"):
    """
    Analyzes emotional tone and intensity locally using XLM-RoBERTa.
    Returns a dictionary compatible with the existing NarrativeIQ scoring engine.
    """
    # Safe defaults
    polarity = 0.0
    intensity = 0.5
    label = "Neutral"

    if not sentiment_pipeline:
        return {
            "polarity": 0.0,
            "intensity": 0.5,
            "emotion_score": 0.5,
            "label": "Neutral"
        }

    try:
        # Step 1: Inference
        # Model returns: [{'label': 'Positive'/'Negative'/'Neutral', 'score': 0.99}]
        result = sentiment_pipeline(paragraph[:512])[0] # Truncate for model safety
        
        model_label = result["label"]
        confidence = result["score"]

        # Step 2: Map Model Output to NarrativeIQ Schema
        # Labels are usually: "Positive", "Negative", "Neutral"
        if model_label.lower() == "positive":
            polarity = confidence
            label = "Positive"
        elif model_label.lower() == "negative":
            polarity = -confidence
            label = "Negative"
        else:
            polarity = 0.0
            label = "Neutral"

        # Intensity is proxied by confidence (how strong the detected emotion is)
        intensity = confidence

    except Exception as e:
        print(f"Local Inference Error: {e}")

    # Step 3: Return structure compatible with weakness_scorer.py
    return {
        "polarity": round(float(polarity), 2),
        "intensity": round(float(intensity), 2),
        "emotion_score": round(float(intensity), 2), # Maintain key compatibility
        "label": label
    }

if __name__ == "__main__":
    test_cases = [
        {"lang": "English", "text": "I am so happy and excited about this new adventure! The sun is shining bright."},
        {"lang": "Hindi", "text": "मुझे बहुत डर लग रहा है, रात के अंधेरे में कोई चिल्ला रहा था।"},
        {"lang": "Marathi", "text": "आजचा दिवस खूपच कंटाळवाणा होता, काहीही चांगले घडले नाही."}
    ]

    print("\n" + "="*50)
    print("LOCAL EMOTION ANALYSIS TEST")
    print("="*50)

    for tc in test_cases:
        start_time = time.time()
        scores = get_emotion_score(tc["text"], language=tc["lang"].lower())
        end_time = time.time()
        
        print(f"Language: {tc['lang']}")
        print(f"Text: {tc['text'][:50]}...")
        print(f"Result: {scores}")
        print(f"Inference Time: {(end_time - start_time)*1000:.2f}ms")
        print("-" * 30)
