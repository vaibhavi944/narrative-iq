import json
import os

def check_score_distribution():
    file_path = "data/processed/full_narrative_analysis.json"
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found. Run the analysis pipeline first.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    total = len(data)
    if total == 0:
        print("No data found in analysis file.")
        return

    print("=" * 60)
    print("NARRATIVE IQ - SCORE DISTRIBUTION AUDIT")
    print("=" * 60)

    # 1. Label Distribution
    labels = [obj["label"] for obj in data]
    label_counts = {l: labels.count(l) for l in ["Strong", "Moderate", "Weak"]}
    
    print(f"Total Chunks Analyzed: {total}")
    print("\nLabel Distribution:")
    for label, count in label_counts.items():
        percentage = (count / total) * 100
        print(f"  - {label}: {count} ({percentage:.1f}%)")

    # 2. Strong Threshold Warning
    strong_pct = (label_counts["Strong"] / total) * 100
    if strong_pct > 60:
        print("\nWARNING: Selective calibration issue! More than 60% of chunks are 'Strong'.")
    else:
        print("\nSUCCESS: Calibration appears healthy. 'Strong' labels are selective.")

    # 3. Top 3 Strongest Chunks
    sorted_data = sorted(data, key=lambda x: x["combined_score"], reverse=True)
    
    print("\n" + "-" * 30)
    print("TOP 3 STRONGEST CHUNKS")
    print("-" * 30)
    for i, chunk in enumerate(sorted_data[:3], 1):
        print(f"{i}. [{chunk['chunk_id']}] Score: {chunk['combined_score']} | Lang: {chunk['language']}")
        print(f"   Genre: {chunk['genre']} | Scene: {chunk['scene_type']}")
        print(f"   Feedback: {chunk['feedback']['summary']}")
        print(f"   Text: {chunk['text'][:150]}...")
        print()

    # 4. Top 3 Weakest Chunks
    print("\n" + "-" * 30)
    print("TOP 3 WEAKEST CHUNKS")
    print("-" * 30)
    for i, chunk in enumerate(sorted_data[-3:][::-1], 1):
        print(f"{i}. [{chunk['chunk_id']}] Score: {chunk['combined_score']} | Lang: {chunk['language']}")
        print(f"   Reasons: {chunk['reasons']}")
        print(f"   Feedback: {chunk['feedback']['summary']}")
        print(f"   Text: {chunk['text'][:150]}...")
        print()

    print("=" * 60)

if __name__ == "__main__":
    check_score_distribution()
