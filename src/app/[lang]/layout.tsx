import type { Metadata } from "next";
import { Inter, Outfit } from "next/font/google";
import "../globals.css";
import Header from "@/components/Header";
import Sidebar from "@/components/Sidebar";
import { getSortedPostsData } from "@/lib/posts";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const outfit = Outfit({ subsets: ["latin"], variable: "--font-outfit" });

export const metadata: Metadata = {
  title: "Wook's AI and Marketing",
  description: "글로벌 Digital Marketing & eCommerce 전문가. Data와 AI를 공부하면서 배운 내용들을 AI로 만든 자동화 블로그로 기록합니다.",
  verification: {
    google: "VEKICMa0sx4OpQaX_Aj0-5pNDI9NrEjyK9D7-W_R0Ug",
  },
};

export async function generateStaticParams() {
  return [{ lang: "ko" }, { lang: "en" }];
}

export default async function RootLayout({
  children,
  params,
}: Readonly<{
  children: React.ReactNode;
  params: Promise<{ lang: string }>;
}>) {
  const { lang } = await params;

  // Header에 전달할 카테고리별 포스트 수 계산
  const posts = getSortedPostsData(lang);
  const categoriesMap = posts.reduce((acc, post) => {
    const cat = post.category || "Insight";
    acc[cat] = (acc[cat] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);
  
  const excludedCategories = new Set(['backups']);
  const categoryCounts = Object.entries(categoriesMap)
    .filter(([name]) => !excludedCategories.has(name.toLowerCase()))
    .map(([name, count]) => ({
      name,
      slug: name.toLowerCase().replace(/\s+/g, '-'),
      count
    }));

  return (
    <html lang={lang} className={`${inter.variable} ${outfit.variable}`}>
      <body className="antialiased overflow-x-hidden min-h-screen bg-white">
        <Header lang={lang} categoryCounts={categoryCounts} />
        
        {/* Minimal Mistakes 2-column Layout */}
        <div className="max-w-[1180px] mx-auto px-6 pt-2 md:pt-3 pb-8 md:flex md:gap-10 lg:gap-14">
          <Sidebar lang={lang} />
          
          <main className="flex-1 w-full max-w-3xl min-w-0">
            {children}
          </main>
        </div>

        {/* Global Footer */}
        <footer className="w-full text-center py-3 border-t border-gray-100 mt-auto bg-gray-50/50">
          <p className="text-xs text-neutral-500 max-w-2xl mx-auto px-6 leading-relaxed">
            <span className="font-bold text-neutral-800">Wook Kwon</span> — Digital Marketing and Ecommerce expert, Ph.D candidate, Data science and AI.
            <a href="https://www.linkedin.com/in/wook-kwon/" target="_blank" rel="noopener noreferrer" className="ml-2 text-blue-600 hover:text-blue-800 hover:underline">
              LinkedIn
            </a>
          </p>
        </footer>
      </body>
    </html>
  );
}
