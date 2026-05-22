import os
import requests
import json

def generate_story():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in environment.")
        return

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    prompt = """एक छोटी हिंदी कहानी लिखो जिसमें 3 अनुच्छेद हों।
हर अनुच्छेद में 4-5 वाक्य हों।
अनुच्छेदों के बीच एक खाली पंक्ति छोड़ो।
विषय: बारिश में बच्चे का खेलना और घर वापस आना।
केवल शुद्ध हिंदी देवनागरी लिपि में लिखो।
कोई अंग्रेजी, रूसी या चीनी अक्षर नहीं।
कोई शीर्षक नहीं। कोई स्पष्टीकरण नहीं।"""

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        story = response.json()['choices'][0]['message']['content'].strip()
        
        # Ensure the directory exists
        os.makedirs("data/raw_stories/hindi", exist_ok=True)
        
        with open("data/raw_stories/hindi/story_050.txt", "w", encoding="utf-8") as f:
            f.write(story)
        print("Story generated and saved successfully.")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    generate_story()
