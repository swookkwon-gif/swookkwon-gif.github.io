import { Metadata } from "next";
import Link from "next/link";
import { getSortedPostsData } from "@/lib/posts";
import { notFound } from "next/navigation";
import { ArrowLeft, Calendar, Tag } from "lucide-react";

interface CategoryPageProps {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  const posts = getSortedPostsData();
  const categories = Array.from(new Set(posts.map((post) => post.category)));
  return categories.map((category) => ({
    slug: category.toLowerCase().replace(/\s+/g, "-"),
  }));
}

export async function generateMetadata({ params }: CategoryPageProps): Promise<Metadata> {
  const { slug } = await params;
  const posts = getSortedPostsData();
  const filteredPosts = posts.filter((post) => {
    const postCategorySlug = post.category.toLowerCase().replace(/\s+/g, "-");
    return postCategorySlug === slug;
  });

  if (filteredPosts.length === 0) {
    return { title: "Category Not Found" };
  }

  const displayCategory = filteredPosts[0].category;

  return {
    title: `${displayCategory} 리서치 리포트`,
    description: `${displayCategory} 관련 GEO 리서치 리포트 목록입니다.`,
    alternates: {
      canonical: `https://swookkwon-gif.github.io/category/${slug}/`,
    },
  };
}

export default async function CategoryPage({ params }: CategoryPageProps) {
  const { slug } = await params;
  const posts = getSortedPostsData();

  const filteredPosts = posts.filter((post) => {
    const postCategorySlug = post.category.toLowerCase().replace(/\s+/g, "-");
    return postCategorySlug === slug;
  });

  if (filteredPosts.length === 0) {
    notFound();
  }

  const displayCategory = filteredPosts[0].category;

  return (
    <div className="space-y-8">
      <div>
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-neutral-500 hover:text-neutral-900 transition-colors"
        >
          <ArrowLeft size={14} /> 전체 리서치로 돌아가기
        </Link>
      </div>

      <header className="pb-4 border-b border-neutral-200">
        <span className="text-xs font-bold text-blue-600 uppercase tracking-wider">
          Research Category
        </span>
        <h1 className="text-2xl md:text-3xl font-extrabold text-neutral-950 tracking-tight mt-1">
          {displayCategory}
        </h1>
        <p className="text-sm text-neutral-600 mt-1">
          총 {filteredPosts.length}편의 리포트
        </p>
      </header>

      <div className="divide-y divide-neutral-200">
        {filteredPosts.map((post) => (
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
