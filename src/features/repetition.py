import re
import nltk
from collections import Counter

# Ensure NLTK punkt is downloaded for sentence tokenization
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

def get_repetition_score(paragraph, language="english"):
    """
    Analyzes a paragraph for various types of repetition:
    - Repeated sentence starters
    - Repeated content words (ignoring stopwords)
    - Repeated bigrams
    Calculates a score from 1.0 (no repetition) down to 0.0.
    """
    
    # Step 1 - Split paragraph into sentences
    if language.lower() == "english":
        sentences = nltk.sent_tokenize(paragraph)
    elif language.lower() in ["hindi", "marathi"]:
        sentences = re.split(r'[।?!]', paragraph)
    else:
        sentences = paragraph.split('.')
    
    # Clean empty sentences
    clean_sentences = [s.strip() for s in sentences if s.strip()]
    
    # Step 2 - Detect repeated sentence starters
    starters = []
    for s in clean_sentences:
        words = s.split()
        if words:
            # Take the first word of each sentence
            starters.append(words[0])
    
    starter_counts = Counter(starters)
    # Flag starters appearing more than twice
    repeated_starters = [word for word, count in starter_counts.items() if count > 2]

    # Step 3 - Detect repeated words in full paragraph
    # Split full paragraph into words and lowercase
    all_words = re.findall(r'\w+', paragraph.lower())
    # Filter to remove single character words
    all_words = [w for w in all_words if len(w) > 1]

    # Define stopwords for each language
    stopwords_map = {
        "english": ["the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "is", "was", "it", "he", "she", "they", "his", "her", "that", "this", "as", "by"],
        "hindi": ["और", "में", "के", "की", "का", "पर", "से", "को", "है", "था", "एक", "यह", "वह", "भी", "तो", "ने", "हैं", "थे", "जो", "कि"],
        "marathi": ["आणि", "मध्ये", "च्या", "ला", "ने", "तो", "ती", "हे", "होते", "आहे", "एक", "या", "त्या", "पण", "की", "म्हणून"]
    }
    
    current_stopwords = stopwords_map.get(language.lower(), [])
    # Remove common stopwords
    content_words = [w for w in all_words if w not in current_stopwords]
    
    word_counts = Counter(content_words)
    # Flag words appearing more than twice
    repeated_words = [word for word, count in word_counts.items() if count > 2]

    # Step 4 - Detect repeated bigrams
    bigrams = []
    # Create bigrams from the lowercase word list (including all words for structure)
    raw_words = paragraph.lower().split()
    for i in range(len(raw_words) - 1):
        bigram = f"{raw_words[i]} {raw_words[i+1]}"
        bigrams.append(bigram)
    
    bigram_counts = Counter(bigrams)
    # Flag bigrams appearing more than once
    repeated_bigrams = [bg for bg, count in bigram_counts.items() if count > 1]

    # Step 5 - Calculate repetition score between 0 and 1
    # Start with base score 1.0
    score = 1.0
    
    # Penalize for each type of repetition
    score -= len(repeated_starters) * 0.15
    score -= len(repeated_words) * 0.1
    score -= len(repeated_bigrams) * 0.1
    
    # Clamp final score between 0 and 1
    final_score = max(0.0, min(1.0, score))

    # Step 6 - Return dictionary with exact keys
    return {
        "repeated_starters": repeated_starters,
        "repeated_words": repeated_words,
        "repeated_bigrams": repeated_bigrams,
        "repetition_score": round(float(final_score), 2)
    }
