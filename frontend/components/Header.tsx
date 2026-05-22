import Link from "next/link";

interface HeaderProps {
  showBack?: boolean;
}

export default function Header({ showBack = false }: HeaderProps) {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-[#fafaf8]/80 backdrop-blur-md border-b border-[#e9e9e5]">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-8">
          <Link href="/" className="text-[18px] font-bold tracking-tighter text-[#1a1a18] font-serif italic">
            NarrativeIQ
          </Link>
          
          {showBack && (
            <Link href="/" className="text-[11px] uppercase tracking-widest font-black text-[#9e9e9a] hover:text-[#1a1a18] transition-colors">
              &larr; Back to Home
            </Link>
          )}
        </div>

        <div className="flex items-center gap-6">
          {!showBack ? (
            <Link href="/workspace" className="text-[13px] font-black uppercase tracking-widest text-[#4338ca] hover:opacity-70 transition-opacity">
              Open Workspace &rarr;
            </Link>
          ) : (
            <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-50 border border-indigo-100">
              <div className="w-1.5 h-1.5 rounded-full bg-[#4338ca] animate-pulse"></div>
              <span className="text-[10px] font-black uppercase tracking-widest text-[#4338ca]">Live Session</span>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
