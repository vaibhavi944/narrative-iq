def get_localized_ui(language):
    translations = {
        "english": {
            "title": "✍️ NarrativeIQ: Multilingual Writing Analysis",
            "subtitle": "Analyze your prose for **pacing, repetition, and emotion**. Get specific rewrite suggestions powered by RAG-based story examples.",
            "placeholder": "The sun was hot...",
            "button": "Analyze Prose",
            "metrics_header": "📊 Analysis Metrics",
            "quality_label": "Overall Quality",
            "issues_header": "Issues Detected:",
            "critique_header": "💡 AI Critique & Suggestions",
            "rag_header": "📚 Learning from the Pros (RAG Benchmark)",
            "benchmark_id": "Benchmark Found:",
            "genre": "Genre:",
            "rewrite_header": "✨ Suggested Rewrite",
            "rewrite_button": "Generate Improved Version",
            "rewrite_label": "Improved Version:"
        },
        "hindi": {
            "title": "✍️ नैरेटिवआईक्यू: बहुभाषी लेखन विश्लेषण",
            "subtitle": "**गति, दोहराव और भावना** के लिए अपने गद्य का विश्लेषण करें। RAG-आधारित कहानी उदाहरणों का उपयोग करके विशिष्ट पुनर्लेखन सुझाव प्राप्त करें।",
            "placeholder": "सूरज गर्म था...",
            "button": "गद्य का विश्लेषण करें",
            "metrics_header": "📊 विश्लेषण मेट्रिक्स",
            "quality_label": "कुल गुणवत्ता",
            "issues_header": "पहचानी गई समस्याएँ:",
            "critique_header": "💡 एआई समीक्षा और सुझाव",
            "rag_header": "📚 दिग्गजों से सीखना (RAG बेंचमार्क)",
            "benchmark_id": "बेंचमार्क मिला:",
            "genre": "शैली:",
            "rewrite_header": "✨ सुझाया गया पुनर्लेखन",
            "rewrite_button": "बेहतर संस्करण बनाएँ",
            "rewrite_label": "बेहतर संस्करण:"
        },
        "marathi": {
            "title": "✍️ नॅरेटिव्हआयक्यू: बहुभाषिक लेखन विश्लेषण",
            "subtitle": "**गती, पुनरावृत्ती आणि भावना** साठी तुमच्या गद्याचे विश्लेषण करा। RAG-आधारित कथा उदाहरणांचा वापर करून विशिष्ट पुनर्लेखन सुचवा।",
            "placeholder": "सूर्य गरम होता...",
            "button": "गद्याचे विश्लेषण करा",
            "metrics_header": "📊 विश्लेषण मेट्रिक्स",
            "quality_label": "एकूण गुणवत्ता",
            "issues_header": "आढळलेल्या समस्या:",
            "critique_header": "💡 एआई समीक्षा आणि सूचना",
            "rag_header": "📚 दिग्गजांकडून शिकणे (RAG बेंचमार्क)",
            "benchmark_id": "बेंचमार्क सापडला:",
            "genre": "शैली:",
            "rewrite_header": "✨ सुचवलेले पुनर्लेखन",
            "rewrite_button": "सुधारित आवृत्ती तयार करा",
            "rewrite_label": "सुधारित आवृत्ती:"
        }
    }
    return translations.get(language, translations["english"])
