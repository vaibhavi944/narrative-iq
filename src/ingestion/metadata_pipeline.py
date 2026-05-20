import os
import json
import time
from groq import Groq
from dotenv import load_dotenv

# Step 1: Import required libraries and load environment variables
load_dotenv(override=True)

# Step 2: Create Groq client and setup output directory
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
PROCESSED_DIR = "data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

def tag_chunks(chunks):
    """
    Analyzes story paragraphs in batches of 10 using Groq.
    Adds metadata tags for genre, scene type, and dialogue density.
    """
    tagged_chunks = []
    batch_size = 10
    total_chunks = len(chunks)
    
    # Progress paths
    progress_file = os.path.join(PROCESSED_DIR, "tagged_chunks_progress.json")
    final_file = os.path.join(PROCESSED_DIR, "tagged_chunks_final.json")

    # Step 3: Process chunks in batches of 10
    for i in range(0, total_chunks, batch_size):
        batch = chunks[i:i + batch_size]
        batch_copies = [chunk.copy() for chunk in batch] # Fix 4: Avoid mutating original
        
        # Prepare batch prompt
        paragraphs_text = ""
        for idx, chunk in enumerate(batch_copies):
            paragraphs_text += f"{idx + 1}. {chunk['text']}\n\n"
            
        prompt = f"""Analyze these story paragraphs and return a JSON array.
Each array item must contain EXACTLY:
- genre: one of [romance, thriller, drama, fantasy, slice_of_life]
- scene_type: one of [action, emotional, dialogue, description, conflict]
- dialogue_density: one of [high, medium, low, none]

Return one JSON object per paragraph in the SAME ORDER.

Paragraphs:
{paragraphs_text}

Return ONLY the JSON array.
No explanation.
No markdown."""

        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            
            # Fix 2: Add rate limit protection
            time.sleep(1)
            
            response_text = completion.choices[0].message.content.strip()
            
            # Fix 5: Safer markdown cleanup
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            batch_tags = json.loads(response_text)
            
            # Step 4: Parse JSON response and add metadata
            for idx, chunk in enumerate(batch_copies):
                # Fix 6: Fallback defaults
                genre = "slice_of_life"
                scene_type = "description"
                dialogue_density = "none"
                
                if idx < len(batch_tags):
                    tags = batch_tags[idx]
                    genre = tags.get("genre", genre)
                    scene_type = tags.get("scene_type", scene_type)
                    dialogue_density = tags.get("dialogue_density", dialogue_density)
                
                chunk["genre"] = genre
                chunk["scene_type"] = scene_type
                chunk["dialogue_density"] = dialogue_density
                
        except Exception as e:
            print(f"Error processing batch starting at {i}: {e}")
            # Fallback for entire batch
            for chunk in batch_copies:
                chunk["genre"] = "slice_of_life"
                chunk["scene_type"] = "description"
                chunk["dialogue_density"] = "none"
            
        tagged_chunks.extend(batch_copies)
        
        # Step 5: Print progress every 100 chunks and save progress
        processed_count = i + len(batch)
        if processed_count % 100 == 0 or processed_count == total_chunks:
            print(f"Tagged {processed_count}/{total_chunks} chunks...")
            # Fix 3: Add progress saving
            with open(progress_file, "w", encoding="utf-8") as f:
                json.dump(tagged_chunks, f, ensure_ascii=False, indent=2)
            
    # Fix 7: Final output
    with open(final_file, "w", encoding="utf-8") as f:
        json.dump(tagged_chunks, f, ensure_ascii=False, indent=2)
        
    # Step 6: Return tagged chunks list
    return tagged_chunks

# Step 7: Add main block to test
if __name__ == "__main__":
    from src.rag.chunking import load_and_chunk_stories
    
    chunks = load_and_chunk_stories()
    
    # For testing, we process 20 chunks (2 batches)
    test_limit = 20
    print(f"Tagging {test_limit} chunks for testing...")
    tagged = tag_chunks(chunks[:test_limit])
    
    # Statistical analysis
    genre_counts = {}
    scene_counts = {}
    
    for chunk in tagged:
        g = chunk["genre"]
        s = chunk["scene_type"]
        genre_counts[g] = genre_counts.get(g, 0) + 1
        scene_counts[s] = scene_counts.get(s, 0) + 1
        
    print(f"\nTotal tagged chunks: {len(tagged)}")
    
    print("\nGenre Counts:")
    for g, count in genre_counts.items():
        print(f" - {g}: {count}")
        
    print("\nScene Type Counts:")
    for s, count in scene_counts.items():
        print(f" - {s}: {count}")

    print("\nSample Tagged Chunks (Top 2):")
    for chunk in tagged[:2]:
        print(json.dumps(chunk, indent=2, ensure_ascii=False))
        print("-" * 20)
