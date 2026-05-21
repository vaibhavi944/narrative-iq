import os
import json
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# =========================================================
# NarrativeIQ - Embeddings Pipeline
# =========================================================
# Purpose:
# Convert multilingual narrative chunks into semantic vectors
# using Sentence Transformers.
#
# Input:
# tagged_chunks_final.json
#
# Output:
# embedded_chunks.pkl
#
# Supported Languages:
# - English
# - Hindi
# - Marathi
# =========================================================

# ---------------------------------------------------------
# Step 1: Load multilingual embedding model globally
# ---------------------------------------------------------
# Why globally?
# Loading transformer models repeatedly is expensive.
# We load once into RAM and reuse throughout pipeline.
# ---------------------------------------------------------

MODEL_NAME = "intfloat/multilingual-e5-base"

print(f"Loading embedding model: {MODEL_NAME}...")
model = SentenceTransformer(MODEL_NAME)

# ---------------------------------------------------------
# Step 2: Main embedding function
# ---------------------------------------------------------

def embed_chunks(chunks, batch_size=32):
    """
    Convert chunks into semantic embeddings using resilient
    batch processing.

    Input:
    [
        {
            "text": "...",
            "language": "...",
            ...
        }
    ]

    Output:
    [
        {
            "text": "...",
            "embedding": numpy_array,
            "embedding_status": "success",
            ...
        }
    ]
    """

    embedded_chunks = []

    success_count = 0
    fail_count = 0

    total_chunks = len(chunks)

    print(f"\nGenerating embeddings for {total_chunks} chunks...")
    print(f"Batch Size: {batch_size}")

    # ---------------------------------------------------------
    # Manual batching
    # ---------------------------------------------------------

    for start_idx in range(0, total_chunks, batch_size):

        end_idx = min(start_idx + batch_size, total_chunks)

        batch = chunks[start_idx:end_idx]

        # ---------------------------------------------------------
        # E5 models require "passage: " prefix
        # ---------------------------------------------------------
        # Without this prefix retrieval quality degrades.
        # ---------------------------------------------------------

        batch_texts = [
            f"passage: {chunk['text']}"
            for chunk in batch
        ]

        try:

            # ---------------------------------------------------------
            # Generate embeddings for THIS batch only
            # ---------------------------------------------------------
            # convert_to_numpy=True returns numpy arrays
            # useful for FAISS later.
            # ---------------------------------------------------------

            batch_embeddings = model.encode(
                batch_texts,
                batch_size=batch_size,
                show_progress_bar=False,
                convert_to_numpy=True
            )

            # ---------------------------------------------------------
            # Attach embeddings back to metadata
            # ---------------------------------------------------------

            for idx, chunk in enumerate(batch):

                enriched_chunk = chunk.copy()

                enriched_chunk["embedding"] = batch_embeddings[idx]
                enriched_chunk["embedding_status"] = "success"

                embedded_chunks.append(enriched_chunk)

                success_count += 1

        except Exception as e:

            # ---------------------------------------------------------
            # IMPORTANT:
            # Only THIS batch fails.
            # Entire pipeline continues safely.
            # ---------------------------------------------------------

            print(
                f"\nError processing batch "
                f"{start_idx} -> {end_idx}: {e}"
            )

            for chunk in batch:

                failed_chunk = chunk.copy()

                failed_chunk["embedding"] = None
                failed_chunk["embedding_status"] = "failed"

                embedded_chunks.append(failed_chunk)

                fail_count += 1

        # ---------------------------------------------------------
        # Progress Logging
        # ---------------------------------------------------------

        if end_idx % 100 == 0 or end_idx == total_chunks:
            print(f"Processed {end_idx}/{total_chunks} chunks...")

    # ---------------------------------------------------------
    # Final Statistics
    # ---------------------------------------------------------

    print("\n===================================")
    print("Embedding Generation Summary")
    print("===================================")

    print(f"Total Chunks: {total_chunks}")
    print(f"Successful Embeddings: {success_count}")
    print(f"Failed Embeddings: {fail_count}")

    return embedded_chunks


# ---------------------------------------------------------
# Step 3: Save embeddings
# ---------------------------------------------------------

def save_embedded_chunks(
    embedded_chunks,
    output_path="data/processed/embedded_chunks.pkl"
):
    """
    Save embedded chunks using pickle.

    Why pickle?
    - preserves numpy arrays efficiently
    - faster than JSON for vector storage
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:

        with open(output_path, "wb") as f:
            pickle.dump(embedded_chunks, f)

        print(f"\nSaved embedded chunks to:")
        print(output_path)

    except Exception as e:
        print(f"Error saving embeddings: {e}")


# ---------------------------------------------------------
# Step 4: Main Execution Block
# ---------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate embeddings for story chunks.")
    parser.add_argument("--test", action="store_true", help="Process only a small test set (20 chunks).")
    args = parser.parse_args()

    INPUT_PATH = "data/processed/tagged_chunks_final.json"

    # ---------------------------------------------------------
    # Verify metadata pipeline output exists
    # ---------------------------------------------------------

    if not os.path.exists(INPUT_PATH):
        print(f"Error: {INPUT_PATH} not found.")
        print("Run metadata_pipeline.py first.")
    else:
        # ---------------------------------------------------------
        # Load tagged chunks
        # ---------------------------------------------------------
        with open(INPUT_PATH, "r", encoding="utf-8") as f:
            all_chunks = json.load(f)

        print(f"\nLoaded {len(all_chunks)} tagged chunks.")

        # ---------------------------------------------------------
        # Selection Logic
        # ---------------------------------------------------------
        if args.test:
            TEST_LIMIT = 20
            chunks_to_embed = all_chunks[:TEST_LIMIT]
            print(f"\nStarting embedding TEST for {len(chunks_to_embed)} chunks...")
        else:
            chunks_to_embed = all_chunks
            print(f"\nStarting FULL embedding for {len(chunks_to_embed)} chunks...")

        # ---------------------------------------------------------
        # Generate embeddings
        # ---------------------------------------------------------
        embedded_results = embed_chunks(chunks_to_embed)

        # ---------------------------------------------------------
        # Find successful sample
        # ---------------------------------------------------------
        success_sample = next(
            (
                chunk
                for chunk in embedded_results
                if chunk["embedding_status"] == "success"
            ),
            None
        )

        if success_sample:
            embedding_dim = success_sample["embedding"].shape[0]

            print("\n===================================")
            print("Sample Embedding Verification")
            print("===================================")

            print(f"Chunk ID: {success_sample['chunk_id']}")
            print(f"Language: {success_sample['language']}")
            print(f"Embedding Status: {success_sample['embedding_status']}")
            print(f"Embedding Dimension: {embedding_dim}")

            print("\nFirst 5 Embedding Values:")
            print(success_sample["embedding"][:5])

        # ---------------------------------------------------------
        # Save embeddings
        # ---------------------------------------------------------
        save_embedded_chunks(embedded_results)