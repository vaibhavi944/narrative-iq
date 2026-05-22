import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "NarrativeIQ — Premium AI Developmental Editor",
  description: "Elevate your storytelling with multilingual narrative intelligence.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="font-sans bg-[#fafaf8] text-[#1a1a18] min-h-screen selection:bg-[#eef2ff] selection:text-[#4338ca] antialiased">
        {children}
      </body>
    </html>
  );
}
