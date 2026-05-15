#!/usr/bin/env python3
"""
agents/writer.py — 포스트 작성 에이전트
Evaluator가 필터링한 기사 데이터를 바탕으로 마크다운 포스트를 작성한다.
포맷/스타일 규칙에만 집중한다.
"""
from __future__ import annotations
from datetime import datetime, timezone, timedelta
from slugify import slugify

from skills.llm_client import LLMClient
from skills.config_loader import load_prompts, load_guidelines
from agents.reviewer import review_llm_output


# ── JSON 스키마 ────────────────────────────────────────────────

RSS_SCHEMA = {
    "type": "object",
    "properties": {
        "has_ai_news": {"type": "boolean"},
        "evaluations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "target": {"type": "string"},
                    "score": {"type": "number"},
                    "reasoning": {"type": "string"},
                    "url": {"type": "string"}
                },
                "required": ["target", "score", "reasoning", "url"],
            },
        },
        "markdown_content": {"type": "string"},
    },
    "required": ["has_ai_news", "evaluations", "markdown_content"],
}

NEWSLETTER_SCHEMA = {
    "type": "object",
    "properties": {
        "post_title": {"type": "string"},
        "evaluations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "target": {"type": "string"},
                    "score": {"type": "number"},
                    "reasoning": {"type": "string"},
                    "url": {"type": "string"}
                },
                "required": ["target", "score", "reasoning", "url"],
            },
        },
        "markdown_content": {"type": "string"},
    },
    "required": ["post_title", "evaluations", "markdown_content"],
}


# ── RSS 포스트 작성 ────────────────────────────────────────────

def write_rss_post(articles: list[dict], llm: LLMClient) -> dict | None:
    """
    RSS 기사 목록을 바탕으로 종합 AI 뉴스 포스트를 작성한다.
    
    Args:
        articles: Collector가 수집한 기사 목록
        llm: LLMClient 인스턴스
    
    Returns:
        dict: {"has_ai_news": bool, "evaluations": list, "markdown_content": str}
    """
    prompts = load_prompts()
    custom_rules, custom_feedback = load_guidelines()

    # 기사 텍스트 조합
    articles_text = ""
    for idx, item in enumerate(articles, 1):
        articles_text += (
            f"\n\n--- 기사 {idx} (출처: {item['source_name']}) ---\n"
            f"제목: {item['title']}\n"
            f"링크: {item['url']}\n"
            f"내용(HTML): {item['content']}\n"
        )

    requirements = prompts.get("rss_requirements", "")

    prompt = f"""당신은 최고 수준의 AI 뉴스 에디터입니다.
아래 여러 RSS 소스에서 수집된 새 기사들을 바탕으로, 종합 AI 뉴스 마크다운 포스트 본문을 작성하세요.

[사용자 맞춤형 평가 핵심 룰]
{custom_rules}

[최근 사용자 직접 교정 예시 (Few-Shot)]
{custom_feedback}

[원문 정보]
{articles_text}

[요구사항]
{requirements}
"""

    return llm.call_with_review(
        prompt=prompt,
        schema=RSS_SCHEMA,
        reviewer_fn=review_llm_output,
        max_rounds=1,
    )


# ── 뉴스레터 포스트 작성 ──────────────────────────────────────

def write_newsletter_post(sender: str, letters: list[dict], llm: LLMClient) -> dict | None:
    """
    특정 발신자의 뉴스레터들을 바탕으로 블로그 포스트를 작성한다.
    
    Args:
        sender: 뉴스레터 발신자 이름
        letters: [{"subject": str, "body": str}, ...]
        llm: LLMClient 인스턴스
    
    Returns:
        dict: {"post_title": str, "evaluations": list, "markdown_content": str}
    """
    prompts = load_prompts()
    custom_rules, custom_feedback = load_guidelines()

    articles_text = ""
    for idx, letter in enumerate(letters, 1):
        articles_text += f"\n\n[제목: {letter['subject']}]\n{letter['body']}\n"

    requirements = prompts.get("gmail_requirements", "")
    # sender 변수를 요구사항 내에서 치환
    requirements = requirements.replace("{sender}", sender)

    prompt = f"""당신은 '윤(Yoon)' 님을 위한 수석 뉴스레터 AI 에디터입니다.
발신자 [{sender}](이)가 보낸 뉴스레터 데이터를 기반으로 블로그 포스트를 작성합니다.

[사용자 맞춤형 평가 핵심 룰]
{custom_rules}

[최근 사용자 직접 교정 예시 (Few-Shot)]
{custom_feedback}

[뉴스레터 데이터]
{articles_text}

[요구사항]
{requirements}
"""

    return llm.call_with_review(
        prompt=prompt,
        schema=NEWSLETTER_SCHEMA,
        reviewer_fn=review_llm_output,
        max_rounds=1,
    )


# ── 뉴스레터 일괄 분석 (API 최적화) ────────────────────────────

def write_newsletters_batch(all_senders: dict[str, list[dict]], llm: LLMClient) -> dict | None:
    """
    모든 발신자의 뉴스레터를 하나의 LLM 호출로 일괄 분석한다.
    기존 write_newsletter_post()가 발신자마다 개별 호출하던 것을 1회로 통합.

    Args:
        all_senders: {"발신자명": [{"id", "subject", "body"}, ...], ...}
        llm: LLMClient 인스턴스

    Returns:
        dict: {"post_title": str, "evaluations": list, "markdown_content": str}
    """
    prompts = load_prompts()
    custom_rules, custom_feedback = load_guidelines()

    # 모든 뉴스레터 본문을 하나의 텍스트로 합침
    articles_text = ""
    total_letters = 0
    sender_list = []
    for sender, letters in all_senders.items():
        sender_list.append(sender)
        for idx, letter in enumerate(letters, 1):
            total_letters += 1
            articles_text += (
                f"\n\n--- [{sender}] 뉴스레터 {idx} ---\n"
                f"[제목: {letter['subject']}]\n{letter['body']}\n"
            )

    requirements = prompts.get("gmail_requirements", "")
    # {sender} 치환을 전체 발신자 목록으로 대체
    sender_names = ", ".join(sender_list)
    requirements = requirements.replace("{sender}", sender_names)

    prompt = f"""당신은 '윤(Yoon)' 님을 위한 수석 뉴스레터 AI 에디터입니다.
아래 여러 발신자({sender_names})가 보낸 뉴스레터 데이터를 **통합 분석**하여 블로그 포스트를 작성합니다.
각 기사의 evaluations에는 반드시 해당 기사가 속한 발신자 이름도 reasoning에 포함해 주세요.

[사용자 맞춤형 평가 핵심 룰]
{custom_rules}

[최근 사용자 직접 교정 예시 (Few-Shot)]
{custom_feedback}

[뉴스레터 데이터 ({total_letters}건, 발신자 {len(sender_list)}명)]
{articles_text}

[요구사항]
{requirements}
"""

    print(f"   📦 뉴스레터 일괄 분석: {len(sender_list)}개 발신자, {total_letters}건 → 1회 LLM 호출")

    return llm.call_with_review(
        prompt=prompt,
        schema=NEWSLETTER_SCHEMA,
        reviewer_fn=review_llm_output,
        max_rounds=1,
    )
