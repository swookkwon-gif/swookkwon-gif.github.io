"use client";

import Link from "next/link";
import { BookOpen, ExternalLink } from "lucide-react";

export default function Header() {
  return (
    <header className="border-b border-neutral-200/80 bg-white/95 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-4xl mx-auto px-6 h-16 flex items-center justify-between">
        {/* Site Branding */}
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="w-8 h-8 rounded-lg bg-neutral-900 text-white flex items-center justify-center font-bold text-sm tracking-wider shadow-sm group-hover:bg-blue-600 transition-colors">
            G
          </div>
          <div className="flex flex-col">
            <span className="font-bold text-base tracking-tight text-neutral-900 group-hover:text-blue-600 transition-colors">
              GEO Research
            </span>
            <span className="text-[11px] font-medium text-neutral-500 tracking-normal -mt-0.5">
              Generative Engine Optimization Lab
            </span>
          </div>
        </Link>

        {/* Navigation & Author Links */}
        <nav className="flex items-center gap-6 text-sm font-medium text-neutral-600">
          <Link
            href="/"
            className="hover:text-neutral-900 transition-colors flex items-center gap-1.5"
          >
            <BookOpen size={16} />
            <span>Research</span>
          </Link>
          <a
            href="https://www.linkedin.com/in/wook-kwon/"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-neutral-900 transition-colors flex items-center gap-1 text-xs text-neutral-500 bg-neutral-100 hover:bg-neutral-200 px-2.5 py-1 rounded-md"
          >
            <span>Author</span>
            <ExternalLink size={12} />
          </a>
        </nav>
      </div>
    </header>
  );
}
