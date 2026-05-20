import os
import json
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Step 1: Initialize the multilingual E5 model
MODEL_NAME = "intfloat/multilingual-e5-base"
print(f"Loading embedding model: {MODEL_NAME}...")
model = SentenceTransformer(MODEL_NAME)

def embed_chunks(chunks, batch_size=32):
    """
    Converts chunk text into semantic vector embeddings using manual batching
    and isolated exception handling for resilience.
    """
    embedded_chunks = []
    success_count = 0
    fail_count = 0
    total_chunks = len(chunks)
    
    print(f"Generating embeddings for {total_chunks} chunks in batches of {batch_size}...")
    
    # Step 2: Manual batching using range
    for i in range(0, total_chunks, batch_size):
        batch = chunks[i:i + batch_size]
        batch_end = min(i + batch_size, total_chunks)
        
        # Prepare texts with E5 specific prefix "passage: "
        batch_texts = [f"passage: {chunk['text']}" for chunk in batch]
        
        try:
            # Step 3: Compute embeddings for the isolated batch
            # We disable the built-in progress bar as we handle manual progress logging
            batch_embeddings = model.encode(
                batch_texts, 
                batch_size=len(batch), 
                show_progress_bar=False,
                convert_to_numpy=True
            )
            
            # Step 4: Map successful embeddings back to chunks
            for idx, chunk in enumerate(batch):
                new_chunk = chunk.copy()
                new_chunk["embedding"] = batch_embeddings[idx]
                new_chunk["embedding_status"] = "success"
                embedded_chunks.append(new_chunk)
                success_count += 1
                
        except Exception as e:
            # Step 5: Isolated batch-level exception handling
            print(f"Error processing batch {i} to {batch_end}: {e}")
            for chunk in batch:
                new_chunk = chunk.copy()
                new_chunk["embedding"] = None
                new_chunk["embedding_status"] = "failed"
                embedded_chunks.append(new_chunk)
                fail_count += 1
                
        # Logging progress every 100 chunks
        if batch_end % 100 == 0 or batch_end == total_chunks:
            print(f"Processed up to chunk {batch_end}/{total_chunks}...")

    # Print final embedding statistics
    print("\n--- Embedding Generation Stats ---")
    print(f"Total Successful: {success_count}")
    print(f"Total Failed: {fail_count}")
    
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
        
        # Embed a subset for testing (first 20 chunks)
        test_limit = 20
        test_chunks = all_chunks[:test_limit]
        
        print(f"Starting resilient embedding test for {len(test_chunks)} chunks...")
        results = embed_chunks(test_chunks)
        
        if results:
            # Verify results and print sample
            # Find the first successful one for sample printing
            success_sample = next((c for c in results if c["embedding_status"] == "success"), None)
            
            if success_sample:
                embedding_dim = success_sample["embedding"].shape[0]
                print(f"Embedding dimension: {embedding_dim}")
                print(f"\nSample Chunk ID: {success_sample['chunk_id']}")
                print(f"Status: {success_sample['embedding_status']}")
                print(f"First 5 embedding values: {success_sample['embedding'][:5]}")
            
            # Save results to disk
            save_embedded_chunks(results)
        else:
            print("Embedding generation failed.")
