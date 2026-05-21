export const MOCK_ANALYSIS = {
  chunk_id: "demo_chunk_queen",
  language: "english",
  genre: "fantasy",
  scene_type: "description",
  dialogue_density: "none",
  combined_score: 0.45,
  label: "Weak",
  pacing: {
    avg_sentence_length: 5.2,
    variance: 1.5,
    pacing_score: 0.4,
  },
  repetition: {
    repeated_starters: ["The", "She"],
    repeated_words: ["queen", "castle", "bug", "relax"],
    repeated_bigrams: ["the queen"],
    repetition_score: 0.55,
  },
  emotion: {
    polarity: 0.2,
    intensity: 0.4,
    emotion_score: 0.4,
    label: "Neutral",
  },
  reasons: [
    "Heavy repetition weakens readability",
    "Pacing is monotonous or lacks rhythmic variety",
    "Prose is overly simplistic or choppy",
  ],
  feedback: {
    summary: "The scene communicates clearly, but repetitive wording and short sentences reduce the narrative richness.",
    tips: [
      "Vary sentence structure: Combine your observations into more fluid descriptions.",
      "Vary your word choice: Instead of repeating 'queen' and 'castle', try descriptive alternatives.",
      "Show character reactions: Describe the queen's surroundings and feelings in more detail.",
    ],
  },
  text: "Once upon a time, there was a queen. She was a very nice queen. She had a big, pretty castle. The queen had a lot of work to do every day. But today, she wanted to relax.\n\nThe queen went to the park to relax. She sat on a soft, green grass. The queen saw a bug. The bug was disgusting. The queen did not like the disgusting bug.\n\nThe queen went back to her castle. She was happy to be away from the disgusting bug. Now, the queen could relax in her big, pretty castle. The queen smiled and had a good day.",
  benchmark_example: {
    chunk_id: "eng_245_07",
    text: "So off they went, happy to enjoy the day together. They spent hours talking and playing, and they both felt so lucky to have each other as friends. It was a day they would never forget.",
    label: "Strong",
    reasons: ["Well-balanced prose with good rhythm and clarity"],
    genre: "slice_of_life",
    scene_type: "action",
  },
  agent_critique: `Your story has a wonderful, classic feel, but the rhythm is currently quite uniform. 

**Craft Comparison**
The benchmark example shows how to use transitional phrases and varied sentence lengths to create a sense of momentum. Notice how it groups actions ("talking and playing") to keep the pace moving. In your draft, each small action gets its own short sentence, which can feel a bit repetitive to a reader.

**Actionable Steps:**
1. **Combine Actions**: Try merging some of the queen's daily routine into a single, fluid sentence.
2. **Describe the Setting**: Instead of saying the castle is "big and pretty," pick one specific detail—like "towering spires" or "sun-drenched halls"—to make it feel unique.
3. **Show the Disgust**: Instead of stating the bug was "disgusting," describe how the queen's nose wrinkled or how she gathered her silk skirts to hurry away.`,
  suggested_rewrite: "The queen spent most of her days working inside her grand castle, but today she longed for rest. Hoping for peace and quiet, she wandered into the royal park and settled onto the soft green grass. \n\nAs she relaxed beneath the warm sunlight, a strange bug crawled across her dress. The queen quickly stood up in disgust and hurried back toward the safety of her beautiful castle. Once inside, she finally relaxed again, smiling as the castle doors closed behind her.",
};

export type AnalysisResult = typeof MOCK_ANALYSIS;
