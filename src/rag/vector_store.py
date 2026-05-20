import os
import faiss
import numpy as np
import pickle

# Step 1: Configuration for storage paths
PROCESSED_DIR = "data/processed"
INDEX_PATH = os.path.join(PROCESSED_DIR, "narrative_index.faiss")
METADATA_PATH = os.path.join(PROCESSED_DIR, "chunk_metadata.pkl")

def create_faiss_index(embedded_chunks):
    """
    Creates a FAISS index from embedded chunks and prepares metadata.
    
    Why float32? FAISS is optimized for float32 precision for both speed 
    and memory efficiency. Most embedding models output float32 or higher, 
    but FAISS specifically requires float32 for its core algorithms.
    
    What is IndexFlatL2? It is a "brute-force" exact search index that 
    calculates the L2 (Euclidean) distance between vectors. For datasets 
    of this size, it provides perfect accuracy with high speed.
    """
    embeddings_list = []
    metadata_list = []
    
    for chunk in embedded_chunks:
        # Step 2: Safe exception handling for missing or failed embeddings
        if "embedding" in chunk and chunk["embedding"] is not None:
            embeddings_list.append(chunk["embedding"])
            
            # Step 3: Remove embedding from metadata before saving
            # Why store separately? Metadata is for human/LLM readability. 
            # Keeping the huge vectors inside the pickle file would make it 
            # bloated and slow to load. FAISS handles the vectors; we only 
            # need the text and IDs in metadata.
            chunk_meta = chunk.copy()
            del chunk_meta["embedding"]
            metadata_list.append(chunk_meta)
        else:
            print(f"Skipping chunk {chunk.get('chunk_id')} due to missing embedding.")

    if not embeddings_list:
        print("Error: No valid embeddings found to index.")
        return None, []

    # Step 4: Convert list to float32 numpy matrix
    embeddings_matrix = np.array(embeddings_list).astype('float32')
    dimension = embeddings_matrix.shape[1]
    
    # Step 5: Create and populate FAISS IndexFlatL2
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_matrix)
    
    return index, metadata_list

def save_faiss_index(index, metadata, index_path=INDEX_PATH, meta_path=METADATA_PATH):
    """Saves the FAISS index and metadata to disk."""
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    # Save FAISS index
    faiss.write_index(index, index_path)
    
    # Save Metadata
    with open(meta_path, "wb") as f:
        pickle.dump(metadata, f)
    
    print(f"Index saved to {index_path}")
    print(f"Metadata saved to {meta_path}")

def load_faiss_index(index_path=INDEX_PATH, meta_path=METADATA_PATH):
    """Loads the FAISS index and metadata from disk."""
    if not os.path.exists(index_path) or not os.path.exists(meta_path):
        print("Error: Index or Metadata file not found.")
        return None, None
        
    index = faiss.read_index(index_path)
    with open(meta_path, "rb") as f:
        metadata = pickle.load(f)
        
    return index, metadata

if __name__ == "__main__":
    # Step 6: Main Testing Block
    EMBEDDED_FILE = os.path.join(PROCESSED_DIR, "embedded_chunks.pkl")
    
    if not os.path.exists(EMBEDDED_FILE):
        print(f"Error: {EMBEDDED_FILE} not found. Please run embeddings.py first.")
    else:
        # Load the embedded chunks generated in the previous stage
        with open(EMBEDDED_FILE, "rb") as f:
            all_embedded_chunks = pickle.load(f)
        
        # Test using the first 50 embedded chunks
        test_limit = 50
        print(f"Indexing first {min(test_limit, len(all_embedded_chunks))} chunks...")
        
        index, metadata = create_faiss_index(all_embedded_chunks[:test_limit])
        
        if index:
            # Step 7: Print Verification Stats
            print("\n--- Vector Store Summary ---")
            print(f"Total vectors indexed: {index.ntotal}")
            print(f"Embedding dimension: {index.d}")
            print(f"FAISS ntotal count: {index.ntotal}")
            
            # Print metadata sample
            sample = metadata[0]
            print(f"\nMetadata Sample (Chunk ID: {sample['chunk_id']}):")
            print(f"Text Preview: {sample['text'][:50]}...")
            print(f"Language: {sample['language']}")
            print(f"Has embedding key? {'embedding' in sample}")
            
            # Save the test index
            save_faiss_index(index, metadata)
            
            # Verify loading works
            loaded_index, loaded_meta = load_faiss_index()
            print(f"\nVerification: Loaded index has {loaded_index.ntotal} vectors.")
