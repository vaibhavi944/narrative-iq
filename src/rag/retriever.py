import os
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from src.rag.vector_store import load_faiss_index

# =========================================================
# NarrativeIQ - Semantic Retriever
# =========================================================
# Purpose:
# Retrieve top-k semantically similar story chunks from
# the FAISS vector database using multilingual queries.
#
# Model:
# intfloat/multilingual-e5-base
# =========================================================

# ---------------------------------------------------------
# Step 1: Model & Data Configuration
# ---------------------------------------------------------

MODEL_NAME = "intfloat/multilingual-e5-base"

# Global model and index cache
_MODEL = None
_INDEX = None
_METADATA = None

def get_resources():
    """
    Lazy loader for the embedding model and FAISS index.
    Ensures they are only loaded into RAM once.
    """
    global _MODEL, _INDEX, _METADATA
    
    if _MODEL is None:
        print(f"Loading embedding model: {MODEL_NAME}...")
        _MODEL = SentenceTransformer(MODEL_NAME)
        
    if _INDEX is None or _METADATA is None:
        print("Loading FAISS vector store...")
        _INDEX, _METADATA = load_faiss_index()
        
    return _MODEL, _INDEX, _METADATA

# ---------------------------------------------------------
# Step 2: Retrieval Function
# ---------------------------------------------------------

def retrieve_similar_chunks(query, top_k=5):
    """
    Finds the most semantically relevant story chunks for a given query.
    
    Args:
        query (str): The search query (can be English, Hindi, or Marathi).
        top_k (int): Number of results to return.
        
    Returns:
        list: A list of dictionaries containing rank, score, and metadata.
    """
    model, index, metadata = get_resources()
    
    if index is None or metadata is None:
        return []

    try:
        # ---------------------------------------------------------
        # E5 Model Requirement: Queries MUST start with "query: "
        # ---------------------------------------------------------
        formatted_query = f"query: {query}"
        
        # 1. Generate query embedding
        query_embedding = model.encode(
            [formatted_query],
            convert_to_numpy=True
        ).astype("float32")
        
        # 2. Search FAISS index (L2 distance)
        # distances is a 2D array [1, top_k], indices is [1, top_k]
        distances, indices = index.search(query_embedding, top_k)
        
        # 3. Format results
        results = []
        for i in range(top_k):
            idx = indices[0][i]
            if idx == -1: # FAISS returns -1 if not enough results
                continue
                
            chunk_data = metadata[idx].copy()
            results.append({
                "rank": i + 1,
                "score": float(distances[0][i]),
                "chunk_id": chunk_data["chunk_id"],
                "language": chunk_data["language"],
                "genre": chunk_data.get("genre", "N/A"),
                "scene_type": chunk_data.get("scene_type", "N/A"),
                "text": chunk_data["text"]
            })
            
        return results

    except Exception as e:
        print(f"Retrieval Error: {e}")
        return []

# ---------------------------------------------------------
# Step 3: Main Testing Block
# ---------------------------------------------------------

if __name__ == "__main__":
    test_queries = [
        "emotional family conflict",
        "mysterious night sounds",
        "mother preparing dinner",
        "magical forest adventure"
    ]
    
    print("\n" + "="*70)
    print("NARRATIVE IQ - SEMANTIC RETRIEVAL TEST")
    print("="*70)

    for query in test_queries:
        print(f"\nQUERY: '{query}'")
        print("-" * 70)
        
        results = retrieve_similar_chunks(query, top_k=3)
        
        if not results:
            print("No matching chunks found.")
            continue
            
        for res in results:
            print(f"Rank {res['rank']} | Score: {res['score']:.4f}")
            print(f"[{res['language'].upper()}] {res['chunk_id']} | {res['genre']} | {res['scene_type']}")
            
            # Print first 250 chars of text
            preview = res['text'].replace('\n', ' ')
            if len(preview) > 250:
                preview = preview[:247] + "..."
            print(f"Text: {preview}")
            print("-" * 30)
            
        print("=" * 70)
