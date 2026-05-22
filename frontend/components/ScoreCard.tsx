interface ScoreCardProps {
  label: string;
  summary: string;
  score: number;
  pacing: number;
  repetition: number;
  emotion: number;
  language: string;
}

export default function ScoreCard({ label, summary, score, pacing, repetition, emotion, language }: ScoreCardProps) {
  const allLabels = {
    english: {
      strength: "Writing Strength",
      flow: "Flow",
      variety: "Word Variety",
      depth: "Emotion"
    },
    hindi: {
      strength: "लेखन की शक्ति",
      flow: "प्रवाह",
      variety: "शब्दों का बदलाव",
      depth: "भावना"
    },
    marathi: {
      strength: "लेखन सामर्थ्य",
      flow: "प्रवाह",
      variety: "शब्दांमधील विविधता",
      depth: "भावना"
    }
  };

  const labels = allLabels[language as keyof typeof allLabels] || allLabels.english;

  const metrics = [
    { label: labels.flow, val: pacing },
    { label: labels.variety, val: repetition },
    { label: labels.depth, val: emotion }
  ];

  return (
    <div className="flex flex-col gap-10 animate-in fade-in duration-500" lang={language === 'english' ? 'en' : language === 'hindi' ? 'hi' : 'mr'}>
      {/* Primary Strength Header */}
      <div className="flex flex-col gap-6">
        <div className="flex items-end justify-between border-b border-[#e9e9e5] pb-6">
          <div className="flex flex-col gap-1">
            <span className={`text-[12px] font-black uppercase tracking-[0.2em] ${
              label.toLowerCase().includes('strong') || label.includes('मजबूत') ? 'text-green-600' : 
              label.toLowerCase().includes('moderate') || label.includes('मध्यम') ? 'text-amber-600' : 'text-red-600'
            } ${language !== 'english' ? 'font-devanagari' : ''}`}>
              {label}
            </span>
            <h2 className={`text-[32px] font-serif italic text-[#1a1a18] leading-none ${language !== 'english' ? 'font-devanagari not-italic' : ''}`}>
              {labels.strength}
            </h2>
          </div>
          <span className="text-[54px] font-black text-[#4338ca] leading-none tracking-tighter">
            {Math.round(score * 100)}%
          </span>
        </div>
        
        <p className={`text-[17px] text-[#52524e] italic leading-relaxed font-serif opacity-90 border-l-2 border-[#4338ca] pl-6 py-1 ${language !== 'english' ? 'font-devanagari not-italic' : ''}`}>
          &ldquo;{summary}&rdquo;
        </p>
      </div>

      {/* Metric Grid */}
      <div className="grid grid-cols-1 gap-8">
        {metrics.map((m, i) => (
          <div key={i} className="flex flex-col gap-3 group">
            <div className="flex justify-between items-end">
              <span className={`text-[11px] font-bold text-[#9e9e9a] uppercase tracking-[0.15em] group-hover:text-[#4338ca] transition-colors ${language !== 'english' ? 'font-devanagari' : ''}`}>
                {m.label}
              </span>
              <span className="text-[14px] font-black text-[#1a1a18]">
                {Math.round(m.val * 100)}%
              </span>
            </div>
            <div className="h-[3px] w-full bg-[#e9e9e5] relative overflow-hidden rounded-full">
              <div 
                className="absolute top-0 left-0 h-full bg-[#4338ca] transition-all duration-1000 ease-out group-hover:bg-indigo-400"
                style={{ width: `${m.val * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
