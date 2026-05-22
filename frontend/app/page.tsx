import Header from "@/components/Header";
import Link from "next/link";

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col bg-[#fafaf8]">
      <Header />
      
      <main className="flex-1 flex flex-col">
        
        {/* 1. HERO: Minimal & Graceful */}
        <section className="min-h-[90vh] flex flex-col items-center justify-center px-6 text-center relative overflow-hidden pt-20 md:pt-32 hero-glow">
          <div className="absolute inset-0 opacity-[0.02] pointer-events-none bg-[url('https://www.transparenttextures.com/patterns/p6-dark.png')]"></div>
          
          <div className="max-w-4xl mx-auto flex flex-col items-center reveal">
            <div className="inline-flex items-center gap-2.5 px-3 py-1 rounded-full bg-white border border-[#e5e5e1] mb-10 shadow-sm luxury-card">
              <span className="w-1.5 h-1.5 bg-[#4338ca] rounded-full animate-pulse"></span>
              <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-[#4338ca]">The Developmental Editor</span>
            </div>
            
            <h1 className="cinematic-heading text-[52px] md:text-[86px] text-[#1a1a18] mb-10 italic text-glow">
              Where stories find <br/> <span className="text-[#4338ca] not-italic">their rhythm.</span>
            </h1>
            
            <p className="text-[18px] md:text-[21px] text-[#52524e] leading-relaxed max-w-[580px] mb-14 font-light tracking-tight">
              Refine flow and depth across English, हिन्दी, and मराठी — <span className="font-medium">without losing your unique voice.</span>
            </p>
            
            <div className="flex flex-col items-center gap-3 mt-6 pb-20">
              <Link 
                href="/workspace" 
                className="group relative bg-[#1a1a18] text-white px-14 py-4.5 rounded-full font-bold text-[16px] transition-all hover:bg-[#4338ca] hover:shadow-2xl active:scale-95 overflow-hidden"
              >
                <span className="relative z-10">Enter the Workspace &rarr;</span>
                <div className="absolute inset-0 bg-gradient-to-r from-[#4338ca] to-[#3730a3] opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              </Link>
              
              <div className="flex items-center justify-center gap-2">
                <span className="text-[11px] text-[#1a1a18] font-black uppercase tracking-[0.1em] opacity-40">English</span>
                <span className="w-1 h-1 bg-[#1a1a18] rounded-full opacity-40"></span>
                <span className="text-[11px] text-[#1a1a18] font-black uppercase tracking-[0.1em] opacity-40">हिन्दी</span>
                <span className="w-1 h-1 bg-[#1a1a18] rounded-full opacity-40"></span>
                <span className="text-[11px] text-[#1a1a18] font-black uppercase tracking-[0.1em] opacity-40">मराठी</span>
              </div>
            </div>
          </div>
        </section>

        {/* 2. THE PHILOSOPHY: Stronger Contrast & Meaning */}
        <section className="bg-white py-24 px-6 border-y border-[#e9e9e5] relative">
          <div className="max-w-6xl mx-auto flex flex-col gap-16">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-20 items-center">
              
              <div className="lg:col-span-5 flex flex-col gap-8">
                <div className="space-y-4">
                  <h2 className="text-[11px] uppercase tracking-[0.4em] font-black text-[#4338ca] opacity-70">The Philosophy</h2>
                  <h3 className="cinematic-heading text-[48px] md:text-[68px] leading-tight text-[#1a1a18]">The soul of <br/> <span className="text-[#4338ca]">the sentence.</span></h3>
                </div>
                <p className="text-[18px] text-[#52524e] font-light leading-relaxed max-w-[440px]">
                  Good writing is about more than rules—it&apos;s about rhythm. NarrativeIQ finds the friction in your prose and releases the narrative voice hidden beneath.
                </p>
                <div className="flex items-center gap-4 text-[#4338ca] font-bold text-[13px] uppercase tracking-widest">
                  <span className="w-10 h-px bg-[#4338ca] opacity-30"></span>
                  Refinement through resonance
                </div>
              </div>

              <div className="lg:col-span-7 flex flex-col gap-px rounded-[40px] overflow-hidden shadow-2xl luxury-card">
                {/* Before */}
                <div className="bg-[#fafaf8] p-10 md:p-14 border-b border-[#e9e9e5]">
                  <div className="flex items-center gap-3 mb-6">
                    <div className="w-1.5 h-1.5 rounded-full bg-[#9e9e9a]"></div>
                    <span className="text-[10px] uppercase tracking-[0.3em] font-black text-[#9e9e9a]">Initial Thought (Friction)</span>
                  </div>
                  <p className="literary-prose italic text-[#52524e] opacity-60 leading-relaxed text-[20px]">
                    &ldquo;He opened the door. He looked inside the room. It was dark and cold. He felt a shiver. He was very scared.&rdquo;
                  </p>
                </div>
                
                {/* After */}
                <div className="bg-[#1a1a18] p-10 md:p-16 relative overflow-hidden group">
                  <div className="absolute top-0 right-0 w-64 h-64 bg-[#4338ca] opacity-[0.07] blur-[100px]"></div>
                  
                  <div className="flex items-center gap-3 mb-8 relative z-10">
                    <div className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-pulse"></div>
                    <span className="text-[10px] uppercase tracking-[0.3em] font-black text-indigo-300">Refined Rhythm (The Soul)</span>
                  </div>
                  <p className="literary-prose text-white leading-relaxed text-[22px] md:text-[24px] relative z-10 font-medium">
                    &ldquo;The door yielded with a heavy creak. Beyond the threshold, a sudden chill cut through his coat, anchoring him to the shadow-drenched floor.&rdquo;
                  </p>
                  
                  <div className="mt-10 flex gap-2 relative z-10">
                    <span className="px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-[9px] font-bold uppercase tracking-widest">Enhanced Imagery</span>
                    <span className="px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-[9px] font-bold uppercase tracking-widest">Varied Flow</span>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </section>

        {/* 3. MULTILINGUAL PRIDE: Editorial Asymmetric Layout */}
        <section className="bg-[#f4f4f2] py-24 px-6 relative overflow-hidden">
          <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            
            {/* Descriptive Side */}
            <div className="lg:col-span-5 flex flex-col gap-8">
              <div className="space-y-4">
                <h2 className="text-[11px] uppercase tracking-[0.4em] font-black text-[#4338ca] opacity-70">Native Intelligence</h2>
                <h3 className="cinematic-heading text-[42px] md:text-[56px] leading-tight text-[#1a1a18]">Global stories. <br/> <span className="text-[#4338ca] italic">Local textures.</span></h3>
              </div>
              <p className="text-[17px] text-[#52524e] font-light leading-relaxed max-w-[400px]">
                Analysis built for the unique emotional cadence of English, हिन्दी, and मराठी. We respect the script as much as the story.
              </p>
              <div className="flex gap-4 items-center opacity-40">
                <span className="text-[12px] font-black uppercase tracking-widest">EN</span>
                <div className="w-8 h-px bg-[#d8d8d4]"></div>
                <span className="text-[12px] font-black uppercase tracking-widest">हि</span>
                <div className="w-8 h-px bg-[#d8d8d4]"></div>
                <span className="text-[12px] font-black uppercase tracking-widest">म</span>
              </div>
            </div>

            {/* Stacked Card Side */}
            <div className="lg:col-span-7 relative pt-10 pb-10">
              <div className="flex flex-col gap-4">
                
                {/* English */}
                <div className="bg-white p-8 rounded-3xl luxury-card transform -rotate-1 hover:rotate-0 transition-all duration-500 max-w-[500px] ml-auto">
                  <p className="text-[13px] text-[#52524e] italic opacity-40 mb-3">&ldquo;The sun went down. It was a cold evening.&rdquo;</p>
                  <p className="text-[16px] text-[#1a1a18] font-medium">&ldquo;The sun dipped below jagged peaks, casting bruised shadows.&rdquo;</p>
                  <p className="text-[9px] font-black uppercase tracking-[0.2em] text-[#4338ca] mt-4 border-t border-[#f1f1ee] pt-3">English Refinement</p>
                </div>

                {/* Hindi */}
                <div className="bg-white p-8 rounded-3xl luxury-card transform rotate-2 translate-x-[-20px] hover:rotate-0 hover:translate-x-0 transition-all duration-500 max-w-[500px] relative z-10">
                  <p className="font-devanagari text-[16px] text-[#52524e] italic opacity-40 mb-3" lang="hi">&ldquo;बारिश हो रही थी। वह उदास था।&rdquo;</p>
                  <p className="font-devanagari text-[19px] text-[#1a1a18] leading-relaxed" lang="hi">&ldquo;रिमझिम फुहारों के बीच, वह खिड़की की चौखट थामे बैठा रहा, यादों की धुंध में कहीं खोया हुआ।&rdquo;</p>
                  <p className="text-[9px] font-black uppercase tracking-[0.2em] text-[#4338ca] mt-4 border-t border-[#f1f1ee] pt-3">Hindi Refinement</p>
                </div>

                {/* Marathi */}
                <div className="bg-white p-8 rounded-3xl luxury-card transform -rotate-1 translate-x-4 hover:rotate-0 hover:translate-x-0 transition-all duration-500 max-w-[500px] ml-auto">
                  <p className="font-devanagari text-[16px] text-[#52524e] italic opacity-40 mb-3" lang="mr">&ldquo;तो बागेत गेला। त्याने फुले पाहिली।&rdquo;</p>
                  <p className="font-devanagari text-[19px] text-[#1a1a18] leading-relaxed" lang="mr">&ldquo;बागेतील टवटवीत फुलांच्या सुगंधाने मनात एक नवी लहर उमटली।&rdquo;</p>
                  <p className="text-[9px] font-black uppercase tracking-[0.2em] text-[#4338ca] mt-4 border-t border-[#f1f1ee] pt-3">Marathi Refinement</p>
                </div>

              </div>
            </div>

          </div>
        </section>

        {/* 4. THE CRAFT: Clean Grid */}
        <section className="py-24 px-6 bg-[#fafaf8]">
          <div className="max-w-6xl mx-auto flex flex-col gap-16">
            <div className="flex flex-col gap-6 text-center">
              <h2 className="text-[12px] uppercase tracking-[0.5em] font-black text-[#4338ca] opacity-60">Editorial Intelligence</h2>
              <h3 className="cinematic-heading text-[42px] md:text-[56px] italic text-[#1a1a18]">Expertise in <span className="text-[#4338ca]">every byte.</span></h3>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-px bg-[#e9e9e5] border border-[#e9e9e5] rounded-[32px] overflow-hidden shadow-sm">
              {[
                { h: "Reading Flow", p: "We analyze rhythmic variance to eliminate monotonous patterns and strengthen engagement." },
                { h: "Narrative Variety", p: "Spot repetitive vocabulary and sentence structures that fatigue your reader." },
                { h: "Emotional Texture", p: "Identify moments that need more sensory grounding to truly immerse the reader." }
              ].map((item, i) => (
                <div key={i} className="flex flex-col gap-10 p-12 bg-[#fafaf8] hover:bg-white transition-colors group">
                  <span className="text-[13px] font-black text-[#4338ca] uppercase tracking-widest opacity-30 group-hover:opacity-100 transition-opacity">0{i+1}</span>
                  <div className="space-y-6">
                    <h4 className="text-[24px] font-bold font-serif italic text-[#1a1a18]">{item.h}</h4>
                    <p className="text-[15px] text-[#52524e] leading-relaxed font-light">{item.p}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* 5. MULTILINGUAL HERITAGE: Quiet Luxury Icons */}
        <section className="py-24 px-6 bg-white border-y border-[#e9e9e5]">
          <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div className="flex flex-col gap-8">
              <h2 className="text-[11px] uppercase tracking-[0.3em] font-black text-[#4338ca]">Universal Voice</h2>
              <h3 className="cinematic-heading text-[42px] md:text-[56px] text-[#1a1a18]">Three Scripts. <br/> <span className="text-[#4338ca]">One Editor.</span></h3>
              <p className="text-[18px] text-[#52524e] font-light leading-relaxed">
                NarrativeIQ is built to bridge linguistic boundaries. We provide native-level analysis for English, हिन्दी, and मराठी.
              </p>
            </div>
            
            <div className="grid grid-cols-1 gap-4">
              {[
                { l: "English", d: "Global storytelling.", s: "abc" },
                { l: "हिन्दी", d: "Rhythm of Devanagari.", s: "अ" },
                { l: "मराठी", d: "Emotional cadence.", s: "म" }
              ].map((lang) => (
                <div key={lang.l} className="flex items-center justify-between p-8 rounded-3xl bg-[#fafaf8] border border-[#e9e9e5] luxury-card">
                  <div className="flex items-center gap-8">
                    <span className="text-[28px] font-serif italic text-[#4338ca] opacity-30 w-10 text-center">{lang.s}</span>
                    <div className="space-y-0.5">
                      <h4 className="text-[17px] font-bold text-[#1a1a18]">{lang.l}</h4>
                      <p className="text-[13px] text-[#52524e] font-light">{lang.d}</p>
                    </div>
                  </div>
                  <div className="w-2 h-2 rounded-full bg-[#4338ca] opacity-20"></div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* 6. CLOSER */}
        <section className="h-[60vh] flex flex-col items-center justify-center px-6 bg-[#fafaf8] relative">
          <div className="max-w-2xl mx-auto flex flex-col items-center text-center reveal">
            <h2 className="cinematic-heading text-[40px] md:text-[64px] mb-10 text-[#1a1a18]">Every story <br/> <span className="text-[#4338ca]">deserves an editor.</span></h2>
            <Link 
              href="/workspace" 
              className="group relative bg-[#1a1a18] text-white px-14 py-4.5 rounded-full font-bold text-[16px] transition-all hover:bg-[#4338ca] hover:shadow-2xl active:scale-95 overflow-hidden"
            >
              <span className="relative z-10">Start Your Scene &rarr;</span>
              <div className="absolute inset-0 bg-gradient-to-r from-[#4338ca] to-[#3730a3] opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            </Link>
          </div>
          <div className="absolute bottom-10 left-1/2 -translate-x-1/2 font-serif text-[120px] md:text-[240px] opacity-[0.04] select-none pointer-events-none whitespace-nowrap tracking-tighter font-black text-[#1a1a18]">
            NARRATIVE
          </div>
        </section>
      </main>

      <footer className="py-16 px-12 border-t border-[#e9e9e5] bg-white text-[10px] text-[#9e9e9a] font-black uppercase tracking-[0.25em]">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-10">
          <div className="flex flex-col items-center md:items-start gap-4">
            <span className="text-[18px] font-bold tracking-tighter text-[#1a1a18] font-serif italic normal-case" lang="en">NarrativeIQ</span>
            <p className="opacity-60">Storytelling, refined.</p>
          </div>
          <p className="opacity-60 text-center md:text-right leading-loose">
            English &middot; हिन्दी &middot; मराठी <br/>
            &copy; 2026 NarrativeIQ &middot; Created by Vaibhavi Thote
          </p>
        </div>
      </footer>
    </div>
  );
}
