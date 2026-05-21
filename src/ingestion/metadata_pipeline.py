import os
import json
import time
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Load multiple API keys
keys = []
for i in range(1, 6):
    key = os.getenv(f"GROQ_API_KEY_{i}")
    if key:
        keys.append(key)
if not keys:
    single = os.getenv("GROQ_API_KEY")
    if single:
        keys.append(single)

if not keys:
    raise ValueError("No Groq API keys found in .env file")

print(f"Loaded {len(keys)} API key(s)")
current_key_index = 0

def get_client():
    return Groq(api_key=keys[current_key_index])

def call_groq_with_rotation(prompt):
    global current_key_index
    attempts = 0
    max_attempts = len(keys) * 2
    
    while attempts < max_attempts:
        try:
            client = get_client()
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            time.sleep(0.5)
            return completion.choices[0].message.content.strip()
            
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "rate_limit" in error_str.lower():
                print(f"Key {current_key_index + 1} hit rate limit.")
                current_key_index += 1
                if current_key_index >= len(keys):
                    print("All keys exhausted. Waiting 65 seconds for reset...")
                    time.sleep(65)
                    current_key_index = 0
                print(f"Switching to key {current_key_index + 1}...")
            else:
                print(f"Non-rate-limit error: {e}")
                return None
        attempts += 1
    
    print("Max attempts reached for this batch.")
    return None

def tag_chunks(chunks, resume=True):
    progress_file = "data/processed/tagged_chunks_progress.json"
    final_file = "data/processed/tagged_chunks_final.json"
    os.makedirs("data/processed", exist_ok=True)
    
    tagged_chunks = []
    start_index = 0
    
    if resume and os.path.exists(progress_file):
        try:
            with open(progress_file, "r", encoding="utf-8") as f:
                tagged_chunks = json.load(f)
                start_index = len(tagged_chunks)
                print(f"Resuming from chunk {start_index}...")
        except:
            tagged_chunks = []
            start_index = 0
    
    batch_size = 10
    total_chunks = len(chunks)
    
    if start_index >= total_chunks:
        print("All chunks already processed.")
        return tagged_chunks
    
    for i in range(start_index, total_chunks, batch_size):
        batch = chunks[i:i + batch_size]
        batch_copies = [chunk.copy() for chunk in batch]
        
        paragraphs_text = ""
        for idx, chunk in enumerate(batch_copies):
            paragraphs_text += f"{idx + 1}. {chunk['text']}\n\n"
        
        prompt = f"""You are a literary analyst. Analyze these story paragraphs carefully.
For each paragraph return a JSON object with exactly these keys:
- genre: must be exactly one of [romance, thriller, drama, fantasy, slice_of_life]
  romance = love stories, relationships, emotional bonds
  thriller = suspense, danger, mystery, fear
  drama = conflict, family issues, emotional struggle
  fantasy = magical, supernatural, imaginary worlds
  slice_of_life = everyday life, daily routines, realistic scenarios
- scene_type: must be exactly one of [action, emotional, dialogue, description, conflict]
  action = characters doing things, movement, events happening
  emotional = feelings, inner thoughts, emotional moments
  dialogue = conversation between characters
  description = describing places, people, atmosphere
  conflict = argument, problem, tension between characters
- dialogue_density: must be exactly one of [high, medium, low, none]
  high = mostly conversation
  medium = mix of dialogue and narration
  low = little dialogue
  none = no dialogue at all

Return a JSON array with one object per paragraph in the SAME ORDER as given.
Return ONLY the JSON array. No explanation. No markdown. No extra text.

Paragraphs:
{paragraphs_text}"""

        response = call_groq_with_rotation(prompt)
        
        if response:
            try:
                if "```json" in response:
                    response = response.split("```json")[1].split("```")[0].strip()
                elif "```" in response:
                    response = response.split("```")[1].split("```")[0].strip()
                
                batch_tags = json.loads(response)
                
                if not isinstance(batch_tags, list):
                    batch_tags = []
                
                valid_genres = ["romance", "thriller", "drama", "fantasy", "slice_of_life"]
                valid_scenes = ["action", "emotional", "dialogue", "description", "conflict"]
                valid_density = ["high", "medium", "low", "none"]
                
                for idx, chunk in enumerate(batch_copies):
                    if idx < len(batch_tags) and isinstance(batch_tags[idx], dict):
                        tags = batch_tags[idx]
                        genre = tags.get("genre", "slice_of_life")
                        scene_type = tags.get("scene_type", "description")
                        dialogue_density = tags.get("dialogue_density", "none")
                        
                        if genre not in valid_genres:
                            genre = "slice_of_life"
                        if scene_type not in valid_scenes:
                            scene_type = "description"
                        if dialogue_density not in valid_density:
                            dialogue_density = "none"
                    else:
                        genre = "slice_of_life"
                        scene_type = "description"
                        dialogue_density = "none"
                    
                    chunk["genre"] = genre
                    chunk["scene_type"] = scene_type
                    chunk["dialogue_density"] = dialogue_density
                    
            except json.JSONDecodeError as e:
                print(f"JSON parse error at batch {i}: {e}")
                for chunk in batch_copies:
                    chunk["genre"] = "slice_of_life"
                    chunk["scene_type"] = "description"
                    chunk["dialogue_density"] = "none"
        else:
            for chunk in batch_copies:
                chunk["genre"] = "slice_of_life"
                chunk["scene_type"] = "description"
                chunk["dialogue_density"] = "none"
        
        tagged_chunks.extend(batch_copies)
        processed_count = len(tagged_chunks)
        
        if processed_count % 100 == 0 or processed_count == total_chunks:
            print(f"Tagged {processed_count}/{total_chunks} chunks...")
            with open(progress_file, "w", encoding="utf-8") as f:
                json.dump(tagged_chunks, f, ensure_ascii=False, indent=2)
    
    with open(final_file, "w", encoding="utf-8") as f:
        json.dump(tagged_chunks, f, ensure_ascii=False, indent=2)
    
    print("Tagging complete. Saved to tagged_chunks_final.json")
    return tagged_chunks

if __name__ == "__main__":
    from src.rag.chunking import load_and_chunk_stories
    
    chunks = load_and_chunk_stories()
    print(f"Processing {len(chunks)} chunks...")
    tagged = tag_chunks(chunks, resume=True)
    
    genre_counts = {}
    scene_counts = {}
    dialogue_counts = {}
    
    for chunk in tagged:
        g = chunk.get("genre", "unknown")
        s = chunk.get("scene_type", "unknown")
        d = chunk.get("dialogue_density", "unknown")
        genre_counts[g] = genre_counts.get(g, 0) + 1
        scene_counts[s] = scene_counts.get(s, 0) + 1
        dialogue_counts[d] = dialogue_counts.get(d, 0) + 1
    
    print(f"\nTotal tagged: {len(tagged)}")
    print(f"Genre distribution: {genre_counts}")
    print(f"Scene distribution: {scene_counts}")
    print(f"Dialogue distribution: {dialogue_counts}")
