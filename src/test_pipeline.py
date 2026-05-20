import os
from dotenv import load_dotenv
from src.utils.text_splitter import split_into_paragraphs
from src.scoring.weakness_scorer import score_paragraph
from src.scoring.feedback_generator import generate_feedback

# Step 2 - Create three sample test chapters
# English chapter with intentional weaknesses
english_chapter = """He walked to the door. He opened the door. He looked outside the door and saw the car. The car was red. The car was fast. The car was parked on the street.

The long and winding road stretched out before them for miles and miles without any sign of a single resting place or a source of water to quench their growing thirst which was becoming unbearable in the heat of the afternoon sun that beat down upon them relentlessly. They continued walking slowly and methodically.

The man sat on the chair. He looked at the wall. The wall was white. He waited for the clock to tick. It was three o'clock. Nothing happened.

She turned slowly, her breath catching as the first light of dawn broke over the mountains. It was quiet — beautifully, achingly quiet. For the first time in years, she felt something loosen in her chest. She was free."""

# Hindi chapter with intentional weaknesses (repeated starters 'वह', slow descriptive)
hindi_chapter = """वह बाजार जा रही थी। वह सब्जी खरीदने वाली थी। वह बहुत धीरे चल रही थी क्योंकि उसके पैर में चोट लगी थी। बाजार बहुत दूर था।

सूरज की रोशनी चारों तरफ फैली हुई थी और हवा बहुत धीरे-धीरे चल रही थी जिससे पत्तों की आवाज आ रही थी जो कानों को सुकून दे रही थी पर रास्ते की धूल आँखों में जा रही थी। वह अपनी ओढ़नी से चेहरा ढंकने की कोशिश कर रही थी।

बाजार में बहुत भीड़ थी। लोग शोर मचा रहे थे। सामान की कीमतें बढ़ गई थीं। वह बस खड़ी होकर सब देख रही थी। उसे कुछ समझ नहीं आ रहा था।"""

# Marathi chapter with intentional weaknesses (slow pacing, repeated words)
marathi_chapter = """तो घरी चालला होता. तो खूप थकला होता. तो हळूहळू चालत होता कारण रस्ता खूप खराब होता आणि अंधार पडत होता. त्याला भीती वाटत होती.

रस्त्यावर खूप शांतता होती आणि लांबवर कोणीही दिसत नव्हते फक्त झाडांची सळसळ ऐकू येत होती जी खूप अस्वस्थ करणारी होती आणि गार वारा सुटला होता जो अंगाला झोंबत होता. त्याला लवकर घरी पोहोचायचे होते.

घर अजून लांब होते. तो थांबला. त्याने मागे वळून पाहिले. मागे कोणीच नव्हते. तो पुन्हा चालायला लागला. त्याला खूप घाम आला होता."""

def run_pipeline_test():
    # Step 3 - Create a list of tuples for test cases
    test_cases = [
        (english_chapter, "english"),
        (hindi_chapter, "hindi"),
        (marathi_chapter, "marathi")
    ]

    # Step 4 - Loop through each test case
    for chapter_text, language in test_cases:
        print(f"========================================")
        print(f"Testing Language: {language.upper()}")
        print(f"========================================\n")
        
        # Split into paragraphs
        paragraphs = split_into_paragraphs(chapter_text)
        
        counts = {"Strong": 0, "Moderate": 0, "Weak": 0}
        
        # Loop through each paragraph
        for i, para in enumerate(paragraphs, 1):
            # Call score_paragraph with correct language
            score_result = score_paragraph(para, language=language)
            
            # Call generate_feedback on result
            feedback = generate_feedback(score_result, language=language)
            
            # Print clearly
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
            
            # Track counts
            counts[feedback['label']] += 1
            
        # Step 5 - Print summary for the language
        print(f"--- {language.upper()} Summary ---")
        print(f"Total paragraphs: {len(paragraphs)}")
        print(f"Strong: {counts['Strong']}")
        print(f"Moderate: {counts['Moderate']}")
        print(f"Weak: {counts['Weak']}\n")

if __name__ == "__main__":
    # Load environment variables for Groq API (required for Hindi/Marathi)
    load_dotenv()
    
    run_pipeline_test()
