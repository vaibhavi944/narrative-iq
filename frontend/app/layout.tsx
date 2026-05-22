import type { Metadata } from "next";
import { Geist, Newsreader, Mukta } from "next/font/google";
import "./globals.css";

const geist = Geist({ 
  subsets: ["latin"],
  variable: "--font-geist",
  display: "swap"
});

const newsreader = Newsreader({ 
  subsets: ["latin"],
  variable: "--font-newsreader",
  display: "swap",
  style: ["normal", "italic"],
  weight: ["300", "400", "500", "600", "700", "800"]
});

const mukta = Mukta({
  subsets: ["devanagari", "latin"],
  variable: "--font-mukta",
  display: "swap",
  weight: ["200", "300", "400", "500", "600", "700", "800"]
});

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
      <body className={`${geist.variable} ${newsreader.variable} ${mukta.variable} font-sans bg-[#fafaf8] text-[#1a1a18] min-h-screen selection:bg-[#eef2ff] selection:text-[#4338ca] antialiased`}>
        {children}
      </body>
    </html>
  );
}
