import os
import json
from groq import Groq

def get_emotion_score(paragraph, language="english"):
    """
    Analyzes the emotional tone and intensity of a paragraph using Groq API.
    """

    # Step 1 - Handle any errors with safe defaults
    polarity = 0.0
    emotion_intensity = 0.5

    try:
        # Step 2 - Load Groq client
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        # Step 3 - Build prompt for all languages
        prompt = f"""You are a literary editor analyzing narrative prose.
Analyze the emotional tone of this paragraph.
Return only a valid JSON object with exactly these two keys:
- polarity: a float between -1.0 and 1.0
  (-1.0 = deeply sad/fearful/angry, 0.0 = neutral/flat, 1.0 = joyful/hopeful/loving)
- emotion_intensity: a float between 0.0 and 1.0
  (0.0 = completely emotionally flat, 1.0 = very emotionally rich and powerful)

Important rules:
- Evaluate based on literary quality not just keywords
- A paragraph describing grief with beautiful imagery should score high intensity
- A paragraph listing facts or actions with no emotional depth should score low
- Consider subtext, sensory details, and inner thoughts as emotional signals
- The paragraph may be in English, Hindi, or Marathi — evaluate accordingly

Paragraph:
{paragraph}

Return only the JSON object. No explanation. No markdown. No code blocks."""

        # Step 4 - Call Groq API
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        # Step 5 - Parse response
        response_text = completion.choices[0].message.content.strip()
        
        # Strip markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif response_text.startswith("```"):
            response_text = response_text.split("```")[1].split("```")[0].strip()

        # Parse JSON and extract values
        data = json.loads(response_text)
        polarity = float(data.get("polarity", 0.0))
        emotion_intensity = float(data.get("emotion_intensity", 0.5))

    except Exception:
        # Step 6 - Error handling (already initialized with defaults)
        pass

    # Step 7 - Calculate emotion_score = emotion_intensity directly
    emotion_score = emotion_intensity

    # Step 8 - Return dictionary
    return {
        "polarity": round(float(polarity), 2),
        "emotion_intensity": round(float(emotion_intensity), 2),
        "emotion_score": round(float(emotion_score), 2)
    }
