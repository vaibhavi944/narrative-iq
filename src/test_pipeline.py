from src.utils.text_splitter import split_into_paragraphs
from src.scoring.weakness_scorer import score_paragraph
from src.scoring.feedback_generator import generate_feedback

def run_test():
    # Step 2 - Create a sample test chapter string with 4 paragraphs
    # Paragraph 1: Repetitive
    # Paragraph 2: Slow pacing (long sentences)
    # Paragraph 3: Emotionally flat
    # Paragraph 4: Strong/Well-balanced
    sample_chapter = """He walked to the door. He opened the door. He looked outside the door and saw the car. The car was red. The car was fast. The car was parked on the street.

The long and winding road stretched out before them for miles and miles without any sign of a single resting place or a source of water to quench their growing thirst which was becoming unbearable in the heat of the afternoon sun that beat down upon them relentlessly. They continued walking slowly and methodically as if they were machines programmed to move forward regardless of the obstacles that lay in their path or the exhaustion that threatened to overwhelm their spirits.

The man sat on the chair. He looked at the wall. The wall was white. He waited for the clock to tick. It was three o'clock. Nothing happened.

The shadows lengthened across the cobblestone street as Elena quickened her pace, her heart hammering against her ribs like a trapped bird. She knew they were close; the scent of damp earth and woodsmoke always heralded their arrival. One wrong turn could mean the end, yet she felt a strange surge of hope as she reached for the silver locket tucked beneath her cloak."""

    # Step 3 - Split into paragraphs
    paragraphs = split_into_paragraphs(sample_chapter)
    
    counts = {"Strong": 0, "Moderate": 0, "Weak": 0}

    # Step 4 - Loop through each paragraph and analyze
    for i, para in enumerate(paragraphs, 1):
        # Call score_paragraph
        score_result = score_paragraph(para, language="english")
        
        # Call generate_feedback
        feedback = generate_feedback(score_result, language="english")
        
        # Print results clearly
        print(f"--- Paragraph {i} ---")
        print(f"Text: {para[:80]}...")
        print(f"Label: {feedback['label']}")
        print(f"Score: {feedback['combined_score']}")
        print(f"Reasons: {', '.join(score_result['reasons'])}")
        print(f"Summary: {feedback['summary']}")
        print("Tips:")
        for tip in feedback['tips']:
            print(f"  - {tip}")
        print("\n")
        
        # Track counts for final summary
        counts[feedback['label']] += 1

    # Step 5 - Final summary
    print("--- Final Summary ---")
    print(f"Total paragraphs: {len(paragraphs)}")
    print(f"Strong: {counts['Strong']}")
    print(f"Moderate: {counts['Moderate']}")
    print(f"Weak: {counts['Weak']}")

if __name__ == "__main__":
    # Load environment variables if needed for Groq (though this test is English only)
    # import os
    # from dotenv import load_dotenv
    # load_dotenv()
    
    run_test()
