# Centralized Multilingual UI Strings for NarrativeIQ

UI_STRINGS = {
    "english": {
        "strength": "Writing Strength",
        "flow": "Flow",
        "variety": "Word Variety",
        "depth": "Emotion",
        "label_strong": "Strong",
        "label_moderate": "Moderate",
        "label_weak": "Weak"
    },
    "hindi": {
        "strength": "लेखन की शक्ति",
        "flow": "प्रवाह",
        "variety": "शब्दों का बदलाव",
        "depth": "भावना",
        "label_strong": "मजबूत",
        "label_moderate": "मध्यम",
        "label_weak": "कमजोर"
    },
    "marathi": {
        "strength": "लेखन सामर्थ्य",
        "flow": "प्रवाह",
        "variety": "शब्दांमधील विविधता",
        "depth": "भावना",
        "label_strong": "मजबूत",
        "label_moderate": "मध्यम",
        "label_weak": "कमजोर"
    }
}

def get_ui_string(key, language="english"):
    return UI_STRINGS.get(language, UI_STRINGS["english"]).get(key, key)
