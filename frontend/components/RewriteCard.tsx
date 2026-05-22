import { useState } from "react";

interface RewriteCardProps {
  heading: string;
  rewrite: string | null;
  loading: boolean;
  btnText: string;
  loadingText: string;
  onRewrite: () => void;
}

export default function RewriteCard({ 
  heading, 
  rewrite, 
  loading, 
  btnText, 
  loadingText, 
  onRewrite 
}: RewriteCardProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    if (rewrite) {
      navigator.clipboard.writeText(rewrite);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="flex flex-col gap-6 animate-in fade-in">
      {!rewrite ? (
        <button 
          onClick={onRewrite}
          disabled={loading}
          className="w-full py-4 text-[14px] font-bold border border-[#4338ca] text-[#4338ca] rounded-full hover:bg-indigo-50 transition-all flex items-center justify-center gap-3 disabled:opacity-50 uppercase tracking-[0.2em]"
        >
          {loading && <div className="spinner" />}
          {loading ? loadingText : btnText}
        </button>
      ) : (
        <div className="flex flex-col gap-4 animate-in slide-in-from-top-2">
          <h3 className="text-[12px] font-bold text-[#9e9e9a] uppercase tracking-widest">
            {heading}
          </h3>
          <div className="bg-white border border-[#4338ca]/20 rounded-3xl p-8 relative group luxury-card">
            <button 
              onClick={handleCopy}
              className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity text-[#9e9e9a] hover:text-[#4338ca]"
              title="Copy to clipboard"
            >
              {copied ? (
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
              ) : (
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
              )}
            </button>
            <p className="font-serif text-[17px] text-[#1a1a18] leading-relaxed">
              {rewrite}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
