import { MetadataRoute } from 'next';
import { getSortedPostsData } from '@/lib/posts';

export const dynamic = 'force-static';

const BASE_URL = 'https://swookkwon-gif.github.io';

export default function sitemap(): MetadataRoute.Sitemap {
  // 한국어 글 목록 가져오기
  const posts = getSortedPostsData('ko');

  const postUrls = posts.map((post) => ({
    url: `${BASE_URL}/ko/posts/${post.slug}`,
    lastModified: new Date(post.date).toISOString().split('T')[0],
  }));

  // 카테고리 목록 추출
  const categories = Array.from(new Set(posts.map(p => p.category)));
  const categoryUrls = categories.map((category) => ({
    url: `${BASE_URL}/ko/category/${encodeURIComponent(category)}`,
    lastModified: new Date().toISOString().split('T')[0],
  }));

  return [
    {
      url: `${BASE_URL}/ko`,
      lastModified: new Date().toISOString().split('T')[0],
      priority: 1,
    },
    ...categoryUrls.map(url => ({ ...url, priority: 0.8 })),
    ...postUrls.map(url => ({ ...url, priority: 0.6 })),
  ];
}
