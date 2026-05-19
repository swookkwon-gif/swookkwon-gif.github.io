import { MetadataRoute } from 'next';
import { getSortedPostsData } from '@/lib/posts';

export const dynamic = 'force-static';

const BASE_URL = 'https://swookkwon-gif.github.io';

export default function sitemap(): MetadataRoute.Sitemap {
  const postsKo = getSortedPostsData('ko'); // 182개
  const postsEn = getSortedPostsData('en'); // 6개 (fallback 제거 후)

  // 한국어 포스트: /posts/[slug]
  const koPostUrls = postsKo.map((post) => ({
    url: `${BASE_URL}/posts/${post.slug}`,
    lastModified: new Date(post.date).toISOString().split('T')[0],
    priority: 0.6,
  }));

  // 영어 포스트: /en/posts/[slug] — 실제 .en.md 존재하는 6개만
  const enPostUrls = postsEn.map((post) => ({
    url: `${BASE_URL}/en/posts/${post.slug}`,
    lastModified: new Date(post.date).toISOString().split('T')[0],
    priority: 0.5,
  }));

  // 한국어 카테고리: /category/[slug]
  const koCategoryUrls = Array.from(new Set(postsKo.map(p => p.category))).map((category) => ({
    url: `${BASE_URL}/category/${encodeURIComponent(category)}`,
    lastModified: new Date().toISOString().split('T')[0],
    priority: 0.8,
  }));

  // 영어 카테고리: /en/category/[slug] — 실제 영어 포스트가 있는 카테고리만
  const enCategoryUrls = Array.from(new Set(postsEn.map(p => p.category))).map((category) => ({
    url: `${BASE_URL}/en/category/${encodeURIComponent(category)}`,
    lastModified: new Date().toISOString().split('T')[0],
    priority: 0.7,
  }));

  return [
    {
      url: `${BASE_URL}/`,
      lastModified: new Date().toISOString().split('T')[0],
      priority: 1,
    },
    {
      url: `${BASE_URL}/en`,
      lastModified: new Date().toISOString().split('T')[0],
      priority: 0.8,
    },
    ...koCategoryUrls,
    ...enCategoryUrls,
    ...koPostUrls,
    ...enPostUrls,
  ];
}
