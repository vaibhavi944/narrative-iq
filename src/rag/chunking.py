import os
import glob
from pathlib import Path

# Configuration for data directories
BASE_DATA_DIR = "data/raw_stories"
LANG_DIRS = {
    "english": "eng",
    "hindi": "hin",
    "marathi": "mar"
}

def load_and_chunk_stories():
    """
    Recursively reads all .txt story files, splits them into paragraphs,
    and returns a list of dictionaries containing chunks and metadata.
    """
    all_chunks = []
    
    # Iterate through each language directory
    for lang, prefix in LANG_DIRS.items():
        search_path = os.path.join(BASE_DATA_DIR, lang, "*.txt")
        files = glob.glob(search_path)
        
        for file_path in files:
            # Extract story number from filename (e.g., story_001.txt -> 001)
            filename = Path(file_path).name
            story_no = filename.split("_")[1].split(".")[0]
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Split into paragraphs using double newlines and clean up
                paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
                
                # Process each paragraph as a chunk
                for idx, para in enumerate(paragraphs):
                    para_no = f"{idx + 1:02d}"
                    chunk_id = f"{prefix}_{story_no}_{para_no}"
                    
                    # Create the chunk dictionary with exact keys
                    chunk = {
                        "chunk_id": chunk_id,
                        "text": para,
                        "language": lang,
                        "source_file": filename,
                        "word_count": len(para.split())
                    }
                    all_chunks.append(chunk)
                    
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                
    return all_chunks

if __name__ == "__main__":
    # Header for the test run
    print("-" * 30)
    print("NarrativeIQ Chunking Test")
    print("-" * 30)
    
    # Run the chunking pipeline
    chunks = load_and_chunk_stories()
    
    # Statistics gathering
    total_chunks = len(chunks)
    counts_by_lang = {}
    for c in chunks:
        lang = c["language"]
        counts_by_lang[lang] = counts_by_lang.get(lang, 0) + 1
        
    # Print results
    print(f"Total chunks created: {total_chunks}")
    print("Chunks per language:")
    for lang, count in counts_by_lang.items():
        print(f" - {lang.capitalize()}: {count}")
    
    print("\nSample Chunks (First 2):")
    print("-" * 30)
    for i in range(min(2, total_chunks)):
        sample = chunks[i]
        print(f"Chunk ID: {sample['chunk_id']}")
        print(f"File: {sample['source_file']} | Lang: {sample['language']}")
        print(f"Words: {sample['word_count']}")
        print(f"Text Preview: {sample['text'][:100]}...")
        print("-" * 15)
