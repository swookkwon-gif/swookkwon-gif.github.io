---
title: '[Antigravity 활용 가이드 2] 토큰 한계를 넘는 비법: YOLO 모드와 청킹(Chunking)'
date: '2026-05-09'
excerpt: 'Gemini CLI의 강력한 기능인 YOLO 모드를 활용한 브레인스토밍 이터레이션 기법과 제한된 컨텍스트 윈도우를 효율적으로 극복하는 청킹(Chunking) 기술을 소개합니다.'
category: 'AI Learnings'
---

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

# 2단계 ~ 4단계: 3번의 자율 개선 이터레이션 (YOLO 모드)
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
