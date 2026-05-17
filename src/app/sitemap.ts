import { MetadataRoute } from 'next';
import { getSortedPostsData } from '@/lib/posts';

export const dynamic = 'force-static';

const BASE_URL = 'https://swookkwon-gif.github.io';

export default function sitemap(): MetadataRoute.Sitemap {
  const postsKo = getSortedPostsData('ko');
  const postsEn = getSortedPostsData('en');

  const createPostUrls = (posts: any[], lang: string) => 
    posts.map((post) => ({
      url: `${BASE_URL}/${lang}/posts/${post.slug}`,
      lastModified: new Date(post.date).toISOString().split('T')[0],
    }));

  const createCategoryUrls = (posts: any[], lang: string) => {
    const categories = Array.from(new Set(posts.map(p => p.category)));
    return categories.map((category) => ({
      url: `${BASE_URL}/${lang}/category/${encodeURIComponent(category)}`,
      lastModified: new Date().toISOString().split('T')[0],
    }));
  };

  const postUrls = [
    ...createPostUrls(postsKo, 'ko'),
    ...createPostUrls(postsEn, 'en')
  ];

  const categoryUrls = [
    ...createCategoryUrls(postsKo, 'ko'),
    ...createCategoryUrls(postsEn, 'en')
  ];

  return [
    {
      url: `${BASE_URL}/ko`,
      lastModified: new Date().toISOString().split('T')[0],
      priority: 1,
    },
    {
      url: `${BASE_URL}/en`,
      lastModified: new Date().toISOString().split('T')[0],
      priority: 1,
    },
    ...categoryUrls.map(url => ({ ...url, priority: 0.8 })),
    ...postUrls.map(url => ({ ...url, priority: 0.6 })),
  ];
}
