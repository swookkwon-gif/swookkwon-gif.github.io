---
title: '[Antigravity 활용 가이드 1] Antigravity와 Gemini CLI, 어떻게 다르게 써야 할까?'
date: '2026-05-08'
excerpt: 'Agentic AI 코딩 어시스턴트인 Antigravity와 강력한 터미널 도구인 Gemini CLI의 차이점을 알아보고, 각 도구를 어떤 상황에서 어떻게 활용해야 완벽한 시너지를 낼 수 있는지 분석합니다.'
category: 'AI Learnings'
---

![Antigravity vs Gemini CLI](/images/posts/antigravity-vs-cli-sketch.png)
*Antigravity와 Gemini CLI의 개념적 차이를 나타낸 스케치. 좌측은 자율적이고 탐색적인 로봇 에이전트, 우측은 결정론적이고 정밀하게 맞물려 돌아가는 자동화 톱니바퀴 메커니즘을 상징합니다.*

Google DeepMind 팀이 주도하는 Advanced Agentic Coding의 결정체인 **Antigravity**는 개발자의 워크플로우를 완전히 뒤바꿔 놓고 있습니다. 하지만 Antigravity 생태계를 100% 활용하기 위해서는 UI 기반의 에이전트 환경과 터미널 기반의 **Gemini CLI**를 정확히 이해하고 구분해서 사용할 줄 알아야 합니다.

이번 시리즈에서는 Antigravity와 Gemini CLI의 차별화된 사용법부터 YOLO 모드를 활용한 브레인스토밍, 그리고 오픈소스 Skill을 활용한 개발 자동화까지 상세히 다루어 보겠습니다. 첫 번째 시간으로, 두 도구의 근본적인 차이와 올바른 활용 전략을 살펴봅니다.

---

## 1. Antigravity: "탐색형, 대화형, 그리고 자율 주행"

Antigravity 에이전트(GUI 기반)는 개발자와 '페어 프로그래밍(Pair Programming)'을 하는 동료 개발자와 같습니다.

### 가장 적합한 활용 사례
* **맥락이 부족한 새로운 버그 디버깅**: "지금 로그인 페이지에서 500 에러가 나는데 왜 그런지 찾아줘"라고 지시하면, Antigravity가 스스로 파일을 열어보고 터미널 로그를 확인하며 원인을 추적합니다.
* **초기 아키텍처 설계 및 기획**: 구체적인 코딩 전, 사용자와 대화를 나누며 어떤 기술 스택을 쓸지, 폴더 구조는 어떻게 잡을지 지속적으로 피드백을 주고받습니다.
* **복잡한 다중 파일 리팩토링**: 여러 파일에 걸쳐 의존성이 얽혀 있는 코드를 수정할 때, 스스로 코드를 검색(grep)하고, 수정 사항을 반영한 뒤 린트(Lint) 에러를 수정하는 자율성을 발휘합니다.

**요약하자면, Antigravity는 명확한 정답이 없는 상태에서 길을 찾아가는 '자율 주행'에 최적화되어 있습니다.**

---

## 2. Gemini CLI: "반복형, 결정론적, 그리고 자동화"

반면, 터미널에서 실행되는 **Gemini CLI**는 명확하게 정의된 작업을 빠르고 반복적으로 처리하는 데 특화된 **정밀 타격 무기**입니다.

### 가장 적합한 활용 사례
* **반복적인 파이프라인 통합**: 매일 아침 RSS를 파싱해서 블로그 포스트를 만드는 크론잡(Cronjob)처럼, 쉘 스크립트(.sh) 내부에 삽입하여 백그라운드에서 AI를 가동할 때 필수적입니다.
* **단일 목적의 고속 작업**: 특정 코드 블록을 던져주고 "이 코드의 시간 복잡도만 계산해" 혹은 "이 함수의 Docstring을 작성해"와 같이 즉각적인 인풋/아웃풋이 필요할 때 압도적으로 빠릅니다.
* **Skill 기반의 정규화된 태스크**: 뒤에서 자세히 설명하겠지만, 사전에 잘 짜인 프롬프트와 컨텍스트를 `.yaml` 형태의 Skill로 저장해 두고 원할 때마다 터미널에서 훅(Hook)처럼 불러와 사용할 수 있습니다.

**요약하자면, Gemini CLI는 개발자가 파이프라인과 쉘 스크립트 속에 AI를 부품처럼 끼워 넣는 '자동화 엔진'입니다.**

---

## 3. 완벽한 시너지: 어떻게 차별화해서 사용할까?

최고의 개발 효율을 내려면 이 둘을 배타적으로 쓰는 것이 아니라 **상호 보완적**으로 사용해야 합니다.

1. **설계와 스크립팅은 Antigravity로**: 복잡한 비즈니스 로직을 구상하고 쉘 스크립트나 파이썬 데몬 코드를 작성하는 것은 Antigravity 에이전트에게 맡깁니다.
2. **실행과 반복은 Gemini CLI로**: Antigravity가 만들어준 자동화 스크립트 내부에 `gemini --skill code-review`와 같은 CLI 명령어를 삽입합니다. 이후 Github Actions나 로컬 Cron을 통해 인간의 개입 없이 코드가 실행되도록 만듭니다.

즉, **Antigravity는 'AI 자동화 공장'을 짓는 데 사용하고, Gemini CLI는 그 공장 안에서 돌아가는 '기계 부품'으로 사용하는 것**이 가장 이상적인 활용법입니다.

다음 편에서는 Gemini CLI를 한 단계 더 깊게 활용하기 위한 핵심 기술, **YOLO 모드를 활용한 다중 이터레이션(Iteration)과 청킹(Chunking) 기법**에 대해 상세히 알아보겠습니다.

---

## 📚 참고자료
* Google DeepMind Antigravity Documentation (2026)
* Gemini CLI Official Usage Guide & Command Line Reference
* Automating Workflows with CLI Agents, *AI Developer Journal* (2025)
