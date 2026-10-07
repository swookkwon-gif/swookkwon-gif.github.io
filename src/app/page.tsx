import Link from "next/link";
import { getSortedPostsData } from "@/lib/posts";
import { ArrowRight, Calendar, Clock, Tag } from "lucide-react";

export default function Home() {
  const posts = getSortedPostsData();

  return (
    <main className="space-y-12">
      {/* Hero Section */}
      <section className="space-y-4 pb-8 border-b border-neutral-200">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 text-blue-700 text-xs font-semibold tracking-wide">
          <span className="w-2 h-2 rounded-full bg-blue-600 animate-pulse" />
          Technical Research Lab
        </div>
        <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight text-neutral-950 leading-[1.2]">
          Generative Engine Optimization (GEO)
        </h1>
        <p className="text-base md:text-lg text-neutral-600 max-w-2xl leading-relaxed">
          SearchGPT, Perplexity, Claude 등 차세대 생성형 AI 검색 엔진의 인용 메커니즘을 규명하고, 기업과 데이터의 가시성을 극대화하기 위한 아키텍처 방법론을 탐구합니다.
        </p>
      </section>

      {/* Research Papers & Articles Section */}
      <section className="space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold tracking-tight text-neutral-900">
            최신 연구 리포트 (Latest Research)
          </h2>
          <span className="text-xs font-medium text-neutral-500">
            총 {posts.length}편의 리포트
          </span>
        </div>

        {posts.length === 0 ? (
          <div className="rounded-xl border border-dashed border-neutral-300 p-12 text-center bg-white space-y-3">
            <h3 className="font-semibold text-neutral-800 text-base">
              새로운 연구 리포트를 준비 중입니다
            </h3>
            <p className="text-sm text-neutral-500 max-w-md mx-auto">
              GEO 알고리즘 분석 및 인용 최적화 벤치마크 데이터 리포트가 곧 발행될 예정입니다.
            </p>
          </div>
        ) : (
          <div className="divide-y divide-neutral-200">
            {posts.map((post) => (
              <article
                key={post.slug}
                className="py-6 first:pt-0 last:pb-0 group transition-all"
              >
                <div className="space-y-3">
                  <div className="flex flex-wrap items-center gap-3 text-xs text-neutral-500">
                    <span className="inline-flex items-center gap-1 font-semibold text-blue-600 bg-blue-50 px-2 py-0.5 rounded">
                      <Tag size={12} />
                      {post.category}
                    </span>
                    <span className="inline-flex items-center gap-1">
                      <Calendar size={12} />
                      {post.date}
                    </span>
                    {post.readingTime && (
                      <span className="inline-flex items-center gap-1">
                        <Clock size={12} />
                        {post.readingTime}분 분량
                      </span>
                    )}
                  </div>

                  <h3 className="text-xl md:text-2xl font-bold text-neutral-900 group-hover:text-blue-600 transition-colors tracking-tight">
                    <Link href={`/posts/${post.slug}/`}>
                      {post.title}
                    </Link>
                  </h3>

                  <p className="text-sm md:text-base text-neutral-600 leading-relaxed line-clamp-2">
                    {post.excerpt}
                  </p>

                  <div className="pt-1">
                    <Link
                      href={`/posts/${post.slug}/`}
                      className="inline-flex items-center gap-1.5 text-xs font-semibold text-neutral-900 group-hover:text-blue-600 transition-colors"
                    >
                      리포트 전문 읽기 <ArrowRight size={13} className="transition-transform group-hover:translate-x-1" />
                    </Link>
                  </div>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}
