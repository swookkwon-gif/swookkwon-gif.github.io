"use client";

import { useState, useEffect } from "react";
import { ChevronRight, FileText } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

interface PostItem {
  slug: string;
  title: string;
  date: string;
  category: string;
}

interface CategoryData {
  name: string;
  slug: string;
  posts: PostItem[];
}

interface SidebarNavProps {
  categories: CategoryData[];
  lang: string;
}

export default function SidebarNav({ categories, lang }: SidebarNavProps) {
  const pathname = usePathname();
  const INITIAL_COUNT = 5;

  // 현재 URL에서 활성 카테고리 감지
  const detectActiveCategory = (): string | null => {
    // 카테고리 페이지: /ko/category/ai-news
    const catMatch = pathname.match(/\/category\/([^/]+)/);
    if (catMatch) {
      return catMatch[1];
    }
    // 포스트 페이지: /ko/posts/slug → 해당 포스트의 카테고리 찾기
    const postMatch = pathname.match(/\/posts\/([^/]+)/);
    if (postMatch) {
      const postSlug = postMatch[1];
      for (const cat of categories) {
        if (cat.posts.some(p => p.slug === postSlug)) {
          return cat.slug;
        }
      }
    }
    return null;
  };

  const activeSlug = detectActiveCategory();
  const defaultOpen = categories.length > 0 ? categories[0].slug : null;
  const [openCategory, setOpenCategory] = useState<string | null>(activeSlug || defaultOpen);

  // URL 변경 시 활성 카테고리 갱신
  useEffect(() => {
    const active = detectActiveCategory();
    if (active) {
      setOpenCategory(active);
    }
  }, [pathname]);

  const toggleCategory = (slug: string) => {
    setOpenCategory(prev => (prev === slug ? null : slug));
  };

  // 현재 보고 있는 포스트의 slug
  const currentPostSlug = pathname.match(/\/posts\/([^/]+)/)?.[1] || null;

  return (
    <nav className="sidebar-nav">
      {/* 전체 개요 헤더 */}
      <div className="sidebar-overview">
        <FileText className="w-4 h-4 text-neutral-400" />
        <span className="text-xs font-medium text-neutral-500 uppercase tracking-wider">
          Categories
        </span>
        <span className="sidebar-total-badge">
          {categories.reduce((sum, c) => sum + c.posts.length, 0)}
        </span>
      </div>

      {/* 카테고리 리스트 */}
      <ul className="sidebar-category-list">
        {categories.map((cat) => {
          const isOpen = openCategory === cat.slug;
          const isActiveCategory = activeSlug === cat.slug;
          const displayPosts = cat.posts.slice(0, INITIAL_COUNT);
          const hasMore = cat.posts.length > INITIAL_COUNT;

          return (
            <li key={cat.slug} className="sidebar-category-item">
              {/* 카테고리 헤더 */}
              <button
                onClick={() => toggleCategory(cat.slug)}
                className={`sidebar-category-header ${isActiveCategory ? "active" : ""}`}
                aria-expanded={isOpen}
              >
                <div className="sidebar-category-left">
                  <ChevronRight
                    className={`sidebar-chevron ${isOpen ? "open" : ""}`}
                  />
                  <span className="sidebar-category-name">{cat.name}</span>
                </div>
                <span className={`sidebar-count-badge ${isActiveCategory ? "active" : ""}`}>
                  {cat.posts.length}
                </span>
              </button>

              {/* 포스트 리스트 (아코디언) */}
              <div className={`sidebar-posts-wrapper ${isOpen ? "open" : ""}`}>
                <ul className="sidebar-posts-list">
                  {displayPosts.map((post) => {
                    const isCurrentPost = currentPostSlug === post.slug;
                    return (
                      <li key={post.slug}>
                        <Link
                          href={`/${lang}/posts/${post.slug}`}
                          className={`sidebar-post-link ${isCurrentPost ? "current" : ""}`}
                          title={post.title}
                        >
                          <span className="sidebar-post-dot" />
                          <span className="sidebar-post-title">{post.title}</span>
                        </Link>
                      </li>
                    );
                  })}

                  {/* 카테고리 전체보기 링크 */}
                  {hasMore && (
                    <li>
                      <Link
                        href={`/${lang}/category/${cat.slug}`}
                        className="sidebar-expand-btn text-neutral-500 hover:text-blue-600 hover:border-blue-200 transition-colors"
                      >
                        카테고리 전체보기 ({cat.posts.length}) &rarr;
                      </Link>
                    </li>
                  )}
                </ul>
              </div>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
