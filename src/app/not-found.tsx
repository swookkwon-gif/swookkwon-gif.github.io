'use client';

import { useEffect, useState } from 'react';

export default function NotFound() {
  const [isRedirecting, setIsRedirecting] = useState(false);

  useEffect(() => {
    const path = window.location.pathname;
    
    // '/wooksai'로 시작하는 이전 경로가 입력된 경우, 새 도메인 규칙에 맞게 제거 후 리다이렉션
    if (path.startsWith('/wooksai')) {
      setIsRedirecting(true);
      const newPath = path.replace(/^\/wooksai/, '');
      // 새 경로가 없으면 루트로, 있으면 해당 경로로 이동 (url 쿼리스트링 및 해시 보존)
      window.location.replace(`${newPath || '/'}${window.location.search}${window.location.hash}`);
    }
  }, []);

  if (isRedirecting) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', fontFamily: 'sans-serif' }}>
        <p>이전 주소로 접속하셨습니다. 올바른 주소로 이동 중입니다...</p>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '100vh', fontFamily: 'sans-serif' }}>
      <h1>404 - Page Not Found</h1>
      <p>요청하신 페이지를 찾을 수 없거나 이동되었습니다.</p>
      <a href="/ko" style={{ marginTop: '20px', color: '#0070f3', textDecoration: 'none' }}>메인 홈으로 돌아가기</a>
    </div>
  );
}
