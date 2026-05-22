interface TipsListProps {
  heading: string;
  tips: string[];
}

export default function TipsList({ heading, tips }: TipsListProps) {
  if (!tips || tips.length === 0) return null;

  return (
    <div className="flex flex-col gap-6 animate-in fade-in duration-700">
      <h3 className="text-[11px] font-bold text-[#9e9e9a] uppercase tracking-[0.2em]">
        {heading}
      </h3>
      <div className="flex flex-col gap-4">
        {tips.map((tip, i) => (
          <div key={i} className="flex gap-5 group">
            <div className="w-[1.5px] h-auto bg-[#4338ca] opacity-20 group-hover:opacity-100 transition-opacity"></div>
            <p className="text-[16px] text-[#1a1a18] leading-relaxed py-0.5">
              {tip}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
