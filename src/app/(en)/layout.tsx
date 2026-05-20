import type { Metadata } from "next";
import { Inter, Outfit } from "next/font/google";
import "../globals.css";
import Header from "@/components/Header";
import Sidebar from "@/components/Sidebar";
import { getSortedPostsData } from "@/lib/posts";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const outfit = Outfit({ subsets: ["latin"], variable: "--font-outfit" });

export const metadata: Metadata = {
  metadataBase: new URL("https://swookkwon-gif.github.io"),
  title: {
    template: "%s | Wook's AI and Marketing",
    default: "Wook's AI and Marketing",
  },
  description: "Global Digital Marketing & eCommerce expert. Recording my learnings in Data and AI through an automated blog.",
  verification: {
    google: "VEKICMa0sx4OpQaX_Aj0-5pNDI9NrEjyK9D7-W_R0Ug",
  },
};

export default async function EnLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const lang = 'en';
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

        <div className="max-w-[1180px] mx-auto px-6 pt-2 md:pt-3 pb-8 md:flex md:gap-10 lg:gap-14">
          <Sidebar lang={lang} />
          <main className="flex-1 w-full max-w-3xl min-w-0">
            {children}
          </main>
        </div>

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
