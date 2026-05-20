import { MetadataRoute } from 'next';

export const dynamic = 'force-static';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        disallow: '/',
      },
      {
        userAgent: ['Googlebot', 'Yeti', 'Daumoa'],
        allow: '/',
        disallow: '/private/',
      },
    ],
    sitemap: 'https://swookkwon-gif.github.io/sitemap.xml',
  };
}
