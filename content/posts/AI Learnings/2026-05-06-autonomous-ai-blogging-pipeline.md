---
title: "2주 만에 포스트 100개 — AI 자동 블로그 구축기 - v0.1"
date: 2026-05-06T14:00:00+09:00
excerpt: "GitHub Actions, Next.js, Gemini 2.5 Search Grounding을 결합하여 2주 만에 100개 이상의 전문 분석 포스트를 생산한 1인 AI 미디어 파이프라인의 설계, 구현, 그리고 성과를 공유한다."
category: AI Learnings
tags: ["AI Agent", "GitHub Actions", "Next.js", "Gemini API", "Automation", "1인 미디어"]
---

2주 전, "AI 뉴스 자동 포스팅"을 만들었다.
오늘, 블로그 포스트가 **100개를 넘었다.**

매일 쏟아지는 해외 아티클을 팔로업하기 벅차서 시작한 자동화 프로젝트가, 2주 만에 100개 이상의 전문 분석 포스트를 생산하는 **"1인 AI 미디어"**로 진화했다. 비싼 서버 없이, 혼자서, 운영 비용 $0으로.

이 글에서는 별도의 서버 비용 없이 **GitHub Actions**, **Next.js**, 그리고 **Gemini 2.5 Flash (Search Grounding)**를 활용하여 100% 자동으로 굴러가는 **무인 AI 블로그 파이프라인**을 구축한 과정과, 그 결과로 탄생한 4대 콘텐츠 시리즈의 성과를 공유한다.

---

## 🏗️ 전체 아키텍처 개요 — Zero-Cost Pipeline

비싼 클라우드 서버나 복잡한 인프라 대신, 개발자들에게 친숙한 도구들을 조합하여 '비용 0원'의 완전 자동화 환경을 구성했다.

<img src="/images/posts/pipeline_architecture.png" alt="파이프라인 아키텍처 — GitHub Actions Cron → Python Agent → Gemini 2.5 Flash + Search Grounding → .md 자동 커밋 → GitHub Pages 배포" width="100%" />

파이프라인의 핵심 흐름은 다음과 같다:

| 단계 | 컴포넌트 | 역할 | 비용 |
|:---:|:---|:---|:---:|
| 1 | **GitHub Actions (Cron)** | 매일 새벽 5시 Python 에이전트를 깨우는 무료 스케줄러 | $0 |
| 2 | **Python Agent** | 뉴스 소스 크롤링, 프롬프트 조립, 결과 파싱 | $0 |
| 3 | **Gemini 2.5 Flash** | Google Search Grounding으로 실시간 팩트 체크 + 분석 | 무료 티어 |
| 4 | **Git Auto-Commit** | frontmatter 포함 `.md` 파일 자동 커밋 & 푸시 | $0 |
| 5 | **GitHub Pages (Next.js)** | 새 파일 감지 → 정적 빌드 → 자동 배포 | $0 |

> [!TIP]
> **핵심 포인트**: 서버를 띄워둘 필요 없이 GitHub Actions의 `cron` 스케줄러를 통해 정해진 시간에만 워커가 깨어나 작업을 수행하고 종료된다. 24시간 상시 가동되는 서버 없이도 매일 새벽 자동으로 콘텐츠가 생산된다.

---

## 🛠️ 핵심 기술 스택 및 구현 방법

### 1. Gemini 2.5 Flash + Google Search Grounding

가장 큰 고민은 AI의 고질적인 병인 **'할루시네이션(환각)'**이었다. 없는 뉴스를 지어내거나 날짜를 헷갈리면 블로그의 신뢰도가 바닥을 친다.

이를 해결하기 위해 **Gemini API의 Google Search Grounding** 기능을 도입했다.

<img src="/images/posts/search_grounding.png" alt="Search Grounding 개념도 — 기존 LLM의 환각 문제를 실시간 검색 연동으로 해결하고 출처를 자동 첨부하는 구조" width="100%" />

```python
# 실제 파이프라인에 사용된 코드 스니펫
payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "tools": [{"googleSearch": {}}], # 구글 실시간 검색 강제 활성화
    "generationConfig": {
        "temperature": 0.4
    }
}
```

이 옵션을 켜면 Gemini는 자체 뇌피셜로 글을 쓰지 않고, 실시간 구글 검색(Hacker News, TechCrunch 등)을 수행한 뒤 그 **팩트에 기반해서만** 답변을 생성한다. 마크다운 주석(`[^1]`) 형태로 원문 링크(Citation)까지 완벽하게 달아준다.

### 2. 정교한 프롬프트 엔지니어링 (CMS 표준화)

AI가 글을 쓸 때마다 양식이 바뀌면 Next.js 블로그에서 렌더링 에러가 발생한다. 이를 막기 위해 매우 엄격한 프롬프트 가이드라인을 설정했다.

*   **Frontmatter 강제**: `title`, `date`, `category`, `excerpt` 등 블로그 시스템이 요구하는 YAML 메타데이터를 첫 줄에 정확히 출력하도록 지시.
*   **어조(Tone & Manner)**: '해요체'를 금지하고, 테크 저널과 같은 전문적인 문어체(~이다, ~한다)를 사용하도록 강제.
*   **구조화된 출력**: 단순히 글만 쓰는 것이 아니라, 'Top 3 심층 분석'과 'Top 10 뉴스 중요도 평가 테이블(표)'을 마크다운 문법으로 완벽히 렌더링하도록 세팅.

### 3. GitHub Actions를 통한 완전 자동화 연동

파이썬 스크립트가 완성된 후, 이를 매일 자동으로 실행해 줄 일꾼이 필요했다. `.github/workflows/gemini_daily_research.yml` 파일을 생성하여 다음과 같이 세팅했다.

```yaml
on:
  schedule:
    - cron: '0 20 * * *' # 한국 시간 매일 오전 5시 실행

jobs:
  research-and-post:
    # ... (환경 세팅 생략) ...
    steps:
      - name: Run Auto Blogger
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: python scripts/gf2_auto_blogger.py

      - name: Commit and Push
        run: |
          git add content/posts/AI\ News/*.md
          git commit -m "auto: Gemini deep research post generated"
          git push
```

파이프라인이 `.md` 파일을 레포지토리에 푸시하면, 이를 감지한 또 다른 Actions 워크플로우(`nextjs.yml`)가 즉시 Next.js 정적 빌드를 수행하고 GitHub Pages에 새 글을 라이브로 배포한다.

---

## 📊 2주간의 성과 — 4대 핵심 시리즈

이 파이프라인이 2주 만에 생산해낸 100개 이상의 포스트는 단순한 스크래핑 결과물이 아니다. 각각의 포스트에는 AI가 수행한 심층 리서치와, 사람이 검수한 인사이트가 담겨 있다.

<img src="/images/posts/content_portfolio.png" alt="2주간 100+ 포스트 성과 — AI 뉴스 자동 분석, 마케팅 심층 분석, 데이터 리터러시, AI 도구 리뷰 4개 시리즈" width="100%" />

### 🤖 시리즈 1: AI 뉴스 자동 분석 (매일 자동 발행)

파이프라인의 핵심 자동화 산출물이다. 매일 새벽 글로벌 뉴스레터들을 자동으로 수집하고 분석한다.

*   **TLDR, The Rundown AI, AI Breakfast** 등 7개 글로벌 뉴스레터 자동 요약 · 분석
*   **매일 Top 3 AI 뉴스** 심층 리포트 자동 생성 — 단순 요약이 아닌, 산업적 맥락과 시사점까지 분석

### 📈 시리즈 2: 마케팅 심층 분석

자동화 파이프라인 위에 수동으로 심층 분석을 더해 발행하는 시리즈다.

*   **구글 Performance Max의 숨겨진 함정** — Optmyzr/Adalysis 데이터 기반, AI 자동화가 오히려 성과를 악화시키는 메커니즘 분석
*   디지털 광고 시장 구조 분석 (**구글 제국의 해부**)
*   **브랜드 키워드 전략 4부작** — Tadelis(2015) 논문 기반 실전 가이드

### 🧠 시리즈 3: 데이터 리터러시

잘못된 상식과 통계적 오류를 근거 기반으로 해체하는 시리즈다.

*   **마시멜로 테스트의 재현 실패**가 주는 교훈
*   **"하루 8잔 물" 신화**의 탄생과 붕괴 — 1945 FNB 보고서 추적
*   **"아침식사가 가장 중요하다" 신화** 해체 — 켈로그 → 버네이즈 → RCT
*   **생존자 편향, 심슨의 역설, p-해킹** 등 통계 사례 20편

### 🔬 시리즈 4: AI 도구 심층 리뷰

실제 사용 경험 기반의 AI 도구 분석이다.

*   **NotebookLM 완벽 가이드 5부작** — 입문부터 자동화까지
*   AI 리서치 프레임워크 분석 (**카파시 Auto Research** 등)
*   **EliseAI** — 미국 최고속 성장 AI 스타트업 해부

---

## 🎯 이 프로젝트에서 배운 것

이 파이프라인을 구축하고 2주간 운영하면서 얻은 세 가지 핵심 인사이트가 있다.

### 1. AI는 '대신 써주는 도구'가 아니다

AI는 **내가 소화할 수 없는 정보를 먼저 정리해주는 리서치 파트너**다. 매일 새벽 7개 뉴스레터를 읽고 분석하는 것은 사람이 하기에 비효율적이다. AI가 1차 정리를 하고, 사람은 인사이트를 더하는 구조가 가장 효과적이다.

### 2. 자동화의 핵심은 "무엇을 자동화하지 않을 것인가"

뉴스 수집과 요약은 자동화했지만, **인사이트 도출과 최종 편집은 사람이 한다.** "하루 8잔 물 신화" 같은 심층 분석은 AI가 제시한 팩트를 바탕으로, 사람이 서사를 구성하고 의미를 부여한 결과물이다.

### 3. 비용 $0 ≠ 품질 저하

올바른 프롬프트 설계 + 검증 파이프라인이면 충분하다. Search Grounding으로 팩트를 보장하고, 엄격한 프롬프트 가이드라인으로 포맷을 통일하면, 서버 비용 없이도 전문 미디어 수준의 콘텐츠를 생산할 수 있다.

> [!IMPORTANT]
> 이 시스템의 진정한 가치는 **'시간의 해방'**이다. 뉴스 검색과 요약에 시간을 쏟는 대신, AI가 정리해 준 팩트를 바탕으로 더 깊은 차원의 분석과 인사이트 도출에 집중할 수 있게 되었다.

---

## 🚀 앞으로의 계획

이 시스템을 더욱 고도화하여, 특정 논문(Paper)이나 기술 키워드에 대해서만 더 깊게 파고드는 **개인 맞춤형 리서치 에이전트**로 발전시켜 갈 계획이다. 100개의 포스트는 시작일 뿐, 이 파이프라인이 만들어낼 지식의 깊이는 계속해서 진화할 것이다.

## 📚 참고자료

*   [Google Gemini API — Search Grounding 공식 문서](https://ai.google.dev/gemini-api/docs/grounding)
*   [GitHub Actions — Scheduled Workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)
*   [Next.js Static Export 공식 가이드](https://nextjs.org/docs/app/building-your-application/deploying/static-exports)
*   Wook's AI and Marketing 블로그: [https://swookkwon-gif.github.io/wooksai/](https://swookkwon-gif.github.io/wooksai/)
