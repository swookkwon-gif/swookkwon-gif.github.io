import { Metadata } from "next";
import { getSortedPostsData, getPostData } from "@/lib/posts";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import rehypeExternalLinks from "rehype-external-links";
import remarkGfm from "remark-gfm";
import remarkKoreanBold from "@/lib/remark-korean-bold";
import Link from "next/link";
import { ArrowLeft, Calendar, Clock, Tag, Share2 } from "lucide-react";
import React from "react";
import ChartRenderer from "@/components/ChartRenderer";
import MermaidRenderer from "@/components/MermaidRenderer";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const post = getPostData(slug);
  const url = `https://swookkwon-gif.github.io/posts/${slug}/`;

  return {
    title: post.title,
    description: post.excerpt,
    keywords: post.tags,
    alternates: {
      canonical: url,
    },
    openGraph: {
      title: post.title,
      description: post.excerpt,
      type: "article",
      url,
      publishedTime: post.date,
      authors: ["Wook Kwon"],
      tags: post.tags,
    },
    twitter: {
      card: "summary_large_image",
      title: post.title,
      description: post.excerpt,
    },
  };
}

export async function generateStaticParams() {
  const posts = getSortedPostsData();
  return posts.map((post) => ({ slug: post.slug }));
}

export default async function PostPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const post = getPostData(slug);
  const postUrl = `https://swookkwon-gif.github.io/posts/${slug}/`;

  // TechArticle Schema.org JSON-LD (LLM 및 검색엔진 인용 신뢰도 최적화)
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "TechArticle",
    headline: post.title,
    description: post.excerpt,
    author: {
      "@type": "Person",
      name: "Wook Kwon",
      url: "https://www.linkedin.com/in/wook-kwon/",
    },
    publisher: {
      "@type": "Organization",
      name: "GEO Research",
      url: "https://swookkwon-gif.github.io",
    },
    datePublished: post.date,
    dateModified: post.date,
    mainEntityOfPage: {
      "@type": "WebPage",
      "@id": postUrl,
    },
    keywords: post.tags?.join(", ") || "GEO, AI Search, LLM",
    inLanguage: "ko-KR",
  };

  return (
    <article className="w-full space-y-8">
      {/* Schema.org Injection */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      {/* Navigation Back */}
      <div>
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-neutral-500 hover:text-neutral-900 transition-colors"
        >
          <ArrowLeft size={14} /> 리서치 목록으로 돌아가기
        </Link>
      </div>

      {/* Post Header */}
      <header className="space-y-4 pb-6 border-b border-neutral-200">
        <div className="flex flex-wrap items-center gap-3 text-xs text-neutral-500">
          <span className="font-semibold text-blue-700 bg-blue-50 px-2 py-0.5 rounded flex items-center gap-1">
            <Tag size={12} />
            {post.category}
          </span>
          <span className="flex items-center gap-1">
            <Calendar size={12} />
            {post.date}
          </span>
          {post.readingTime && (
            <span className="flex items-center gap-1">
              <Clock size={12} />
              {post.readingTime}분 분량
            </span>
          )}
        </div>

        <h1 className="text-2xl md:text-4xl font-extrabold text-neutral-950 tracking-tight leading-[1.25]">
          {post.title}
        </h1>

        {post.excerpt && (
          <div className="bg-neutral-100/70 border-l-4 border-blue-600 p-4 rounded-r-lg text-sm md:text-base text-neutral-700 leading-relaxed font-medium">
            <span className="block text-xs font-bold uppercase tracking-wider text-blue-600 mb-1">
              Executive Summary (TL;DR)
            </span>
            {post.excerpt}
          </div>
        )}
      </header>

      {/* Post Body (Markdown) */}
      <div className="prose prose-neutral md:prose-lg max-w-none pb-12
        prose-headings:font-bold prose-headings:text-neutral-900 prose-headings:tracking-tight
        prose-h2:text-2xl md:prose-h2:text-3xl prose-h2:mt-10 prose-h2:mb-4 prose-h2:border-b prose-h2:border-neutral-200 prose-h2:pb-2
        prose-h3:text-xl md:prose-h3:text-2xl prose-h3:mt-8 prose-h3:mb-3
        prose-p:leading-relaxed prose-p:text-neutral-800
        prose-li:text-neutral-800
        prose-a:text-blue-600 prose-a:font-medium prose-a:underline hover:prose-a:text-blue-800
        prose-code:text-blue-700 prose-code:bg-blue-50 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:before:content-none prose-code:after:content-none
        prose-pre:bg-neutral-900 prose-pre:text-neutral-100 prose-pre:rounded-xl
        prose-blockquote:border-l-4 prose-blockquote:border-neutral-400 prose-blockquote:italic prose-blockquote:text-neutral-700
        prose-table:text-sm md:prose-table:text-base
      ">
        <ReactMarkdown
          remarkPlugins={[remarkGfm, remarkKoreanBold]}
          rehypePlugins={[
            rehypeRaw,
            [rehypeExternalLinks, { target: "_blank", rel: ["noopener", "noreferrer"] }],
          ]}
          components={{
            code({ node, inline, className, children, ...props }: any) {
              const match = /language-(\w+)/.exec(className || "");
              const lang = match ? match[1] : "";
              const value = String(children).replace(/\n$/, "");

              if (!inline && lang === "mermaid") {
                return <MermaidRenderer chart={value} />;
              }
              if (!inline && (lang === "chart" || lang === "chartjs" || lang === "json:chart")) {
                return <ChartRenderer dataStr={value} />;
              }

              return (
                <code className={className} {...props}>
                  {children}
                </code>
              );
            },
          }}
        >
          {post.content}
        </ReactMarkdown>
      </div>

      {/* Author Card & Footer */}
      <footer className="pt-8 border-t border-neutral-200 bg-white p-6 rounded-xl space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <span className="text-xs font-semibold text-neutral-500 uppercase tracking-wider block">
              Author
            </span>
            <span className="text-base font-bold text-neutral-900">
              Wook Kwon (권욱)
            </span>
            <p className="text-xs text-neutral-600 mt-1">
              Digital Marketing & eCommerce Director · Data Science & AI · Generative Engine Optimization
            </p>
          </div>
          <a
            href="https://www.linkedin.com/in/wook-kwon/"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-white bg-neutral-900 hover:bg-neutral-800 px-4 py-2 rounded-lg transition-colors self-start sm:self-center"
          >
            LinkedIn 프로필 방문
          </a>
        </div>
      </footer>
    </article>
  );
}
