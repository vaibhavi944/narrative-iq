export interface PacingData {
  avg_sentence_length: number;
  variance: number;
  pacing_score: number;
}

export interface RepetitionData {
  repeated_starters: string[];
  repeated_words: string[];
  repeated_bigrams: string[];
  repetition_score: number;
}

export interface EmotionData {
  polarity: number;
  intensity: number;
  emotion_score: number;
  label: string;
}

export interface AnalysisData {
  paragraph: string;
  language: string;
  pacing: PacingData;
  repetition: RepetitionData;
  emotion: EmotionData;
  combined_score: number;
  label: string;
  reasons: string[];
}

export interface FeedbackData {
  label: string;
  combined_score: number;
  summary: string;
  tips: string[];
}

export interface BenchmarkExample {
  chunk_id: string;
  text: string;
  label: string;
  reasons: string[];
  genre: string;
  scene_type: string;
  language: string;
}

export interface CritiqueResponse {
  analysis: AnalysisData;
  feedback: FeedbackData;
  benchmark_example: BenchmarkExample;
  agent_critique: string;
  suggested_rewrite: string;
}
