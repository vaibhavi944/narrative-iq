"use client";

import React, { useState } from "react";
import { analyzeText, rewriteText } from "@/lib/api";
import Header from "@/components/Header";
import ScoreCard from "@/components/ScoreCard";
import BenchmarkCard from "@/components/BenchmarkCard";
import RewriteCard from "@/components/RewriteCard";
import TipsList from "@/components/TipsList";
import LanguageSelector from "@/components/LanguageSelector";

export default function WorkspacePage() {
  const [text, setText] = useState("");
  const [language, setLanguage] = useState("English");
  const [isLoading, setIsLoading] = useState(false);
  const [analysis, setAnalysis] = useState<any>(null);
  const [rewrite, setRewrite] = useState<any>(null);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!text.trim()) {
      setError("Please enter some text to analyze.");
      return;
    }
    setError("");
    setIsLoading(true);
    try {
      const result = await analyzeText(text, language);
      if (result.success) {
        setAnalysis(result);
        setRewrite(null); // Clear previous rewrite
      } else {
        setError("Analysis failed. Please try again.");
      }
    } catch (err: any) {
      setError(err.message || "Failed to connect to the server.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleRewrite = async (benchmarkText: string, benchmarkId: string) => {
    setIsLoading(true);
    setError("");
    try {
      const result = await rewriteText(text, language, benchmarkText, benchmarkId);
      if (result.success) {
        setRewrite(result.rewrite);
      } else {
        setError("Rewrite failed.");
      }
    } catch (err: any) {
      setError(err.message || "Failed to connect to the server.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#fafaf8] text-[#1a1a18] font-sans">
      <Header />
      
      <main className="max-w-7xl mx-auto px-6 py-12">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Left Column: Input */}
          <div className="flex-1 space-y-6">
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-[#e9e9e5]">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-sm font-black uppercase tracking-widest text-[#9e9e9a]">Draft your scene</h2>
                <LanguageSelector selected={language} onChange={setLanguage} />
              </div>
              
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Start writing your story here..."
                className="w-full h-96 p-4 bg-transparent text-lg leading-relaxed focus:outline-none resize-none font-light"
              />
              
              <div className="flex justify-end mt-4">
                <button
                  onClick={handleAnalyze}
                  disabled={isLoading}
                  className={`bg-[#1a1a18] text-white px-8 py-3 rounded-full font-bold transition-all hover:bg-[#4338ca] active:scale-95 ${
                    isLoading ? "opacity-50 cursor-not-allowed" : ""
                  }`}
                >
                  {isLoading ? "Analyzing..." : "Analyze Scene"}
                </button>
              </div>
            </div>

            {error && (
              <div className="p-4 bg-red-50 text-red-600 rounded-xl border border-red-100 text-sm">
                {error}
              </div>
            )}

            {rewrite && (
              <RewriteCard rewrite={rewrite} />
            )}
          </div>

          {/* Right Column: Analysis */}
          <div className="w-full lg:w-96 space-y-6">
            {analysis ? (
              <>
                <ScoreCard score={analysis.score} label={analysis.label} summary={analysis.summary} />
                <TipsList tips={analysis.tips} />
                <BenchmarkCard 
                  benchmark={analysis.benchmark} 
                  onRewrite={(bText: string, bId: string) => handleRewrite(bText, bId)} 
                />
              </>
            ) : (
              <div className="bg-white/50 border-2 border-dashed border-[#e9e9e5] rounded-2xl p-12 text-center">
                <p className="text-[#9e9e9a] text-sm font-medium italic">
                  Complete your draft and click analyze to see feedback here.
                </p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
