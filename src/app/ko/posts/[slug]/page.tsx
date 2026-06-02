import { Metadata } from 'next';
import { getSortedPostsData } from '@/lib/posts';

export const dynamic = 'force-static';

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  return {
    title: 'Redirecting...',
    alternates: {
      canonical: `https://swookkwon-gif.github.io/posts/${slug}/`,
    },
  };
}

export async function generateStaticParams() {
  const posts = getSortedPostsData('ko');
  return posts.map((post) => ({ slug: post.slug }));
}

export default async function KoPostRedirectPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const targetUrl = `https://swookkwon-gif.github.io/posts/${slug}/`;

  return (
    <>
      <noscript>
        <meta http-equiv="refresh" content={`0;url=${targetUrl}`} />
      </noscript>
      <script
        dangerouslySetInnerHTML={{
          __html: `window.location.replace("${targetUrl}");`,
        }}
      />
      <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
        <p>Redirecting to <a href={targetUrl}>{targetUrl}</a>...</p>
      </div>
    </>
  );
}
