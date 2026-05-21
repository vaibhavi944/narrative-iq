import os
import json
import time
from src.scoring.weakness_scorer import score_paragraph
from src.scoring.feedback_generator import generate_feedback

# =========================================================
# NarrativeIQ - Full Batch Analysis Pipeline
# =========================================================
# Purpose:
# Process all story chunks through the analysis engine
# (Pacing, Repetition, Emotion, Scoring, Feedback).
#
# Inputs:
# tagged_chunks_final.json
#
# Output:
# full_narrative_analysis.json
# =========================================================

# ---------------------------------------------------------
# Step 1: Configuration
# ---------------------------------------------------------

INPUT_FILE = "data/processed/tagged_chunks_final.json"
OUTPUT_FILE = "data/processed/full_narrative_analysis.json"
PROGRESS_FILE = "data/processed/full_narrative_analysis_progress.json"

# Set TEST_MODE = False for full production run (2654 chunks)
TEST_MODE = True
TEST_LIMIT = 20

def run_analysis_pipeline():
    """
    Main loop to process narrative chunks and generate intelligence.
    Supports resuming from progress file.
    """
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    # Load input data
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    total_chunks = len(chunks)
    
    # Apply test limit
    if TEST_MODE:
        chunks = chunks[:TEST_LIMIT]
        total_chunks = len(chunks)
        print(f"--- RUNNING IN TEST MODE ({total_chunks} chunks) ---")
    else:
        print(f"--- RUNNING FULL PRODUCTION ANALYSIS ({total_chunks} chunks) ---")

    analyzed_data = []
    start_index = 0

    # Resume logic
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                analyzed_data = json.load(f)
                start_index = len(analyzed_data)
                print(f"Resuming from chunk {start_index}...")
        except Exception as e:
            print(f"Error loading progress: {e}. Starting fresh.")
            analyzed_data = []
            start_index = 0

    if start_index >= total_chunks:
        print("All chunks in this set already processed.")
        return analyzed_data

    success_count = 0
    fail_count = 0
    
    print("\nStarting analysis loop...")
    print("=" * 40)

    for i in range(start_index, total_chunks):
        chunk = chunks[i]
        chunk_id = chunk.get("chunk_id", "unknown")
        text = chunk.get("text", "")
        language = chunk.get("language", "english")
        
        try:
            # 1. Run full analysis (Pacing, Repetition, Emotion)
            score_result = score_paragraph(text, language=language)
            
            # 2. Generate feedback/tips
            feedback = generate_feedback(score_result)
            
            # 3. Build intelligence object
            analyzed_obj = {
                "chunk_id": chunk_id,
                "language": language,
                "genre": chunk.get("genre", "unknown"),
                "scene_type": chunk.get("scene_type", "unknown"),
                "dialogue_density": chunk.get("dialogue_density", "none"),
                
                "combined_score": score_result["combined_score"],
                "label": score_result["label"],
                
                "pacing": score_result["pacing"],
                "repetition": score_result["repetition"],
                "emotion": score_result["emotion"],
                "reasons": score_result["reasons"],
                
                "feedback": feedback,
                "text": text
            }
            
            analyzed_data.append(analyzed_obj)
            success_count += 1
            
        except Exception as e:
            print(f"\n[FAIL] Chunk {chunk_id}: {e}")
            fail_count += 1
            # Add failed placeholder to maintain index if needed, 
            # or just skip. Here we skip but log.
            continue

        # Progress Logging
        processed_so_far = len(analyzed_data)
        if processed_so_far % 25 == 0 or processed_so_far == total_chunks:
            print(f"Analyzed {processed_so_far}/{total_chunks} chunks...")
            # Save progress
            with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
                json.dump(analyzed_data, f, ensure_ascii=False, indent=2)

    # Final Save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(analyzed_data, f, ensure_ascii=False, indent=2)
    
    # Cleanup progress file if finished
    if not TEST_MODE and len(analyzed_data) == total_chunks:
        if os.path.exists(PROGRESS_FILE):
            os.remove(PROGRESS_FILE)

    # ---------------------------------------------------------
    # Final Statistics
    # ---------------------------------------------------------
    print("\n" + "="*40)
    print("ANALYSIS SUMMARY")
    print("="*40)
    print(f"Total Attempted: {total_chunks}")
    print(f"Successful: {success_count}")
    print(f"Failed: {fail_count}")
    
    if analyzed_data:
        labels = [obj["label"] for obj in analyzed_data]
        label_counts = {l: labels.count(l) for l in set(labels)}
        avg_score = sum(obj["combined_score"] for obj in analyzed_data) / len(analyzed_data)
        
        print(f"\nLabel Distribution: {label_counts}")
        print(f"Average Combined Score: {avg_score:.2f}")
        
        # Print 2 samples
        print("\n--- SAMPLE ANALYZED OUTPUTS ---")
        samples = analyzed_data[:2]
        for s in samples:
            print(f"\nID: {s['chunk_id']} | Label: {s['label']} | Score: {s['combined_score']}")
            print(f"Feedback: {s['feedback']['summary']}")
            print(f"Text Preview: {s['text'][:100]}...")
    
    print("\nPipeline Complete.")
    return analyzed_data

if __name__ == "__main__":
    run_analysis_pipeline()
