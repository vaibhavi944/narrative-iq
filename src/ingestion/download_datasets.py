import os
from datasets import load_dataset
from groq import Groq
from dotenv import load_dotenv

# Step 1: Load environment variables
load_dotenv()

# Step 2: Define output folder paths and create directories
ENGLISH_DIR = "data/raw_stories/english"
HINDI_DIR = "data/raw_stories/hindi"
MARATHI_DIR = "data/raw_stories/marathi"

os.makedirs(ENGLISH_DIR, exist_ok=True)
os.makedirs(HINDI_DIR, exist_ok=True)
os.makedirs(MARATHI_DIR, exist_ok=True)

# Step 3: Download English stories from TinyStories
def download_english():
    try:
        print("Loading TinyStories dataset...")
        dataset = load_dataset("roneneldan/TinyStories", split="train[:500]")
        
        count = 0
        for i, story in enumerate(dataset):
            content = story["text"]
            filename = os.path.join(ENGLISH_DIR, f"story_{i+1:03d}.txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            
            count += 1
            if count % 100 == 0:
                print(f"Saved {count} English stories...")
        
        print(f"Total English stories saved: {count}")
    except Exception as e:
        print(f"Error downloading English stories: {e}")

# Step 4: Generate Hindi stories using Groq
def download_hindi():
    """
    Replaced legacy midas/hindi_discourse dataset download with synthetic generation.
    Legacy dataset scripts are often blocked or inconsistent. Synthetic generation 
    provides higher quality, controlled length, and emotionally expressive narratives.
    """
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("GROQ_API_KEY not found in environment variables.")
            return

        client = Groq(api_key=api_key)
        
        topics = [
            "family conflict", "village life", "school memories", "festivals", 
            "friendship", "emotional conversations", "suspense moments", 
            "travel", "daily life", "rainy season"
        ]
        
        count = 0
        for i in range(50):
            topic = topics[i % len(topics)]
            prompt = (
                f"Write a short Hindi story with exactly 3 paragraphs about {topic}.\n"
                "Each paragraph should be 3-5 sentences long.\n"
                "Separate paragraphs with a blank line.\n"
                "Use natural Hindi script (Devanagari) in a narrative storytelling style.\n"
                "The tone should be emotionally expressive with varied pacing.\n"
                "Include dialogue in at least one paragraph.\n"
                "Return only the story paragraphs separated by blank lines.\n"
                "No title. No markdown. No explanations."
            )
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = completion.choices[0].message.content.strip()
            filename = os.path.join(HINDI_DIR, f"story_{i+1:03d}.txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            
            count += 1
            if count % 10 == 0:
                print(f"Generated {count} Hindi stories...")
                
        print(f"Total Hindi stories generated: {count}")
    except Exception as e:
        print(f"Error generating Hindi stories: {e}")

# Step 5: Generate Marathi story paragraphs using Groq
def generate_marathi():
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("GROQ_API_KEY not found in environment variables.")
            return

        client = Groq(api_key=api_key)
        
        count = 0
        for i in range(30):
            prompt = (
                "Write a short Marathi story with exactly 3 paragraphs about daily life in Maharashtra.\n"
                "Each paragraph should be 3-5 sentences long.\n"
                "Separate paragraphs with a blank line.\n"
                "Topics to choose from: going to market, morning routine, family dinner,\n"
                "walking to school, farming, festival preparation, visiting relatives.\n"
                "Include dialogue in at least one paragraph.\n"
                "Return only the story paragraphs separated by blank lines.\n"
                "No title. No explanation."
            )
            
            # Using llama-3.3-70b-versatile as llama3-8b-8192 is deprecated
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = completion.choices[0].message.content.strip()
            filename = os.path.join(MARATHI_DIR, f"story_{i+1:03d}.txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            
            count += 1
            if count % 10 == 0:
                print(f"Generated {count} Marathi stories...")
                
        print(f"Total Marathi stories generated: {count}")
    except Exception as e:
        print(f"Error generating Marathi stories: {e}")

def regenerate_indic():
    """Regenerates only Hindi and Marathi datasets."""
    print("Regenerating Hindi stories...")
    download_hindi()
    print("Regenerating Marathi stories...")
    generate_marathi()

# Step 6: Main function to orchestrate the downloads
def main():
    print("Downloading English stories...")
    download_english()
    print("Downloading Hindi stories...")
    download_hindi()
    print("Generating Marathi stories...")
    generate_marathi()
    print("All datasets ready.")

if __name__ == "__main__":
    print("Regenerating Hindi and Marathi stories with multi-paragraph format...")
    regenerate_indic()
    print("Done.")
