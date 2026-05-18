import re
import nltk

# Ensure NLTK punkt is downloaded for sentence tokenization
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

def get_pacing_score(paragraph, language="english"):
    """
    Analyzes narrative pacing by calculating average sentence length,
    variance, and a categorical pacing score.
    """
    
    # Handle English sentence tokenization
    if language.lower() == "english":
        sentences = nltk.sent_tokenize(paragraph)
    # Handle Hindi and Marathi using regex for traditional punctuation (। ? !)
    elif language.lower() in ["hindi", "marathi"]:
        sentences = re.split(r'[।?!]', paragraph)
    # Basic fallback split
    else:
        sentences = paragraph.split('.')

    # Strip and remove empty sentences after splitting
    clean_sentences = [s.strip() for s in sentences if s.strip()]

    # If no sentences found return default empty structure
    if not clean_sentences:
        return {"avg_sentence_length": 0, "variance": 0, "pacing_score": 0.5}

    # Count words in each sentence by splitting on spaces
    sentence_lengths = [len(s.split()) for s in clean_sentences]
    count = len(sentence_lengths)

    # Calculate average sentence length
    avg_length = sum(sentence_lengths) / count

    # Calculate variance in sentence lengths
    # Formula: sum of (each length minus average) squared, divided by count
    sum_sq_diff = sum((length - avg_length) ** 2 for length in sentence_lengths)
    variance = sum_sq_diff / count

    # Pacing score logic based on avg and variance thresholds
    if avg_length > 25:
        pacing_score = 0.3
    elif variance < 2:
        pacing_score = 0.4
    elif 10 <= avg_length <= 20 and variance > 5:
        pacing_score = 0.8
    else:
        pacing_score = 0.5

    # Return a dictionary with exact keys and rounded values
    return {
        "avg_sentence_length": round(avg_length, 2),
        "variance": round(variance, 2),
        "pacing_score": pacing_score
    }
