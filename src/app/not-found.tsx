"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowLeft, RefreshCw } from "lucide-react";

export default function NotFound() {
  const [redirecting, setRedirecting] = useState(false);
  const [targetPath, setTargetPath] = useState("");

  useEffect(() => {
    if (typeof window !== "undefined") {
      const pathname = window.location.pathname;
      setTargetPath(pathname);

      // 과거 /en/ 경로 또는 삭제된 레거시 경로로 진입한 경우 메인으로 자동 복구 리다이렉트
      if (pathname.startsWith("/en") || pathname.includes("/(en)")) {
        setRedirecting(true);
        const timer = setTimeout(() => {
          window.location.replace("/");
        }, 800);
        return () => clearTimeout(timer);
      }
    }
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4">
      <span className="text-sm font-semibold tracking-widest text-blue-600 uppercase mb-2">
        {redirecting ? "Redirecting Legacy Route" : "404 Not Found"}
      </span>
      <h1 className="text-3xl md:text-4xl font-extrabold text-neutral-900 mb-4 tracking-tight">
        {redirecting ? "새로운 주소로 연결하고 있습니다" : "요청하신 페이지를 찾을 수 없습니다"}
      </h1>
      <p className="text-neutral-600 max-w-md mb-8 leading-relaxed text-sm md:text-base">
        {redirecting ? (
          <>
            이전 다국어 주소(<code>{targetPath}</code>)에서 단일 한국어 연구 블로그로 개편되었습니다. 메인 페이지로 자동 이동합니다.
          </>
        ) : (
          "페이지가 이동되었거나 삭제되었습니다. 아래 버튼을 통해 GEO Research 홈으로 이동해 주세요."
        )}
      </p>

      {redirecting ? (
        <div className="flex items-center gap-2 text-sm text-neutral-500">
          <RefreshCw className="animate-spin text-blue-600" size={18} />
          <span>메인으로 이동 중...</span>
        </div>
      ) : (
        <Link
          href="/"
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-neutral-900 text-white text-sm font-medium hover:bg-neutral-800 transition-colors shadow-sm"
        >
          <ArrowLeft size={16} />
          홈으로 돌아가기
        </Link>
      )}
    </div>
  );
}
