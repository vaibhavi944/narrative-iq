export const MOCK_ANALYSIS = {
  chunk_id: "demo_chunk_001",
  language: "english",
  genre: "slice_of_life",
  scene_type: "description",
  dialogue_density: "none",
  combined_score: 0.45,
  label: "Weak",
  pacing: {
    avg_sentence_length: 4.0,
    variance: 0.0,
    pacing_score: 0.4,
  },
  repetition: {
    repeated_starters: ["The"],
    repeated_words: ["boy"],
    repeated_bigrams: ["the boy"],
    repetition_score: 0.65,
  },
  emotion: {
    polarity: -0.71,
    intensity: 0.71,
    emotion_score: 0.71,
    label: "Negative",
  },
  reasons: [
    "Prose is overly simplistic or choppy",
    "Pacing is monotonous or lacks rhythmic variety",
    "Repetitive wording reduces narrative richness",
  ],
  feedback: {
    summary: "This section feels repetitive, which distracts from the story. Focusing on word variety will help.",
    tips: [
      "Vary sentence structure: Combine short and long sentences to create a more dynamic rhythm.",
      "Use descriptive language: Replace repetitive phrases with more descriptive adjectives.",
      "Show, don't tell: Try to show the boy's emotions through actions rather than just stating he was sad.",
    ],
  },
  text: "The boy walked home. The boy saw rain. The boy was sad. The boy went inside. The rain was cold.",
  benchmark_example: {
    chunk_id: "eng_301_03",
    text: "The mother said to the father, 'Let's go inside quick and get the pup warm.' But the father said, 'It's ok, the pup will be fine in this weather,' and he began to walk away into the swirling gray mist.",
    label: "Strong",
    reasons: ["Well-balanced prose with good rhythm and clarity"],
    genre: "slice_of_life",
    scene_type: "dialogue",
  },
  agent_critique: `The BENCHMARK PARAGRAPH excels in its use of varied sentence structure, creating a more dynamic rhythm. It also employs dialogue and specific sensory details like "swirling gray mist", which adds depth and nuance. In contrast, the USER'S PARAGRAPH suffers from repetitive sentence starters and a monotonous pace.

### Actionable Steps:
1. **Vary Sentence Structure**: Merge some of your shorter sentences. "As the cold rain began to fall, the boy walked home with a heavy heart."
2. **Inject Specificity**: Instead of "The boy saw rain," describe how it felt or sounded.
3. **Enhance Flow**: Use transitional words like "Suddenly" or "Meanwhile" to connect the boy's actions to the environment.`,
};

export type AnalysisResult = typeof MOCK_ANALYSIS;
