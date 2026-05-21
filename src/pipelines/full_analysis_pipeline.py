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
TEST_MODE = False
TEST_LIMIT = 20

def run_analysis_pipeline(chunks_to_process):
    """
    Main loop to process narrative chunks and generate intelligence.
    Supports resuming from progress file.
    """
    total_chunks = len(chunks_to_process)
    
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
        chunk = chunks_to_process[i]
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
    # Load total raw count to check if 100% done
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        total_raw_count = len(json.load(f))
        
    if len(analyzed_data) == total_raw_count:
        print("\n[COMPLETE] 100% of dataset processed.")
        if os.path.exists(PROGRESS_FILE):
            os.remove(PROGRESS_FILE)

    # ---------------------------------------------------------
    # Final Statistics
    # ---------------------------------------------------------
    print("\n" + "="*40)
    print("ANALYSIS SUMMARY")
    print("="*40)
    print(f"Total in this run: {total_chunks}")
    print(f"Current Progress: {len(analyzed_data)}/{total_raw_count}")
    print(f"Successful in this run: {success_count}")
    print(f"Failed in this run: {fail_count}")
    
    if analyzed_data:
        labels = [obj["label"] for obj in analyzed_data]
        label_counts = {l: labels.count(l) for l in set(labels)}
        avg_score = sum(obj["combined_score"] for obj in analyzed_data) / len(analyzed_data)
        
        print(f"\nTotal Label Distribution: {label_counts}")
        print(f"Overall Average Combined Score: {avg_score:.2f}")
    
    print("\nRun Complete.")
    return analyzed_data

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run full narrative analysis pipeline.")
    parser.add_argument("--limit", type=int, help="Limit the number of NEW chunks to process in this run.")
    parser.add_argument("--all", action="store_true", help="Attempt to process the entire remaining dataset.")
    args = parser.parse_args()

    # Load input data
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
    else:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            all_chunks = json.load(f)
            
        # Determine how many to process
        if args.all:
            chunks_to_process = all_chunks
            print(f"--- RUNNING FULL PRODUCTION ANALYSIS ({len(all_chunks)} chunks) ---")
        elif args.limit:
            # We will take the next 'limit' chunks after the current progress
            current_count = 0
            if os.path.exists(PROGRESS_FILE):
                with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                    current_count = len(json.load(f))
            
            end_idx = current_count + args.limit
            chunks_to_process = all_chunks[:end_idx]
            print(f"--- RUNNING BURST ANALYSIS (Targeting up to chunk {end_idx}) ---")
        else:
            # Default to a small safe batch if no args provided
            chunks_to_process = all_chunks[:50]
            print(f"--- RUNNING SMALL BATCH (50 chunks) ---")

        run_analysis_pipeline(chunks_to_process)
