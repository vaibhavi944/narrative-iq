from src.agents.writer_critique_agent import WriterCritiqueAgent

def test_grounding():
    agent = WriterCritiqueAgent()
    
    # Test case 1: Hallucination check (English)
    user_text = "The boy sat on the bench. He was waiting for his mother. She was late."
    # Benchmark is a fantasy scene (potentially distracting)
    benchmark = {"text": "The dragon soared over the burning kingdom, its scales shimmering like obsidian as it let out a roar that shook the very foundations of the earth."}
    
    print("\n--- TEST: HALLUCINATION CHECK (English) ---")
    print(f"User: {user_text}")
    print(f"Benchmark: {benchmark['text'][:100]}...")
    
    rewrite = agent.generate_rewrite(user_text, benchmark, language="english")
    print(f"Rewrite: {rewrite}")
    
    # Test case 2: Language Locking (Hindi)
    user_text_hi = "वह बेंच पर बैठा था। वह अपनी माँ का इंतज़ार कर रहा था। वह लेट थी।"
    print("\n--- TEST: LANGUAGE LOCKING (Hindi) ---")
    print(f"User: {user_text_hi}")
    
    rewrite_hi = agent.generate_rewrite(user_text_hi, benchmark, language="hindi")
    print(f"Rewrite: {rewrite_hi}")
    
    # Test case 3: Language Locking (Marathi)
    user_text_mr = "तो बाकावर बसला होता. तो त्याच्या आईची वाट पाहत होता. तिला उशीर झाला होता."
    print("\n--- TEST: LANGUAGE LOCKING (Marathi) ---")
    print(f"User: {user_text_mr}")
    
    rewrite_mr = agent.generate_rewrite(user_text_mr, benchmark, language="marathi")
    print(f"Rewrite: {rewrite_mr}")

if __name__ == "__main__":
    test_grounding()
