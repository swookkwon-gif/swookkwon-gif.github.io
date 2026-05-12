---
title: "[AdTech 도서 리뷰] 수수료의 민낯을 파헤치다: 『Jounce Media Little Black Book』 심층 분석"
date: 2026-05-12 15:30:00 +0900
category: Marketing
tags: ["애드테크", "JounceMedia", "SPO", "헤더비딩", "TechTax", "디지털마케팅도서"]
---

"구글 공식 문서보다 구글의 속내와 돈의 흐름을 더 정확히 파헤치는 가이드."
레딧(Reddit)의 r/adops(애드옵스) 실무자 커뮤니티에서 극찬을 받는 자료가 있습니다. 정식으로 출판된 묵직한 하드커버 도서가 아니라, 특정 컨설팅 펌에서 매년 무료로 발행하는 얇은 가이드북입니다. 

애드테크 컨설팅 전문 기업 **Jounce Media(바운스 미디어)**가 발행하는 **『The Little Black Book』** 시리즈는 시장에서 누가 가장 큰 마진을 가져가고 있는지, 그리고 광고주는 어떻게 그 낭비를 막을 수 있는지를 가장 적나라하게 분석합니다.

---

## 📖 핵심 시리즈 리스트 해부 (Core Series Topics)

The Little Black Book은 하나의 책이 아니라, 프로그래매틱 생태계의 핵심 화두가 생길 때마다 발간되는 '딥다이브 리포트' 시리즈입니다. 그중에서도 실무적으로 가장 큰 파장을 일으켰던 핵심 시리즈는 다음과 같습니다.

1.  **The Little Black Book of Ads**: 프로그래매틱의 기본 생리 파악
2.  **The Little Black Book of Header Bidding**: 워터폴(Waterfall)의 붕괴와 동시 입찰 방식의 부상
3.  **The Little Black Book of Private Marketplaces (PMP)**: 오픈 경매의 위험성과 폐쇄형 안전 마켓의 부상
4.  **The Little Black Book of Supply Path Optimization (SPO)**: 공급망 최적화를 통한 테크 텍스(Tech Tax) 다이어트

---

## 💡 시리즈가 폭로하는 자본의 흐름과 진실

### 1. 서플라이 체인 미로 (The Supply Chain Maze)
SPO(Supply Path Optimization) 편에서 등장하는 가장 유명한 시각 자료는 바로 **'스파게티 네트워크'**입니다. 
광고주가 예산을 집행하면, ATD(대행사 트레이딩 데스크) $\rightarrow$ 수많은 DSP $\rightarrow$ 수많은 Exchange $\rightarrow$ 수많은 SSP $\rightarrow$ 최종 퍼블리셔(매체)로 거미줄처럼 이어집니다. 문제는 하나의 광고 지면(Inventory)을 두고 A라는 SSP와 B라는 SSP가 동시에 같은 DSP에 입찰 요청을 보낸다는 것입니다.

이 과정에서 광고주는 **"나 자신과 입찰 경쟁을 하는(Bidding against oneself)"** 기형적인 현상이 벌어지며 불필요한 단가 상승과 수수료 중복 지출을 겪게 됩니다.

### 2. 헤더 비딩(Header Bidding)의 민낯
매체(퍼블리셔) 입장에서 쓰인 헤더 비딩 편은 구글의 독점을 꼬집습니다. 
과거에는 구글(AdX)이 가장 먼저 광고를 살 권리(Waterfall 방식)를 독점했습니다. 이를 타파하기 위해 매체들이 웹사이트 헤더(Header) 영역에 자바스크립트를 삽입하여 구글을 포함한 모든 SSP가 **'동시에'** 입찰하게 만든 것이 헤더 비딩입니다. 
책은 이 기술적 반란이 퍼블리셔의 수익(Yield)을 어떻게 30% 이상 끌어올렸는지 수치로 증명합니다.

### 3. PMP(Private Marketplace)로의 대이동 트렌드
오픈 익스체인지(OEX)는 말 그대로 누구나 들어올 수 있는 '난장판'입니다. 이곳에는 앞서 다룬 MFA 사이트와 가짜 트래픽이 득실거립니다. 
시리즈 데이터에 따르면, 글로벌 대형 광고주들의 예산이 점차 OEX를 떠나, 검증된 프리미엄 매체들과 직접 계약을 맺고 안전한 환경에서만 입찰을 진행하는 **PMP(비공개 마켓플레이스)**로 급격히 이동하는 막대그래프 트렌드를 보여줍니다.

---

## 📊 현업 퍼포먼스 마케터를 위한 적용점

이 가이드 시리즈는 "어떻게 타겟팅을 잘 할까"를 넘어 "어떻게 파이프라인(Supply Path)을 잘 뚫을까"를 고민하게 만듭니다.

*   **실무 추천 액션 (SPO 적용하기)**: 
    내가 쓰는 DSP 대시보드에서 똑같은 조선일보 웹사이트 지면을 사더라도 어떤 SSP(예: Rubicon, PubMatic, Google AdX)를 거쳐서 사는 게 가장 저렴한 수수료(Take rate)를 지불하는지 분석해야 합니다. 불필요하고 중복되는 SSP 경로를 차단(Turn off)하는 것만으로도 CPA(전환단가)를 즉시 낮출 수 있습니다.

---

## 📚 참고자료
1. Jounce Media, *The Little Black Book of Supply Path Optimization*.
2. Jounce Media, *The Little Black Book of Header Bidding*.
3. (해당 시리즈는 Jounce Media 공식 웹사이트에서 PDF 형태로 정기 배포됩니다.)
