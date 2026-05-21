import json
import random
import os

def check_metadata():
    file_path = "data/processed/tagged_chunks_final.json"
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("=" * 60)
    print("NARRATIVE IQ - METADATA VALIDATION")
    print("=" * 60)

    # 1. Statistics
    total = len(data)
    genres = {}
    scenes = {}
    densities = {}
    fallback_count = 0

    for chunk in data:
        g = chunk.get("genre", "unknown")
        s = chunk.get("scene_type", "unknown")
        d = chunk.get("dialogue_density", "unknown")
        
        genres[g] = genres.get(g, 0) + 1
        scenes[s] = scenes.get(s, 0) + 1
        densities[d] = densities.get(d, 0) + 1
        
        if g == "slice_of_life" and s == "description":
            fallback_count += 1

    print(f"Total Chunks: {total}\n")
    print("Genre Distribution:")
    for k, v in genres.items(): print(f"  - {k}: {v} ({v/total:.1%})")
    
    print("\nScene Type Distribution:")
    for k, v in scenes.items(): print(f"  - {k}: {v} ({v/total:.1%})")
    
    print("\nDialogue Density Distribution:")
    for k, v in densities.items(): print(f"  - {k}: {v} ({v/total:.1%})")

    # 2. Fallback Pollution Detection
    print("\n" + "-" * 40)
    pollution_rate = fallback_count / total
    print(f"Fallback Pattern (slice_of_life + description): {pollution_rate:.1%}")
    if pollution_rate > 0.60:
        print("WARNING: Possible fallback pollution detected from failed API batches.")
    else:
        print("SUCCESS: Data appears semantically diverse.")
    print("-" * 40 + "\n")

    # 3. Random Sampling
    random.seed(42)
    langs = ["english", "hindi", "marathi"]
    
    for lang in langs:
        lang_chunks = [c for c in data if c["language"] == lang]
        sample_size = min(len(lang_chunks), 5)
        samples = random.sample(lang_chunks, sample_size)
        
        print(f"RANDOM SAMPLES: {lang.upper()}")
        print("-" * 30)
        
        for i, s in enumerate(samples, 1):
            print(f"{i}. [{s['chunk_id']}]")
            print(f"   Genre: {s['genre']} | Scene: {s['scene_type']} | Dialogue: {s['dialogue_density']}")
            text_preview = s['text'][:250].replace('\n', ' ')
            print(f"   Text: {text_preview}...")
            print()

if __name__ == "__main__":
    check_metadata()
