export interface AnalysisResult {
  chunk_id: string;
  language: string;
  genre: string;
  scene_type: string;
  dialogue_density: string;
  combined_score: number;
  label: string;
  pacing: {
    avg_sentence_length: number;
    variance: number;
    pacing_score: number;
  };
  repetition: {
    repeated_starters: string[];
    repeated_words: string[];
    repeated_bigrams: string[];
    repetition_score: number;
  };
  emotion: {
    polarity: number;
    intensity: number;
    emotion_score: number;
    label: string;
  };
  reasons: string[];
  feedback: {
    summary: string;
    tips: string[];
  };
  text: string;
  benchmark_example: {
    chunk_id: string;
    text: string;
    label: string;
    reasons: string[];
    genre: string;
    scene_type: string;
  };
  agent_critique: string;
  suggested_rewrite: string;
}

export function getMockAnalysis(userInput: string, language: string): AnalysisResult {
  const isWeak = userInput.split('.').length > 3 && userInput.includes('the boy') || userInput.includes('queen');
  
  // Logic to simulate context-preserving behavior
  let rewrite = "";
  let critique = "";
  let benchmark = {
    chunk_id: "eng_301_03",
    text: "The mother said to the father, 'Let's go inside quick and get the pup warm.' But the father said, 'It's ok, the pup will be fine in this weather,' and he began to walk away into the swirling gray mist.",
    label: "Strong",
    reasons: ["Well-balanced prose with good rhythm and clarity"],
    genre: "slice_of_life",
    scene_type: "dialogue",
  };

  if (language === "marathi") {
    rewrite = "राणीने आपल्या भव्य राजवाड्यात दिवसभर काम केले, पण आज तिला विश्रांती हवी होती. शांततेच्या आशेने ती शाही बागेत गेली आणि मऊ हिरव्या गवतावर बसली. तिथे तिला एक कीटक दिसला आणि ती घाबरून पुन्हा आपल्या राजवाड्याकडे निघाली.";
    critique = "तुमच्या लेखनात वाक्यांची लांबी खूपच सारखी आहे. थोडी विविधता आणल्यास वाचक अधिक गुंतून राहतील.";
    benchmark = {
        chunk_id: "mar_012_02",
        text: "पहाटेच्या वेळी जेव्हा सूर्यकिरणे झाडांच्या पानांतून झिरपत होती, तेव्हा त्याने पाहिले की निसर्ग किती सुंदर आहे. प्रत्येक पक्ष्याचा आवाज एका नवीन गाण्याची आठवण करून देत होता.",
        label: "Strong",
        reasons: ["चांगली लय आणि स्पष्टता"],
        genre: "slice_of_life",
        scene_type: "description"
    };
  } else if (language === "hindi") {
    rewrite = "रानी अपने महल में बहुत व्यस्त रहती थी, पर आज उसका मन शांत बैठने का था। वह महल के बगीचे में टहलने गई और ठंडी घास पर बैठ गई। अचानक उसे एक कीड़ा दिखा जिसे देख वह घबरा गई और जल्दी से अपने महल लौट आई।";
    critique = "आपकी कहानी का आधार बहुत अच्छा है, लेकिन शब्दों के दोहराव को कम करने से भाषा अधिक प्रभावशाली बनेगी।";
    benchmark = {
        chunk_id: "hin_005_01",
        text: "शाम की ठंडी हवाएं चल रही थीं और माँ रसोई में खाना बना रही थी। उसकी चूड़ियों की खनक से पूरे घर में एक अलग ही रौनक महसूस हो रही थी।",
        label: "Strong",
        reasons: ["बेहतरीन शब्द चयन"],
        genre: "slice_of_life",
        scene_type: "description"
    };
  } else {
    // English
    if (userInput.toLowerCase().includes("queen")) {
      rewrite = "The queen spent most of her days working inside her grand castle, but today she longed for rest. Hoping for peace and quiet, she wandered into the royal park and settled onto the soft green grass. As she relaxed beneath the warm sunlight, a strange bug crawled across her dress. The queen quickly stood up in disgust and hurried back toward the safety of her beautiful castle.";
      critique = "Your story has a wonderful, classic feel, but the rhythm is currently quite uniform. By merging some of your shorter sentences and adding sensory details like 'warm sunlight', you can make the scene feel much more immersive.";
    } else {
      rewrite = "As the first cold drops began to fall, he started his long walk home, his heart heavy with a weight he couldn't quite name. Through the swirling gray mist, he watched the world blur into a somber shade of blue before finally escaping into the quiet warmth of his room.";
      critique = "The draft effectively conveys the mood, but the sentence structure needs more variety to sustain the reader's interest.";
    }
  }

  return {
    chunk_id: "demo_chunk_" + Math.random().toString(36).substr(2, 5),
    language: language,
    genre: "slice_of_life",
    scene_type: "description",
    dialogue_density: "none",
    combined_score: 0.45,
    label: isWeak ? "Weak" : "Moderate",
    pacing: {
      avg_sentence_length: 5.2,
      variance: 1.5,
      pacing_score: 0.4,
    },
    repetition: {
      repeated_starters: ["The"],
      repeated_words: ["queen", "boy"],
      repeated_bigrams: ["the queen"],
      repetition_score: 0.55,
    },
    emotion: {
      polarity: 0.2,
      intensity: 0.4,
      emotion_score: 0.4,
      label: "Neutral",
    },
    reasons: ["Repetitive sentence structure", "Limited sensory details"],
    feedback: {
      summary: language === "marathi" ? "तुमची कथा स्पष्ट आहे पण शब्दसंग्रह वाढवणे गरजेचे आहे." : language === "hindi" ? "आपकी कहानी अच्छी है लेकिन शब्दों का चयन बेहतर हो सकता है।" : "The scene communicates clearly, but repetitive wording reduces the narrative richness.",
      tips: ["Vary sentence length", "Show character reactions"]
    },
    text: userInput,
    benchmark_example: benchmark,
    agent_critique: critique || "Comparative analysis shows the benchmark uses better pacing.",
    suggested_rewrite: rewrite,
  };
}

export const MOCK_ANALYSIS = getMockAnalysis("The boy walked home.", "english");
