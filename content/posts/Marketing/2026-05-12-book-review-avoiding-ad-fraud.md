---
title: "[AdTech 도서 리뷰] 마케팅 예산을 훔치는 어둠의 기술: 『Avoiding Ad Fraud』 심층 분석"
date: 2026-05-12 15:25:00 +0900
category: Marketing
tags: ["AdFraud", "광고사기", "브랜드세이프티", "애드테크", "MFA", "마케팅도서"]
---

"절반의 광고비가 낭비되고 있다는 것은 안다. 문제는 어느 쪽 절반인지 모른다는 것이다." 
존 워너메이커의 이 유명한 명언은 디지털 시대에 와서 더욱 잔혹한 현실이 되었습니다. 오늘날 낭비되는 절반의 광고비는 단순히 타겟팅이 안 된 유저에게 가는 것이 아니라, **'사기꾼(Fraudster)'들의 주머니**로 직접 들어가기 때문입니다.

학술/기술서 **『Avoiding Ad Fraud and Supporting Brand Safety』 (Muhammad Ibrahim Khan 외 편저)**는 바로 이 어둠의 자본 흐름을 추적하고, AI/ML(머신러닝)을 이용해 어떻게 이를 방어할 수 있는지 다룬 가장 전문적인 딥다이브 서적입니다.

---

## 📈 광고 사기, 얼마나 심각한가? (글로벌 데이터)

숫자는 거짓말을 하지 않습니다. 광고 사기의 규모를 먼저 직시해야 합니다.

| 연도 | 글로벌 광고 사기 피해 추정액 | 출처 |
| :---: | :---: | :---: |
| 2024 | **$37.7B** (약 51조 원) | Juniper Research / TrafficGuard |
| 2025 | **$41.4B** (약 56조 원) | 업계 복수 리서치 종합 |
| 2028 (전망) | **$172B** (약 234조 원) | Business of Apps |

*   글로벌 디지털 광고 예산의 **20-30%**가 무효 트래픽(IVT)이나 사기에 오염되어 있습니다.
*   IVT(Invalid Traffic) 비율은 채널에 따라 **8% - 20% 이상**까지 편차가 큽니다. 특히 CTV(커넥티드 TV)와 모바일 앱 환경에서 사기 비율이 가장 높습니다.
*   클릭 스패밍(Click Spamming) 단일 기법이 전체 IVT의 **75% 이상**을 차지한다는 보고도 있습니다.

---

## 📖 핵심 목차 해부 (Core Table of Contents)

이 책은 단순한 마케팅 개론서가 아닌, 무효 트래픽과 사기 기술의 '아키텍처'를 뜯어보는 기술서에 가깝습니다.

1.  **Chapter 1. The Ethics of Ad Fraud**: 생태계 교란과 윤리적 타격
2.  **Chapter 2. The Role of AI in Ad Fraud Detection**: AI를 활용한 비정상 트래픽 탐지 시스템
3.  **Chapter 3. Ad Fraud Types**: 사기 기법의 3대장 (배치, 트래픽, 액션 사기)
4.  **Chapter 4. Combating Evolving Threats**: MFA(Made For Advertising) 사이트 집중 해부
5.  **Chapter 5-6. Machine Learning for Brand Protection**: 머신러닝 기반 브랜드 보호 전략
6.  **Chapter 8. Combating Criminal Use of AI**: 딥페이크 및 범죄에 악용되는 AI 분석

---

## 💡 책에서 폭로하는 광고 사기(Ad Fraud)의 실체

### 1. 당신의 ROAS를 망치는 사기 기법의 3대장
책에서는 광고 사기를 크게 세 가지 축으로 분류하며, 각각이 마케터의 대시보드를 어떻게 망가뜨리는지 분석합니다.

*   **트래픽 사기 (Traffic Fraud / IVT)**: 데이터 센터에 구축된 서버나, 악성코드에 감염된 좀비 PC(Botnet)들이 무작위로 웹페이지를 새로고침하여 노출(Impression)과 클릭(Click)을 가짜로 만들어냅니다.
*   **배치 사기 (Placement Fraud)**: 1픽셀 크기의 투명한 iframe에 수십 개의 영상 광고를 쑤셔 넣거나(Pixel Stuffing), 광고 위에 다른 광고를 겹쳐서 송출하는(Ad Stacking) 수법입니다. 시스템 상으로는 100% 뷰어빌리티(Viewability)로 기록되지만 실제 사람은 아무도 보지 못합니다.
*   **액션 사기 (Action/Install Fraud)**: 가장 치명적인 수법으로, 실제 유저가 자연적으로(Organic) 앱을 설치하는 순간, 백그라운드에서 가짜 클릭 신호를 보내어 자신들의 광고 성과(Attribution)인 것처럼 가로채는 '클릭 인젝션(Click Injection)' 기법입니다.

### 2. 최악의 기생충: MFA (Made for Advertising)
책의 중반부는 최근 가장 심각한 화두인 **MFA 웹사이트**를 집중 조명합니다. MFA는 오직 '광고를 많이 게재하여 트래픽을 현금화'할 목적으로만 만들어진 쓰레기 사이트입니다. 
최근에는 생성형 AI를 이용해 하루에도 수천 개의 가짜 뉴스 기사를 찍어내고, 기사 하나당 30개가 넘는 배너 광고를 덕지덕지 붙여놓습니다. 프로그래매틱의 허점을 노려 광고주 예산을 진공청소기처럼 빨아들이는 주범으로 지목됩니다.

### 3. 역사에 남은 실제 사건: Methbot과 3ve

책에서는 광고 사기의 규모를 체감시키기 위해 실제 적발된 대형 범죄 사건을 사례로 다룹니다.

*   **Methbot (2016)**: 러시아 사이버 범죄 조직이 데이터 센터에 약 6,000개의 가짜 도메인과 25만 개의 URL을 구축하고, 봇(Bot)을 이용해 하루 **3억 건의 가짜 영상 광고 노출(Video Impression)**을 만들어냈습니다. 이를 통해 하루 300만-500만 달러(약 40억-68억 원)의 부정 수익을 올린 것으로 추정됩니다.
*   **3ve ("Eve", 2018)**: FBI가 직접 수사에 나선 역대 최대 규모의 디지털 광고 사기 사건입니다. 8개국에 걸친 170만 대의 감염 PC(Botnet)를 이용해 하루 **120억 건의 가짜 광고 입찰 요청(Bid Request)**을 생성했습니다. 총 피해액은 **3,600만 달러(약 490억 원)**에 달했고, 주동자 8명이 기소되었습니다.

### 4. 방어의 최전선: 머신러닝(ML) 기반의 패턴 탐지
이 책의 백미는 사기꾼들을 막기 위한 AI/ML 탐지 아키텍처 부분입니다.

*   **마우스 다이내믹스(Mouse Dynamics)**: 사람의 마우스 궤적은 곡선적이고 머뭇거림이 있지만, 봇(Bot)의 마우스 궤적은 자로 잰 듯한 직선이거나 지나치게 일정한 속도를 가집니다. 머신러닝 산점도(Scatter Plot)를 통해 정상 유저와 봇의 행동 패턴을 분리해 내는 기술적 원리를 상세히 보여줍니다.
*   **IP 및 디바이스 지문(Fingerprinting)**: 프록시 서버나 데이터 센터에서 대량으로 쏟아지는 IP 대역을 실시간으로 차단하는 알고리즘을 소개합니다.
*   **세션 행동 분석 (Session Behavior Analysis)**: 개별 지표(클릭, 노출)를 넘어 유저의 전체 세션을 종합적으로 분석합니다. 페이지 체류 시간이 0.3초이면서 3개의 광고를 모두 클릭하는 패턴, 혹은 완벽하게 일정한 시간 간격으로 반복 방문하는 패턴은 봇의 전형적인 시그널입니다.
*   **Anomaly Detection (이상 탐지)**: 비지도 학습(Unsupervised ML) 모델을 사용하여, 과거에 없던 새로운 유형의 사기를 라벨 없이도 감지합니다. 정상 트래픽의 통계적 분포에서 벗어난 '이상치(Outlier)'를 자동으로 플래그 처리합니다.

---

## 📊 현업 퍼포먼스 마케터를 위한 적용점

캠페인의 클릭률(CTR)이 비정상적으로 높게 나오거나, 밤 시간대에 특정 알 수 없는 매체에서 전환이 쏟아진다면 기뻐할 일이 아닙니다. 사기 트래픽의 타겟이 되었을 확률이 매우 높습니다.

*   **실무 추천 액션 1 — 게재위치 감사**: 당장 DSP 대시보드를 열람하여 **'게재위치(Placement) 리포트'**를 다운로드하세요. 이름 없는 무의미한 도메인(.tk, .xyz 등)이나 지나치게 많은 노출이 몰린 특정 사이트를 블랙리스트(Exclude) 처리해야 합니다.
*   **실무 추천 액션 2 — IVT 모니터링 도입**: 예산 규모가 크다면 DoubleVerify, IAS(Integral Ad Science), 또는 TrafficGuard 같은 써드파티 사기 탐지 솔루션 도입을 강력히 검토해야 합니다.
*   **실무 추천 액션 3 — ads.txt / sellers.json 검증**: IAB에서 제정한 ads.txt(매체측)와 sellers.json(SSP측) 파일을 교차 검증하여, 내 광고가 실제로 허가된 경로를 통해서만 거래되고 있는지 확인하세요. 도메인 스푸핑(Domain Spoofing) 방어의 1차 방어선입니다.

---

## 📚 참고자료
1. Muhammad Ibrahim Khan 외, *Avoiding Ad Fraud and Supporting Brand Safety*, IGI Global, 2025.
2. ANA(Association of National Advertisers), *Programmatic Media Supply Chain Transparency Study*, 2024.
3. FBI, *3ve: Takedown of Major Digital Ad Fraud Operation*, 2018.
4. White Ops (현 HUMAN Security), *Methbot Investigation Report*, 2016.
5. Juniper Research / TrafficGuard, *Ad Fraud Global Cost Estimates*, 2024–2025.
