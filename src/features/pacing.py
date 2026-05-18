import re
import nltk

# Ensure NLTK punkt is downloaded for sentence tokenization
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

def get_pacing_score(paragraph, language="english"):
    """
    Calculates the pacing score (average sentence length) of a paragraph.
    Lower scores indicate faster pacing, while higher scores indicate slower, more descriptive pacing.
    """
    sentences = []

    # Handle English sentence tokenization
    if language.lower() == "english":
        sentences = nltk.sent_tokenize(paragraph)
    
    # Handle Hindi and Marathi using regex for traditional punctuation (। ? !)
    elif language.lower() in ["hindi", "marathi"]:
        # Split on Danda (।), question mark, and exclamation mark
        sentences = re.split(r'[।?!]', paragraph)
    
    # Default fallback for other languages (basic period split)
    else:
        sentences = paragraph.split('.')

    # Strip whitespace and remove empty sentences
    clean_sentences = [s.strip() for s in sentences if s.strip()]

    if not clean_sentences:
        return 0.0

    # Count words in each sentence by splitting on spaces
    sentence_lengths = [len(s.split()) for s in clean_sentences]

    # Calculate average sentence length across all sentences
    average_length = sum(sentence_lengths) / len(clean_sentences)

    return float(average_length)
