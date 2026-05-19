---
title: "Gemini CLI & Antigravity 에이전트 완벽 가이드: 개발자 생산성 극대화 (통합본)"
date: 2026-05-10
category: "AI Learnings"
author: "Wook"
tags: []
---


## [Antigravity 활용 가이드 1] Antigravity와 Gemini CLI, 어떻게 다르게 써야 할까?

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

## [Antigravity 활용 가이드 2] 토큰 한계를 넘는 비법: YOLO 모드와 청킹(Chunking)

![YOLO Mode and Chunking](/images/posts/yolo-chunking-sketch.png)
*YOLO 모드와 청킹(Chunking)의 개념 스케치. 방대한 문서가 작게 쪼개져(Chunking) 처리된 후 병합되며, 우측의 순환하는 화살표는 사용자의 개입 없이 지속적으로 반복되는 YOLO 모드 루프를 의미합니다.*

지난 글에서 Antigravity(자율 탐색)와 Gemini CLI(스크립트 자동화)의 역할 분담을 알아보았습니다. 이번에는 개발 워크플로우를 극한으로 끌어올릴 수 있는 Gemini CLI만의 강력한 고급 기능, **YOLO(You Only Look Once) 모드**와 **청킹(Chunking)** 기법을 실전 사례와 함께 살펴보겠습니다.

---

## 1. YOLO 모드: 무한 브레인스토밍과 자율 이터레이션

일반적으로 터미널에서 위험한 명령어나 파일 수정을 수행할 때 AI는 사용자에게 Y/N 승인을 요청합니다. 하지만 쉘 스크립트를 통한 완전 자동화 환경에서는 이러한 멈춤(Pause)이 장애물이 됩니다. 

Gemini CLI의 `--yolo` 플래그는 사용자의 승인 절차를 생략하고 AI가 스스로 결정을 내리도록 허용합니다. 이를 가장 잘 활용할 수 있는 분야가 바로 **다중 이터레이션(Iteration) 기반의 브레인스토밍과 코드 개선**입니다.

### 실전 활용 사례: 자율 개선 루프
단일 프롬프트로 완벽한 결과물을 얻기란 어렵습니다. YOLO 모드를 쉘 스크립트의 `for` 루프와 결합하면, AI가 초안을 작성하고 스스로 비판한 뒤 다시 수정하는 과정을 자동화할 수 있습니다.

```bash
#!/bin/bash
# 1단계: 초안 작성
gemini --yolo "새로운 AI 팟캐스트를 위한 기획안 초안을 작성해줘." > draft.md

# 2단계 - 4단계: 3번의 자율 개선 이터레이션 (YOLO 모드)
for i in {1..3}
do
  gemini --yolo "이전 기획안(draft.md)을 읽고, 비판적인 시각으로 약점을 찾아 더 창의적이고 도발적으로 수정해줘." --file draft.md > temp.md
  mv temp.md draft.md
done
```
명령어 한 줄만 실행해 두고 커피를 마시고 오면, 인간의 개입 없이 AI 스스로 3번의 피드백 루프를 거친 고도화된 결과물이 탄생합니다.

---

## 2. 청킹(Chunking): 제한된 AI 토큰 안에서 최고의 품질 뽑아내기

최신 LLM들이 수백만 토큰의 컨텍스트 윈도우를 지원하지만, 한 번에 너무 많은 코드를 밀어 넣으면 AI가 중요한 디테일을 놓치거나(Lost in the middle) 생성 길이 제한으로 인해 답변이 중간에 잘리는 현상이 발생합니다.

이때 Gemini CLI를 활용해 입력 데이터를 작은 단위로 나누는 **청킹(Chunking)** 기법을 적용하면 결과물의 품질을 극적으로 끌어올릴 수 있습니다.

### 청킹 기반의 코드 리뷰 파이프라인
거대한 모노레포(Monorepo) 전체를 리뷰해야 한다고 가정해 봅시다. 폴더 전체를 한 번에 AI에게 던지는 대신, CLI 스크립트를 이용해 파일별로 쪼개어 접근합니다.

1. **분할 처리 (Map)**: `find` 명령어와 조합하여 각 소스 파일마다 독립된 Gemini CLI 프로세스를 실행합니다.
   ```bash
   find ./src -name "*.ts" -exec gemini --yolo "이 파일의 보안 취약점만 분석해줘" --file {} \; > review_raw.txt
   ```
2. **선택적 병합 (Reduce)**: 수십 개의 파일에서 나온 개별 분석 결과를 모아, 다시 한 번 AI에게 요약을 맡깁니다.
   ```bash
   gemini --yolo "다음 개별 보안 리뷰 결과들을 종합해서, 가장 시급한 Top 3 크리티컬 이슈만 리포트로 만들어줘" --file review_raw.txt > final_report.md
   ```

### 왜 청킹이 중요한가?
* **정밀도 향상**: AI가 한 번에 하나의 파일(또는 함수)에만 집중하므로, 놓치는 버그 없이 촘촘한 분석이 가능합니다.
* **비용 및 토큰 절약**: 불필요한 전체 컨텍스트를 매번 전달하지 않아 API 비용을 줄이고 생성 토큰 한도(Output Limits)에 걸릴 위험을 제거합니다.

---

Gemini CLI의 YOLO 모드와 청킹은 단순한 프롬프팅을 넘어 'AI 엔지니어링'의 영역으로 우리를 안내합니다. 다음 마지막 편에서는 전 세계 개발자들이 만들어 공유하는 **오픈소스 Skill 생태계**를 활용하여 내 입맛에 맞는 코딩 자동화 도구를 구축하는 방법을 알아보겠습니다.

---

## 📚 참고자료
* Effective Prompting and Chunking Strategies for LLMs, *AI Developer Journal* (2025)
* Gemini CLI Documentation: The `--yolo` Flag and Unattended Execution
* Advanced Bash Scripting with Language Models (2026)

## [Antigravity 활용 가이드 3] 오픈소스 Skill로 코딩 자동화 파이프라인 구축하기

![Skill Pipeline](/images/posts/skill-pipeline-sketch.png)
*오픈소스 Skill이 개발 파이프라인에 결합되는 과정을 묘사한 스케치. 개발자가 퍼즐 조각(Skill)을 기존 코드(Code)와 자동화 워크플로우(Automation Workflow) 사이에 끼워 넣어 완벽한 파이프라인을 완성하는 모습입니다.*

[Antigravity 활용 가이드] 시리즈의 마지막 편입니다. 1편에서 Antigravity와 Gemini CLI의 차별점을, 2편에서 YOLO 모드와 청킹(Chunking)을 다루었다면, 이번에는 실제 개발 현장에서 가장 유용하게 쓰이는 **Skill 생태계와 확장 방법**에 대해 알아봅니다.

---

## 1. Skill이란 무엇인가?

Gemini CLI에서 말하는 **Skill**은 단순히 '명령어 모음'이 아닙니다. 특정 작업을 완벽하게 수행하기 위해 필요한 **프롬프트, 모델 설정, 시스템 컨텍스트, 그리고 사용할 Tool(명령어 실행, 파일 접근 등)의 권한**을 하나의 `.yaml` 파일이나 설정 블록으로 패키징한 단위입니다.

매번 터미널에서 길고 복잡한 프롬프트를 타이핑할 필요 없이, `gemini --skill <skill_name>` 한 줄이면 특정 도메인 전문가 모드로 AI를 소환할 수 있습니다.

---

## 2. 오픈소스 Skill 생태계의 힘

Gemini CLI가 특히 개발자들에게 환영받는 이유는 방대한 **오픈소스 Skill 생태계** 덕분입니다. Github을 비롯한 다양한 커뮤니티에는 전 세계 개발자들이 깎고 다듬은 훌륭한 스킬들이 무수히 공개되어 있습니다.

### 주목할 만한 오픈소스 스킬 사례
* **`commit-msg-gen`**: `git diff` 결과를 분석하여 Conventional Commits 규격에 맞는 완벽한 커밋 메시지를 자동 생성합니다.
* **`security-audit`**: 로컬 프로젝트의 의존성(package.json 등)과 코드를 스캔하여 알려진 취약점(CVE)이나 하드코딩된 시크릿 키를 찾아냅니다.
* **`test-writer`**: 특정 함수를 선택하면 Jest나 PyTest 기반의 엣지 케이스가 포함된 단위 테스트 코드를 자동으로 생성해 파일로 저장합니다.

개발자는 처음부터 프롬프트를 설계할 필요 없이, 커뮤니티에서 검증된 스킬을 그대로 가져다 쓰기만 하면 됩니다.

---

## 3. 커스텀 스킬 확장: 내 프로젝트에 완벽하게 맞추기

공개된 스킬을 그대로 사용하는 것도 좋지만, 진정한 위력은 **스킬의 확장(Extension)**에서 나옵니다. 오픈소스 스킬을 가져와 우리 팀의 컨벤션이나 프레임워크에 맞게 커스터마이징해 봅시다.

### 예시: React/Next.js 전용 코드 리뷰어 만들기
범용적인 `code-review` 스킬을 가져와, Next.js 팀의 컨벤션에 맞게 확장하는 시나리오입니다. 스킬 설정 파일(`my-nextjs-reviewer.yaml`)을 아래와 같이 수정합니다.

```yaml
name: my-nextjs-reviewer
base_skill: community/code-review
system_prompt: |
  당신은 Next.js (App Router) 전문가입니다. 
  제공된 코드의 리뷰를 수행하되, 다음 3가지를 집중적으로 검사하세요.
  1. 클라이언트 컴포넌트("use client")가 불필요하게 사용되지 않았는지
  2. Server Action의 보안(Authorization)이 적절히 처리되었는지
  3. Tailwind CSS 클래스가 최적화되어 있는지
```

이제 터미널에서 코드를 커밋하기 전, 혹은 Git Pre-commit 훅에 다음 명령어를 추가합니다.
```bash
git diff --cached | gemini --skill my-nextjs-reviewer --yolo
```
팀만의 완벽한 맞춤형 시니어 프론트엔드 개발자가 로컬 터미널에 상주하며 코드를 검증하게 됩니다.

---

## 4. 맺음말: 개발 패러다임의 전환

Antigravity의 GUI 환경이 우리의 코딩 여정을 이끌어주는 든든한 내비게이션이라면, Gemini CLI와 Skill 시스템은 험난한 오프로드를 거침없이 달릴 수 있게 해주는 고성능 엔진입니다.

* **UI에서 큰 그림을 그리고 (Antigravity)**
* **CLI로 잘게 쪼개어 반복시키며 (Chunking & YOLO)**
* **검증된 스킬로 자동화의 레버리지를 높이세요 (Skills)**

이 세 가지 요소가 결합될 때, 개발자는 단순 코더를 넘어 시스템을 오케스트레이션하는 진정한 의미의 '소프트웨어 아키텍트'로 거듭날 수 있습니다.

---

## 📚 참고자료
* Antigravity Open Skill Repository, *GitHub* (2026)
* Customizing System Prompts for Local CLI Agents
* Next.js App Router Security Best Practices (2025)