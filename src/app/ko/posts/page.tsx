import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Redirecting...',
  alternates: {
    canonical: 'https://swookkwon-gif.github.io/posts/',
  },
};

export default function KoPostsRedirectPage() {
  const targetUrl = 'https://swookkwon-gif.github.io/posts/';
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
