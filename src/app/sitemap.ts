import { MetadataRoute } from 'next';
import { getSortedPostsData } from '@/lib/posts';

export const dynamic = 'force-static';

const BASE_URL = 'https://swookkwon-gif.github.io';

// Helper to format date safely to YYYY-MM-DD without timezone shifts
function safeFormatDate(dateStr?: string): string {
  if (!dateStr) return new Date().toISOString().split('T')[0];
  // If dateStr is already in YYYY-MM-DD format, use it directly to prevent timezone shift
  const match = dateStr.match(/^\d{4}-\d{2}-\d{2}/);
  if (match) return match[0];
  
  try {
    const d = new Date(dateStr);
    if (isNaN(d.getTime())) {
      return new Date().toISOString().split('T')[0];
    }
    return d.toISOString().split('T')[0];
  } catch {
    return new Date().toISOString().split('T')[0];
  }
}

export default function sitemap(): MetadataRoute.Sitemap {
  const posts = getSortedPostsData();

  // Posts: /posts/[slug]/
  const postUrls = posts.map((post) => ({
    url: `${BASE_URL}/posts/${post.slug}/`,
    lastModified: safeFormatDate(post.date),
    changeFrequency: 'weekly' as const,
    priority: 0.6,
  }));

  // Categories: /category/[slug]/
  const categoryUrls = Array.from(new Set(posts.map(p => p.category))).map((category) => ({
    url: `${BASE_URL}/category/${(category || "Insight").toLowerCase().replace(/\s+/g, '-')}/`,
    lastModified: safeFormatDate(),
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }));

  return [
    {
      url: `${BASE_URL}/`,
      lastModified: safeFormatDate(),
      changeFrequency: 'daily' as const,
      priority: 1.0,
    },
    {
      url: `${BASE_URL}/posts/`,
      lastModified: safeFormatDate(),
      changeFrequency: 'daily' as const,
      priority: 0.8,
    },
    ...categoryUrls,
    ...postUrls,
  ];
}
