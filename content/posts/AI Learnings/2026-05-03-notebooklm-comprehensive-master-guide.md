---
title: "구글 NotebookLM 100% 실전 활용 가이드 (통합본)"
date: 2026-05-03
category: "AI Learnings"
author: "Wook"
tags: ["Deep Research", "MCP", "책 출간", "Google AI", "Studio", "질의응답", "CLI", "AI 리서치", "아티팩트", "콘텐츠 전략", "생산성", "NotebookLM", "전자책", "인포그래픽", "튜토리얼", "자동화", "팟캐스트", "블로그 시리즈", "리서치", "블로그"]
---


## NotebookLM 100% 활용하기 (1편) — 소개부터 기본 세팅까지

Google이 만든 **NotebookLM**은 단순한 메모장이 아닙니다. PDF, 웹페이지, YouTube 영상, Google Drive 문서를 던져넣으면, AI가 모든 내용을 읽고 이해한 뒤 — 질문에 답하고, 팟캐스트를 만들고, 인포그래픽을 그려주는 **AI 기반 연구 플랫폼**입니다.

이 시리즈에서는 NotebookLM을 블로그 포스트 작성, 심층 리서치, 데이터 시각화, 그리고 책 출간까지 활용하는 방법을 5편에 걸쳐 다룹니다.

## 시리즈 목차

| 편 | 주제 | 핵심 |
|----|------|------|
| **1편 (이 글)** | 소개 & 기본 세팅 | 노트북 생성, 소스 추가, UI 이해 |
| 2편 | 리서치 & 질의응답 | Deep Research, AI Q&A, 노트 작성 |
| 3편 | Studio 아티팩트 완전정복 | Audio, Video, Infographic 등 9가지 |
| 4편 | 블로그 자동화 연동 | MCP CLI, 파이프라인, 품질 검증 |
| 5편 | 책 출간 워크플로우 | 시리즈→책 컴파일, PDF 변환 |

---

## NotebookLM이란?

NotebookLM은 Google이 2023년에 공개하고, 2024-2026년 동안 급격히 발전시킨 **AI 기반 연구 도구**입니다. 기존 ChatGPT나 Gemini와의 가장 큰 차이점은:

> **"내가 제공한 소스만을 기반으로 답변한다"**

일반 AI 챗봇은 학습 데이터 전체를 기반으로 답하기 때문에, 때때로 관련 없는 정보를 섞거나 '환각(Hallucination)'을 일으킵니다. 반면 NotebookLM은 **내가 업로드한 자료**만을 참고하여, 출처가 명확한 분석 결과를 제공합니다.

### 왜 NotebookLM을 사용해야 하나?

| 기존 방식 | NotebookLM 방식 |
|-----------|----------------|
| PDF를 열어 직접 읽기 | AI가 100페이지 PDF를 읽고 핵심 요약 |
| 여러 기사를 탭으로 열어놓고 비교 | 소스 50개를 동시에 분석하여 교차 비교 |
| 노트 앱에 수동으로 메모 | AI가 자동으로 구조화된 노트 생성 |
| 블로그 초안을 처음부터 작성 | 소스 기반으로 블로그 포스트 초안 생성 |
| 발표 자료를 직접 만들기 | 슬라이드 덱, 인포그래픽 자동 생성 |

### 주요 기능 한눈에

NotebookLM은 크게 **4가지 핵심 기능**을 제공합니다:

1. **소스 관리** — PDF, URL, YouTube, Drive, 텍스트 등 다양한 형식의 자료를 노트북에 추가
2. **AI 채팅** — 추가된 소스를 기반으로 질문하고 답변 받기 (출처 인용 포함)
3. **Deep Research** — 웹이나 Google Drive에서 새로운 소스를 자동으로 검색하여 추가
4. **Studio** — 소스를 기반으로 9가지 유형의 콘텐츠(팟캐스트, 슬라이드, 인포그래픽 등) 자동 생성

---

## Step 1: NotebookLM 시작하기

### 접속 방법

1. 브라우저에서 [notebooklm.google.com](https://notebooklm.google.com)에 접속합니다.
2. Google 계정으로 로그인합니다.
3. 아래와 같은 대시보드 화면이 표시됩니다.

![NotebookLM 대시보드 — 추천 노트북과 최근 노트북 목록이 표시됩니다](/images/notebooklm-guide/nlm-dashboard.png)

대시보드에는 **추천 노트북**(Google이 제공하는 샘플)과 **내 노트북** 목록이 표시됩니다. 오른쪽 상단의 `+ 새로 만들기` 버튼으로 새 노트북을 생성할 수 있습니다.

> **💡 팁**: NotebookLM Ultra(유료)를 사용하면 더 큰 소스 용량과 추가 기능을 이용할 수 있습니다. 무료 버전으로도 대부분의 기능을 충분히 활용 가능합니다.

### 새 노트북 만들기

**`+ 새로 만들기`** 버튼을 클릭하면 곧바로 새 노트북이 생성되면서 소스 추가 화면이 나타납니다.

---

## Step 2: 소스 추가하기

NotebookLM의 핵심은 **소스(Sources)**입니다. AI가 분석할 자료를 추가하는 단계로, 노트북의 품질을 결정하는 가장 중요한 과정입니다.

### 소스 추가 화면

![소스 추가 다이얼로그 — 파일 업로드, 웹사이트, Drive, 복사된 텍스트 옵션](/images/notebooklm-guide/nlm-add-source.png)

소스 추가 방법은 크게 **5가지**입니다:

| 방법 | 아이콘 | 적합한 용도 | 최대 용량 |
|------|--------|------------|----------|
| **파일 업로드** | 📤 | PDF, 텍스트 파일, 오디오 파일 | 파일당 500KB-200MB |
| **웹사이트** | 🔗 | 뉴스 기사, 블로그 포스트, 문서 | URL 입력 |
| **YouTube** | ▶️ | 강연, 인터뷰, 튜토리얼 영상 | URL 입력 (자막 기반) |
| **Google Drive** | 📁 | Docs, Sheets, Slides, PDF | Drive 연동 |
| **복사된 텍스트** | 📋 | 메모, 코드, 이메일 내용 | 직접 붙여넣기 |

### 소스 추가 실습: 웹사이트 URL

가장 자주 사용하는 **웹사이트 URL 추가**를 실습해봅시다:

1. 소스 추가 화면에서 **`웹사이트`** 버튼을 클릭합니다.
2. URL 입력란에 분석하고 싶은 웹페이지 주소를 붙여넣습니다.
3. **Enter** 키를 누르면 NotebookLM이 해당 페이지의 내용을 자동으로 가져와 인덱싱합니다.

```
예시 URL:
https://www.aitimes.com/news/articleView.html?idxno=210020
```

4. 잠시 후 좌측 **출처** 패널에 추가된 소스가 표시됩니다.

### 소스 추가 실습: Deep Research (웹 검색)

소스 추가 화면 상단에는 **웹 검색** 기능도 있습니다:

1. 검색창에 조사하고 싶은 주제를 입력합니다 (예: "AI 에이전트 최신 동향 2026").
2. **웹 🌐** 또는 **Drive** 중 검색 범위를 선택합니다.
3. **Fast Research** (빠른 리서치, 약 30초) 또는 **Deep Research** (심층 리서치, 약 5분)를 선택합니다.
4. 검색이 완료되면 발견된 소스 목록이 표시되고, 원하는 것만 선택하여 노트북에 추가할 수 있습니다.

> **💡 팁**: Fast Research는 약 10개, Deep Research는 약 40개의 관련 소스를 자동으로 찾아줍니다. 처음에는 Fast Research로 시작하고, 더 깊은 조사가 필요하면 Deep Research를 활용하세요.

---

## Step 3: 노트북 인터페이스 이해하기

소스를 추가한 후의 노트북 화면은 **3단 구조**로 나뉩니다:

![NotebookLM 노트북 뷰 — 왼쪽: 출처, 가운데: 채팅, 오른쪽: 스튜디오](/images/notebooklm-guide/nlm-notebook-view.png)

### 좌측: 출처 (Sources) 패널

- 추가된 모든 소스가 리스트로 표시됩니다.
- 각 소스 옆의 **체크박스**로 AI가 참고할 소스를 선택/해제할 수 있습니다.
- `모두 선택` / 개별 선택으로, 특정 소스만 기반으로 질문하는 것이 가능합니다.
- 소스를 클릭하면 **원문 내용과 AI 요약**을 볼 수 있습니다.

### 가운데: 채팅 (Chat) 패널

- AI에게 질문을 입력하는 메인 인터페이스입니다.
- 하단의 입력란에 질문을 타이핑하면, AI가 **선택된 소스들만을 기반으로** 답변합니다.
- 모든 답변에는 **출처 인용 번호**가 달려, 어느 소스에서 가져온 정보인지 확인 가능합니다.
- 상단에는 **노트북 요약**과 **추천 질문**이 자동으로 표시됩니다.

### 우측: 스튜디오 (Studio) 패널

![Studio 패널 — 9가지 아티팩트 생성 옵션](/images/notebooklm-guide/nlm-studio-panel.png)

스튜디오는 소스를 기반으로 **9가지 유형의 콘텐츠**를 자동 생성하는 기능입니다:

| 아티팩트 | 설명 | 활용 예시 |
|---------|------|----------|
| 🎙️ **AI 오디오 오버뷰** | 팟캐스트 스타일 오디오 | 통근 중 듣기, 콘텐츠 리뷰 |
| 🎬 **동영상 개요** | 설명 동영상 | SNS 공유, 교육 자료 |
| 📊 **슬라이드 자료** | 프레젠테이션 PDF | 발표, 회의, 브리핑 |
| 🗺️ **마인드맵** | 주제 연결 시각화 | 구조 파악, 아이디어 정리 |
| 📝 **보고서** | 브리핑 문서 / 학습 가이드 / 블로그 | 보고, 학습, 블로깅 |
| 🃏 **플래시카드** | 학습용 카드 | 시험 대비, 암기 |
| ❓ **퀴즈** | 객관식 문제 | 이해도 확인 |
| 📈 **인포그래픽** | 시각적 정보 요약 | 블로그, SNS 공유 |
| 📋 **데이터 표** | 구조화된 표 | 비교 분석, 데이터 정리 |

> 각 아티팩트의 상세한 사용법은 **3편 "Studio 아티팩트 완전정복"**에서 다룹니다.

---

## Step 4: 첫 번째 질문하기

소스를 추가했으니, 이제 AI에게 첫 질문을 해봅시다.

### 효과적인 질문 작성법

NotebookLM에서 좋은 답변을 얻으려면 **구체적으로 질문**하는 것이 중요합니다:

| ❌ 나쁜 질문 | ✅ 좋은 질문 |
|------------|------------|
| "이것에 대해 알려줘" | "이 논문의 핵심 주장 3가지를 요약해줘" |
| "AI에 대해 설명해" | "소스에서 언급된 AI 에이전트의 보안 위험을 구체적 사례와 함께 정리해줘" |
| "요약해줘" | "이 자료들의 공통 주제와 상반되는 견해를 비교 분석해줘" |

### 유용한 프롬프트 패턴

```markdown
1. 요약: "이 소스들의 핵심 논점을 3가지로 정리하고, 각각에 대한 근거를 인용해줘"
2. 비교: "소스 A와 소스 B에서 AI 규제에 대한 입장 차이를 표로 정리해줘"
3. 비판: "이 논문의 방법론적 한계와 반론을 제시해줘"
4. 적용: "이 리서치 결과를 마케팅 전략에 적용한다면 어떤 액션 아이템이 가능한지 제안해줘"
5. 블로그: "이 소스들을 기반으로 1500단어 분량의 한국어 블로그 포스트 초안을 작성해줘"
```

---

## 실전 활용 시나리오

### 시나리오 1: 경쟁사 분석 보고서

1. 경쟁사 관련 뉴스 기사 10개를 URL로 추가
2. 경쟁사 IR 자료(PDF)를 파일로 업로드
3. "이 소스들을 기반으로 경쟁사의 전략 방향, 투자 영역, 리스크 요인을 분석해줘"라고 질문
4. Studio에서 **보고서**(브리핑 문서)와 **슬라이드 자료**를 생성

### 시나리오 2: 논문 리뷰

1. 분석할 논문 PDF를 업로드
2. 관련 후속 연구 3-5편을 URL로 추가
3. "이 논문의 핵심 가설, 실험 설계, 결론을 요약하고, 후속 연구에서 어떻게 확장되었는지 정리해줘"
4. Studio에서 **마인드맵**으로 논문 간 관계 시각화

### 시나리오 3: 블로그 포스트 작성

1. 주제 관련 소스를 Deep Research로 자동 수집
2. AI 채팅으로 구조와 핵심 논점 정리
3. Studio에서 **보고서** (Blog Post 형식)로 초안 생성
4. 초안을 다듬어 블로그에 발행

---

## 핵심 정리

| 항목 | 요약 |
|------|------|
| **NotebookLM이란** | 내 소스 기반 AI 연구 도구 (환각 최소화) |
| **소스 추가** | URL, PDF, YouTube, Drive, 텍스트 5가지 방식 |
| **UI 구조** | 출처 / 채팅 / 스튜디오 3단 구조 |
| **핵심 차별점** | 출처 인용 + 9가지 아티팩트 자동 생성 |

**다음 편(2편)**에서는 **Deep Research**로 웹에서 자동으로 소스를 수집하고, AI 채팅으로 심층 분석하며, 노트를 체계적으로 관리하는 방법을 다룹니다.

## 📚 참고자료

- [Google NotebookLM 공식 사이트](https://notebooklm.google.com)
- [Google NotebookLM 도움말](https://support.google.com/notebooklm)
- [NotebookLM 소개 블로그 (Google)](https://blog.google/technology/ai/notebooklm-google/)
- [NotebookLM MCP CLI](https://github.com/nicholasgriffintn/notebooklm-mcp)

## NotebookLM 100% 활용하기 (2편) — Deep Research와 AI 질의응답

[1편](/posts/2026-05-03-notebooklm-guide-part1-intro)에서는 NotebookLM의 기본 개념과 노트북 생성, 소스 추가 방법을 알아봤습니다. 이번 2편에서는 NotebookLM의 가장 강력한 기능들을 깊이 다룹니다.

- **Deep Research**: AI가 자동으로 웹을 검색하여 관련 소스를 수집
- **AI 채팅**: 소스 기반 질의응답과 출처 인용
- **노트 관리**: AI 응답을 저장하고 체계적으로 정리

---

## Deep Research: AI가 자료를 모아준다

### Deep Research란?

기존에는 자료를 직접 찾아서 URL이나 PDF로 하나씩 추가해야 했습니다. **Deep Research**는 이 과정을 AI가 대신 수행합니다. 키워드나 질문을 입력하면 AI가 웹을 검색하여 관련 소스를 자동으로 찾아 노트북에 추가해줍니다.

### Step 1: Deep Research 시작

![Deep Research 인터페이스 — 검색어 입력과 연구 모드 선택](/images/notebooklm-guide/nlm-deep-research.png)

1. 노트북 화면의 **소스 추가** 영역에서 상단 검색창에 조사 주제를 입력합니다.
2. 검색 범위를 선택합니다:
   - **🌐 웹**: 인터넷 전체 검색
   - **Drive**: 내 Google Drive 문서 검색
3. 리서치 모드를 선택합니다:

| 모드 | 소요 시간 | 결과 수 | 적합한 용도 |
|------|----------|---------|------------|
| **Fast Research** | 약 30초 | 약 10개 | 빠른 개요 파악, 트렌드 확인 |
| **Deep Research** | 약 5분 | 약 40개 | 심층 분석, 학술 리서치, 종합 보고서 |

4. **→ 화살표 버튼**을 클릭하면 리서치가 시작됩니다.

### Step 2: 리서치 결과 확인

리서치가 완료되면 좌측 패널에 결과가 표시됩니다:

- **발견된 소스 수**: "소스 46개 발견됨" 등으로 표시
- **주요 소스**: 가장 관련성 높은 소스 목록
- **리서치 보고서**: AI가 자동 생성한 조사 요약

### Step 3: 소스 가져오기

**`+ 가져오기`** 버튼을 클릭하면 발견된 소스들이 노트북에 추가됩니다. 특정 소스만 선택하여 가져올 수도 있습니다.

> **💡 실전 팁**: Deep Research는 **영어 키워드**로 검색하면 더 풍부한 결과를 얻습니다. 한국어로 검색하면 한국어 소스 위주로 찾아지니, 목적에 따라 언어를 선택하세요.

### Deep Research 활용 사례

| 주제 | 검색어 예시 | 모드 | 결과 |
|------|-----------|------|------|
| AI 에이전트 동향 | "AI agent frameworks 2026 comparison" | Deep | 최신 논문, 기술 블로그, 벤치마크 40+개 |
| 마케팅 전략 | "digital marketing ROI measurement" | Fast | 핵심 사례 연구 10개 |
| 사이버보안 | "금융 사이버 공격 사례 2020-2026" | Deep | 사고 보고서, 분석 기사 40+개 |

---

## AI 채팅: 소스 기반 질의응답

### 출처가 명확한 AI 답변

NotebookLM의 채팅은 일반 AI 챗봇과 근본적으로 다릅니다. **내가 추가한 소스만**을 기반으로 답변하며, 모든 답변에 **출처 번호**가 달립니다.

![AI 채팅 응답 — 소스 54개 기반의 상세 답변과 출처 인용 번호](/images/notebooklm-guide/nlm-chat-response.png)

위 스크린샷에서 볼 수 있듯이:

1. **질문**: "What are the key security threats discussed in these sources?"
2. **답변**: 소스들을 종합 분석하여 구조화된 답변 제공
3. **출처 표시**: 답변 내 `[1]`, `[...]` 등의 번호를 클릭하면 원문 소스의 해당 부분으로 이동
4. **소스 기반**: 하단에 "소스 53개" 표시 — 53개 소스를 모두 분석한 결과

### 효과적인 채팅 활용법

#### 1단계: 전체 요약 요청

```
"이 소스들의 핵심 주제를 5개로 정리하고, 각 주제별 핵심 인사이트를 요약해줘"
```

노트북에 소스를 추가한 직후에는 먼저 **전체 그림**을 파악하는 것이 좋습니다. AI가 자동으로 노트북 요약을 보여주지만, 더 구체적인 방향으로 요약을 요청하면 연구의 초점을 빠르게 잡을 수 있습니다.

#### 2단계: 구체적 분석 질문

```
"소스에서 언급된 AI 기반 사이버 공격의 구체적 사례를 시간순으로 정리하고,
각 사례별 피해 규모와 공격 방법을 표로 만들어줘"
```

전체 그림을 파악한 후에는 특정 주제에 대해 **깊이 파고드는 질문**을 합니다. 표 형식을 요청하면 구조화된 결과를 얻을 수 있습니다.

#### 3단계: 비교/분석 질문

```
"소스 A의 관점과 소스 B의 관점을 비교하고, 어느 쪽이 더 설득력 있는지 근거를 들어 평가해줘"
```

개별 소스를 선택하여 비교 분석을 요청할 수 있습니다. 좌측 패널에서 비교할 소스만 체크하면 됩니다.

#### 4단계: 블로그 초안 생성

```
"지금까지 분석한 내용을 바탕으로, '2026년 AI 사이버보안 위협 심층 분석'이라는 제목의 
블로그 포스트 초안을 1500단어 분량으로 작성해줘. 
구조: 도입 → 주요 위협 3가지 분석 → 방어 전략 → 시사점"
```

리서치의 최종 결과물로 블로그 포스트 초안을 직접 요청할 수 있습니다.

### 소스 선택으로 범위 좁히기

채팅할 때 **특정 소스만 선택**하면 더 정확한 답변을 얻을 수 있습니다:

| 사용 방법 | 효과 |
|----------|------|
| `모두 선택` ✅ | 전체 소스 기반 종합 분석 |
| 특정 소스 3-5개만 ✅ | 해당 소스에 집중한 깊이 있는 분석 |
| 같은 주제 소스끼리 ✅ | 주제별 비교 분석 |

---

## 노트 관리: 연구 결과를 체계적으로

### 노트란?

NotebookLM의 **노트(Note)**는 AI 채팅 결과를 저장하거나, 직접 메모를 작성하여 보관하는 기능입니다. 소스가 '입력'이라면, 노트는 '출력'에 해당합니다.

![노트 관리 화면 — 생성된 아티팩트와 메모가 스튜디오 패널에 정리됨](/images/notebooklm-guide/nlm-notes.png)

### 노트 생성 방법

#### 방법 1: 채팅 응답 저장

1. AI 채팅에서 유용한 답변을 받았을 때
2. 답변 옆의 **📋 클립보드/저장 아이콘**을 클릭
3. 자동으로 노트에 저장됩니다

#### 방법 2: 직접 메모 작성

1. 우측 하단의 **`메모 추가`** 버튼 클릭
2. 제목과 내용을 직접 입력
3. 마크다운 형식 지원 — 제목, 목록, 표 등 활용 가능

#### 방법 3: Studio 아티팩트에서 생성

Studio에서 생성한 보고서, 마인드맵, 데이터 표 등은 자동으로 스튜디오 패널에 저장되며, 이를 노트로도 변환할 수 있습니다.

### 노트 활용 전략

| 단계 | 노트 유형 | 활용 |
|------|----------|------|
| 1. 탐색 | **키워드 메모** | 주요 개념, 인물, 수치 기록 |
| 2. 분석 | **비교 표** | 소스 간 관점 차이 정리 |
| 3. 통합 | **아웃라인** | 블로그/보고서 구조 설계 |
| 4. 완성 | **초안** | 최종 콘텐츠 작성 |

> **💡 팁**: 노트에 저장된 내용은 이후 채팅에서도 참조됩니다. "이전에 저장한 비교 표를 기반으로 결론을 작성해줘"처럼 활용할 수 있습니다.

---

## 채팅 설정 커스터마이징

NotebookLM은 채팅의 동작 방식을 커스터마이징할 수 있습니다:

### 맞춤 설정 옵션

우측 상단의 **`맞춤설정`** 버튼을 클릭하면:

| 설정 | 옵션 | 설명 |
|------|------|------|
| **응답 목표** | 기본 / 학습 가이드 / 커스텀 | 답변의 방향성 설정 |
| **응답 길이** | 기본 / 더 길게 / 더 짧게 | 답변 분량 조절 |
| **커스텀 프롬프트** | 자유 입력 (최대 10,000자) | 특정 역할이나 형식 지정 |

### 커스텀 프롬프트 예시

```
당신은 블로그 전문 편집자입니다. 모든 답변을 한국어로 하고,
다음 형식을 따르세요:
1. 핵심 요약 (3줄)
2. 상세 분석 (구조화된 목록)
3. 블로그 활용 포인트
4. 추천 제목 3개
```

이렇게 설정하면 이후 모든 채팅 응답이 블로그 작성에 최적화된 형태로 나옵니다.

---

## 실전 워크플로우: 리서치부터 블로그까지

아래는 실제로 이 블로그 시리즈를 작성할 때 사용한 워크플로우입니다:

```
1️⃣ 노트북 생성
   └→ "NotebookLM Complete Guide" 제목으로 생성

2️⃣ Deep Research (Fast, 웹)
   └→ "NotebookLM features 2026 tutorial guide" 검색
   └→ 10개 소스 자동 수집

3️⃣ 추가 소스 수동 추가
   └→ Google 공식 블로그 URL
   └→ NotebookLM 도움말 URL
   └→ YouTube 튜토리얼 영상 URL

4️⃣ AI 채팅으로 구조 설계
   └→ "이 소스들을 기반으로 5편 시리즈 목차를 제안해줘"
   └→ 결과를 노트에 저장

5️⃣ 각 편별 초안 생성
   └→ "1편: NotebookLM 소개 & 기본 세팅에 대한 1500단어 블로그 초안 작성"
   └→ 초안을 노트에 저장 후 수정

6️⃣ Studio로 시각 자료 생성
   └→ 인포그래픽, 마인드맵, 슬라이드 자동 생성
```

---

## 핵심 정리

| 기능 | 핵심 포인트 |
|------|-----------|
| **Deep Research** | Fast(30초/10개) vs Deep(5분/40개), 영어 키워드 권장 |
| **AI 채팅** | 소스 기반 답변 + 출처 인용, 소스 선택으로 범위 조절 |
| **노트** | 채팅 저장 + 직접 메모 + 아티팩트, 이후 채팅에서 참조 가능 |
| **맞춤 설정** | 커스텀 프롬프트로 블로그 전용 어시스턴트 생성 |

**다음 편(3편)**에서는 NotebookLM의 **Studio 기능**을 완전 정복합니다. 팟캐스트부터 인포그래픽, 슬라이드, 퀴즈까지 9가지 아티팩트를 생성하는 방법을 다룹니다.

## 📚 참고자료

- [Google NotebookLM 공식 사이트](https://notebooklm.google.com)
- [NotebookLM 도움말: 소스 추가](https://support.google.com/notebooklm/answer/13579304)
- [Google AI Blog: NotebookLM updates](https://blog.google/technology/ai/notebooklm-google/)
- [NotebookLM MCP CLI GitHub](https://github.com/nicholasgriffintn/notebooklm-mcp)

## NotebookLM 100% 활용하기 (3편) — Studio 아티팩트 9종 완전정복

[1편](/posts/2026-05-03-notebooklm-guide-part1-intro)에서 기본 세팅을, [2편](/posts/2026-05-03-notebooklm-guide-part2-research)에서 리서치와 채팅을 다뤘습니다. 이번 3편에서는 NotebookLM의 가장 인상적인 기능 — **Studio 아티팩트**를 완전히 정복합니다.

---

## Studio란?

**Studio**는 NotebookLM에 추가한 소스를 기반으로 **9가지 유형의 콘텐츠를 자동 생성**하는 기능입니다. 보고서를 작성하고, 팟캐스트를 녹음하고, 인포그래픽을 디자인하는 작업을 AI가 몇 분 안에 처리합니다.

### Studio 패널 열기

노트북 화면 우측에 **스튜디오** 패널이 있으며, 9개의 아티팩트 생성 버튼이 그리드 형태로 배치되어 있습니다:

![Studio 패널 — 9가지 아티팩트 유형과 생성된 결과물 목록](/images/notebooklm-guide/nlm-studio-9types.png)

---

## 아티팩트 1: 🎙️ AI 오디오 오버뷰

소스 내용을 기반으로 **팟캐스트 스타일의 오디오 콘텐츠**를 생성합니다. 두 명의 AI 진행자가 대화 형식으로 소스 내용을 설명합니다.

### 생성 방법

1. 스튜디오 패널에서 **`AI 오디오 ...`** 클릭
2. 옵션 설정:

| 옵션 | 값 | 설명 |
|------|-----|------|
| **포맷** | Deep Dive / Brief / Critique / Debate | 대화 스타일 |
| **길이** | Short / Default / Long | 오디오 길이 |
| **언어** | ko, en, ja, de 등 | 진행 언어 |
| **포커스 프롬프트** | 자유 입력 | 특정 주제에 집중 |

3. **생성** 버튼 클릭 → 수 분 후 오디오 파일 생성

### 포맷별 특징

| 포맷 | 스타일 | 적합한 용도 |
|------|--------|------------|
| **Deep Dive** | 심층 대담 (2인 대화) | 복잡한 주제 이해, 통근 중 학습 |
| **Brief** | 간략 요약 | 빠른 핵심 파악 |
| **Critique** | 비평적 리뷰 | 논문/보고서 비판적 분석 |
| **Debate** | 찬반 토론 | 양측 관점 이해 |

> **💡 팁**: `Deep Dive` + `Long` + 한국어(ko)로 설정하면 20-30분 분량의 한국어 팟캐스트가 생성됩니다. 블로그에 Audio Overview를 임베드하면 콘텐츠 접근성이 크게 향상됩니다.

---

## 아티팩트 2: 🎬 동영상 개요

소스 내용을 **동영상 형태**로 시각화합니다. AI가 내레이션과 애니메이션을 자동으로 구성합니다.

### 생성 옵션

| 옵션 | 값 | 설명 |
|------|-----|------|
| **포맷** | Explainer / Brief / Cinematic | 영상 스타일 |
| **비주얼 스타일** | Auto / Classic / Whiteboard / Kawaii / Anime / Watercolor / Retro Print / Heritage / Paper Craft | 시각적 테마 |
| **언어** | BCP-47 코드 | 내레이션 언어 |

### 비주얼 스타일 비교

| 스타일 | 분위기 | 적합한 용도 |
|--------|--------|------------|
| Classic | 깔끔한 기본 디자인 | 비즈니스, 공식 프레젠테이션 |
| Whiteboard | 화이트보드 드로잉 | 교육, 설명 영상 |
| Kawaii | 귀여운 캐릭터 | SNS 공유, 가벼운 주제 |
| Anime | 애니메이션 스타일 | 기술 콘텐츠, 젊은 타겟 |
| Watercolor | 수채화 | 예술, 문화 주제 |
| Paper Craft | 종이 공예 | 크래프트 느낌 |

---

## 아티팩트 3: 📊 인포그래픽

소스의 핵심 데이터와 인사이트를 **시각적 인포그래픽**으로 자동 생성합니다. 블로그나 SNS에서 즉시 활용 가능한 품질의 이미지가 만들어집니다.

### 실제 생성 결과

![NotebookLM이 자동 생성한 인포그래픽 — 보안 위협 진화 비교](/images/notebooklm-guide/nlm-infographic-preview.png)

위 인포그래픽은 **54개 소스**를 기반으로 AI가 자동 생성한 결과입니다. "2014년 개인정보 유출 사건"과 "2025년 AI 기반 지능형 공격"을 시각적으로 비교하고 있으며, 구체적인 수치(1억 4백만 건, 87% 증가 등)까지 포함되어 있습니다.

### 생성 옵션

| 옵션 | 값 | 설명 |
|------|-----|------|
| **방향** | Landscape / Portrait / Square | 이미지 비율 |
| **디테일 수준** | Concise / Standard / Detailed | 정보 밀도 |
| **언어** | BCP-47 코드 | 텍스트 언어 |
| **포커스 프롬프트** | 자유 입력 | 특정 데이터에 집중 |

### 블로그 활용 팁

```markdown
1. Portrait (세로) → 모바일 최적화, Instagram/Pinterest
2. Landscape (가로) → 블로그 본문 삽입, LinkedIn
3. Square (정사각) → Twitter/X, 범용
```

> **💡 팁**: 같은 소스로 **포커스 프롬프트를 달리하여** 여러 인포그래픽을 생성하면, 하나의 리서치에서 다양한 시각 자료를 확보할 수 있습니다.

---

## 아티팩트 4: 📑 슬라이드 자료

소스 내용을 **프레젠테이션 슬라이드**로 자동 생성합니다. PDF 형식으로 다운로드 가능하며, PPTX로도 변환할 수 있습니다.

### 생성 옵션

| 옵션 | 값 | 설명 |
|------|-----|------|
| **포맷** | Detailed Deck / Presenter Slides | 슬라이드 밀도 |
| **길이** | Short / Default | 슬라이드 수 |

### 포맷 비교

| 포맷 | 특징 | 적합한 용도 |
|------|------|------------|
| **Detailed Deck** | 텍스트 풍부, 자체 완결형 | 메일 배포, 사전 리딩 |
| **Presenter Slides** | 키워드 중심, 발표자 보조 | 현장 프레젠테이션 |

### 슬라이드 수정 (Revise 기능)

생성된 슬라이드의 개별 슬라이드를 수정할 수 있습니다:

```
예시: 슬라이드 3번의 제목을 "AI 위협 현황"으로 변경하고, 
      통계 수치를 더 크게 강조해줘
```

> 이 기능은 API/MCP를 통해서도 활용 가능합니다 (4편에서 상세히 다룸).

---

## 아티팩트 5: 📝 보고서

가장 실용적인 아티팩트입니다. 소스를 기반으로 **체계적인 문서**를 자동 생성합니다.

### 보고서 유형

| 유형 | 설명 | 적합한 용도 |
|------|------|------------|
| **Briefing Doc** | 핵심 요약 브리핑 문서 | 임원 보고, 의사결정 지원 |
| **Study Guide** | 학습 가이드 | 시험 준비, 교육 자료 |
| **Blog Post** | 블로그 포스트 초안 | 콘텐츠 마케팅, 기술 블로그 |
| **Create Your Own** | 커스텀 형식 | 논문 초록, FAQ, 비교 분석 등 |

### Create Your Own 활용

`Create Your Own`을 선택하면 **커스텀 프롬프트**로 원하는 형식의 문서를 생성할 수 있습니다:

```
커스텀 프롬프트 예시:

"이 소스들을 기반으로 '2026년 AI 사이버보안 백서'를 작성하세요.
구조: 
1. 요약 (300자)
2. 현황 분석 (위협 유형별 분류)
3. 사례 연구 (3건)
4. 대응 전략
5. 시사점 및 권고사항
6. 참고문헌"
```

---

## 아티팩트 6: 🃏 플래시카드

소스 내용에서 핵심 개념을 추출하여 **학습용 플래시카드**를 생성합니다.

### 생성 옵션

| 옵션 | 값 | 설명 |
|------|-----|------|
| **난이도** | Easy / Medium / Hard | 질문 깊이 |
| **포커스 프롬프트** | 자유 입력 | 특정 주제 집중 |

### 다운로드 형식

- **JSON**: 프로그래밍 연동, Anki 변환
- **Markdown**: 블로그/문서에 삽입
- **HTML**: 브라우저에서 바로 학습

---

## 아티팩트 7: ❓ 퀴즈

소스 기반으로 **객관식 문제**를 자동 생성합니다. 이해도 확인이나 교육 자료로 유용합니다.

### 생성 옵션

| 옵션 | 값 | 설명 |
|------|-----|------|
| **문항 수** | 2-20+ | 퀴즈 분량 |
| **난이도** | Easy / Medium / Hard | 질문 깊이 |
| **포커스 프롬프트** | 자유 입력 | 특정 영역 집중 |

---

## 아티팩트 8: 📋 데이터 표

소스에서 특정 데이터를 추출하여 **구조화된 표(CSV)**로 변환합니다.

### 생성 방법

```
설명(description) 필수 입력 예시:

"각 소스에서 언급된 사이버 공격 사건을 추출하여 
다음 컬럼으로 정리해줘:
- 연도
- 공격 유형
- 피해 기관
- 피해 규모
- 사용된 기술"
```

### 활용 팁

- **Google Sheets로 내보내기** 가능 — 추가 분석이나 차트 생성에 활용
- 블로그 포스트에 표로 삽입 가능
- 데이터 비교 분석의 기초 자료로 사용

---

## 아티팩트 9: 🗺️ 마인드맵

소스의 핵심 주제와 관계를 **시각적 마인드맵**으로 구조화합니다. JSON 형식으로 다운로드되며, 다양한 마인드맵 도구와 호환됩니다.

### 활용 시나리오

| 시나리오 | 효과 |
|---------|------|
| 논문 리뷰 | 핵심 개념 간 관계 한눈에 파악 |
| 프로젝트 계획 | 구성 요소와 의존성 시각화 |
| 블로그 시리즈 | 편별 주제 관계와 흐름 정리 |

---

## 생성된 아티팩트 관리

### 아티팩트 확인

생성된 아티팩트는 스튜디오 패널 하단에 리스트로 표시됩니다:

![생성된 아티팩트 — 오디오 오버뷰와 슬라이드 결과](/images/notebooklm-guide/nlm-artifact-detail.png)

각 아티팩트에서 할 수 있는 작업:

| 작업 | 아이콘 | 설명 |
|------|--------|------|
| **재생/미리보기** | ▶️ | 오디오/동영상 재생, 인포그래픽 확인 |
| **공유** | 🔗 | 링크 공유 또는 소셜 미디어 공유 |
| **다운로드** | ⬇️ | 파일로 다운로드 (MP4, PDF, PNG, CSV 등) |
| **수정** | ✏️ | 이름 변경, 슬라이드 수정 |
| **삭제** | 🗑️ | 아티팩트 삭제 (되돌릴 수 없음) |

### Google Docs/Sheets로 내보내기

보고서는 **Google Docs**로, 데이터 표는 **Google Sheets**로 직접 내보낼 수 있습니다:

1. 아티팩트의 **`...`** 메뉴 클릭
2. **`Google Docs로 내보내기`** 또는 **`Google Sheets로 내보내기`** 선택
3. Google Drive에 자동 저장

---

## 아티팩트 활용 매트릭스

어떤 상황에서 어떤 아티팩트를 사용해야 할까요?

| 목적 | 추천 아티팩트 | 이유 |
|------|-------------|------|
| 블로그 작성 | 보고서 (Blog Post) + 인포그래픽 | 본문 + 시각 자료 동시 확보 |
| 발표 준비 | 슬라이드 + 오디오 | 발표자료 + 리허설 자료 |
| 학습/복습 | 플래시카드 + 퀴즈 | 핵심 암기 + 이해도 확인 |
| 데이터 분석 | 데이터 표 + 마인드맵 | 구조화된 데이터 + 관계 시각화 |
| SNS 공유 | 인포그래픽 + 동영상 | 시각적 임팩트 |
| 팀 브리핑 | 보고서 (Briefing Doc) + 슬라이드 | 요약 + 프레젠테이션 |

---

## 핵심 정리

| 아티팩트 | 핵심 옵션 | 출력 형식 |
|---------|----------|----------|
| AI 오디오 | Deep Dive/Brief/Critique/Debate | MP4/MP3 |
| 동영상 | Explainer/Brief + 9가지 비주얼 스타일 | MP4 |
| 인포그래픽 | 방향 3종 + 디테일 3단계 | PNG |
| 슬라이드 | Detailed/Presenter + 수정 가능 | PDF/PPTX |
| 보고서 | Briefing/Study Guide/Blog/Custom | Markdown |
| 플래시카드 | 난이도 3단계 | JSON/MD/HTML |
| 퀴즈 | 문항 수 + 난이도 | JSON/MD/HTML |
| 데이터 표 | 설명 필수 입력 | CSV |
| 마인드맵 | 제목 커스터마이즈 | JSON |

**다음 편(4편)**에서는 NotebookLM을 **프로그래밍으로 자동화**하는 방법을 다룹니다. MCP CLI를 통해 블로그 포스트 자동 생성 파이프라인을 구축하는 과정을 step by step으로 안내합니다.

## 📚 참고자료

- [Google NotebookLM Studio 공식 가이드](https://support.google.com/notebooklm)
- [NotebookLM Audio Overview 소개](https://blog.google/technology/ai/notebooklm-audio-overviews/)
- [NotebookLM MCP CLI — Studio 기능](https://github.com/nicholasgriffintn/notebooklm-mcp)
- [NotebookLM 인포그래픽 생성 사례](https://notebooklm.google.com)

## NotebookLM 100% 활용하기 (4편) — 블로그 자동화 파이프라인

[1편](/posts/2026-05-03-notebooklm-guide-part1-intro)~[3편](/posts/2026-05-03-notebooklm-guide-part3-studio)까지 NotebookLM의 UI 기반 사용법을 다뤘습니다. 이번 4편에서는 **프로그래밍으로 NotebookLM을 자동화**하는 방법을 다룹니다.

> 이 글은 개발자 또는 자동화에 관심 있는 파워유저를 대상으로 합니다.

---

## MCP CLI란?

**MCP (Model Context Protocol)**는 AI 시스템이 외부 도구와 데이터 소스에 연결되는 표준 프로토콜입니다. **NotebookLM MCP CLI**는 이 프로토콜을 통해 NotebookLM의 모든 기능을 **프로그래밍으로 제어**할 수 있게 해줍니다.

### 기존 방식 vs MCP CLI

| 기존 (웹 UI) | MCP CLI |
|-------------|---------|
| 브라우저에서 수동 클릭 | 터미널에서 명령어 실행 |
| 한 번에 하나씩 처리 | 배치 처리 가능 |
| 반복 작업 비효율적 | 스크립트로 자동화 |
| 결과를 수동으로 복사 | 파일로 직접 다운로드 |

---

## Step 1: MCP CLI 설치

### 설치 명령어

```bash
# uv (권장 — 빠르고 안정적)
uv tool install notebooklm-mcp-cli

# 또는 pip
pip install notebooklm-mcp-cli
```

### 인증 설정

```bash
# 자동 로그인 (브라우저 팝업)
nlm login

# 계정 전환
nlm login switch <profile>
```

`nlm login` 명령어를 실행하면 브라우저가 열리고 Google 계정 인증이 진행됩니다. 인증이 완료되면 토큰이 로컬에 저장되어, 이후 CLI 명령어를 바로 사용할 수 있습니다.

---

## Step 2: 기본 CLI 명령어

### 노트북 목록 확인

```bash
# 모든 노트북 조회
nlm notebooks list

# 결과 예시:
# ID: eac87d4a-2144-...  Title: AI and Cybersecurity  Sources: 54
# ID: 84a40771-cb67-...  Title: Autonomous AI Reasoning  Sources: 10
```

### 새 노트북 생성

```bash
nlm notebooks create --title "블로그 리서치 - AI 트렌드 2026"
```

### 소스 추가

```bash
# URL 소스 추가
nlm sources add --notebook <ID> --type url --url "https://example.com/article"

# 여러 URL 한 번에 추가
nlm sources add --notebook <ID> --type url --urls "url1,url2,url3"

# 텍스트 소스 추가
nlm sources add --notebook <ID> --type text --text "분석할 내용..." --title "메모"

# 파일 업로드
nlm sources add --notebook <ID> --type file --file-path "./report.pdf"
```

---

## Step 3: Deep Research 자동화

### 웹 리서치 실행

```bash
# Fast Research (약 30초, 약 10개 소스)
nlm research start \
  --notebook <ID> \
  --query "AI agent security vulnerabilities 2026" \
  --mode fast \
  --source web

# Deep Research (약 5분, 약 40개 소스)
nlm research start \
  --notebook <ID> \
  --query "AI agent security vulnerabilities 2026" \
  --mode deep \
  --source web
```

### 리서치 상태 확인 & 소스 가져오기

```bash
# 진행 상태 확인 (완료까지 대기)
nlm research status --notebook <ID> --max-wait 300

# 발견된 소스를 노트북에 가져오기
nlm research import --notebook <ID> --task-id <TASK_ID>
```

---

## Step 4: AI 질의응답 (프로그래밍)

### 기본 쿼리

```bash
nlm query --notebook <ID> --query "이 소스들의 핵심 주제를 5개로 요약해줘"
```

### 대화 맥락 유지

```bash
# 첫 번째 질문
nlm query --notebook <ID> --query "AI 에이전트의 보안 위험을 분석해줘"
# → conversation_id: abc123 반환

# 후속 질문 (같은 대화 맥락)
nlm query --notebook <ID> \
  --query "그 중 가장 심각한 위험은 무엇인가?" \
  --conversation-id abc123
```

### 특정 소스만 지정

```bash
nlm query --notebook <ID> \
  --query "이 두 소스의 견해를 비교해줘" \
  --source-ids "source-id-1,source-id-2"
```

---

## Step 5: Studio 아티팩트 생성

### 보고서 생성 (Blog Post)

```bash
nlm studio create --notebook <ID> \
  --type report \
  --report-format "Blog Post" \
  --language ko
```

### 인포그래픽 생성

```bash
nlm studio create --notebook <ID> \
  --type infographic \
  --orientation landscape \
  --detail-level detailed \
  --language ko \
  --focus-prompt "AI 에이전트 보안 위협 비교"
```

### 오디오 오버뷰 생성

```bash
nlm studio create --notebook <ID> \
  --type audio \
  --audio-format deep_dive \
  --audio-length long \
  --language ko
```

### 아티팩트 다운로드

```bash
# 인포그래픽 다운로드
nlm studio download --notebook <ID> \
  --type infographic \
  --output ./output/infographic.png

# 보고서 다운로드
nlm studio download --notebook <ID> \
  --type report \
  --output ./output/report.md

# 데이터 표 다운로드
nlm studio download --notebook <ID> \
  --type data_table \
  --output ./output/data.csv
```

---

## 실전: 블로그 자동 발행 파이프라인

아래는 **리서치 → 분석 → 포스트 생성 → 발행**까지 전 과정을 자동화하는 파이프라인입니다.

### 파이프라인 아키텍처

<div class="workflow-timeline">
  <div class="workflow-step">
    <div class="workflow-step-badge badge-blue">1</div>
    <div class="workflow-step-content">
      <h4>💡 주제 입력</h4>
      <ul><li>"AI 에이전트 보안 위협 분석 2026"</li></ul>
    </div>
  </div>
  <div class="workflow-step">
    <div class="workflow-step-badge badge-indigo">2</div>
    <div class="workflow-step-content">
      <h4>🔍 Deep Research</h4>
      <ul>
        <li><code>nlm research start --mode deep</code></li>
        <li>40+ 소스 자동 수집</li>
      </ul>
    </div>
  </div>
  <div class="workflow-step">
    <div class="workflow-step-badge badge-violet">3</div>
    <div class="workflow-step-content">
      <h4>🧠 AI 분석</h4>
      <ul>
        <li><code>nlm query "핵심 주제 분석..."</code></li>
        <li>구조 설계 & 요약</li>
      </ul>
    </div>
  </div>
  <div class="workflow-step">
    <div class="workflow-step-badge badge-purple">4</div>
    <div class="workflow-step-content">
      <h4>🎨 아티팩트 생성</h4>
      <ul>
        <li><code>nlm studio create --type report</code></li>
        <li><code>nlm studio create --type infographic</code></li>
      </ul>
    </div>
  </div>
  <div class="workflow-step">
    <div class="workflow-step-badge badge-fuchsia">5</div>
    <div class="workflow-step-content">
      <h4>📥 다운로드 & 변환</h4>
      <ul>
        <li><code>nlm studio download</code></li>
        <li>Markdown → 블로그 포스트</li>
      </ul>
    </div>
  </div>
  <div class="workflow-step">
    <div class="workflow-step-badge badge-teal">6</div>
    <div class="workflow-step-content">
      <h4>🚀 Git Push & 배포</h4>
      <ul>
        <li><code>git add, commit, push</code></li>
        <li>블로그 자동 배포</li>
      </ul>
    </div>
  </div>
</div>

### 자동화 스크립트 예시

```python
#!/usr/bin/env python3
"""NotebookLM → Blog Post 자동 발행 파이프라인"""

import subprocess
import json
import time
from datetime import date

def run_nlm(args):
    """NLM CLI 명령어 실행"""
    result = subprocess.run(
        ["nlm"] + args,
        capture_output=True, text=True
    )
    return json.loads(result.stdout) if result.stdout else None

def auto_blog_pipeline(topic, category="AI Learnings"):
    """블로그 자동 발행 파이프라인"""
    
    # 1. 노트북 생성
    notebook = run_nlm([
        "notebooks", "create", 
        "--title", f"Blog Research: {topic}"
    ])
    nb_id = notebook["id"]
    print(f"✅ 노트북 생성: {nb_id}")
    
    # 2. Deep Research 실행
    research = run_nlm([
        "research", "start",
        "--notebook", nb_id,
        "--query", topic,
        "--mode", "deep",
        "--source", "web"
    ])
    task_id = research["task_id"]
    
    # 3. 리서치 완료 대기
    print("⏳ Deep Research 진행 중...")
    run_nlm([
        "research", "status",
        "--notebook", nb_id,
        "--max-wait", "300"
    ])
    
    # 4. 소스 가져오기
    run_nlm([
        "research", "import",
        "--notebook", nb_id,
        "--task-id", task_id
    ])
    print("✅ 소스 가져오기 완료")
    
    # 5. 블로그 보고서 생성
    run_nlm([
        "studio", "create",
        "--notebook", nb_id,
        "--type", "report",
        "--report-format", "Blog Post",
        "--language", "ko"
    ])
    time.sleep(60)  # 생성 대기
    
    # 6. 인포그래픽 생성
    run_nlm([
        "studio", "create",
        "--notebook", nb_id,
        "--type", "infographic",
        "--orientation", "landscape",
        "--language", "ko",
        "--focus-prompt", topic
    ])
    time.sleep(120)  # 생성 대기
    
    # 7. 다운로드
    today = date.today().isoformat()
    slug = topic.lower().replace(" ", "-")[:50]
    
    run_nlm([
        "studio", "download",
        "--notebook", nb_id,
        "--type", "report",
        "--output", f"content/posts/{category}/{today}-{slug}.md"
    ])
    
    run_nlm([
        "studio", "download",
        "--notebook", nb_id,
        "--type", "infographic",
        "--output", f"public/images/{slug}-infographic.png"
    ])
    
    print(f"✅ 블로그 포스트 생성 완료: {today}-{slug}.md")

# 실행
auto_blog_pipeline("AI 에이전트 보안 위협 분석 2026")
```

---

## 배치 처리: 여러 노트북 동시 작업

### 여러 노트북에 같은 질문

```bash
nlm batch query \
  --notebook-names "AI Research,Cybersecurity" \
  --query "2026년 가장 중요한 트렌드를 3가지로 요약해줘"
```

### 교차 노트북 쿼리

```bash
nlm cross-notebook-query \
  --tags "ai,security" \
  --query "공통적으로 언급되는 위험 요소는?"
```

---

## GitHub Actions 연동

GitHub Actions에 파이프라인을 연동하면, 정기적으로 블로그를 자동 발행할 수 있습니다:

```yaml
# .github/workflows/auto-blog.yml
name: Auto Blog Pipeline
on:
  schedule:
    - cron: '0 9 * * 1'  # 매주 월요일 9시
  workflow_dispatch:      # 수동 실행

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install NLM CLI
        run: pip install notebooklm-mcp-cli
      - name: Run Pipeline
        env:
          NLM_AUTH_TOKEN: ${{ secrets.NLM_AUTH_TOKEN }}
        run: python scripts/auto_blog_nlm.py
      - name: Commit & Push
        run: |
          git config user.name "Blog Bot"
          git config user.email "bot@blog.com"
          git add content/ public/images/
          git commit -m "auto: new blog post generated"
          git push
```

---

## 핵심 정리

| 기능 | CLI 명령어 | 용도 |
|------|----------|------|
| 노트북 생성 | `nlm notebooks create` | 주제별 노트북 |
| Deep Research | `nlm research start` | 자동 소스 수집 |
| AI 쿼리 | `nlm query` | 소스 분석 |
| 아티팩트 생성 | `nlm studio create` | 보고서/인포그래픽 |
| 다운로드 | `nlm studio download` | 파일 저장 |
| 배치 처리 | `nlm batch` | 대량 처리 |

**다음 편(5편)**에서는 이 파이프라인을 확장하여 **블로그 시리즈를 책으로 컴파일하는 워크플로우**를 다룹니다.

## 📚 참고자료

- [NotebookLM MCP CLI GitHub](https://github.com/nicholasgriffintn/notebooklm-mcp)
- [Model Context Protocol 공식 문서](https://modelcontextprotocol.io/)
- [GitHub Actions 문서](https://docs.github.com/en/actions)
- [NotebookLM API 참고](https://notebooklm.google.com)

## NotebookLM 100% 활용하기 (5편) — 블로그 시리즈에서 책 출간까지

[1편](/posts/2026-05-03-notebooklm-guide-part1-intro)부터 [4편](/posts/2026-05-03-notebooklm-guide-part4-automation)까지 NotebookLM의 기본 사용법, 리서치, Studio 아티팩트, 그리고 자동화를 다뤘습니다. 이 마지막 편에서는 **블로그 시리즈를 책으로 발전시키는 워크플로우**를 완성합니다.

---

## 왜 블로그를 책으로?

블로그 포스트를 지속적으로 작성하다 보면, 자연스럽게 **특정 주제에 대한 체계적인 지식 체계**가 쌓입니다. 이를 **전자책(eBook)** 또는 **인쇄 출판**으로 발전시키면:

| 블로그만 운영 | 책으로 발전 |
|-------------|-----------|
| 개별 포스트가 흩어져 있음 | 체계적 목차와 흐름 |
| 검색 기반 유입에 의존 | 단행본으로 독립된 가치 |
| 전문성 증명이 어려움 | 출판물 = 신뢰도 강화 |
| 일회성 소비 | 장기적 수익/자산 |

---

## 전체 워크플로우 개요

<div class="workflow-timeline">
  <div class="workflow-step">
    <div class="workflow-step-badge badge-indigo">1</div>
    <div class="workflow-step-content">
      <h4>📝 Phase 1: 블로그 시리즈 작성 & 관리</h4>
      <ul>
        <li>시리즈 레지스트리로 편 관리</li>
        <li>각 편을 NotebookLM 소스로 축적</li>
      </ul>
    </div>
  </div>
  <div class="workflow-step">
    <div class="workflow-step-badge badge-violet">2</div>
    <div class="workflow-step-content">
      <h4>🏗️ Phase 2: NotebookLM으로 책 구조 설계</h4>
      <ul>
        <li>전체 시리즈를 하나의 노트북에 통합</li>
        <li>AI에게 목차 & 챕터 구조 제안 요청</li>
        <li>보고서(Study Guide) 형태로 초안 생성</li>
      </ul>
    </div>
  </div>
  <div class="workflow-step">
    <div class="workflow-step-badge badge-purple">3</div>
    <div class="workflow-step-content">
      <h4>🔬 Phase 3: 챕터별 심화 & 편집</h4>
      <ul>
        <li>각 챕터를 개별 노트북으로 분리</li>
        <li>Deep Research로 추가 자료 보강</li>
        <li>AI Q&A로 부족한 부분 보완</li>
      </ul>
    </div>
  </div>
  <div class="workflow-step">
    <div class="workflow-step-badge badge-fuchsia">4</div>
    <div class="workflow-step-content">
      <h4>📖 Phase 4: 컴파일 & 출판</h4>
      <ul>
        <li>마크다운 → PDF (pandoc/LaTeX)</li>
        <li>인포그래픽/데이터 표 삽입</li>
        <li>전자책(ePub) 또는 인쇄 출판</li>
      </ul>
    </div>
  </div>
</div>

---

## Phase 1: 시리즈 레지스트리 관리

### 시리즈 레지스트리란?

블로그 시리즈의 메타데이터를 체계적으로 관리하는 JSON 파일입니다. 각 시리즈의 편 수, 진행 상황, NotebookLM 노트북 ID를 추적합니다.

```json
{
  "notebooklm-guide": {
    "title": "NotebookLM 100% 활용하기",
    "description": "Google NotebookLM의 모든 기능을 마스터하는 5편 시리즈",
    "category": "AI Learnings",
    "total_parts": 5,
    "status": "completed",
    "notebook_id": "c83636ab-678d-44c4-9971-0facba066cd0",
    "parts": [
      {"order": 1, "title": "소개 & 기본 세팅", "slug": "part1-intro", "status": "published"},
      {"order": 2, "title": "Deep Research & AI 질의응답", "slug": "part2-research", "status": "published"},
      {"order": 3, "title": "Studio 아티팩트 완전정복", "slug": "part3-studio", "status": "published"},
      {"order": 4, "title": "블로그 자동화 파이프라인", "slug": "part4-automation", "status": "published"},
      {"order": 5, "title": "책 출간 워크플로우", "slug": "part5-book", "status": "published"}
    ],
    "book_candidate": true
  }
}
```

### 관리 규칙

| 규칙 | 설명 |
|------|------|
| `status` 관리 | draft → writing → review → published |
| `notebook_id` 연결 | 각 시리즈의 리서치 노트북 추적 |
| `book_candidate` | true인 시리즈만 책 출간 후보 |

---

## Phase 2: NotebookLM으로 책 구조 설계

### Step 1: 시리즈를 하나의 노트북에 통합

```bash
# 새 노트북 생성
nlm notebooks create --title "Book: NotebookLM 완전 가이드"

# 각 편의 블로그 포스트를 소스로 추가
nlm sources add --notebook <BOOK_NB_ID> --type text \
  --file-path "content/posts/AI Learnings/2026-05-03-notebooklm-guide-part1-intro.md" \
  --title "1편: 소개 & 기본 세팅"

# 나머지 편도 동일하게 추가
```

### Step 2: AI에게 목차 제안 요청

```bash
nlm query --notebook <BOOK_NB_ID> \
  --query "이 5편의 블로그 시리즈를 하나의 책으로 재구성한다면, 
  최적의 목차 구조를 제안해줘. 
  각 챕터의 제목, 핵심 내용, 예상 페이지 수를 포함해줘.
  블로그에 없지만 책에서 추가해야 할 내용도 제안해줘."
```

AI가 제안하는 목차 예시:

```
📖 NotebookLM 완전 가이드

Part I. 시작하기
  Chapter 1. NotebookLM이란? (10p)
  Chapter 2. 첫 번째 노트북 만들기 (15p)
  
Part II. 리서치 마스터
  Chapter 3. 소스 관리의 기술 (20p)
  Chapter 4. Deep Research 실전 가이드 (25p)
  Chapter 5. AI 채팅으로 심층 분석 (20p)
  
Part III. 콘텐츠 창작
  Chapter 6. Studio 아티팩트 활용 (30p)
  Chapter 7. 블로그 포스트 자동 발행 (20p)
  
Part IV. 고급 활용
  Chapter 8. MCP CLI 프로그래밍 (25p)
  Chapter 9. 팀 협업과 공유 (15p)
  Chapter 10. 책 출간 워크플로우 (15p)
  
부록
  A. 자주 묻는 질문 (FAQ)
  B. 프롬프트 레시피 모음
  C. 참고 자료
```

### Step 3: 보고서로 챕터 초안 생성

```bash
# Study Guide 형식으로 종합 초안 생성
nlm studio create --notebook <BOOK_NB_ID> \
  --type report \
  --report-format "Create Your Own" \
  --custom-prompt "이 소스들을 기반으로 교재 형식의 종합 문서를 작성하세요. 
  각 장의 학습 목표, 핵심 개념, 실습 과제, 요약을 포함하세요." \
  --language ko
```

---

## Phase 3: 챕터별 심화 & 편집

### 보강이 필요한 영역 파악

```bash
nlm query --notebook <BOOK_NB_ID> \
  --query "이 시리즈에서 충분히 다루지 못한 주제는 무엇인가?
  책으로 발행하려면 어떤 내용을 추가로 조사해야 하는가?"
```

### Deep Research로 보강

AI가 부족한 영역을 지적하면, 해당 주제에 대해 추가 리서치를 진행합니다:

```bash
# 부족한 주제 보강
nlm research start --notebook <BOOK_NB_ID> \
  --query "NotebookLM team collaboration features best practices" \
  --mode deep
```

### 시각 자료 생성

책에 포함할 시각 자료를 일괄 생성합니다:

```bash
# 각 챕터용 마인드맵
nlm studio create --notebook <BOOK_NB_ID> \
  --type mind_map --title "Chapter 6: Studio 아티팩트 전체 구조"

# 핵심 데이터 비교 표
nlm studio create --notebook <BOOK_NB_ID> \
  --type data_table \
  --description "각 아티팩트 유형별 옵션, 출력 형식, 적합한 용도를 정리"

# 챕터 인포그래픽
nlm studio create --notebook <BOOK_NB_ID> \
  --type infographic \
  --orientation portrait \
  --detail-level detailed \
  --focus-prompt "NotebookLM 활용 워크플로우 전체 흐름"
```

---

## Phase 4: 컴파일 & 출판

### 마크다운 → PDF 변환

[Pandoc](https://pandoc.org/)을 사용하여 마크다운을 PDF로 변환합니다:

```bash
# pandoc 설치 (macOS)
brew install pandoc

# 단일 파일로 합치기
cat chapter_*.md > book_combined.md

# PDF 생성 (한글 지원)
pandoc book_combined.md \
  -o "NotebookLM_완전_가이드.pdf" \
  --pdf-engine=xelatex \
  -V mainfont="NanumGothic" \
  -V geometry:margin=2cm \
  --toc \
  --toc-depth=3 \
  --highlight-style=tango
```

### ePub 전자책 생성

```bash
pandoc book_combined.md \
  -o "NotebookLM_완전_가이드.epub" \
  --metadata title="NotebookLM 완전 가이드" \
  --metadata author="WooksAI" \
  --epub-cover-image=cover.png \
  --toc \
  --toc-depth=3
```

### 출판 옵션

| 플랫폼 | 형식 | 비용 | 도달 범위 |
|--------|------|------|----------|
| **Amazon KDP** | ePub/PDF | 무료 (인세 70%) | 글로벌 |
| **브런치 by Kakao** | 웹 연재 | 무료 | 한국 |
| **교보문고 POD** | PDF | 출판비 | 한국 |
| **Lulu** | PDF | 무료 (인쇄비) | 글로벌 |
| **Gumroad** | PDF/ePub | 무료 (수수료 10%) | 글로벌 |

---

## 자동화 파이프라인: 시리즈 → 책

전체 프로세스를 스크립트로 자동화할 수 있습니다:

```python
#!/usr/bin/env python3
"""블로그 시리즈 → 책 컴파일 파이프라인"""

import json
import subprocess
from pathlib import Path

def compile_series_to_book(series_id, output_dir="./book_output"):
    """시리즈 레지스트리 기반으로 책 컴파일"""
    
    # 1. 시리즈 레지스트리 읽기
    registry = json.load(open("scripts/config/series_registry.json"))
    series = registry[series_id]
    
    if not series.get("book_candidate"):
        print(f"⚠️ {series_id}는 book_candidate가 아닙니다")
        return
    
    # 2. 출력 디렉토리 생성
    output = Path(output_dir)
    output.mkdir(exist_ok=True)
    
    # 3. 각 편의 마크다운 결합
    combined = f"# {series['title']}\n\n"
    combined += f"**{series['description']}**\n\n---\n\n"
    
    for part in sorted(series["parts"], key=lambda x: x["order"]):
        # 블로그 포스트 파일 찾기
        posts_dir = Path(f"content/posts/{series['category']}")
        matching = list(posts_dir.glob(f"*{part['slug']}*"))
        
        if matching:
            content = matching[0].read_text()
            # front matter 제거
            if content.startswith("---"):
                content = content.split("---", 2)[2]
            combined += f"## 제 {part['order']}장: {part['title']}\n\n"
            combined += content + "\n\n---\n\n"
    
    # 4. 결합 파일 저장
    combined_path = output / "book_combined.md"
    combined_path.write_text(combined)
    
    # 5. PDF 생성
    subprocess.run([
        "pandoc", str(combined_path),
        "-o", str(output / f"{series_id}.pdf"),
        "--pdf-engine=xelatex",
        "-V", "mainfont=NanumGothic",
        "-V", "geometry:margin=2cm",
        "--toc", "--toc-depth=3"
    ])
    
    print(f"✅ 책 컴파일 완료: {output / f'{series_id}.pdf'}")

# 실행
compile_series_to_book("notebooklm-guide")
```

---

## 시리즈 전체 요약

이 5편 시리즈에서 다룬 내용을 정리합니다:

| 편 | 주제 | 핵심 기술 |
|----|------|----------|
| **1편** | 기본 세팅 | 노트북 생성, 소스 추가 5가지 방법, UI 구조 |
| **2편** | 리서치 | Deep Research, AI 채팅 출처 인용, 노트 관리 |
| **3편** | Studio | 9가지 아티팩트 생성 & 다운로드 |
| **4편** | 자동화 | MCP CLI, 블로그 파이프라인, GitHub Actions |
| **5편** | 책 출간 | 시리즈→목차→챕터→PDF/ePub 컴파일 |

### NotebookLM으로 할 수 있는 것들

```
📚 리서치    → Deep Research로 40+ 소스 자동 수집
💬 분석     → AI 채팅으로 출처 기반 심층 분석
🎙️ 팟캐스트  → AI 오디오 오버뷰 자동 생성
🎬 동영상    → 설명 동영상 자동 제작
📊 인포그래픽 → 데이터 시각화 자동 생성
📑 슬라이드  → 프레젠테이션 자동 제작
📝 보고서    → 브리핑/학습가이드/블로그 자동 작성
📋 데이터 표 → 구조화된 데이터 추출
🗺️ 마인드맵  → 주제 관계 시각화
🤖 자동화    → MCP CLI로 전 과정 프로그래밍 가능
📖 출판     → 시리즈를 책으로 컴파일 & 출간
```

NotebookLM은 단순한 AI 도구가 아닌, **연구에서 출판까지의 전 과정을 통합하는 지식 플랫폼**입니다. 이 시리즈를 통해 NotebookLM을 100% 활용하여 여러분만의 콘텐츠를 창작해보세요.

## 📚 참고자료

- [Pandoc 공식 문서](https://pandoc.org/MANUAL.html)
- [Amazon KDP 출판 가이드](https://kdp.amazon.com/)
- [NotebookLM MCP CLI GitHub](https://github.com/nicholasgriffintn/notebooklm-mcp)
- [Google NotebookLM 공식 사이트](https://notebooklm.google.com)
- [ePub 전자책 규격 (IDPF)](https://www.w3.org/publishing/epubcheck/)