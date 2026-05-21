import os
import json
import time
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Global API Key management
_KEYS = []
for i in range(1, 6):
    key = os.getenv(f"GROQ_API_KEY_{i}")
    if key:
        _KEYS.append(key)
if not _KEYS:
    single = os.getenv("GROQ_API_KEY")
    if single:
        _KEYS.append(single)

_CURRENT_KEY_INDEX = 0

def get_client():
    global _CURRENT_KEY_INDEX
    if not _KEYS:
        return None
    return Groq(api_key=_KEYS[_CURRENT_KEY_INDEX])

def get_emotion_score(paragraph, language="english"):
    """
    Analyzes the emotional tone and intensity of a paragraph using Groq API with key rotation.
    """
    global _CURRENT_KEY_INDEX
    
    polarity = 0.0
    emotion_intensity = 0.5
    
    if not _KEYS:
        print("Warning: No Groq API keys found. Using defaults for emotion.")
        return {"polarity": 0.0, "emotion_intensity": 0.5, "emotion_score": 0.5}

    attempts = 0
    max_attempts = len(_KEYS) * 2
    
    while attempts < max_attempts:
        try:
            client = get_client()
            
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

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )

            response_text = completion.choices[0].message.content.strip()
            
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            data = json.loads(response_text)
            polarity = float(data.get("polarity", 0.0))
            emotion_intensity = float(data.get("emotion_intensity", 0.5))
            
            # Success - small delay and return
            time.sleep(0.5)
            break

        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "rate_limit" in error_str.lower():
                _CURRENT_KEY_INDEX += 1
                if _CURRENT_KEY_INDEX >= len(_KEYS):
                    print("Emotion Scorer: All keys exhausted. Waiting 65 seconds...")
                    time.sleep(65)
                    _CURRENT_KEY_INDEX = 0
                print(f"Emotion Scorer: Switching to key {_CURRENT_KEY_INDEX + 1}...")
            else:
                # Non-rate-limit error: log and return defaults
                print(f"Emotion Analysis Error: {e}")
                break
        
        attempts += 1

    emotion_score = emotion_intensity

    return {
        "polarity": round(float(polarity), 2),
        "emotion_intensity": round(float(emotion_intensity), 2),
        "emotion_score": round(float(emotion_score), 2)
    }
