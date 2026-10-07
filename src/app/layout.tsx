import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Header from "@/components/Header";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  metadataBase: new URL("https://swookkwon-gif.github.io"),
  title: {
    template: "%s | GEO Research",
    default: "GEO Research | 생성형 검색 최적화 연구소",
  },
  description:
    "SearchGPT, Perplexity, Claude 등 생성형 AI 검색 엔진(GEO) 아키텍처와 LLM 인용 최적화 방법론을 연구하는 테크니컬 리서치 블로그입니다.",
  authors: [{ name: "Wook Kwon", url: "https://www.linkedin.com/in/wook-kwon/" }],
  creator: "Wook Kwon",
  publisher: "GEO Research Lab",
  openGraph: {
    title: "GEO Research | 생성형 검색 최적화 연구소",
    description:
      "SearchGPT, Perplexity, Claude 등 생성형 AI 검색 엔진(GEO) 아키텍처와 LLM 인용 최적화 방법론을 연구하는 테크니컬 리서치 블로그입니다.",
    url: "https://swookkwon-gif.github.io",
    siteName: "GEO Research",
    locale: "ko_KR",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "GEO Research | 생성형 검색 최적화 연구소",
    description:
      "SearchGPT, Perplexity, Claude 등 생성형 AI 검색 엔진(GEO) 아키텍처와 LLM 인용 최적화 방법론 연구",
  },
  verification: {
    google: "VEKICMa0sx4OpQaX_Aj0-5pNDI9NrEjyK9D7-W_R0Ug",
  },
  alternates: {
    canonical: "https://swookkwon-gif.github.io",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko" className={inter.variable}>
      <body className="antialiased min-h-screen bg-neutral-50/40 text-neutral-900 flex flex-col font-sans">
        <Header />

        <div className="flex-1 w-full max-w-4xl mx-auto px-6 py-8 md:py-12">
          {children}
        </div>

        <footer className="w-full border-t border-neutral-200/80 bg-white py-8 mt-auto">
          <div className="max-w-4xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-neutral-500">
            <p className="leading-relaxed">
              © {new Date().getFullYear()} <span className="font-semibold text-neutral-800">GEO Research</span>. All rights reserved.
            </p>
            <div className="flex items-center gap-4">
              <a
                href="https://www.linkedin.com/in/wook-kwon/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-neutral-600 hover:text-blue-600 transition-colors"
              >
                Wook Kwon (Lead Researcher)
              </a>
              <span className="text-neutral-300">|</span>
              <a
                href="https://swookkwon-gif.github.io/sitemap.xml"
                target="_blank"
                rel="noopener noreferrer"
                className="text-neutral-500 hover:text-neutral-800 transition-colors"
              >
                Sitemap
              </a>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
