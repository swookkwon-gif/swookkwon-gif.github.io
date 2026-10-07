import { MetadataRoute } from 'next';
import { getSortedPostsData } from '@/lib/posts';

export const dynamic = 'force-static';

const BASE_URL = 'https://swookkwon-gif.github.io';

export default function sitemap(): MetadataRoute.Sitemap {
  const posts = getSortedPostsData();

  const postUrls = posts.map((post) => ({
    url: `${BASE_URL}/posts/${post.slug}/`,
    lastModified: post.date,
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }));

  const uniqueCategories = Array.from(new Set(posts.map((p) => p.category)));
  const categoryUrls = uniqueCategories.map((cat) => ({
    url: `${BASE_URL}/category/${cat.toLowerCase().replace(/\s+/g, '-')}/`,
    lastModified: new Date().toISOString().split('T')[0],
    changeFrequency: 'weekly' as const,
    priority: 0.6,
  }));

  return [
    {
      url: `${BASE_URL}/`,
      lastModified: new Date().toISOString().split('T')[0],
      changeFrequency: 'daily' as const,
      priority: 1.0,
    },
    ...categoryUrls,
    ...postUrls,
  ];
}
