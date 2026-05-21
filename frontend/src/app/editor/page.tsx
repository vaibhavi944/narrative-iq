"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  PenLine, 
  Sparkles, 
  RotateCcw, 
  ShieldCheck, 
  Activity, 
  Languages,
  BookMarked,
  LayoutDashboard,
  CheckCircle2,
  ChevronRight
} from "lucide-react";
import { cn } from "@/lib/utils";
import { MOCK_ANALYSIS, type AnalysisResult } from "@/lib/mockData";

export default function EditorPage() {
  const [text, setText] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  const handleAnalyze = () => {
    if (!text.trim()) return;
    setIsAnalyzing(true);
    // Simulate API delay
    setTimeout(() => {
      setResult(MOCK_ANALYSIS);
      setIsAnalyzing(false);
    }, 1800);
  };

  const handleReset = () => {
    setText("");
    setResult(null);
  };

  return (
    <div className="flex h-screen bg-stone-50 text-stone-900 selection:bg-indigo-500/10 overflow-hidden font-sans">
      {/* Sidebar - Minimal Nav */}
      <aside className="w-16 flex flex-col items-center py-8 border-r border-stone-200 bg-white z-50">
        <div className="w-10 h-10 bg-indigo-700 rounded-xl flex items-center justify-center mb-10 shadow-sm">
          <PenLine className="w-5 h-5 text-white" />
        </div>
        <div className="flex flex-col gap-6">
          <button className="p-2.5 rounded-lg bg-stone-100 text-indigo-700 transition-all">
            <PenLine className="w-5 h-5" />
          </button>
          <button className="p-2.5 rounded-lg text-stone-400 hover:bg-stone-100 hover:text-stone-600 transition-all">
            <LayoutDashboard className="w-5 h-5" />
          </button>
        </div>
      </aside>

      {/* Main Container */}
      <div className="flex-1 flex overflow-hidden">
        {/* Editor Area - Document Centered */}
        <main className="flex-1 flex flex-col bg-white relative">
          <header className="flex items-center justify-between px-12 py-5 border-b border-stone-100">
            <div className="flex items-center gap-4">
              <h2 className="text-[13px] font-bold uppercase tracking-[0.15em] text-stone-400">Untitled Scene</h2>
              <div className="w-1 h-1 rounded-full bg-stone-200" />
              <div className="flex items-center gap-1.5 text-stone-500 text-[13px] font-medium">
                <Languages className="w-3.5 h-3.5 text-stone-400" />
                Auto: English
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <button 
                onClick={handleReset}
                className="text-stone-400 hover:text-stone-600 transition-colors p-1"
                title="Reset Document"
              >
                <RotateCcw className="w-4 h-4" />
              </button>
            </div>
          </header>

          {/* Centered Document Pad */}
          <div className="flex-1 overflow-y-auto custom-scrollbar bg-stone-50/30">
            <div className="max-w-3xl mx-auto w-full px-8 py-24 min-h-full flex flex-col">
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Start your narrative here..."
                className="w-full flex-1 bg-transparent border-none outline-none resize-none text-[22px] font-serif leading-[1.8] placeholder:text-stone-200 text-stone-800 focus:ring-0 selection:bg-indigo-100"
              />
              
              <div className="h-40" />
            </div>
          </div>

          {/* Floating Action Bar */}
          <div className="absolute bottom-10 left-1/2 -translate-x-1/2 z-40">
            <motion.button
              whileHover={{ y: -2 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleAnalyze}
              disabled={isAnalyzing || !text.trim()}
              className={cn(
                "flex items-center gap-3 px-8 py-4 rounded-full font-bold transition-all shadow-xl disabled:opacity-30 disabled:cursor-not-allowed text-[15px]",
                isAnalyzing 
                  ? "bg-stone-800 text-white" 
                  : "bg-stone-900 hover:bg-indigo-700 text-white shadow-stone-200"
              )}
            >
              {isAnalyzing ? (
                <>
                  <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                  Deconstructing...
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  Analyze Narrative
                </>
              )}
            </motion.button>
          </div>
        </main>

        {/* Right Panel - Editorial Mentor */}
        <aside className="w-[450px] flex flex-col bg-white border-l border-stone-200 overflow-hidden relative">
          {!result && !isAnalyzing && (
            <div className="flex-1 flex flex-col items-center justify-center p-16 text-center">
              <div className="w-14 h-14 bg-stone-50 rounded-2xl flex items-center justify-center mb-8 border border-stone-100 text-stone-300">
                <BookMarked className="w-7 h-7" />
              </div>
              <h2 className="text-lg font-semibold text-stone-900 mb-3 tracking-tight">Ready for Review</h2>
              <p className="text-stone-400 text-[14px] leading-relaxed max-w-[240px]">
                I'll analyze your pacing, emotion, and rhythm to provide structural benchmarks.
              </p>
            </div>
          )}

          {isAnalyzing && (
            <div className="flex-1 flex flex-col items-center justify-center p-12 space-y-8 bg-stone-50/20">
              <div className="w-12 h-12 border-2 border-indigo-100 border-t-indigo-600 rounded-full animate-spin" />
              <div className="text-center">
                <p className="text-sm font-semibold text-stone-800 uppercase tracking-widest mb-2">Analyzing Quality</p>
                <p className="text-[12px] text-stone-400 font-medium">Scanning 2,600+ Literary Benchmarks</p>
              </div>
            </div>
          )}

          <AnimatePresence>
            {result && !isAnalyzing && (
              <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex-1 overflow-y-auto custom-scrollbar"
              >
                {/* Score Summary */}
                <div className="p-8 border-b border-stone-100 bg-stone-50/30">
                  <div className="flex items-center justify-between mb-10">
                    <div>
                      <span className="text-[11px] font-bold uppercase tracking-[0.2em] text-stone-400 block mb-2">Scene Analysis</span>
                      <h3 className={cn(
                        "text-2xl font-bold tracking-tight",
                        result.label === "Strong" ? "text-emerald-600" : "text-amber-600"
                      )}>
                        {result.label === "Strong" ? "Beautifully Written" : result.label === "Moderate" ? "Good Foundation" : "Needs Care"}
                      </h3>
                    </div>
                    <div className="text-right">
                      <div className="text-4xl font-bold tabular-nums text-stone-900">{Math.round(result.combined_score * 100)}</div>
                      <span className="text-[10px] font-bold text-stone-400 uppercase tracking-widest">Narrative Impact</span>
                    </div>
                  </div>

                  <div className="space-y-6">
                    <ScoreBar label="Story Flow" score={result.pacing.pacing_score} />
                    <ScoreBar label="Writing Clarity" score={result.repetition.repetition_score} />
                    <ScoreBar label="Emotional Heart" score={result.emotion.emotion_score} />
                  </div>
                </div>

                <div className="p-8 space-y-12">
                  {/* AI Critique */}
                  <section>
                    <h3 className="text-[11px] font-bold uppercase tracking-[0.2em] text-stone-400 mb-6">Your Mentor's Thoughts</h3>
                    <div className="space-y-6">
                      <p className="text-[15px] text-stone-700 leading-relaxed font-medium bg-indigo-50/50 p-5 rounded-2xl border border-indigo-100/50 italic">
                        {result.feedback.summary}
                      </p>
                      <div className="space-y-4">
                        {result.feedback.tips.map((tip, i) => (
                          <div key={i} className="flex gap-4 items-start group">
                            <CheckCircle2 className="w-4 h-4 text-indigo-500 mt-1 flex-shrink-0" />
                            <p className="text-[14px] text-stone-600 leading-relaxed font-medium">{tip}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  </section>

                  {/* Benchmark Comparison */}
                  <section className="pt-4">
                    <h3 className="text-[11px] font-bold uppercase tracking-[0.2em] text-stone-400 mb-6">A Guiding Example</h3>
                    <div className="document-card p-6 border-stone-200">
                      <div className="flex items-center justify-between mb-5">
                        <span className="text-[10px] font-bold text-indigo-700 uppercase tracking-widest bg-indigo-50 px-2 py-1 rounded">
                          {result.benchmark_example.genre} / {result.benchmark_example.scene_type}
                        </span>
                      </div>
                      <p className="text-[15px] font-serif text-stone-800 leading-[1.7] italic mb-6 border-l-2 border-stone-200 pl-5">
                        "{result.benchmark_example.text}"
                      </p>
                      
                      <div className="pt-6 border-t border-stone-100">
                        <p className="text-[13px] text-stone-500 leading-relaxed whitespace-pre-wrap font-medium italic">
                          {result.agent_critique.split('### Actionable Steps:')[0].trim()}
                        </p>
                      </div>
                    </div>
                  </section>
                </div>

                <div className="h-20" />
              </motion.div>
            )}
          </AnimatePresence>
        </aside>
      </div>
    </div>
  );
}

function ScoreBar({ label, score }: { label: string; score: number }) {
  const percentage = Math.round(score * 100);
  return (
    <div className="space-y-3">
      <div className="flex justify-between items-center">
        <span className="text-[11px] font-bold uppercase tracking-widest text-stone-500">{label}</span>
        <span className="text-[11px] font-bold tabular-nums text-stone-900">{percentage}%</span>
      </div>
      <div className="h-1 w-full bg-stone-200/50 rounded-full overflow-hidden">
        <motion.div 
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 1, ease: "easeOut" }}
          className={cn(
            "h-full rounded-full",
            percentage > 70 ? "bg-emerald-500" : percentage > 40 ? "bg-indigo-600" : "bg-amber-500"
          )}
        />
      </div>
    </div>
  );
}
