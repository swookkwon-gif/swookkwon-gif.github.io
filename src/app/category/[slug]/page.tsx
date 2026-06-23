import { Metadata } from "next";
import Link from "next/link";
import { getSortedPostsData } from "@/lib/posts";
import { notFound } from "next/navigation";

interface CategoryPageProps {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  const posts = getSortedPostsData();
  const categories = Array.from(new Set(posts.map(post => post.category || 'Insight')));
  return categories.map(category => ({
    slug: category.toLowerCase().replace(/\s+/g, '-')
  }));
}

export async function generateMetadata({ params }: CategoryPageProps): Promise<Metadata> {
  const { slug } = await params;
  const posts = getSortedPostsData();
  const filteredPosts = posts.filter(post => {
    const postCategorySlug = (post.category || 'Insight').toLowerCase().replace(/\s+/g, '-');
    return postCategorySlug === slug;
  });

  if (filteredPosts.length === 0) {
    return { title: 'Category Not Found' };
  }

  const displayCategory = filteredPosts[0].category;
  const title = `${displayCategory} | Category`;

  const alternates: { canonical: string } = {
    canonical: `https://swookkwon-gif.github.io/category/${slug}/`,
  };

  return {
    title,
    description: `Articles in the ${displayCategory} category`,
    alternates,
    openGraph: {
      title,
      description: `Articles in the ${displayCategory} category`,
      url: `https://swookkwon-gif.github.io/category/${slug}/`,
    }
  };
}

export default async function CategoryPage({ params }: CategoryPageProps) {
  const { slug } = await params;
  const posts = getSortedPostsData();

  const filteredPosts = posts.filter(post => {
    const postCategorySlug = (post.category || 'Insight').toLowerCase().replace(/\s+/g, '-');
    return postCategorySlug === slug;
  });

  if (filteredPosts.length === 0) {
    notFound();
  }

  const displayCategory = filteredPosts[0].category;

  return (
    <div className="font-sans">
      <div className="flex flex-col">
        {filteredPosts.map((post) => (
          <article key={post.slug} className="mm-post-item group">
            <h2 className="text-lg md:text-xl font-bold mb-2">
              <Link href={`/posts/${post.slug}`} className="text-neutral-900 group-hover:text-blue-600 transition-colors">
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
