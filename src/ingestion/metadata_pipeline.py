import os
import json
from groq import Groq
from dotenv import load_dotenv

# Step 1: Import required libraries and load environment variables
load_dotenv(override=True)

# Step 2: Create Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def tag_chunks(chunks):
    """
    Analyzes story paragraphs using Groq and adds metadata tags for genre,
    scene type, and dialogue density to each chunk dictionary.
    """
    tagged_chunks = []
    
    # Step 3: For each chunk, call Groq to tag it
    for i, chunk in enumerate(chunks):
        text = chunk["text"]
        
        prompt = f"""Analyze this story paragraph and return a JSON object with exactly these keys:
- genre: one of [romance, thriller, drama, fantasy, slice_of_life]
- scene_type: one of [action, emotional, dialogue, description, conflict]
- dialogue_density: one of [high, medium, low, none]

Paragraph:
{text}

Return only the JSON object. No explanation. No markdown."""

        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            
            response_text = completion.choices[0].message.content.strip()
            
            # Step 4: Parse JSON response and add metadata to chunk
            # Strip markdown if present (e.g., ```json ... ```)
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:].strip()
            
            tags = json.loads(response_text)
            
            # Add tags to chunk dictionary
            chunk["genre"] = tags.get("genre", "slice_of_life")
            chunk["scene_type"] = tags.get("scene_type", "description")
            chunk["dialogue_density"] = tags.get("dialogue_density", "none")
            
        except Exception as e:
            # Fallback to defaults if parsing or API fails
            chunk["genre"] = "slice_of_life"
            chunk["scene_type"] = "description"
            chunk["dialogue_density"] = "none"
            
        tagged_chunks.append(chunk)
        
        # Step 5: Print progress every 100 chunks
        if (i + 1) % 100 == 0:
            print(f"Tagged {i + 1} chunks...")
            
    # Step 6: Return tagged chunks list
    return tagged_chunks

# Step 7: Add main block to test
if __name__ == "__main__":
    # Import from the correct location based on directory structure
    from src.rag.chunking import load_and_chunk_stories
    
    chunks = load_and_chunk_stories()
    
    # For testing purposes, only tag a small subset to avoid hitting rate limits
    test_limit = 5
    print(f"Tagging {test_limit} chunks for testing...")
    tagged = tag_chunks(chunks[:test_limit])
    
    print("\n--- Sample of Tagged Chunks ---")
    for chunk in tagged[:3]:
        print(json.dumps(chunk, indent=2, ensure_ascii=False))
        print("-" * 20)
        
    # Statistical analysis (on the test subset)
    genre_counts = {}
    scene_counts = {}
    
    for chunk in tagged:
        g = chunk["genre"]
        s = chunk["scene_type"]
        genre_counts[g] = genre_counts.get(g, 0) + 1
        scene_counts[s] = scene_counts.get(s, 0) + 1
        
    print("\nGenre Counts:")
    for g, count in genre_counts.items():
        print(f" - {g}: {count}")
        
    print("\nScene Type Counts:")
    for s, count in scene_counts.items():
        print(f" - {s}: {count}")
