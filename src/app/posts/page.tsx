import { Metadata } from "next";
import Link from "next/link";
import { getSortedPostsData } from "@/lib/posts";
import { ArrowLeft, Calendar, Tag } from "lucide-react";

export const metadata: Metadata = {
  title: "전체 리서치 아카이브",
  description: "GEO Research의 모든 연구 리포트 및 분석 아카이브입니다.",
  alternates: {
    canonical: "https://swookkwon-gif.github.io/posts/",
  },
};

export default function PostsArchivePage() {
  const posts = getSortedPostsData();

  return (
    <div className="space-y-8">
      <div>
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-neutral-500 hover:text-neutral-900 transition-colors"
        >
          <ArrowLeft size={14} /> 홈으로 돌아가기
        </Link>
      </div>

      <header className="pb-4 border-b border-neutral-200">
        <h1 className="text-2xl md:text-3xl font-extrabold text-neutral-950 tracking-tight">
          전체 리서치 아카이브
        </h1>
        <p className="text-sm text-neutral-600 mt-1">
          총 {posts.length}편의 리포트가 등록되어 있습니다.
        </p>
      </header>

      <div className="divide-y divide-neutral-200">
        {posts.map((post) => (
          <article key={post.slug} className="py-5 first:pt-0 group">
            <div className="flex items-center gap-3 text-xs text-neutral-500 mb-2">
              <span className="font-semibold text-blue-700 bg-blue-50 px-2 py-0.5 rounded flex items-center gap-1">
                <Tag size={12} /> {post.category}
              </span>
              <span className="flex items-center gap-1">
                <Calendar size={12} /> {post.date}
              </span>
            </div>
            <h2 className="text-lg md:text-xl font-bold text-neutral-900 group-hover:text-blue-600 transition-colors">
              <Link href={`/posts/${post.slug}/`}>{post.title}</Link>
            </h2>
            <p className="text-sm text-neutral-600 mt-2 line-clamp-2">
              {post.excerpt}
            </p>
          </article>
        ))}
      </div>
    </div>
  );
}
