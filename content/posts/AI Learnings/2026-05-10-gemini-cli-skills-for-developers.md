---
title: '[Antigravity 활용 가이드 3] 오픈소스 Skill로 코딩 자동화 파이프라인 구축하기'
date: '2026-05-10'
excerpt: 'Gemini CLI의 꽃이라 할 수 있는 Skill 시스템을 이해하고, 오픈소스로 공개된 다양한 스킬을 확장하여 강력한 코딩 자동화 워크플로우를 구축하는 방법을 알아봅니다.'
category: 'AI Learnings'
---

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
