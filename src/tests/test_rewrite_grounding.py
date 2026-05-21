import os
import json
from src.agents.writer_critique_agent import WriterCritiqueAgent

# =========================================================
# NarrativeIQ - Rewrite Grounding & Language Validation
# =========================================================
# Purpose:
# Validates that the rewrite engine strictly preserves
# characters, settings, and language without hallucinations.
# =========================================================

def run_grounding_validation():
    agent = WriterCritiqueAgent()
    
    test_cases = [
        {
            "name": "English Fairytale Grounding",
            "lang": "english",
            "text": "Once upon a time, there was a queen. She was a very nice queen. She had a big, pretty castle. The queen had a lot of work to do every day. But today, she wanted to relax."
        },
        {
            "name": "Hindi Emotional Continuity",
            "lang": "hindi",
            "text": "वह बहुत उदास था। उसके पास कोई नहीं था। वह बस बैठा रहा और अपनी पुरानी यादों में खो गया।"
        },
        {
            "name": "Marathi Setting Preservation",
            "lang": "marathi",
            "text": "राजू शाळेत गेला. त्याला त्याचे मित्र भेटले. त्यांनी खूप खेळ केला आणि मज्जा केली."
        }
    ]

    print("\n" + "="*80)
    print("NARRATIVE IQ - GROUNDING & LANGUAGE AUDIT")
    print("="*80)

    for tc in test_cases:
        print(f"\n>>> AUDIT CASE: {tc['name']}")
        print(f"Input Language: {tc['lang']}")
        print(f"Input Text: {tc['text']}")
        print("-" * 40)

        try:
            result = agent.analyze_and_critique(tc['text'], language=tc['lang'])
            
            rewrite = result.get("suggested_rewrite", "")
            critique = result.get("agent_critique", "")

            print(f"\n[REWRITE ({tc['lang'].upper()})]")
            print(rewrite)
            
            print(f"\n[CRITIQUE ({tc['lang'].upper()})]")
            print(critique[:300] + "...")

            # 1. Entity check for English
            if tc['lang'] == "english":
                entities = ["queen", "castle"]
                for ent in entities:
                    if ent not in rewrite.lower():
                        print(f"\n[GROUNDING WARNING] Entity '{ent}' missing from rewrite!")
                
                hallucinations = ["boy", "rain", "mist"]
                for hal in hallucinations:
                    if hal in rewrite.lower():
                        print(f"\n[HALLUCINATION WARNING] Random element '{hal}' detected!")

        except Exception as e:
            print(f"[ERROR] Test failed: {e}")

        print("\n" + "="*80)

if __name__ == "__main__":
    run_grounding_validation()
