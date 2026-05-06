"use client";

import Link from "next/link";
import { Menu, X } from "lucide-react";
import LanguageSwitcher from "./LanguageSwitcher";
import { useState } from "react";

interface CategoryCount {
  name: string;
  slug: string;
  count: number;
}

export default function Header({ lang, categoryCounts }: { lang: string; categoryCounts?: CategoryCount[] }) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  // Fallback to hardcoded if not provided
  const defaultCategories = [
    { name: "Marketing", slug: "marketing", count: 0 },
    { name: "AI News", slug: "ai-news", count: 0 },
    { name: "AI Learnings", slug: "ai-learnings", count: 0 },
    { name: "Data", slug: "data", count: 0 },
  ];
  
  const displayCategories = categoryCounts || defaultCategories;

  return (
    <header className="border-b border-gray-100 bg-white relative z-50">
      <div className="max-w-[1280px] mx-auto px-6 h-16 flex items-center justify-between">
        {/* Site Title */}
        <Link href={`/${lang}`} className="font-bold text-lg tracking-tight text-neutral-900 group">
          Wook&apos;s <span className="text-neutral-500 group-hover:text-blue-600 transition-colors">AI and Marketing</span>
        </Link>
        
        {/* Desktop Nav */}
        <nav className="hidden md:flex items-center gap-8 text-[13px] font-bold text-neutral-500 uppercase tracking-wider">
          {displayCategories.map(cat => (
            <Link key={cat.slug} href={`/${lang}/category/${cat.slug}`} className="hover:text-blue-600 transition-colors">
              {cat.name}
            </Link>
          ))}
          <LanguageSwitcher currentLang={lang} />
        </nav>
        
        {/* Mobile Nav Toggle */}
        <div className="md:hidden flex items-center gap-4">
          <LanguageSwitcher currentLang={lang} />
          <button 
            className="flex items-center text-neutral-600 hover:text-neutral-900 transition-colors"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            aria-label="Toggle Menu"
          >
            {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Nav Dropdown */}
      {isMobileMenuOpen && (
        <div className="md:hidden absolute top-16 left-0 w-full bg-white border-b border-gray-100 shadow-lg px-6 py-4 flex flex-col gap-4 text-sm font-bold text-neutral-600 uppercase tracking-wider">
          {displayCategories.map(cat => (
            <Link key={cat.slug} href={`/${lang}/category/${cat.slug}`} onClick={() => setIsMobileMenuOpen(false)} className="hover:text-blue-600 py-2 border-b border-gray-50 flex items-center justify-between">
              <span>{cat.name}</span>
              <span className="text-xs text-neutral-400 bg-neutral-100 px-2.5 py-0.5 rounded-full">{cat.count}</span>
            </Link>
          ))}
        </div>
      )}
    </header>
  );
}
