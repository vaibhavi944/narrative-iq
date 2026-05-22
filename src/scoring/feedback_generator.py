def generate_feedback(score_result, language="english"):
    """
    Generates user-friendly feedback and actionable tips based on scoring results.
    Calibrated for realistic and context-aware feedback in English, Hindi, and Marathi.
    """

    # Step 1 - Extract data from score_result
    label = score_result["label"]
    reasons = score_result["reasons"]
    pacing_score = score_result["pacing"]["pacing_score"]
    repetition_data = score_result["repetition"]
    emotion_score = score_result["emotion"]["emotion_score"]
    combined_score = score_result["combined_score"]

    # Translation Map
    translations = {
        "english": {
            "Strong": "Strong",
            "Moderate": "Moderate",
            "Weak": "Weak",
            "Strong_Summary": "This section is strong. The pacing and word choice work together effectively to create a professional narrative tone.",
            "Weak_Repetition": "This paragraph feels repetitive, which distracts from the story. Focusing on word variety will help.",
            "Weak_Simplistic": "The writing here is a bit too simple. Adding complexity to your sentence structures will improve the rhythm.",
            "Weak_General": "This section needs more development in its structure and emotional depth to keep readers engaged.",
            "Moderate_Repetition": "The scene communicates clearly, but repetitive wording reduces narrative richness.",
            "Moderate_General": "This is a solid foundation, but there's room to improve the rhythmic flow and emotional resonance.",
            "Tip_Pacing_Long": "Your sentences are very long and uniform. Try breaking them up with shorter punchy sentences to create rhythm.",
            "Tip_Pacing_Slow": "Your pacing feels slightly slow. Mix short and long sentences to create a natural reading flow.",
            "Tip_Repetition_Starters": "Several sentences start with the same word: {items}. Try varying your sentence openings.",
            "Tip_Repetition_Words": "These words appear too frequently: {items}. Replace some with synonyms.",
            "Tip_Repetition_Phrases": "This phrase repeats too often: {items}. Rephrase some occurrences.",
            "Tip_Emotion": "Consider adding more sensory details or internal character thoughts to deepen the emotional impact.",
            "Tip_Generic": "Try experimenting with more expressive imagery to elevate the prose.",
            "Tip_Strong": "Well-balanced prose. Maintain this level of variety in the rest of your chapter."
        },
        "hindi": {
            "Strong": "मजबूत",
            "Moderate": "मध्यम",
            "Weak": "कमजोर",
            "Strong_Summary": "यह खंड बहुत प्रभावशाली है। इसकी गति और शब्दों का चयन एक पेशेवर कथा शैली बनाने के लिए प्रभावी ढंग से काम करते हैं।",
            "Weak_Repetition": "यह अनुच्छेद दोहराव वाला लगता है, जो कहानी से ध्यान भटकाता है। शब्दों की विविधता पर ध्यान देने से मदद मिलेगी।",
            "Weak_Simplistic": "यहाँ लेखन थोड़ा बहुत सरल है। अपनी वाक्य संरचनाओं में जटिलता जोड़ने से लय में सुधार होगा।",
            "Weak_General": "पाठकों को जोड़े रखने के लिए इस खंड को अपनी संरचना और भावनात्मक गहराई में और अधिक विकास की आवश्यकता है।",
            "Moderate_Repetition": "दृश्य स्पष्ट रूप से संचार करता है, लेकिन दोहराए गए शब्द कथा की समृद्धि को कम करते हैं।",
            "Moderate_General": "यह एक ठोस आधार है, लेकिन लयबद्ध प्रवाह और भावनात्मक गूँज में सुधार की गुंजाइश है।",
            "Tip_Pacing_Long": "आपके वाक्य बहुत लंबे और एक समान हैं। लय बनाने के लिए उन्हें छोटे और प्रभावशाली वाक्यों में तोड़ने का प्रयास करें।",
            "Tip_Pacing_Slow": "आपकी गति थोड़ी धीमी महसूस होती है। प्राकृतिक पठन प्रवाह बनाने के लिए छोटे और लंबे वाक्यों को मिलाएँ।",
            "Tip_Repetition_Starters": "कई वाक्य एक ही शब्द से शुरू होते हैं: {items}। अपने वाक्य की शुरुआत में विविधता लाने का प्रयास करें।",
            "Tip_Repetition_Words": "ये शब्द बहुत बार दिखाई देते हैं: {items}। कुछ को पर्यायवाची शब्दों से बदलें।",
            "Tip_Repetition_Phrases": "यह वाक्यांश बहुत बार दोहराया जाता है: {items}। कुछ को फिर से लिखने का प्रयास करें।",
            "Tip_Emotion": "भावनात्मक प्रभाव को गहरा करने के लिए अधिक संवेदी विवरण या पात्रों के आंतरिक विचार जोड़ने पर विचार करें।",
            "Tip_Generic": "गद्य को बेहतर बनाने के लिए अधिक अभिव्यंजक कल्पना के साथ प्रयोग करने का प्रयास करें।",
            "Tip_Strong": "अच्छी तरह से संतुलित गद्य। अपने शेष अध्याय में भी इसी तरह की विविधता बनाए रखें।"
        },
        "marathi": {
            "Strong": "मजबूत",
            "Moderate": "मध्यम",
            "Weak": "कमकुवत",
            "Strong_Summary": "हा विभाग खूप प्रभावी आहे. त्याची गती आणि शब्द निवड व्यावसायिक कथा शैली तयार करण्यासाठी प्रभावीपणे कार्य करतात।",
            "Weak_Repetition": "हा परिच्छेद पुनरावृत्तीचा वाटतो, ज्यामुळे कथेवरून लक्ष विचलित होते. शब्दांच्या विविधतेवर लक्ष केंद्रित केल्यास मदत होईल।",
            "Weak_Simplistic": "येथील लेखन थोडे जास्त सोपे आहे. आपल्या वाक्य रचनेत गुंतागुंत जोडल्यास लय सुधारेल।",
            "Weak_General": "वाचकांना गुंतवून ठेवण्यासाठी या विभागाला त्याच्या रचनेत आणि भावनिक खोलीत अधिक विकासाची गरज आहे।",
            "Moderate_Repetition": "दृश्य स्पष्टपणे संवाद साधते, परंतु वारंवार येणारे शब्द कथेची समृद्धी कमी करतात।",
            "Moderate_General": "हा एक ठोस पाया आहे, परंतु लयबद्ध प्रवाह आणि भावनिक अनुनाद सुधारण्यास वाव आहे।",
            "Tip_Pacing_Long": "तुमची वाक्ये खूप लांब आणि एकसारखी आहेत. लय तयार करण्यासाठी त्यांना लहान आणि प्रभावी वाक्यांमध्ये तोडण्याचा प्रयत्न करा।",
            "Tip_Pacing_Slow": "तुमची गती थोडी संथ वाटते. नैसर्गिक वाचन प्रवाह तयार करण्यासाठी लहान आणि लांब वाक्यांचे मिश्रण करा।",
            "Tip_Repetition_Starters": "अनेक वाक्ये एकाच शब्दाने सुरू होतात: {items}। तुमच्या वाक्याच्या सुरुवातीला विविधता आणण्याचा प्रयत्न करा।",
            "Tip_Repetition_Words": "हे शब्द वारंवार येतात: {items}। काहींना समानार्थी शब्दांनी बदला।",
            "Tip_Repetition_Phrases": "हा वाक्प्रचार वारंवार पुनरावृत्ती होतो: {items}। काही वेळा वेगळ्या पद्धतीने लिहिण्याचा प्रयत्न करा।",
            "Tip_Emotion": "भावनिक प्रभाव वाढवण्यासाठी अधिक संवेदी तपशील किंवा पात्रांचे अंतर्गत विचार जोडण्याचा विचार करा।",
            "Tip_Generic": "गद्य अधिक चांगले करण्यासाठी अधिक अभिव्यक्त कल्पनाशक्ती वापरून पहा।",
            "Tip_Strong": "चांगले संतुलित गद्य. तुमच्या उर्वरित प्रकरणातही अशीच विविधता ठेवा।"
        }
    }

    t = translations.get(language, translations["english"])

    # Step 2 - Build a context-aware summary message based on label and reasons
    if label == "Strong":
        summary = t["Strong_Summary"]
    elif label == "Weak":
        if "Heavy repetition" in reasons:
            summary = t["Weak_Repetition"]
        elif "Prose is overly simplistic" in reasons:
            summary = t["Weak_Simplistic"]
        else:
            summary = t["Weak_General"]
    else:
        # Moderate
        if "Repetitive wording" in reasons:
            summary = t["Moderate_Repetition"]
        else:
            summary = t["Moderate_General"]

    # Step 3 - Build specific actionable tips based on individual scores
    tips = []

    # Pacing tips
    if pacing_score < 0.5:
        if pacing_score < 0.35:
            tips.append(t["Tip_Pacing_Long"])
        else:
            tips.append(t["Tip_Pacing_Slow"])

    # Repetition tips
    if repetition_data["repetition_score"] < 0.6:
        if repetition_data.get("repeated_starters"):
            tips.append(t["Tip_Repetition_Starters"].format(items=repetition_data['repeated_starters']))
        if repetition_data.get("repeated_words"):
            tips.append(t["Tip_Repetition_Words"].format(items=repetition_data['repeated_words']))
        if repetition_data.get("repeated_bigrams"):
            tips.append(t["Tip_Repetition_Phrases"].format(items=repetition_data['repeated_bigrams']))

    # Emotion tips
    if emotion_score < 0.4:
        tips.append(t["Tip_Emotion"])

    # Default tip if nothing specific found
    if not tips and label != "Strong":
        tips.append(t["Tip_Generic"])
    elif not tips and label == "Strong":
        tips.append(t["Tip_Strong"])

    # Step 4 - Return dictionary with exact keys
    return {
        "label": t[label], # Localized label
        "combined_score": combined_score,
        "summary": summary,
        "tips": tips
    }
