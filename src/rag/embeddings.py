import os
import json
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Step 1: Initialize the multilingual E5 model
# We load it globally to ensure it's only loaded into memory once.
# Model 'intfloat/multilingual-e5-base' is excellent for English, Hindi, and Marathi.
MODEL_NAME = "intfloat/multilingual-e5-base"
print(f"Loading embedding model: {MODEL_NAME}...")
model = SentenceTransformer(MODEL_NAME)

def embed_chunks(chunks, batch_size=32):
    """
    Converts chunk text into semantic vector embeddings.
    Metadata is preserved, and embeddings are added as numpy arrays.
    """
    embedded_chunks = []
    texts_to_embed = []
    
    # Step 2: Prepare texts with E5 specific prefix
    # E5 models require "passage: " prefix for asymmetric retrieval tasks.
    for chunk in chunks:
        texts_to_embed.append(f"passage: {chunk['text']}")
    
    print(f"Generating embeddings for {len(chunks)} chunks...")
    
    try:
        # Step 3: Compute embeddings in batches for efficiency
        # batch_size=32 is a good balance for CPU/GPU memory.
        embeddings = model.encode(
            texts_to_embed, 
            batch_size=batch_size, 
            show_progress_bar=True,
            convert_to_numpy=True
        )
        
        # Step 4: Map embeddings back to their respective chunks
        for i, chunk in enumerate(chunks):
            # We create a copy to avoid mutating the input list if needed,
            # though here we are adding a new key 'embedding'.
            new_chunk = chunk.copy()
            new_chunk["embedding"] = embeddings[i]
            embedded_chunks.append(new_chunk)
            
            # Step 5: Logging progress every 100 chunks
            if (i + 1) % 100 == 0:
                print(f"Processed {i + 1} embeddings...")
                
    except Exception as e:
        print(f"Critical error during embedding generation: {e}")
        # In a real pipeline, you might want to handle partial failures differently,
        # but here we skip the failed batch/operation.
        return []

    return embedded_chunks

def save_embedded_chunks(embedded_chunks, output_path="data/processed/embedded_chunks.pkl"):
    """
    Saves the list of chunks (including numpy embeddings) to a pickle file.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        with open(output_path, "wb") as f:
            pickle.dump(embedded_chunks, f)
        print(f"Successfully saved embedded chunks to {output_path}")
    except Exception as e:
        print(f"Error saving pickle file: {e}")

if __name__ == "__main__":
    # Step 6: Main Testing Block
    INPUT_PATH = "data/processed/tagged_chunks_final.json"
    
    if not os.path.exists(INPUT_PATH):
        print(f"Error: {INPUT_PATH} not found. Please run the metadata pipeline first.")
    else:
        # Load tagged chunks
        with open(INPUT_PATH, "r", encoding="utf-8") as f:
            all_chunks = json.load(f)
        
        # Step 7: Embed a subset for testing (first 20 chunks)
        test_limit = 20
        test_chunks = all_chunks[:test_limit]
        
        print(f"Starting test embedding for {len(test_chunks)} chunks...")
        results = embed_chunks(test_chunks)
        
        if results:
            # Step 8: Verify results and print stats
            total_created = len(results)
            embedding_dim = results[0]["embedding"].shape[0]
            
            print("\n--- Embedding Generation Summary ---")
            print(f"Total embeddings created: {total_created}")
            print(f"Embedding dimension: {embedding_dim}")
            
            # Sample output
            sample = results[0]
            print(f"\nSample Chunk ID: {sample['chunk_id']}")
            print(f"Language: {sample['language']}")
            print(f"First 5 embedding values: {sample['embedding'][:5]}")
            
            # Save results to disk
            save_embedded_chunks(results)
        else:
            print("Embedding generation failed.")
