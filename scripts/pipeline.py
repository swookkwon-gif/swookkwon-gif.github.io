#!/usr/bin/env python3
"""
pipeline.py — Phase 1 오케스트레이터 (수집 + 분석 전용)

RSS 피드와 Gmail 뉴스레터를 수집 · 분석한 뒤,
구조화된 기사 데이터를 state/daily_articles.json에 저장한다.
포스트 생성은 하지 않는다 — Phase 3(daily_digest.py)에서 담당.

GitHub Actions에서 호출:
  python scripts/pipeline.py
"""
from __future__ import annotations
import os
import sys
import json
import time
from datetime import datetime, timezone, timedelta
from slugify import slugify

# 프로젝트 루트 경로 설정 (scripts/ 기준)
sys.path.insert(0, os.path.dirname(__file__))

from skills.llm_client import LLMClient
from agents.collector import collect_rss, collect_gmail
from agents.writer import write_rss_post, write_newsletter_post
from state.state_manager import mark_processed, save_evaluations

STATE_DIR = os.path.join(os.path.dirname(__file__), 'state')
DAILY_ARTICLES_PATH = os.path.join(STATE_DIR, 'daily_articles.json')


def save_daily_articles(articles: list[dict]):
    """수집·분석된 기사 목록을 JSON으로 저장한다."""
    os.makedirs(STATE_DIR, exist_ok=True)
    now_kst = datetime.now(timezone.utc) + timedelta(hours=9)
    payload = {
        "date": now_kst.strftime("%Y-%m-%d"),
        "generated_at": now_kst.isoformat(),
        "total_articles": len(articles),
        "articles": articles,
    }
    with open(DAILY_ARTICLES_PATH, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"   💾 {len(articles)}건 기사 데이터 저장: {DAILY_ARTICLES_PATH}")


def run_rss_phase(llm: LLMClient) -> list[dict]:
    """RSS 수집 → LLM 분석 → 구조화된 기사 목록 반환 (포스트 미생성)."""
    print("\n" + "=" * 55)
    print("📰 [Phase 1-A: RSS 수집 + 분석]")
    print("=" * 55)

    articles = collect_rss()
    if not articles:
        return []

    print(f"\n   📝 Writer: {len(articles)}개 기사 분석 중...")
    result = write_rss_post(articles, llm)
    if result is None:
        print("   ❌ Writer 실패: LLM 응답 없음")
        return []

    # Evaluations 저장 (state.json에 기록)
    evals = result.get("evaluations", [])
    if evals:
        save_evaluations("Global AI News", evals)

    # RSS 아이템 처리 완료 마킹
    for item in articles:
        mark_processed("rss", item["id"])

    if not result.get("has_ai_news"):
        print("   ✅ 중요 기사(3점 이상)가 없어 건너뜀 (처리완료 마킹)")
        return []

    # evaluations에서 구조화된 기사 데이터 추출
    structured_articles = []
    for ev in evals:
        structured_articles.append({
            "title": ev.get("target", ""),
            "summary": ev.get("reasoning", ""),
            "score": ev.get("score", 0),
            "source_name": "RSS (AITimes/Benzinga)",
            "source_urls": [ev.get("url")] if ev.get("url") else [],
            "keywords": [],
        })

    print(f"   ✅ RSS 분석 완료: {len(structured_articles)}건")
    return structured_articles


def run_gmail_phase(llm: LLMClient) -> list[dict]:
    """Gmail 수집 → LLM 분석 → 구조화된 기사 목록 반환 (포스트 미생성)."""
    print("\n" + "=" * 55)
    print("📧 [Phase 1-B: Gmail 뉴스레터 수집 + 분석]")
    print("=" * 55)

    gmail_groups = collect_gmail()
    if not gmail_groups:
        return []

    all_articles = []

    for sender, letters in gmail_groups.items():
        print(f"\n   -> [{sender}] 뉴스레터 분석 중 ({len(letters)}개)")

        result = write_newsletter_post(sender, letters, llm)
        if result is None:
            print(f"   ❌ Writer 실패: [{sender}] LLM 응답 없음")
            # 실패해도 처리 완료 마킹 (무한 재시도 방지)
            for letter in letters:
                mark_processed("gmail", letter["id"])
            continue

        # Evaluations 저장
        evals = result.get("evaluations", [])
        if evals:
            save_evaluations(sender, evals)

        # 처리 완료 마킹
        for letter in letters:
            mark_processed("gmail", letter["id"])

        md_content = result.get("markdown_content", "")
        if not md_content:
            print(f"   ✅ [{sender}] 중요 기사 없음 — 건너뜀")
            continue

        # evaluations에서 구조화된 기사 데이터 추출
        for ev in evals:
            all_articles.append({
                "title": ev.get("target", ""),
                "summary": ev.get("reasoning", ""),
                "score": ev.get("score", 0),
                "source_name": sender,
                "source_urls": [ev.get("url")] if ev.get("url") else [],
                "keywords": [],
            })

        print(f"   ✅ [{sender}] {len(evals)}건 분석 완료")

        # API Pacing
        print("   (발신자 간 대기 10초...)")
        time.sleep(10)

    return all_articles


def main():
    print("=======================================================")
    print("🚀 [Phase 1] 수집 + 분석 파이프라인 v3.0")
    print("=======================================================")

    # Delete stale intermediate files from previous failed runs
    state_file = os.path.join(STATE_DIR, "daily_articles.json")
    if os.path.exists(state_file):
        os.remove(state_file)
        print(f"🧹 이전 세션의 잔류 데이터({state_file})를 삭제했습니다.")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("⚠️ GEMINI_API_KEY is missing.")
        sys.exit(1)

    llm = LLMClient(api_key=api_key)

    # Phase 1-A: RSS
    rss_articles = run_rss_phase(llm)

    print("\n" + "-" * 55)

    # Phase 1-B: Gmail
    gmail_articles = run_gmail_phase(llm)

    # 통합 저장
    all_articles = rss_articles + gmail_articles
    save_daily_articles(all_articles)

    print("\n=======================================================")
    print(f"🎉 Phase 1 완료! 총 {len(all_articles)}건 기사 수집·분석")
    print("   → Phase 3(daily_digest.py)에서 통합 포스트 생성 예정")
    print("=======================================================")


if __name__ == "__main__":
    main()
