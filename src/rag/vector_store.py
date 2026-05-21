import os
import faiss
import numpy as np
import pickle

# =========================================================
# NarrativeIQ - FAISS Vector Store
# =========================================================
# Purpose:
# Create a semantic vector database using FAISS
# from multilingual narrative embeddings.
#
# Input:
# embedded_chunks.pkl
#
# Outputs:
# narrative_index.faiss
# chunk_metadata.pkl
#
# Languages Supported:
# - English
# - Hindi
# - Marathi
# =========================================================

# ---------------------------------------------------------
# Step 1: Storage Configuration
# ---------------------------------------------------------

PROCESSED_DIR = "data/processed"

INDEX_PATH = os.path.join(
    PROCESSED_DIR,
    "narrative_index.faiss"
)

METADATA_PATH = os.path.join(
    PROCESSED_DIR,
    "chunk_metadata.pkl"
)

# ---------------------------------------------------------
# Step 2: Create FAISS Index
# ---------------------------------------------------------

def create_faiss_index(embedded_chunks):
    """
    Create FAISS vector index from embedded chunks.

    Why float32?
    -------------------------------------------------
    FAISS is optimized for float32 vectors for:
    - speed
    - memory efficiency
    - vector operations

    Why separate metadata?
    -------------------------------------------------
    FAISS stores only vectors efficiently.

    Metadata like:
    - text
    - language
    - genre
    - scene_type

    is stored separately for retrieval readability.

    What is IndexFlatL2?
    -------------------------------------------------
    Exact nearest-neighbor search using Euclidean
    distance (L2 distance).

    Good for:
    - small-medium datasets
    - high retrieval accuracy

    Our dataset:
    ~2654 chunks
    so FlatL2 is perfectly suitable.
    """

    embeddings_list = []
    metadata_list = []

    skipped_chunks = 0

    print("\nPreparing embeddings for FAISS indexing...")

    # ---------------------------------------------------------
    # Step 3: Extract valid embeddings only
    # ---------------------------------------------------------

    for chunk in embedded_chunks:

        # ---------------------------------------------------------
        # Skip failed embeddings safely
        # ---------------------------------------------------------

        if (
            chunk.get("embedding") is not None
            and chunk.get("embedding_status") == "success"
        ):

            embeddings_list.append(chunk["embedding"])

            # ---------------------------------------------------------
            # Remove embedding from metadata
            # ---------------------------------------------------------
            # We do NOT want duplicate vector storage.
            # FAISS already stores vectors internally.
            # ---------------------------------------------------------

            chunk_meta = chunk.copy()

            chunk_meta.pop("embedding", None)

            metadata_list.append(chunk_meta)

        else:

            skipped_chunks += 1

            print(
                f"Skipping chunk "
                f"{chunk.get('chunk_id')} "
                f"due to invalid embedding."
            )

    # ---------------------------------------------------------
    # Safety Check
    # ---------------------------------------------------------

    if not embeddings_list:

        print("\nERROR: No valid embeddings found.")
        return None, []

    # ---------------------------------------------------------
    # Step 4: Convert to float32 matrix
    # ---------------------------------------------------------

    embeddings_matrix = np.array(
        embeddings_list
    ).astype("float32")

    dimension = embeddings_matrix.shape[1]

    print("\nEmbedding Matrix Shape:")
    print(embeddings_matrix.shape)

    print(f"Embedding Dimension: {dimension}")

    # ---------------------------------------------------------
    # Step 5: Create FAISS Index
    # ---------------------------------------------------------

    print("\nCreating FAISS IndexFlatL2...")

    index = faiss.IndexFlatL2(dimension)

    # ---------------------------------------------------------
    # Step 6: Add vectors into FAISS
    # ---------------------------------------------------------

    print("Adding embeddings into vector index...")

    index.add(embeddings_matrix)

    print("\nFAISS indexing completed.")

    print(f"Total Indexed Vectors: {index.ntotal}")
    print(f"Skipped Chunks: {skipped_chunks}")

    return index, metadata_list


# ---------------------------------------------------------
# Step 7: Save FAISS Index + Metadata
# ---------------------------------------------------------

def save_faiss_index(
    index,
    metadata,
    index_path=INDEX_PATH,
    meta_path=METADATA_PATH
):
    """
    Save FAISS index and metadata separately.

    Why separate files?
    -------------------------------------------------
    FAISS index:
        optimized vector database

    Metadata pickle:
        readable chunk information
    """

    os.makedirs(PROCESSED_DIR, exist_ok=True)

    try:

        # ---------------------------------------------------------
        # Save FAISS vector database
        # ---------------------------------------------------------

        faiss.write_index(index, index_path)

        # ---------------------------------------------------------
        # Save metadata mapping
        # ---------------------------------------------------------

        with open(meta_path, "wb") as f:
            pickle.dump(metadata, f)

        print("\n===================================")
        print("Vector Store Saved Successfully")
        print("===================================")

        print(f"FAISS Index Path:\n{index_path}")

        print(f"\nMetadata Path:\n{meta_path}")

    except Exception as e:

        print(f"\nError saving vector store: {e}")


# ---------------------------------------------------------
# Step 8: Load FAISS Index + Metadata
# ---------------------------------------------------------

def load_faiss_index(
    index_path=INDEX_PATH,
    meta_path=METADATA_PATH
):
    """
    Load saved FAISS vector database and metadata.
    """

    if (
        not os.path.exists(index_path)
        or not os.path.exists(meta_path)
    ):

        print("\nERROR: Index or metadata file missing.")
        return None, None

    try:

        # ---------------------------------------------------------
        # Load FAISS vector database
        # ---------------------------------------------------------

        index = faiss.read_index(index_path)

        # ---------------------------------------------------------
        # Load metadata mapping
        # ---------------------------------------------------------

        with open(meta_path, "rb") as f:
            metadata = pickle.load(f)

        print("\nFAISS index loaded successfully.")

        return index, metadata

    except Exception as e:

        print(f"\nError loading vector store: {e}")

        return None, None


# ---------------------------------------------------------
# Step 9: Main Execution Block
# ---------------------------------------------------------

if __name__ == "__main__":

    EMBEDDED_FILE = os.path.join(
        PROCESSED_DIR,
        "embedded_chunks.pkl"
    )

    # ---------------------------------------------------------
    # Verify embeddings file exists
    # ---------------------------------------------------------

    if not os.path.exists(EMBEDDED_FILE):

        print(f"\nERROR: {EMBEDDED_FILE} not found.")
        print("Run embeddings.py first.")

    else:

        # ---------------------------------------------------------
        # Load embedded chunks
        # ---------------------------------------------------------

        print("\nLoading embedded chunks...")

        with open(EMBEDDED_FILE, "rb") as f:

            all_embedded_chunks = pickle.load(f)

        print(
            f"Loaded {len(all_embedded_chunks)} embedded chunks."
        )

        # ---------------------------------------------------------
        # FULL MODE
        # ---------------------------------------------------------
        # For testing:
        # FULL_MODE = False
        #
        # For production:
        # FULL_MODE = True
        # ---------------------------------------------------------

        FULL_MODE = True

        if FULL_MODE:

            chunks_to_index = all_embedded_chunks

        else:

            chunks_to_index = all_embedded_chunks[:50]

        print(
            f"\nIndexing {len(chunks_to_index)} chunks..."
        )

        # ---------------------------------------------------------
        # Create FAISS index
        # ---------------------------------------------------------

        index, metadata = create_faiss_index(
            chunks_to_index
        )

        # ---------------------------------------------------------
        # Verification
        # ---------------------------------------------------------

        if index is not None:

            print("\n===================================")
            print("Vector Store Summary")
            print("===================================")

            print(f"Total Indexed Vectors: {index.ntotal}")

            print(f"Embedding Dimension: {index.d}")

            print(f"Metadata Entries: {len(metadata)}")

            # ---------------------------------------------------------
            # Metadata sample verification
            # ---------------------------------------------------------

            sample = metadata[0]

            print("\nMetadata Sample")
            print("-----------------------------------")

            print(f"Chunk ID: {sample['chunk_id']}")

            print(f"Language: {sample['language']}")

            print(f"Genre: {sample.get('genre')}")

            print(f"Scene Type: {sample.get('scene_type')}")

            print(
                f"\nText Preview:\n"
                f"{sample['text'][:200]}..."
            )

            print(
                f"\nContains Embedding Key?\n"
                f"{'embedding' in sample}"
            )

            # ---------------------------------------------------------
            # Save vector store
            # ---------------------------------------------------------

            save_faiss_index(index, metadata)

            # ---------------------------------------------------------
            # Verify loading works
            # ---------------------------------------------------------

            loaded_index, loaded_metadata = load_faiss_index()

            if loaded_index is not None:

                print("\n===================================")
                print("Load Verification Successful")
                print("===================================")

                print(
                    f"Loaded FAISS vectors: "
                    f"{loaded_index.ntotal}"
                )

                print(
                    f"Loaded metadata entries: "
                    f"{len(loaded_metadata)}"
                )
