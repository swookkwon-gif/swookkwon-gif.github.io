import { Metadata } from 'next';

export const metadata: Metadata = {
  title: "Wook's AI and Marketing",
  verification: {
    google: "VEKICMa0sx4OpQaX_Aj0-5pNDI9NrEjyK9D7-W_R0Ug",
  },
};

export default function RootPage() {
  return (
    <html lang="ko">
      <head>
        <meta httpEquiv="refresh" content="0; url=/ko" />
      </head>
      <body>
        <p>Redirecting to <a href="/ko">/ko</a>...</p>
      </body>
    </html>
  );
}
