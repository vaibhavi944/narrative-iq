import os
import json
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from src.rag.vector_store import load_faiss_index

# =========================================================
# NarrativeIQ - Quality-Aware Semantic Retriever
# =========================================================
# Purpose:
# Retrieve top-k semantically similar AND high-quality
# narrative benchmarks using a two-stage process:
# 1. FAISS Semantic Search (Candidate retrieval)
# 2. Quality-Aware Reranking (Benchmark selection)
# =========================================================

MODEL_NAME = "intfloat/multilingual-e5-base"
ANALYSIS_DATA_PATH = "data/processed/full_narrative_analysis.json"

# Global cache
_MODEL = None
_INDEX = None
_METADATA = None
_ANALYSIS_DB = None

def get_resources():
    """Lazy loader for model, FAISS index, and analysis intelligence."""
    global _MODEL, _INDEX, _METADATA, _ANALYSIS_DB
    
    if _MODEL is None:
        print(f"Loading embedding model: {MODEL_NAME}...")
        _MODEL = SentenceTransformer(MODEL_NAME)
        
    if _INDEX is None or _METADATA is None:
        print("Loading FAISS vector store...")
        _INDEX, _METADATA = load_faiss_index()
        
    if _ANALYSIS_DB is None:
        if os.path.exists(ANALYSIS_DATA_PATH):
            print("Loading narrative intelligence for reranking...")
            with open(ANALYSIS_DATA_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                _ANALYSIS_DB = {item["chunk_id"]: item for item in data}
        else:
            print("WARNING: Analysis database not found. Reranking will be limited.")
            _ANALYSIS_DB = {}
            
    return _MODEL, _INDEX, _METADATA, _ANALYSIS_DB

def rerank_candidates(query_embedding, candidates, user_metadata=None):
    """
    Reranks candidates based on writing quality and stylistic alignment.
    
    Weights:
    - Semantic Similarity (L2 distance based): 40%
    - Combined Quality Score: 40%
    - Label Priority (Strong bonus): 20%
    """
    _, _, _, analysis_db = get_resources()
    reranked = []

    for cand in candidates:
        chunk_id = cand["chunk_id"]
        # Default quality signals if missing from DB
        quality_data = analysis_db.get(chunk_id, {})
        
        combined_score = quality_data.get("combined_score", 0.5)
        label = quality_data.get("label", "Moderate")
        
        # 1. Semantic Component (Inverse of FAISS L2 distance)
        # Smaller distance = better. We use 1 / (1 + distance)
        semantic_score = 1.0 / (1.0 + cand["score"])
        
        # 2. Quality Component
        quality_score = combined_score
        
        # 3. Label Priority
        label_bonus = 0.0
        if label == "Strong":
            label_bonus = 1.0
        elif label == "Moderate":
            label_bonus = 0.3
            
        # 4. Stylistic Alignment (Optional bonus if metadata matches)
        style_bonus = 0.0
        if user_metadata:
            if quality_data.get("genre") == user_metadata.get("genre"):
                style_bonus += 0.2
            if quality_data.get("scene_type") == user_metadata.get("scene_type"):
                style_bonus += 0.2

        # Final Weighted Rank Score
        # (semantic * 0.4) + (quality * 0.4) + (label_bonus * 0.2) + style_bonus
        rank_score = (semantic_score * 0.4) + (quality_score * 0.4) + (label_bonus * 0.2) + style_bonus
        
        # Add explanation for logging
        cand["rerank_score"] = round(rank_score, 4)
        cand["quality_label"] = label
        cand["explanation"] = (
            f"Semantic: {semantic_score:.2f} | Quality: {quality_score:.2f} | "
            f"Label: {label} (+{label_bonus}) | Style Match: {style_bonus:.2f}"
        )
        
        # Update metadata from analysis DB for completeness
        cand.update({
            "reasons": quality_data.get("reasons", []),
            "feedback": quality_data.get("feedback", {})
        })
        
        reranked.append(cand)

    # Sort by rank score descending
    reranked.sort(key=lambda x: x["rerank_score"], reverse=True)
    return reranked

def retrieve_similar_chunks(query, top_k=5, user_metadata=None):
    """
    Quality-aware retrieval: Semantic search + Intelligence-based reranking.
    """
    model, index, metadata, _ = get_resources()
    if index is None: return []

    try:
        # Step 1: Broad semantic retrieval (fetch 20 candidates for reranking)
        formatted_query = f"query: {query}"
        query_embedding = model.encode([formatted_query], convert_to_numpy=True).astype("float32")
        
        candidate_count = max(20, top_k * 2)
        distances, indices = index.search(query_embedding, candidate_count)
        
        # Step 2: Build candidate list
        candidates = []
        for i in range(candidate_count):
            idx = indices[0][i]
            if idx == -1: continue
            
            chunk_data = metadata[idx].copy()
            candidates.append({
                "chunk_id": chunk_data["chunk_id"],
                "score": float(distances[0][i]),
                "language": chunk_data["language"],
                "genre": chunk_data.get("genre", "unknown"),
                "scene_type": chunk_data.get("scene_type", "unknown"),
                "text": chunk_data["text"]
            })

        # Step 3: Rerank based on quality signals
        reranked_results = rerank_candidates(query_embedding, candidates, user_metadata)
        
        return reranked_results[:top_k]

    except Exception as e:
        print(f"Retrieval Error: {e}")
        return []

# ---------------------------------------------------------
# Step 4: Testing & Validation
# ---------------------------------------------------------

if __name__ == "__main__":
    test_queries = [
        {"q": "emotional family conflict", "meta": {"genre": "drama", "scene_type": "emotional"}},
        {"q": "scary night in a forest", "meta": {"genre": "thriller", "scene_type": "action"}}
    ]
    
    print("\n" + "="*80)
    print("NARRATIVE IQ - QUALITY-AWARE RETRIEVAL TEST")
    print("="*80)

    for item in test_queries:
        query = item["q"]
        meta = item["meta"]
        print(f"\nQUERY: '{query}'")
        print(f"TARGET STYLE: {meta}")
        print("-" * 80)
        
        results = retrieve_similar_chunks(query, top_k=3, user_metadata=meta)
        
        for res in results:
            print(f"Rank {results.index(res)+1} | Rerank Score: {res['rerank_score']} | [{res['quality_label']}]")
            print(f"ID: {res['chunk_id']} | Language: {res['language']} | {res['genre']}/{res['scene_type']}")
            print(f"Why selected: {res['explanation']}")
            print(f"Preview: {res['text'][:150]}...")
            print("-" * 40)
            
        print("=" * 80)
