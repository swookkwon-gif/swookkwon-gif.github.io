# GEO Research (Generative Engine Optimization Research)

ChatGPT, Claude, Gemini, Perplexity 등 생성형 AI 검색 엔진의 인용 메커니즘을 규명하고, 엔터프라이즈 가시성을 극대화하기 위한 GEO(Generative Engine Optimization) 아키텍처 방법론을 탐구하는 테크니컬 리서치 플랫폼입니다.

- **사이트 URL**: [https://swookkwon-gif.github.io](https://swookkwon-gif.github.io)
- **작성자**: 권욱 (Wook Kwon) — [LinkedIn](https://www.linkedin.com/in/wook-kwon/)

---

## 🛠️ 기술 스택 및 아키텍처

- **Framework**: Next.js 15 (App Router, Static HTML Export)
- **Styling**: Tailwind CSS
- **SEO & GEO Features**:
  - `TechArticle` Schema.org JSON-LD 구조화 데이터
  - AI 크롤러 최적화 (`GPTBot`, `PerplexityBot`, `ClaudeBot` 허용 robots.txt)
  - 404 스마트 Fallback 및 정규(Canonical) Sitemap 파이프라인
  - Recharts 기반 연구 데이터 시각화 & Mermaid 아키텍처 렌더링
- **Deployment**: GitHub Actions → GitHub Pages

---

## 🚀 로컬 개발 및 빌드

```bash
# 의존성 설치
npm install

# 개발 서버 실행
npm run dev

# 프로덕션 정적 빌드 검증
npm run build
```

---

## 📝 리서치 포스트 작성 규칙

모든 신규 연구 리포트는 `content/posts/` 디렉터리에 마크다운(`.md`) 파일로 작성합니다.

```markdown
---
title: "리포트 제목"
date: 2026-10-07T10:00:00+09:00
excerpt: "Executive Summary (TL;DR) 2~3문장"
category: "GEO Fundamentals"
tags: ["GEO", "LLM", "SearchGPT"]
---

본문 내용 작성...

## 📚 참고자료
1. 출처 및 참고 문헌 명시
```
