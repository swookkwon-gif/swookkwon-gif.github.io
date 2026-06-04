import Link from "next/link";
import { getSortedPostsData } from "@/lib/posts";
import { Metadata } from "next";

export const metadata: Metadata = {
  alternates: {
    canonical: 'https://swookkwon-gif.github.io/en/',
    languages: {
      'ko': 'https://swookkwon-gif.github.io/',
      'en': 'https://swookkwon-gif.github.io/en/',
      'x-default': 'https://swookkwon-gif.github.io/',
    }
  },
};

export default async function EnHome() {
  const posts = getSortedPostsData('en').slice(0, 5);

  return (
    <div className="font-sans">
      <div className="flex flex-col">
        {posts.map((post) => (
          <article key={post.slug} className="mm-post-item group">
            <h2 className="text-lg md:text-xl font-bold mb-2">
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

      {posts.length === 5 && (
        <div className="mt-10 pt-4">
          <Link href="/en/posts" className="px-6 py-3 bg-neutral-900 text-white rounded font-medium hover:bg-neutral-800 transition-colors inline-block text-sm shadow-sm ring-1 ring-neutral-900">
            View All Posts
          </Link>
        </div>
      )}
    </div>
  );
}
