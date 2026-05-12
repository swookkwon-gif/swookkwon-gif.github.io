---
title: "포스트 쿠키 시대의 필수 인프라: CAPI와 MMM의 부활"
date: 2026-05-10T14:00:00+09:00
categories: ["Data", "Digital Marketing"]
tags: ["CAPI", "MMM", "Cookieless", "First-party Data", "Attribution", "Data Infrastructure"]
author: "Antigravity"
---

서드파티 쿠키(Third-party Cookies)의 종말과 애플의 iOS 개인정보 보호 정책(ATT) 도입은 디지털 광고 업계에 '데이터 암흑기'를 가져왔습니다. 과거처럼 유저가 우리 웹사이트에서 무엇을 장바구니에 담았는지, 언제 구매했는지 플랫폼 픽셀(Pixel)을 통해 낱낱이 추적하는 것이 불가능해진 것입니다.

데이터의 양과 질이 급감하면서 마케터들은 큰 위기를 맞았습니다. 하지만 이를 극복하기 위해 다시 부상하고 있는 두 가지 핵심 인프라가 있습니다. 바로 **전환 API (CAPI)**와 **마케팅 믹스 모델링 (MMM)**입니다.

---

## 1. 전환 API (CAPI): 서버에서 서버로 쏘는 생명줄

기존의 픽셀(Pixel)은 '클라이언트 사이드(Client-side)' 추적 방식입니다. 유저의 브라우저에서 스크립트가 돌아가며 데이터를 수집합니다. 브라우저가 이를 차단하면 끝입니다.

이를 극복하기 위한 기술이 **CAPI (Conversions API)**입니다. CAPI는 유저의 브라우저를 거치지 않고, 우리(광고주)의 웹/앱 서버에서 플랫폼(구글, 메타)의 서버로 전환 데이터를 직접 쏘아 보내는 '서버 사이드(Server-side)' 추적 기술입니다.

```mermaid
graph TD
    A[유저 웹사이트 방문/결제] --> B[브라우저 Pixel]
    A --> C[우리 백엔드 서버]
    
    B -.->|Ad Block & 브라우저 정책에 의해 막힘| D[광고 플랫폼]
    C ==>|CAPI (서버 to 서버) 안전한 전송| D
    
    style B fill:#ffebee,stroke:#ef5350
    style C fill:#e8f5e9,stroke:#4caf50
    style D fill:#e3f2fd,stroke:#2196f3
```

- **장점 1. 데이터 유실 방지:** 브라우저 차단의 영향을 받지 않아 누락 없는(Data Loss Prevention) 완전한 구매 데이터를 플랫폼에 전달할 수 있습니다.
- **장점 2. 퍼스트 파티 데이터 활용:** 오프라인 매장 결제, CRM 내 등급 변화, 구독 연장 등 웹에서 일어나지 않는 고가치 전환 데이터도 플랫폼에 쏴주어 최적화에 활용할 수 있습니다.

---

## 2. MMM(마케팅 믹스 모델링)의 화려한 부활

CAPI가 개별 유저의 전환 신호를 복구하는 '미시적' 도구라면, **MMM (Marketing Mix Modeling)**은 쿠키에 전혀 의존하지 않고 전체 예산의 인과적 효율을 분석하는 '거시적' 도구입니다.

MMM은 1960년대 소비재 기업들이 TV나 라디오 광고 성과를 분석하기 위해 쓰던 오래된 통계 모델(다중 회귀 분석 등)입니다. 과거에는 수개월의 시간과 막대한 비용이 들었지만, 최근 서드파티 데이터가 막히면서 빅테크(구글의 LightweightMMM, 메타의 Robyn 등)와 오픈소스가 결합하며 빠르고 저렴한 SaaS 형태로 화려하게 부활했습니다.

### MMM이 각광받는 이유
- **프라이버시 이슈 제로:** 유저 개개인을 식별(Tracking)하지 않고, 일별/주별 채널 예산 총액과 전체 매출 총액만으로 통계적 인과관계를 추론합니다.
- **모든 마케팅 활동 통합:** 온라인 퍼포먼스 광고뿐만 아니라 OOH(옥외광고), TV CF, 심지어 강수량이나 경쟁사 세일 등 교란 변수까지 모델에 넣어 진정한 '광고의 기여도(Incrementality)'를 발라낼 수 있습니다.

---

## 3. 투트랙(Two-track) 인프라 전략

앞으로의 마케터는 더 이상 픽셀과 대시보드 ROAS 하나에만 의존할 수 없습니다.

1. **전술적 최적화 (Tactical):** CAPI를 구축하여 우리가 가진 1차 데이터(First-party Data)를 알고리즘에 고품질 신호로 지속적으로 먹여줍니다. (단기 ROAS 방어)
2. **전략적 예산 분배 (Strategic):** MMM을 주기적으로 구동하여 채널 간의 진짜 인과적 기여도(Causal Lift)를 확인하고 분기/연간 예산 비율을 조정합니다.

다음 포스트에서는 이러한 인프라 위에서 마케터가 AI 알고리즘의 노예가 되지 않고, 어떻게 능동적인 통제권을 쥐는 **'신호 설계자(Signal Designer)'**로 진화해야 하는지 알아보겠습니다.

---
## 📚 참고자료
- **Meta Blueprint**, *Conversions API Best Practices.*
- **Google Open Source**, *LightweightMMM Documentation.*
- **Robyn (by Meta)**, *Open source Marketing Mix Modeling framework.*
