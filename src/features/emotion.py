import os
import json
from textblob import TextBlob
from groq import Groq

def get_emotion_score(paragraph, language="english"):
    """
    Analyzes the emotional tone and intensity of a paragraph.
    """
    
    # Step 1 - For English: Use TextBlob to get sentiment polarity
    if language.lower() == "english":
        polarity = TextBlob(paragraph).sentiment.polarity
        emotion_intensity = abs(polarity)
        # polarity is between -1.0 and 1.0

    # Step 2 - For Hindi and Marathi: Use Groq API to analyze emotion
    elif language.lower() in ["hindi", "marathi"]:
        try:
            # Load GROQ_API_KEY from environment using os.getenv
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            
            # Send this prompt to groq
            prompt = f"""Analyze the emotional tone of this paragraph. 
Return only a valid JSON object with exactly these keys:
polarity (float between -1.0 and 1.0, negative means sad/fearful/angry, positive means happy/hopeful/loving, 0.0 means neutral),
emotion_intensity (float between 0.0 and 1.0, 0.0 means completely flat, 1.0 means very emotionally rich).
Paragraph: {paragraph}
Return only the JSON. No explanation. No markdown."""
            
            # Use model: llama-3.3-70b-versatile
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            
            # Parse the JSON response and extract polarity and emotion_intensity
            response_text = completion.choices[0].message.content.strip()
            # Handle potential markdown code blocks in response
            if response_text.startswith("```json"):
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif response_text.startswith("```"):
                response_text = response_text.split("```")[1].split("```")[0].strip()
                
            data = json.loads(response_text)
            polarity = float(data.get("polarity", 0.0))
            emotion_intensity = float(data.get("emotion_intensity", 0.5))
            
        except (Exception, json.JSONDecodeError):
            # If JSON parsing fails return polarity 0.0 and emotion_intensity 0.5 as safe default
            polarity = 0.0
            emotion_intensity = 0.5
    
    else:
        # Default fallback
        polarity = 0.0
        emotion_intensity = 0.0

    # Step 3 - Calculate emotion score
    # emotion_score = emotion_intensity directly
    emotion_score = emotion_intensity

    # Step 4 - Return dictionary with exact keys:
    return {
        "polarity": round(float(polarity), 2),
        "emotion_intensity": round(float(emotion_intensity), 2),
        "emotion_score": round(float(emotion_score), 2)
    }
