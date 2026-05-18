def split_into_paragraphs(text):
    """
    Splits raw text into a list of clean paragraphs based on double newlines.
    """
    # Split the raw text on double newlines
    raw_paragraphs = text.split("\n\n")
    
    # Strip leading/trailing whitespace from each paragraph
    stripped_paragraphs = [p.strip() for p in raw_paragraphs]
    
    # Remove any empty strings from the list
    clean_paragraphs = [p for p in stripped_paragraphs if p]
    
    return clean_paragraphs
