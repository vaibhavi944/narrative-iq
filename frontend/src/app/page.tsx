"use client";

import React from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { PenLine, Zap, Globe2, Sparkles, ArrowRight, BookOpen, ScrollText } from "lucide-react";
import { cn } from "@/lib/utils";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#fafaf9] text-[#1c1917] selection:bg-indigo-500/10">
      <nav className="border-b border-stone-200 bg-white/80 backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center justify-between px-8 py-4 max-w-7xl mx-auto">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 bg-indigo-700 rounded-lg flex items-center justify-center">
              <PenLine className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-semibold tracking-tight text-stone-900 italic serif">NarrativeIQ</span>
          </div>
          <div className="flex items-center gap-8">
            <Link 
              href="/editor"
              className="px-5 py-2 bg-stone-900 text-white text-sm font-medium rounded-full hover:bg-stone-800 transition-all flex items-center gap-2"
            >
              Start Writing
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </nav>

      <main>
        {/* Hero Section */}
        <section className="px-6 pt-32 pb-24 max-w-5xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
          >
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-indigo-50 border border-indigo-100 text-indigo-700 text-[13px] font-semibold mb-8 tracking-tight">
              <Sparkles className="w-3.5 h-3.5" />
              <span>An Intelligent Companion for Your Stories</span>
            </div>
            <h1 className="text-6xl md:text-8xl font-semibold tracking-tight text-stone-900 mb-8 leading-[0.95] serif italic">
              Write with <br /> Heart.
            </h1>
            <p className="text-xl text-stone-500 max-w-2xl mx-auto mb-12 leading-relaxed font-medium tracking-tight">
              A gentle writing mentor that helps you find the perfect rhythm. Improve your flow, clarify your prose, and deepen the emotional impact of every scene.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-5">
              <Link
                href="/editor"
                className="px-10 py-4 bg-indigo-700 hover:bg-indigo-600 text-white rounded-full font-semibold transition-all shadow-lg shadow-indigo-200"
              >
                Go to Workspace
              </Link>
            </div>
          </motion.div>
        </section>

        {/* Feature Grid */}
        <section className="px-8 py-32 border-t border-stone-200 bg-white">
          <div className="max-w-7xl mx-auto">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-16">
              <FeatureCard 
                icon={<Zap className="w-6 h-6 text-indigo-700" />}
                title="Find Your Rhythm"
                description="We help you balance short and long sentences to create a natural, engaging flow for your readers."
              />
              <FeatureCard 
                icon={<ScrollText className="w-6 h-6 text-indigo-700" />}
                title="Learn from the Best"
                description="We compare your scenes against high-quality stories to show you concrete examples of how to elevate your prose."
              />
              <FeatureCard 
                icon={<Globe2 className="w-6 h-6 text-indigo-700" />}
                title="Cross-Lingual Support"
                description="Whether you write in English, Hindi, or Marathi, NarrativeIQ understands the unique beauty of your language."
              />
            </div>
          </div>
        </section>

        {/* Comparison Section - The Differentiator */}
        <section className="px-8 py-32 bg-[#fafaf9] overflow-hidden">
          <div className="max-w-6xl mx-auto">
            <div className="mb-20">
              <h2 className="text-4xl font-semibold text-stone-900 mb-6 serif italic">Guided Improvement.</h2>
              <p className="text-stone-500 text-lg max-w-xl">NarrativeIQ finds beautiful examples from other stories to show you exactly how to transform a simple draft into an immersive scene.</p>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-20 items-start">
              <div className="space-y-12">
                <div className="relative">
                  <div className="absolute -left-4 top-0 bottom-0 w-1 bg-amber-400/20" />
                  <span className="text-[12px] font-bold uppercase tracking-widest text-stone-400 mb-4 block">A Simple Start</span>
                  <p className="text-xl text-stone-600 font-serif leading-relaxed italic">
                    "The boy walked home. The boy saw rain. The boy was sad."
                  </p>
                </div>
                <div className="relative">
                  <div className="absolute -left-4 top-0 bottom-0 w-1 bg-indigo-600" />
                  <span className="text-[12px] font-bold uppercase tracking-widest text-indigo-700 mb-4 block">A Stronger Example</span>
                  <p className="text-xl text-stone-900 font-serif leading-relaxed italic">
                    "As the cold rain began to fall, he walked home with a heavy heart, the mist swirling around his boots."
                  </p>
                </div>
              </div>
              
              <div className="bg-white p-12 rounded-[2rem] border border-stone-200/60 shadow-sm relative">
                <div className="flex items-center gap-3 mb-8">
                  <div className="w-8 h-8 rounded-full bg-indigo-700 flex items-center justify-center">
                    <Sparkles className="w-4 h-4 text-white" />
                  </div>
                  <span className="font-semibold text-stone-900">Your Mentor's Note</span>
                </div>
                <p className="text-stone-600 leading-relaxed text-lg mb-8">
                  "The second version flows better because it uses different sentence lengths and descriptive details that help the reader feel the character's sadness, rather than just stating it."
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Final CTA */}
        <section className="px-8 py-40 bg-white text-center border-t border-stone-100">
          <h2 className="text-5xl font-semibold text-stone-900 mb-12 serif italic tracking-tight">Ready to refine your prose?</h2>
          <Link
            href="/editor"
            className="inline-flex items-center gap-3 px-12 py-5 bg-stone-900 hover:bg-indigo-700 text-white rounded-full font-semibold transition-all shadow-xl shadow-stone-200"
          >
            Enter Workspace
            <ArrowRight className="w-5 h-5" />
          </Link>
        </section>
      </main>

      <footer className="px-8 py-16 bg-white border-t border-stone-200 text-center text-stone-400 text-sm font-medium">
        &copy; 2026 NarrativeIQ. Professional AI Editorial Software.
      </footer>
    </div>
  );
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="group">
      <div className="mb-8 p-4 bg-stone-50 rounded-2xl w-fit group-hover:bg-indigo-50 transition-colors">
        {icon}
      </div>
      <h3 className="text-xl font-semibold text-stone-900 mb-4 tracking-tight">{title}</h3>
      <p className="text-stone-500 leading-relaxed font-medium tracking-tight">
        {description}
      </p>
    </div>
  );
}
