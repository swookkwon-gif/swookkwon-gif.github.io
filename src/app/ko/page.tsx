import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Redirecting...',
  robots: {
    index: false,
    follow: false,
  },
  alternates: {
    canonical: 'https://swookkwon-gif.github.io/',
  },
};

export default function KoRedirectPage() {
  return (
    <>
      <noscript>
        <meta http-equiv="refresh" content="0;url=https://swookkwon-gif.github.io/" />
      </noscript>
      <script
        dangerouslySetInnerHTML={{
          __html: `window.location.replace("https://swookkwon-gif.github.io/");`,
        }}
      />
      <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
        <p>Redirecting to <a href="https://swookkwon-gif.github.io/">Wook's AI and Marketing</a>...</p>
      </div>
    </>
  );
}
