interface LanguageSelectorProps {
  selected: string;
  onChange: (language: string) => void;
}

export default function LanguageSelector({ selected, onChange }: LanguageSelectorProps) {
  const languages = [
    { id: "english", label: "English" },
    { id: "hindi", label: "हिन्दी" },
    { id: "marathi", label: "मराठी" }
  ];

  return (
    <div className="flex gap-4 p-1 bg-[#f1f1ee] rounded-full border border-[#e5e5e1]">
      {languages.map((lang) => {
        const isSelected = selected === lang.id;
        return (
          <button
            key={lang.id}
            onClick={() => onChange(lang.id)}
            className={`px-6 py-1.5 rounded-full text-[11px] font-black uppercase tracking-widest transition-all ${
              isSelected
                ? "bg-white text-[#1a1a18] shadow-sm"
                : "text-[#9e9e9a] hover:text-[#1a1a18]"
            }`}
          >
            {lang.label}
          </button>
        );
      })}
    </div>
  );
}
