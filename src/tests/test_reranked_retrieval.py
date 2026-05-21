import os
import json
import faiss
import numpy as np
from src.rag.retriever import retrieve_similar_chunks, get_resources

# =========================================================
# NarrativeIQ - Reranked Retrieval Validation
# =========================================================
# Purpose:
# Compare basic semantic retrieval with quality-aware reranking.
# Evaluates benchmark quality and thematic alignment.
# =========================================================

def basic_retrieve(query, top_k=5):
    """Simple semantic-only retrieval for comparison."""
    model, index, metadata, _ = get_resources()
    formatted_query = f"query: {query}"
    query_embedding = model.encode([formatted_query], convert_to_numpy=True).astype("float32")
    distances, indices = index.search(query_embedding, top_k)
    
    results = []
    for i in range(top_k):
        idx = indices[0][i]
        if idx == -1: continue
        results.append(metadata[idx])
    return results

def run_rerank_comparison():
    test_cases = [
        {
            "name": "Family Drama",
            "query": "a mother and daughter arguing about secrets",
            "meta": {"genre": "drama", "scene_type": "conflict"}
        },
        {
            "name": "Scary Woods",
            "query": "hearing strange noises in the dark forest",
            "meta": {"genre": "thriller", "scene_type": "description"}
        }
    ]

    print("\n" + "="*90)
    print("NARRATIVE IQ - RERANKED RETRIEVAL AUDIT")
    print("="*90)

    for tc in test_cases:
        print(f"\n>>> AUDIT CASE: {tc['name']}")
        print(f"QUERY: '{tc['query']}'")
        print(f"TARGET: {tc['meta']}")
        print("-" * 50)

        # 1. BASIC RETRIEVAL
        basic_results = basic_retrieve(tc['query'], top_k=3)
        print("\n[BASIC RETRIEVAL (Semantic Only)]")
        for i, res in enumerate(basic_results, 1):
            print(f" {i}. [{res['chunk_id']}] {res['genre']}/{res['scene_type']} | {res['text'][:80]}...")

        # 2. QUALITY-AWARE RETRIEVAL
        reranked_results = retrieve_similar_chunks(tc['query'], top_k=3, user_metadata=tc['meta'])
        print("\n[QUALITY-AWARE RERANKING]")
        for i, res in enumerate(reranked_results, 1):
            print(f" {i}. [{res['chunk_id']}] score: {res['rerank_score']} | label: {res['quality_label']}")
            print(f"    Style Match: {'genre' in res['explanation']} | Explanation: {res['explanation']}")
            print(f"    Preview: {res['text'][:120]}...")
            print()

        # 3. Quality Improvement Analysis
        basic_labels = [r.get('label', 'Unknown') for r in basic_results] # Note: basic metadata might not have label
        # (Need to fetch labels for basic results to compare)
        _, _, _, analysis_db = get_resources()
        basic_quality = [analysis_db.get(r['chunk_id'], {}).get('label', 'Unknown') for r in basic_results]
        
        reranked_quality = [res['quality_label'] for res in reranked_results]
        
        print(f"Summary Comparison:")
        print(f" -> Basic Top-3 Labels: {basic_quality}")
        print(f" -> Reranked Top-3 Labels: {reranked_quality}")
        
        strong_count_diff = reranked_quality.count("Strong") - basic_quality.count("Strong")
        if strong_count_diff > 0:
            print(f" SUCCESS: Reranking found {strong_count_diff} more 'Strong' benchmarks.")
        elif strong_count_diff == 0 and "Strong" in reranked_quality:
            print(" SUCCESS: Reranking prioritized existing 'Strong' benchmarks.")
        else:
            print(" NOTE: No quality gain in top 3 for this specific semantic neighborhood.")

        print("\n" + "="*90)

if __name__ == "__main__":
    run_rerank_comparison()
