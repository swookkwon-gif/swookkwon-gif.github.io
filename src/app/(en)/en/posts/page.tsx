import { Metadata } from "next";
import Link from "next/link";
import { getSortedPostsData } from "@/lib/posts";

export const metadata: Metadata = {
  title: "All Posts",
  description: "Browse all English posts",
  alternates: {
    canonical: '/en/posts/',
    languages: {
      'ko': '/posts/',
      'en': '/en/posts/',
      'x-default': '/posts/',
    }
  },
  openGraph: {
    title: "All Posts",
    description: "Browse all English posts",
    url: '/en/posts/',
  }
};

export default async function EnPostsArchivePage() {
  const posts = getSortedPostsData('en');

  return (
    <div className="font-sans">
      <div className="flex flex-col">
        {posts.map((post) => (
          <article key={post.slug} className="mm-post-item group">
            <h2 className="text-xl md:text-2xl font-bold mb-2">
              <Link href={`/en/posts/${post.slug}`} className="text-neutral-900 group-hover:text-blue-600 transition-colors">
                {post.title}
              </Link>
            </h2>
            <div className="text-sm text-neutral-500 mb-3 space-x-3">
              <time dateTime={post.date}>{post.date}</time>
              <span>•</span>
              <span className="font-medium text-neutral-600">{post.category || "Insight"}</span>
            </div>
            <p className="text-neutral-600 leading-relaxed text-sm md:text-base mb-3 max-w-3xl">
              {post.excerpt}
            </p>
          </article>
        ))}
      </div>
    </div>
  );
}
