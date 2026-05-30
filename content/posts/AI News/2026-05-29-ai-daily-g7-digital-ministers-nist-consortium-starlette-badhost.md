---
title: '5월 29일 - G7 파리 디지털 장관 선언과 NIST AI 컨소시엄 개편, 그리고 BadHost 취약점 사태'
date: '2026-05-29'
excerpt: '📅 분석 및 수집 기간: 2026년 5월 29일 G7 디지털 장관 회의의 파리 공동 선언, NIST AI Safety Institute Consortium의 NIST AI Consortium 확대 개편, 그리고 vLLM 등 AI 에이전트에 치명적인 Starlette BadHost 보안 취약점 경보'
category: 'AI News'
---

* 📅 분석 및 수집 기간: 2026년 5월 29일

## G7 디지털 장관 회의, 안전한 AI 구현과 공급망 회복력 강화를 위한 '파리 공동 선언문' 채택
* 📰 3개 소스에서 보도: Canada Government News, Reuters, European Digital Press
* 관련 출처: [G7 Digital Ministers’ Declaration on Secure and Responsible AI](https://www.canada.ca/en/innovation-science-economic-development/news/2026/05/g7-digital-ministers-declaration.html) — Canada Government News
* 관련 출처: G7 nations reach landmark agreement in Paris on global AI safety and digital environment protection — Reuters

프랑스 파리에서 개최된 G7 디지털 장관 회의(Digital Ministers' Meeting, 5월 28-29일)에서 회원국들이 **'안전하고 책임감 있는 AI와 디지털 복원력 강화'를 골자로 하는 파리 공동 선언문**을 전격 채택했다. 이번 회의에는 미국, 영국, 캐나다, 프랑스, 독일, 이탈리아, 일본 등 G7 회원국뿐만 아니라 EU 대표도 참석하여 최근 급성장한 에어블(Agentic AI) 기술 공급망의 안전 장치 마련을 집중 논의했다.

합의안은 경제 성장을 견인할 고성능 인프라 구축과 AI 산업 촉진을 도모하면서도, 딥페이크 및 가짜 뉴스 생성 봇 등으로 인한 선거 교란과 청소년의 안전 문제에 적극 공동 대응할 방식을 담았다. 캐나다 AI 및 디지털 혁신부 장관은 "빅테크 중심의 공급망 독점을 탈피하고, 신뢰성에 기반한 국제 데이터 환경(DFFT: Data Free Flow with Trust)과 반도체 공급선 다변화를 이끌기 위해 긴밀히 공조할 것"이라고 선언했다.

---

## 미 국립표준기술연구소(NIST), AI 연구 컨소시엄 'NIST AI Consortium'으로 공식 명칭 개편 및 역할 확대
* 📰 3개 소스에서 보도: NIST Press Release, Nextgov, Law360
* 관련 출처: [NIST AI Consortium Expansion and Task Group Assignments](https://www.nist.gov/news-events/news/2026/05/nist-ai-consortium-rebranding/) — NIST News
* 관련 출처: NIST renames AI safety institute consortium to encompass innovation and enterprise adoption — Nextgov

미국 국립표준기술연구소(NIST)는 기존에 운영해 오던 'AI 안전 연구소 컨소시엄(AISIC)'의 공식 명칭을 **'NIST AI Consortium'**으로 변경하고, 안전성 평가 영역을 넘어 AI 산업적 표준 수립, 보급 및 혁신 전반으로 조직의 역할을 전면 확대 개편한다고 발표했다.

NIST는 이와 함께 산하에 6개의 독립 태스크 그룹(Task Groups)을 발족시켰다. 이들 태스크는 생성형 AI 개발을 위한 고품질 학습 데이터의 표준 계측법 수립, 중소기업을 위한 프레임워크 도구 제작, 가속 데이터 센터의 전력 감축 가이드 개발 등을 다룰 예정이다. NIST 관계자는 "이전의 AI 안전 담론이 '잠재적 위협'에 대한 모니터링 수준에 머물렀다면, 앞으로는 실무 현장의 가속적 도입과 안전성 인증의 표준화(Measurement Science)를 정밀 매칭하는 실천적 역할을 가질 것"이라고 강조했다.

---

## vLLM 및 AI 에이전트 구동 엔진의 기반 framework에서 크리티컬 보안 취약점 'BadHost' (CVE-2026-48710) 발견
* 📰 4개 소스에서 보도: CVE Mitre Archive, Hacker News, DarkReading, TLDR Security
* 관련 출처: [Critical Authentication Bypass Vulnerability in Starlette Engine: BadHost](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2026-48710) — Mitre
* 관련 출처: CVE-2026-48710: Starlette vulnerability exposes AI Agents to remote takeover — Hacker News

많은 인공지능 에이전트 및 API 서버인 vLLM, LiteLLM, FastAPI 등의 근간을 이루고 있는 파이썬 웹 프레임워크 Starlette에서 크리티컬한 보안 취약점인 **'BadHost'(CVE-2026-48710)**가 보고되어 업계에 비상이 걸렸다.

이 취약점은 해커가 변조된 호스트 헤더(Host Header Injection) 신호를 주입하면, 웹 프레임워크 내부의 라우팅 필터링과 사용자 세션 검증이 무력화되어 AI 에이전트의 내부 권한을 완전히 획득하거나 데이터를 탈취할 수 있는 보안 루프이다. 특히 클라우드 상에서 도구 자율 사용(Tool-using) 권한을 가진 채 구동되는 많은 백그라운드 에이전트들이 이번 공격의 표적이 될 경우 원격 명령 실행(RCE) 등 치명적인 피해가 우려된다. 보안 당국은 vLLM이나 FastAPI 기반 시스템을 가동 중인 개발 부서와 운영팀은 즉시 최신 패치가 적용된 Starlette 신규 릴리스로 패키지 버전을 업그레이드할 것을 강력히 권고했다.

---

## 📌 기타 단신 모아보기
* **캘리포니아주 AI 규제 법안 Crossover 마감 통과**: 캘리포니아주 하원 및 상원에서 발의된 약 30여 개의 대담한 인공지능 안전 규제 법안들이 5월 29일 법안 심사 유예 마감 시한(Crossover deadline) 직전에 소관 상임위를 전격 통과했다. 이에 따라 주 단위 규제 법제화가 2학기 전후 공식 발효될 전망이다. [출처: Transparency Coalition]
* **K-12 교육용 AI 윤리 지표 출시**: 공익 연대 기구인 Just Horizons Alliance와 보스턴 대학교 휠록 교육대학원은 초·중·고 공교육 환경에 도입되는 에듀테크 및 교실 AI 솔루션들의 편향성과 개인정보 유출을 진단하기 위한 프레임워크인 'K-12 AI Ethics Index'를 공동 출시했다. [출처: Boston University News]

---

## 📚 참고자료
1. Canada Government. (2026). *G7 Digital Ministers’ Declaration on Secure and Responsible AI*. Innovation, Science and Economic Development Canada.
2. National Institute of Standards and Technology. (2026). *NIST AI Consortium Expansion and Task Group Assignments*. NIST Press.
3. Mitre CVE Database. (2026). *CVE-2026-48710: Starlette Host Header Injection Authentication Bypass*. Mitre Corporation.
4. Transparency Coalition. (2026). *California AI Legislative Updates and Crossover Deadlines*. Transparency Coalition News.
5. Boston University. (2026). *AI Ethics Index Launch for K–12 Education Classrooms*. Boston University Wheelock Publications.
6. [[5월 27일~28일 - 앤트로픽의 300억 달러 펀딩 유치와 MS 컴퓨터 조작 에이전트 공식 릴리스]](file:///Users/wook/WookAi/Booklog/content/posts/AI%20News/2026-05-28-ai-daily-anthropic-valuation-microsoft-agents.md)
