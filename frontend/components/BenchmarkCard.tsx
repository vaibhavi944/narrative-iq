interface BenchmarkCardProps {
  heading: string;
  genre: string;
  text: string;
  note: string;
}

export default function BenchmarkCard({ heading, genre, text, note }: BenchmarkCardProps) {
  return (
    <div className="flex flex-col gap-6 animate-in fade-in duration-1000">
      <div className="flex items-center justify-between">
        <h3 className="text-[11px] font-bold text-[#9e9e9a] uppercase tracking-[0.2em]">
          {heading}
        </h3>
        <span className="px-2 py-0.5 rounded bg-[#f1f1ee] text-[9px] font-black uppercase tracking-widest text-[#52524e]">
          {genre}
        </span>
      </div>
      
      <div className="bg-white border border-[#e9e9e5] p-8 rounded-3xl luxury-card">
        <p className="font-serif text-[15px] text-[#1a1a18] leading-relaxed italic">
          &ldquo;{text}&rdquo;
        </p>
        <p className="text-[11px] text-[#9e9e9a] italic mt-4">
          {note}
        </p>
      </div>
    </div>
  );
}
