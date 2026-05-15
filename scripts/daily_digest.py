#!/usr/bin/env python3
"""
daily_digest.py — Phase 3: 통합 데일리 다이제스트 생성

Phase 1(pipeline.py)이 저장한 daily_articles.json과
Phase 2(gf2_auto_blogger.py)가 저장한 deep_research.json을
로드하여 단일 통합 포스트를 생성한다.

GitHub Actions에서 호출:
  python scripts/daily_digest.py
"""
from __future__ import annotations
import os
import sys
import json
import time
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(__file__))

from google import genai
from google.genai import types

STATE_DIR = os.path.join(os.path.dirname(__file__), 'state')
DAILY_ARTICLES_PATH = os.path.join(STATE_DIR, 'daily_articles.json')
DEEP_RESEARCH_PATH = os.path.join(STATE_DIR, 'deep_research.json')
POSTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'content', 'posts', 'AI News')


# ── Utilities ──────────────────────────────────────────────────

def load_json_safe(path: str) -> dict | None:
    """JSON 파일을 안전하게 로드한다."""
    if not os.path.exists(path):
        print(f"   ⚠️ 파일 없음: {path}")
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"   ❌ JSON 로드 실패 ({path}): {e}")
        return None


def clean_json_response(text: str) -> str:
    """LLM 응답에서 JSON 블록을 추출한다."""
    text = text.strip()
    if text.startswith("```json"):
        text = text[len("```json"):].strip()
    if text.endswith("```"):
        text = text[:-len("```")].strip()
    return text


MODELS_TO_TRY = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash-latest']

DIGEST_SCHEMA = {
    "type": "object",
    "properties": {
        "post_title": {"type": "string"},
        "top_topics": {"type": "array", "items": {"type": "string"}},
        "markdown_content": {"type": "string"}
    },
    "required": ["post_title", "top_topics", "markdown_content"]
}


def call_llm_with_retry(prompt: str, schema: dict, label: str = "LLM") -> dict | None:
    """LLM 호출 (재시도 + 모델 폴백)."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("   ❌ GEMINI_API_KEY 환경 변수 없음")
        return None
    
    client = genai.Client(api_key=api_key.strip().strip('"').strip("'"))

    for attempt in range(3):
        for model_name in MODELS_TO_TRY:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.3,
                        response_mime_type="application/json",
                        response_schema=schema
                    )
                )
                raw_text = clean_json_response(response.text)
                return json.loads(raw_text)
            except json.JSONDecodeError as je:
                print(f"      ❌ [{label}] JSON 파싱 에러: {je}")
                time.sleep(10)
                break
            except Exception as e:
                err_msg = str(e)
                if any(x in err_msg for x in ["429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE", "500"]):
                    print(f"      ⚠️ [{label}] '{model_name}' API 제한. 다른 모델 시도...")
                    continue
                else:
                    print(f"      ❌ [{label}] API 실패: {e}")
                    return None
        print(f"      ⏳ [{label}] 모든 모델 실패. 30초 후 재시도... ({attempt+1}/3)")
        time.sleep(30)
    return None


# ── Main Merge Logic ──────────────────────────────────────────

def merge_and_create_digest():
    """Phase 1 + Phase 2 데이터를 로드하여 단일 데일리 다이제스트를 생성한다."""
    now_kst = datetime.now(timezone.utc) + timedelta(hours=9)
    date_str = now_kst.strftime("%Y-%m-%d")

    print("=======================================================")
    print("📰 [Phase 3] 통합 데일리 다이제스트 생성")
    print("=======================================================")

    # ── 1. Phase 1 데이터 로드 ──
    print("\n📂 Phase 1 데이터 로드 (daily_articles.json)...")
    articles_data = load_json_safe(DAILY_ARTICLES_PATH)
    articles = articles_data.get("articles", []) if articles_data else []
    print(f"   → {len(articles)}건 기사 로드")

    # ── 2. Phase 2 데이터 로드 ──
    print("\n📂 Phase 2 데이터 로드 (deep_research.json)...")
    research_data = load_json_safe(DEEP_RESEARCH_PATH)
    deep_research_md = research_data.get("markdown_content", "") if research_data else ""
    deep_research_title = research_data.get("title", "") if research_data else ""
    print(f"   → 딥 리서치 {'있음' if deep_research_md else '없음'}")

    # ── 3. 데이터 유효성 검증 ──
    if not articles and not deep_research_md:
        print("\n⚠️ Phase 1, 2 모두 데이터가 없습니다. 포스트 생성을 건너뜁니다.")
        return

    # ── 4. 통합 다이제스트 생성 ──
    # 4-A: 딥 리서치만 있고 뉴스레터 기사가 없는 경우 → 딥 리서치만으로 포스트 생성
    if not articles and deep_research_md:
        print("\n📝 뉴스레터 기사 없음 — 딥 리서치 단독 포스트 생성")
        final_md = deep_research_md
        post_title = deep_research_title or f"Daily Top 10: {now_kst.strftime('%m월 %d일')} 주요 AI 뉴스"
        title = f"{now_kst.month}월 {now_kst.day}일 - {post_title}"
        save_final_post(date_str, title, final_md)
        return

    # 4-B: 기사가 있는 경우 → LLM으로 통합 다이제스트 생성
    quality_articles = [a for a in articles if a.get("score", 0) >= 3]
    low_articles = [a for a in articles if a.get("score", 0) < 3]
    source_names = sorted(set(a.get("source_name", "Unknown") for a in articles))

    print(f"\n📝 통합 다이제스트 생성 중...")
    print(f"   총 {len(articles)}개 기사 (3점 이상: {len(quality_articles)}개, 미만: {len(low_articles)}개)")
    print(f"   소스: {', '.join(source_names)}")

    # LLM이 쉽게 읽을 수 있도록 구조 정리
    quality_list = []
    for a in quality_articles:
        url = a.get("source_urls", [""])[0] if a.get("source_urls") else ""
        quality_list.append({"title": a["title"], "source_name": a.get("source_name", ""), "score": a["score"], "summary": a.get("summary", ""), "url": url})
        
    articles_json = json.dumps(quality_list, ensure_ascii=False, indent=2)

    low_list = []
    for a in low_articles:
        url = a.get("source_urls", [""])[0] if a.get("source_urls") else ""
        low_list.append({"title": a["title"], "source_name": a.get("source_name", ""), "score": a["score"], "url": url})
        
    low_json = json.dumps(low_list, ensure_ascii=False) if low_list else "[]"

    deep_research_section = ""
    if deep_research_md:
        deep_research_section = f"""

[Deep Research — 오늘의 Top 10 심층 분석]
아래는 구글 검색 기반 딥 리서치로 작성된 오늘의 Top 10 뉴스 심층 분석입니다.
이 내용을 포스트 **가장 상단**에 배치하세요 (있는 그대로 포함, 수정하지 말 것):

{deep_research_md}
"""

    prompt = f"""
당신은 AI 데일리 다이제스트 수석 편집장입니다.
아래는 여러 소스에서 수집 + 분석한 AI 뉴스 기사 목록과 딥 리서치 결과입니다.
이를 하나의 통합 일간 뉴스 포스트(마크다운 본문)로 재구성하세요.
{deep_research_section}

[3점 이상 주요 기사]
{articles_json}

[3점 미만 단신 (하단 기타 뉴스용)]
{low_json}

[통합 규칙]
0. **URL 위생 규칙**: 원문 링크로 `substack.com/redirect/...`, `google.com/url?...`, `t.co/...` 등 리다이렉트/트래커 URL을 절대 사용하지 마세요. 반드시 최종 목적지 URL만 사용합니다.
0. **엄격한 팩트 준수**: 제공된 JSON 데이터(제목, 요약, 수치 등)에 없는 외부 지식을 절대로 덧붙이거나 환각(Hallucination)을 통해 상상해서 지어내지 마세요. 철저하게 주어진 텍스트 내용 안에서만 병합하세요.
1. **포스트 구성**:
   - 딥 리서치가 제공된 경우, 포스트 **최상단**에 배치 (내용을 요약하거나 수정하지 말고 원문 그대로 붙여넣을 것).
   - 이어서 뉴스레터/RSS 기사 기반 "📰 오늘의 주요 AI 뉴스" 섹션 작성.
2. **중복 뉴스 병합**: 같은 사건/발표를 다루는 기사들(keywords가 유사)을 하나로 합침.
   - 병합 시 모든 소스 이름을 "소스: A · B · C" 형태로 표기 (볼드체 없이)
   - 가장 상세한 summary를 기준으로 작성
3. **주요 뉴스 선별 및 정렬**:
   - 뉴스레터/RSS에서 수집된 [3점 이상 주요 기사] 중 가장 중요한 기사 **3~5개**를 선별하여 상세한 메인 뉴스로 작성하세요. (딥 리서치 내용과는 별개로 RSS에서 핵심 3~5개만 뽑아야 합니다).
   - 각 기사의 제목에는 아이콘(이모지)을 절대 사용하지 마세요.
4. **상위 3~5개 메인 뉴스 포맷**:
   - 포스트 최상단에 전체 메인 제목(H1, `# 제목`)을 절대 쓰지 마세요.
   - 각 뉴스: `## 제목`
   - 본문 2-4문장 + 핵심 수치가 있으면 불릿으로 강조
   - 출처 표기:
     `<br><small style="color: #888;">소스: 7min.ai · AITimes &nbsp;|&nbsp; 🔗 [원문 보기](URL) · [원문 2](URL)</small>`
   - 각 기사 끝에는 빈 줄 + `---` 구분선 + 빈 줄
5. **기타 뉴스**: 상위 3~5개 주요 뉴스로 선정되지 않은 나머지 기사 중 **중요도가 낮거나 단순 반복되는 기사는 과감히 제외(필터링)**하여 기타 뉴스 개수를 대폭 줄이세요. 선별된 소수의 단신만 `## 📌 기타 단신 모아보기` 섹션에서 소스별로 그룹핑하세요. (최대 10개 이내로 제한)
   - 소스 홈페이지 링크는 걸지 말고 `### 🔹 소스: 매체명` 형식으로 작성하세요.
   - 각 기사는 `* **[기사 제목](기사 URL)**: 요약 한 줄` 형태로 작성하며, URL이 없는 기사도 제외하지 말고 링크 없이 `* **기사 제목**: 요약 한 줄` 형태로 작성하세요.
6. **post_title 생성 규칙**: 여러 기사를 나열하지 말고, **가장 중요하고 파급력이 큰 단 1개의 핵심 뉴스(또는 딥 리서치 주제)만을 선택하여 간결하고 임팩트 있는 제목**을 작성하세요. 제목의 길이는 공백 포함하여 **절대 50자를 초과하지 마세요.**
7. **top_topics 생성 규칙**: 작성된 `post_title`을 영어로 요약 및 번역하여 파일명으로 사용할 수 있도록, 영문 소문자와 하이픈(-)만으로 이루어진 짧은 영문 슬러그 형태로 배열에 담아 제공하세요. (예: ["ai-security-threats"])
"""

    data = call_llm_with_retry(prompt, DIGEST_SCHEMA, label="Daily Digest")
    if not data:
        # LLM 실패 시 딥 리서치만이라도 발행
        if deep_research_md:
            print("      ⚠️ LLM 병합 실패 — 딥 리서치 단독 발행")
            post_title = deep_research_title or "AI 데일리 다이제스트"
            title = f"{now_kst.month}월 {now_kst.day}일 - {post_title}"
            save_final_post(date_str, title, deep_research_md, [])
        else:
            print("      ❌ 통합 다이제스트 생성 실패")
        return

    result_md = data.get("markdown_content", "")
    post_title = data.get("post_title", "AI 데일리 다이제스트")

    if not result_md:
        print("      ❌ 생성된 본문이 비어 있습니다.")
        return

    # 포스트 상단에 소스 요약 라인 추가
    source_line = f"> 📊 오늘의 AI 뉴스: **{len(quality_articles)}건** | 소스: {', '.join(source_names)}\n\n---\n\n"
    result_md = source_line + result_md

    title = f"{now_kst.month}월 {now_kst.day}일 - {post_title}"
    top_topics = data.get("top_topics", [])
    save_final_post(date_str, title, result_md, top_topics)


def save_final_post(date_str: str, title: str, content: str, top_topics: list = None):
    """최종 통합 포스트를 마크다운 파일로 저장한다."""
    import re

    os.makedirs(POSTS_DIR, exist_ok=True)

    # AI가 생성하는 중복 제목 제거
    content = re.sub(r'^#\s+[^\n]+\n*', '', content.lstrip())
    content = re.sub(r'^##\s+[^\n]+\n*', '', content.lstrip())

    # Excerpt 자동 생성
    clean_content = re.sub(r'<[^>]+>', '', content)
    clean_content = re.sub(r'https?://[^\s]+', '', clean_content)
    clean_content = re.sub(r'[#*`\[\]\(\)]', '', clean_content)
    clean_content = re.sub(r'\s+', ' ', clean_content).strip()
    excerpt_text = clean_content[:120] + "..." if len(clean_content) > 120 else clean_content
    excerpt_text = excerpt_text.replace('"', "'").replace('\n', ' ')

    frontmatter = f"""---
title: '{title.replace("'", "''")}'
date: '{date_str}'
excerpt: '{excerpt_text.replace("'", "''")}'
category: 'AI News'
---

"""
    slug = "daily-ai-digest"
    if top_topics:
        cleaned_topics = [re.sub(r'[^a-z0-9\-]', '', t.lower()) for t in top_topics]
        cleaned_topics = [t for t in cleaned_topics if t]
        if cleaned_topics:
            topic_slug = "-".join(cleaned_topics[:3])
            slug = f"ai-daily-{topic_slug}"
            
    filename = f"{date_str}-{slug}.md"
    file_path = os.path.join(POSTS_DIR, filename)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter)
        f.write(content + "\n\n")

    print(f"\n   ✅ 통합 다이제스트 포스트 저장 완료!")
    print(f"   📁 {file_path}")


def cleanup_intermediate_files():
    """Phase 1, 2의 중간 결과물을 정리한다 (선택적)."""
    for path in [DAILY_ARTICLES_PATH, DEEP_RESEARCH_PATH]:
        if os.path.exists(path):
            os.remove(path)
            print(f"   🧹 중간 파일 제거: {os.path.basename(path)}")


if __name__ == "__main__":
    merge_and_create_digest()
    # 성공적으로 생성 완료 후 중간 파일 삭제
    cleanup_intermediate_files()

    print("\n=======================================================")
    print("🎉 Phase 3 완료! 통합 데일리 다이제스트가 발행되었습니다.")
    print("=======================================================")
