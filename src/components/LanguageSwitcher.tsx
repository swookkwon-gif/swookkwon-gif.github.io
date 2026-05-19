"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Globe } from "lucide-react";

export default function LanguageSwitcher({ currentLang }: { currentLang: string }) {
  const pathname = usePathname();

  // 한국어(루트) → 영어(/en): /posts/X → /en/posts/X
  // 영어(/en) → 한국어(루트): /en/posts/X → /posts/X
  const newPathname = currentLang === 'ko'
    ? `/en${pathname}`
    : (pathname.replace(/^\/en/, '') || '/');

  return (
    <Link
      href={newPathname}
      className="flex items-center gap-1 ml-2 md:ml-4 px-3 py-1.5 rounded-full bg-neutral-100 hover:bg-neutral-200 text-neutral-700 transition-colors text-[12px] font-bold tracking-wider"
    >
      <Globe size={14} />
      {currentLang === "ko" ? "EN" : "KO"}
    </Link>
  );
}
