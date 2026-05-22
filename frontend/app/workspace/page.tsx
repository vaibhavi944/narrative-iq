"use client";

<<<<<<< HEAD
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
=======
import { useState, useRef, useEffect } from "react";
import Header from "@/components/Header";
import ScoreCard from "@/components/ScoreCard";
import TipsList from "@/components/TipsList";
import BenchmarkCard from "@/components/BenchmarkCard";
import RewriteCard from "@/components/RewriteCard";
import { analyzeText, rewriteText } from "@/lib/api";

type AnalysisResult = {
  success: boolean;
  score: number;
  label: string;
  summary: string;
  tips: string[];
  critique: string;
  benchmark: { text: string; genre: string; chunk_id: string } | null;
  pacing_score: number;
  repetition_score: number;
  emotion_score: number;
};

export default function WorkspacePage() {
  const [text, setText] = useState("");
  const [language, setLanguage] = useState("english");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [rewrite, setRewrite] = useState<string | null>(null);
  const [isRewriting, setIsRewriting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [panelWidth, setPanelWidth] = useState(480);
  const [isResizing, setIsResizing] = useState(false);
  
  const panelRef = useRef<HTMLDivElement>(null);

  // Resize handling
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isResizing) return;
      const newWidth = window.innerWidth - e.clientX;
      if (newWidth > 300 && newWidth < 800) {
        setPanelWidth(newWidth);
      }
    };

    const handleMouseUp = () => {
      setIsResizing(false);
    };

    if (isResizing) {
      window.addEventListener("mousemove", handleMouseMove);
      window.addEventListener("mouseup", handleMouseUp);
    }

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  }, [isResizing]);

  const languages = [
    { id: "english", label: "English" },
    { id: "hindi", label: "हिन्दी" },
    { id: "marathi", label: "मराठी" }
  ];

  const ui = {
    english: {
      placeholder: "Paste your writing here...",
      reviewBtn: "Check My Writing",
      reviewing: "Checking...",
      guidance: "Ways to Improve",
      mentorHeader: "Editor's Note",
      benchmarkHeader: "A Better Example",
      benchmarkNote: "How similar scenes look in professional books.",
      rewriteBtn: "Show Better Version",
      rewriting: "Improving...",
      rewriteHeading: "Improved Version",
      errorPrefix: "Editorial Error: ",
      emptyState: "Paste your work to receive an editor's review."
    },
    hindi: {
      placeholder: "यहाँ अपना लेख पेस्ट करें...",
      reviewBtn: "लिखावट की जाँच करें",
      reviewing: "जाँच हो रही है...",
      guidance: "सुधार के तरीके",
      mentorHeader: "मेंटर की सलाह",
      benchmarkHeader: "एक बेहतर उदाहरण",
      benchmarkNote: "देखें कि पेशेवर किताबों में ऐसे दृश्य कैसे लिखे जाते हैं।",
      rewriteBtn: "बेहतर संस्करण देखें",
      rewriting: "सुधार जारी है...",
      rewriteHeading: "सुधारा हुआ संस्करण",
      errorPrefix: "संपादकीय त्रुटि: ",
      emptyState: "संपादकीय समीक्षा प्राप्त करने के लिए अपना काम यहाँ पेस्ट करें।"
    },
    marathi: {
      placeholder: "तुमचे लिखाण येथे पेस्ट करा...",
      reviewBtn: "लिखाण तपासा",
      reviewing: "तपासत आहे...",
      guidance: "सुधारण्याचे मार्ग",
      mentorHeader: "मार्गदर्शकाचा सल्ला",
      benchmarkHeader: "एक अधिक चांगले उदाहरण",
      benchmarkNote: "व्यावसायिक पुस्तकांमध्ये असे प्रसंग कसे असतात ते पाहा.",
      rewriteBtn: "अधिक चांगली आवृत्ती दाखवा",
      rewriting: "सुधारत आहे...",
      rewriteHeading: "सुधारलेली आवृत्ती",
      errorPrefix: "संपादकीय त्रुटी: ",
      emptyState: "संपादकीय पुनरावलोकन प्राप्त करण्यासाठी तुमचे कार्य येथे पेस्ट करा।"
    }
  } as const;

  const t = ui[language as keyof typeof ui] || ui.english;

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    setIsAnalyzing(true);
    setResult(null);
    setRewrite(null);
    setError(null);
    
    try {
      const data = await analyzeText(text, language);
      if (data.success) {
        setResult(data);
        if (panelRef.current) panelRef.current.scrollTo({ top: 0, behavior: "smooth" });
      } else {
        setError(data.error || "Failed to analyze text");
      }
    } catch (e: any) {
      setError(e.message || "Unable to reach the editorial server.");
      console.error(e);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleLanguageChange = (newLang: string) => {
    setLanguage(newLang);
    setText("");
    setResult(null);
    setRewrite(null);
    setError(null);
  };

  const handleRewrite = async () => {
    if (!result || !result.benchmark) return;
    setIsRewriting(true);
    setError(null);
    try {
      const data = await rewriteText(text, language, result.benchmark.text, result.benchmark.chunk_id);
      if (data.success) {
        setRewrite(data.rewrite);
      } else {
        setError(data.error || "Failed to generate rewrite");
      }
    } catch (e: any) {
      setError(e.message || "Rewrite failed.");
      console.error(e);
    } finally {
      setIsRewriting(false);
    }
  };

  const isIndic = language === 'hindi' || language === 'marathi';

  return (
    <div className={`h-screen flex flex-col overflow-hidden bg-[var(--bg-editor)] ${isResizing ? 'cursor-col-resize select-none' : ''}`}>
      <Header showBack={true} />
      
      <div className="flex-1 flex mt-16 overflow-hidden relative">
        
        {/* LEFT: MANUSCRIPT EDITOR */}
        <section className="flex-1 flex flex-col h-full bg-[var(--bg-editor)] border-r border-[var(--border)] overflow-hidden relative">
          
          <div className="flex-1 overflow-y-auto custom-scrollbar py-24 px-12">
            <div className="max-w-[720px] w-full mx-auto flex flex-col gap-12">
              
              <div className="flex gap-6 mb-4">
                {languages.map(l => (
                  <button 
                    key={l.id}
                    onClick={() => handleLanguageChange(l.id)}
                    className={`text-[11px] uppercase tracking-[0.2em] font-bold transition-all ${
                      language === l.id 
                      ? "text-[var(--accent)]" 
                      : "text-[var(--text-hint)] hover:text-[var(--text-secondary)]"
                    }`}
                  >
                    {l.label}
                  </button>
                ))}
              </div>

              {error && (
                <div className="bg-red-50 border border-red-100 p-4 rounded-xl text-red-700 text-[13px] font-medium flex items-center gap-3 animate-in fade-in">
                  <span className="w-1.5 h-1.5 bg-red-400 rounded-full"></span>
                  {t.errorPrefix} {error}
                </div>
              )}

              <textarea
                className={`w-full h-fit min-h-[60vh] bg-transparent text-[22px] leading-[1.9] text-[var(--text-main)] placeholder:text-[var(--border-strong)] resize-none border-none outline-none focus:outline-none focus:ring-0 editor-textarea ${isIndic ? 'font-devanagari' : 'font-sans'}`}
                placeholder={t.placeholder}
                value={text}
                lang={language === 'hindi' ? 'hi' : language === 'marathi' ? 'mr' : 'en'}
                onChange={(e) => setText(e.target.value)}
              />
            </div>
          </div>

          {/* Sticky Action Bar */}
          <div className="bg-[var(--bg-editor)]/80 backdrop-blur-md border-t border-[var(--border)] px-6 md:px-12 py-6 md:py-8 z-10" lang={language === 'hindi' ? 'hi' : language === 'marathi' ? 'mr' : 'en'}>
            <div className="max-w-[720px] w-full mx-auto flex items-center justify-between">
              <span className="text-[10px] md:text-[11px] text-[var(--text-hint)] font-bold uppercase tracking-[0.2em]">
                {text.length} Characters
              </span>
              
              <button
                onClick={handleAnalyze}
                disabled={isAnalyzing || text.trim().length < 10}
                className={`flex items-center gap-4 bg-[var(--text-main)] text-white px-8 md:px-12 py-3.5 md:py-4 rounded-full font-bold transition-all shadow-lg shadow-black/5 ${
                  isIndic 
                  ? "text-[16px] normal-case tracking-normal" 
                  : "text-[14px] uppercase tracking-[0.2em]"
                } hover:opacity-90 disabled:opacity-20 disabled:cursor-not-allowed`}
              >
                {isAnalyzing && <div className="spinner" />}
                {isAnalyzing ? t.reviewing : t.reviewBtn}
              </button>
            </div>
          </div>
        </section>

        {/* RESIZER BAR */}
        <div 
          onMouseDown={() => setIsResizing(true)}
          className={`w-1 h-full cursor-col-resize hover:bg-[var(--accent)] transition-colors absolute z-50 flex items-center justify-center group`}
          style={{ right: `${panelWidth}px` }}
        >
          <div className="w-[1px] h-12 bg-[var(--border-strong)] group-hover:bg-white opacity-40"></div>
        </div>

        {/* RIGHT: EDITORIAL PANEL */}
        <aside 
          ref={panelRef}
          style={{ width: `${panelWidth}px` }}
          lang={language === 'hindi' ? 'hi' : language === 'marathi' ? 'mr' : 'en'}
          className="h-full bg-[var(--bg-panel)] overflow-y-auto flex flex-col custom-scrollbar border-l border-[var(--border)] shrink-0"
        >
          {!result && !isAnalyzing ? (
            <div className="flex-1 flex flex-col items-center justify-center p-12 text-center">
              <div className="w-10 h-[1px] bg-[var(--border-strong)] mb-10 opacity-50"></div>
              <p className={`text-[12px] text-[var(--text-hint)] leading-relaxed max-w-[200px] font-bold uppercase tracking-[0.2em] ${isIndic ? 'font-devanagari' : ''}`}>
                {t.emptyState}
              </p>
            </div>
          ) : isAnalyzing ? (
            <div className="flex-1 flex flex-col items-center justify-center p-12 text-center">
              <div className="spinner w-6 h-6 text-[var(--accent)] mb-8 opacity-40" />
              <p className="text-[12px] text-[var(--text-hint)] uppercase tracking-[0.2em] font-bold">
                Reviewing carefully...
              </p>
            </div>
          ) : (
            <div className="p-12 flex flex-col gap-16 pb-40 animate-in fade-in duration-700">
              
              {result && (
                <ScoreCard 
                  label={result.label} 
                  summary={result.summary} 
                  score={result.score}
                  pacing={result.pacing_score}
                  repetition={result.repetition_score}
                  emotion={result.emotion_score}
                  language={language}
                />
              )}

              {result && <TipsList heading={t.guidance} tips={result.tips} />}

              <RewriteCard 
                heading={t.rewriteHeading}
                rewrite={rewrite}
                loading={isRewriting}
                btnText={t.rewriteBtn}
                loadingText={t.rewriting}
                onRewrite={handleRewrite}
              />

              <div className="flex flex-col gap-6">
                <h3 className="text-[11px] font-bold text-[var(--text-hint)] uppercase tracking-[0.2em]">
                  {t.mentorHeader}
                </h3>
                <div className="flex flex-col gap-4">
                  {result && result.critique.split('→').filter(s => s.trim()).map((note, idx) => (
                    <div key={idx} className="flex gap-4 items-start animate-in slide-in-from-left duration-500" style={{ animationDelay: `${idx * 150}ms` }}>
                      <span className="text-[#4338ca] text-[18px] font-serif italic mt-[-2px]">&rarr;</span>
                      <p className={`text-[16px] text-[var(--text-secondary)] leading-relaxed italic opacity-90 ${isIndic ? 'font-devanagari' : 'font-serif'}`}>
                        {note.trim()}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

              {result && result.benchmark && (
                <BenchmarkCard 
                  heading={t.benchmarkHeader}
                  genre={result.benchmark.genre}
                  text={result.benchmark.text}
                  note={t.benchmarkNote}
                />
              )}

            </div>
          )}
        </aside>

      </div>
>>>>>>> 97560627672de09f8ba5b9671d2d9a310ae2586d
    </div>
  );
}
