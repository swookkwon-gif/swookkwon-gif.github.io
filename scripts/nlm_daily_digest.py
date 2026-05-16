#!/usr/bin/env python3
"""
nlm_daily_digest.py — NotebookLM 기반 데일리 다이제스트 (Gemini API 0회)

기존 pipeline.py + gf2_auto_blogger.py + daily_digest.py를 NotebookLM으로 통합.
로컬 수동 트리거 전용 — `nlm` CLI가 인증된 상태여야 합니다.

사용법:
    python scripts/nlm_daily_digest.py
    python scripts/nlm_daily_digest.py --skip-research   # 웹 리서치 생략
    python scripts/nlm_daily_digest.py --deep             # 딥 리서치 모드 (~5분)
"""
from __future__ import annotations
import os
import sys
import re
import json
import subprocess
import tempfile
import time
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(__file__))

from agents.collector import collect_rss, collect_gmail
from state.state_manager import mark_processed

POSTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'content', 'posts', 'AI News')
STATE_DIR = os.path.join(os.path.dirname(__file__), 'state')


# ── NLM CLI 래퍼 ─────────────────────────────────────────────

def nlm_run(args: list[str], timeout: int = 300) -> str:
    """nlm CLI 명령을 실행하고 stdout을 반환한다."""
    cmd = ["nlm"] + args
    print(f"   🔧 nlm {' '.join(args[:3])}...")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode != 0:
            print(f"      ❌ nlm 에러: {result.stderr.strip()}")
            return ""
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print(f"      ⏱️ nlm 타임아웃 ({timeout}초)")
        return ""
    except FileNotFoundError:
        print("      ❌ nlm CLI를 찾을 수 없습니다. `pip install notebooklm` 필요")
        sys.exit(1)


def nlm_create_notebook(title: str) -> str:
    """노트북을 생성하고 ID를 반환한다."""
    output = nlm_run(["notebook", "create", title])
    # 출력에서 notebook ID 추출 (UUID 형식)
    match = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', output)
    if match:
        return match.group(1)
    # ID가 없으면 출력 전체를 반환 (alias 이름일 수 있음)
    print(f"      📓 노트북 생성 완료: {output[:100]}")
    return output.split('\n')[0].strip() if output else ""


def nlm_add_text_source(notebook_id: str, text: str, title: str) -> bool:
    """텍스트를 파일로 저장한 후 소스로 추가한다."""
    # nlm source add --text 옵션이 긴 텍스트를 받기 어려우므로 파일로 전달
    tmp_path = os.path.join(STATE_DIR, f"_nlm_source_{title.replace(' ', '_')}.md")
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(tmp_path, 'w', encoding='utf-8') as f:
        f.write(text)

    output = nlm_run(["source", "add", notebook_id, "--file", tmp_path, "--title", title, "--wait"], timeout=120)

    # 임시 파일 정리
    try:
        os.remove(tmp_path)
    except Exception:
        pass

    return bool(output)


def nlm_research(notebook_id: str, query: str, mode: str = "fast") -> bool:
    """웹 리서치를 실행하고 소스를 자동 임포트한다."""
    output = nlm_run(
        ["research", "start", query,
         "--notebook-id", notebook_id,
         "--mode", mode,
         "--auto-import"],
        timeout=600 if mode == "deep" else 180,
    )
    return "import" in output.lower() or "complete" in output.lower() or bool(output)


def nlm_configure_chat(notebook_id: str, custom_prompt: str) -> bool:
    """채팅 커스텀 프롬프트를 설정한다."""
    output = nlm_run(
        ["chat", "configure", notebook_id,
         "--goal", "custom",
         "--prompt", custom_prompt,
         "--response-length", "longer"],
        timeout=30,
    )
    return bool(output)


def nlm_query(notebook_id: str, question: str, timeout: int = 300) -> str:
    """노트북에 질문하고 응답을 반환한다. JSON 래핑 응답을 자동 파싱."""
    output = nlm_run(
        ["notebook", "query", notebook_id, question, "--timeout", str(timeout)],
        timeout=timeout + 30,
    )
    if not output:
        return ""

    # NLM CLI가 JSON wrapper로 응답할 경우 answer 필드 추출
    try:
        import json as _json
        parsed = _json.loads(output)
        # {"value": {"answer": "..."}} 형식
        if isinstance(parsed, dict):
            value = parsed.get("value", parsed)
            if isinstance(value, dict) and "answer" in value:
                return value["answer"]
        return output
    except (ValueError, _json.JSONDecodeError):
        # JSON이 아니면 원문 그대로 반환
        return output


def nlm_delete_notebook(notebook_id: str):
    """노트북을 삭제한다."""
    nlm_run(["notebook", "delete", notebook_id, "-y"], timeout=15)


# ── 데이터 포맷터 ────────────────────────────────────────────

def format_rss_as_markdown(articles: list[dict]) -> str:
    """RSS 기사 목록을 NotebookLM 소스용 마크다운으로 변환한다.
    각 기사에 [출처]와 [URL]을 명시하여 NLM이 인용 시 사용하도록 한다."""
    if not articles:
        return ""

    lines = ["# RSS 뉴스 수집 결과\n"]
    lines.append("아래 각 기사의 [출처]와 [원문 URL]을 본문 작성 시 반드시 인용하세요.\n")
    for idx, art in enumerate(articles, 1):
        lines.append(f"## {idx}. {art['title']}")
        lines.append(f"[출처: {art['source_name']}]")
        lines.append(f"[원문 URL: {art['url']}]")
        content_preview = art.get('content', '')[:2000]
        lines.append(f"\n{content_preview}\n")
    return "\n".join(lines)


def format_gmail_as_markdown(gmail_groups: dict[str, list[dict]]) -> str:
    """Gmail 뉴스레터를 NotebookLM 소스용 마크다운으로 변환한다.
    각 뉴스레터에 [출처: 뉴스레터명]을 명시하고, 본문 내 Link 패턴을 보존한다."""
    if not gmail_groups:
        return ""

    lines = ["# Gmail 뉴스레터 수집 결과\n"]
    lines.append("아래 각 뉴스레터의 [출처]를 본문 작성 시 반드시 인용하세요.\n")
    for sender, letters in gmail_groups.items():
        for idx, letter in enumerate(letters, 1):
            lines.append(f"## [{sender}] {letter['subject']}")
            lines.append(f"[출처: {sender}]")
            body_preview = letter.get('body', '')[:5000]
            # body에서 (Link: URL) 패턴을 마크다운 링크로 변환
            body_preview = re.sub(
                r'([^(]+?)\s*\(Link:\s*(https?://[^)]+)\)',
                r'[\1](\2)',
                body_preview,
            )
            lines.append(f"\n{body_preview}\n")
    return "\n".join(lines)


# ── 포스트 저장 ──────────────────────────────────────────────

def parse_and_save_post(raw_response: str, date_str: str, now_kst: datetime):
    """NLM 응답에서 메타데이터를 추출하고 최종 포스트를 저장한다."""
    os.makedirs(POSTS_DIR, exist_ok=True)

    # 메타데이터 추출 시도
    display_title = f"{now_kst.month}월 {now_kst.day}일 - 주요 AI 뉴스"
    slug_parts = ["daily-ai-digest"]
    content = raw_response

    lines = raw_response.split('\n')
    content_start = 0

    for i in range(min(15, len(lines))):
        line = lines[i].strip()
        title_match = re.match(r'^(?:\*\*)?TITLE(?:\*\*)?\s*:\s*(.*)', line, re.IGNORECASE)
        excerpt_match = re.match(r'^(?:\*\*)?EXCERPT(?:\*\*)?\s*:\s*(.*)', line, re.IGNORECASE)
        topics_match = re.match(r'^(?:\*\*)?TOP_TOPICS(?:\*\*)?\s*:\s*(.*)', line, re.IGNORECASE)

        if title_match:
            raw_title = title_match.group(1).replace("[", "").replace("]", "").strip()
            display_title = f"{now_kst.month}월 {now_kst.day}일 - {raw_title}"
            content_start = max(content_start, i + 1)
        elif topics_match:
            raw_topics = topics_match.group(1).replace("[", "").replace("]", "").strip()
            slug_parts = [t.strip() for t in raw_topics.split(",") if t.strip()]
            content_start = max(content_start, i + 1)
        elif excerpt_match:
            content_start = max(content_start, i + 1)

    # 50자 제한 강제
    if len(display_title) > 50:
        display_title = display_title[:47] + "..."

    # 메타데이터 추출 실패 시 본문 첫 소제목에서 제목 추출
    remaining_lines = lines[content_start:]
    if display_title == f"{now_kst.month}월 {now_kst.day}일 - 주요 AI 뉴스":
        for line in remaining_lines:
            heading_match = re.match(r'^##\s+(.+)', line.strip())
            if heading_match:
                raw_title = heading_match.group(1).strip()
                display_title = f"{now_kst.month}월 {now_kst.day}일 - {raw_title}"
                if len(display_title) > 50:
                    display_title = display_title[:47] + "..."
                break

    # TOP_TOPICS 추출 실패 시 제목에서 슬러그 자동 생성
    if slug_parts == ["daily-ai-digest"]:
        # 한글 제목에서 핵심 키워드 추출 → 영문 슬러그
        import hashlib
        title_hash = hashlib.md5(display_title.encode()).hexdigest()[:8]
        slug_parts = [f"news-{title_hash}"]

    # 본문 추출 (메타데이터 라인 제거)
    content = "\n".join(lines[content_start:]).strip()

    # AI가 생성하는 중복 제목 제거
    content = re.sub(r'^#\s+[^\n]+\n*', '', content.lstrip())

    # Excerpt 자동 생성
    clean_content = re.sub(r'<[^>]+>', '', content)
    clean_content = re.sub(r'https?://[^\s]+', '', clean_content)
    clean_content = re.sub(r'[#*`\[\]\(\)]', '', clean_content)
    clean_content = re.sub(r'\s+', ' ', clean_content).strip()
    excerpt_text = clean_content[:120] + "..." if len(clean_content) > 120 else clean_content
    excerpt_text = excerpt_text.replace('"', "'").replace('\n', ' ')

    # 슬러그 생성
    cleaned_topics = [re.sub(r'[^a-z0-9\-]', '', t.lower()) for t in slug_parts]
    cleaned_topics = [t for t in cleaned_topics if t]
    if cleaned_topics:
        slug = f"ai-daily-{'-'.join(cleaned_topics[:3])}"
    else:
        slug = "daily-ai-digest"

    # 프론트매터
    frontmatter = f"""---
title: '{display_title.replace("'", "''")}'
date: '{date_str}'
excerpt: '{excerpt_text.replace("'", "''")}'
category: 'AI News'
---

"""
    filename = f"{date_str}-{slug}.md"
    file_path = os.path.join(POSTS_DIR, filename)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter)
        f.write(content + "\n\n")

    print(f"\n   ✅ 포스트 저장 완료!")
    print(f"   📁 {file_path}")
    print(f"   📝 제목: {display_title}")
    return file_path


# ── 메인 파이프라인 ──────────────────────────────────────────

CHAT_PROMPT = """당신은 AI 데일리 다이제스트 수석 편집장입니다.
노트북에 추가된 소스(RSS 뉴스, Gmail 뉴스레터, 웹 리서치)를 종합하여
한국어로 된 고품질 테크 블로그 포스트를 작성합니다.

[절대 규칙]
- 포스트 최상단에 H1(# 제목)을 절대 쓰지 마세요.
- 소제목은 ## 형식으로 작성하세요.
- [1], [2] 같은 숫자 인용은 절대 사용하지 마세요. 대신 소스의 [출처: ...]에 표기된 이름을 사용하세요.
- 어조: 전문적 테크 저널 어조(~이다, ~한다)를 사용하세요.
- 동일한 뉴스가 여러 소스에서 다뤄졌다면, 반드시 병합하고 출처를 모두 표기하세요.
- 하단에 '## 📚 참고자료' 섹션을 추가하세요.

[출처 표기 규칙]
- 각 뉴스 소제목 바로 아래에 * 관련 출처: 형식으로 해당 뉴스를 다룬 소스명과 원문 링크를 나열하세요.
- 형식: * 관련 출처: [기사제목](원문URL) — 출처명1, 출처명2, ...
- 여러 소스에서 다뤄진 경우: * 📰 N개 소스에서 보도: 출처명1, 출처명2, 출처명3
- 소스의 [원문 URL: ...] 태그에 있는 실제 URL을 사용하세요. 절대 (URL), (PDF) 같은 플레이스홀더를 쓰지 마세요."""

QUERY_PROMPT = """소스에 포함된 모든 뉴스를 분석하여 통합 AI 데일리 다이제스트 블로그 포스트를 작성해주세요.

반드시 응답의 첫 세 줄에 아래 메타데이터를 작성하세요 (이 줄들은 본문과 분리하여 첫 세 줄에만 작성):
TITLE: 가장 중요한 1개 뉴스를 골라 간결한 제목 (50자 이내, 대괄호 없이)
EXCERPT: 전체 요약 2~3문장
TOP_TOPICS: 영문 슬러그 1~3개, 예: ai-security, nvidia-earnings

그 아래에 본문을 작성하세요:

[필수 구조]
1. 가장 중요한 뉴스 5~8개를 ## 소제목으로 상세 분석 (각 뉴스 2~3문단)
2. 각 ## 소제목 바로 아래에 반드시 아래 형식으로 출처를 표기하세요:
   * 관련 출처: [기사제목](원문URL) — 출처명
   * 📰 N개 소스에서 보도: 출처명1, 출처명2 (동일 뉴스가 여러 소스에 있을 때)
3. 본문 안의 주요 사실에는 인라인 링크 [텍스트](URL)를 사용하세요.
4. 하단에 기타 단신 섹션 (## 📌 기타 단신 모아보기) — 각 단신에도 출처명과 링크 포함
5. 최하단에 ## 📚 참고자료 — 본문에 인용된 모든 원문의 [제목](URL) 목록

[금지사항]
- [1], [2], [3] 같은 숫자 인용 절대 금지
- (URL), (PDF) 같은 플레이스홀더 절대 금지
- 소스의 [원문 URL: ...] 태그에 있는 실제 URL을 사용하세요"""


def run_nlm_pipeline(skip_research: bool = False, deep_mode: bool = False):
    """NotebookLM 기반 데일리 다이제스트 파이프라인."""
    now_kst = datetime.now(timezone.utc) + timedelta(hours=9)
    date_str = now_kst.strftime("%Y-%m-%d")
    today_label = now_kst.strftime("%m월 %d일")

    print("=" * 60)
    print(f"📰 NLM 데일리 다이제스트 파이프라인 ({today_label})")
    print(f"   Gemini API 호출: 0회 | NotebookLM 100%")
    print("=" * 60)

    # ── Step 1: 데이터 수집 (API 불필요) ──
    print("\n" + "─" * 50)
    print("📡 [Step 1] RSS + Gmail 데이터 수집")
    print("─" * 50)

    rss_articles = collect_rss()
    gmail_groups = collect_gmail()

    rss_count = len(rss_articles)
    gmail_count = sum(len(v) for v in gmail_groups.values())
    print(f"\n   📊 수집 완료: RSS {rss_count}건, Gmail {gmail_count}건")

    if rss_count == 0 and gmail_count == 0 and skip_research:
        print("   ⚠️ 수집된 데이터가 없고 리서치도 건너뛰기 — 종료")
        return

    # ── Step 2: NLM 노트북 생성 ──
    print("\n" + "─" * 50)
    print("📓 [Step 2] NotebookLM 노트북 생성")
    print("─" * 50)

    notebook_title = f"AI Daily {date_str}"
    notebook_id = nlm_create_notebook(notebook_title)
    if not notebook_id:
        print("   ❌ 노트북 생성 실패 — 종료")
        return
    print(f"   ✅ 노트북 생성: {notebook_id}")

    try:
        # ── Step 3: 수집 데이터를 소스로 추가 ──
        print("\n" + "─" * 50)
        print("📎 [Step 3] 수집 데이터 → NLM 소스 추가")
        print("─" * 50)

        sources_added = 0

        if rss_articles:
            rss_md = format_rss_as_markdown(rss_articles)
            if nlm_add_text_source(notebook_id, rss_md, f"RSS 뉴스 ({rss_count}건)"):
                sources_added += 1
                print(f"   ✅ RSS 소스 추가 완료 ({rss_count}건, {len(rss_md):,}자)")

        if gmail_groups:
            gmail_md = format_gmail_as_markdown(gmail_groups)
            if nlm_add_text_source(notebook_id, gmail_md, f"Gmail 뉴스레터 ({gmail_count}건)"):
                sources_added += 1
                print(f"   ✅ Gmail 소스 추가 완료 ({gmail_count}건, {len(gmail_md):,}자)")

        # ── Step 4: 웹 리서치 (선택) ──
        if not skip_research:
            print("\n" + "─" * 50)
            mode_label = "딥" if deep_mode else "패스트"
            print(f"🔍 [Step 4] 웹 리서치 ({mode_label} 모드)")
            print("─" * 50)

            research_query = f"latest AI technology news {now_kst.strftime('%B %Y')} artificial intelligence breakthroughs"
            mode = "deep" if deep_mode else "fast"
            success = nlm_research(notebook_id, research_query, mode=mode)
            if success:
                print(f"   ✅ 웹 리서치 완료 (소스 자동 임포트)")
                sources_added += 1
            else:
                print(f"   ⚠️ 웹 리서치 실패 — 수집 데이터만으로 진행")
        else:
            print("\n   ⏭️ 웹 리서치 건너뛰기 (--skip-research)")

        if sources_added == 0:
            print("   ❌ 추가된 소스가 없습니다 — 종료")
            return

        # ── Step 5: 채팅 프롬프트 설정 ──
        print("\n" + "─" * 50)
        print("⚙️ [Step 5] NLM 채팅 설정")
        print("─" * 50)

        nlm_configure_chat(notebook_id, CHAT_PROMPT)
        print("   ✅ 커스텀 프롬프트 설정 완료")

        # 소스 처리 대기 (안정화)
        print("   ⏳ 소스 인덱싱 대기 (15초)...")
        time.sleep(15)

        # ── Step 6: 포스트 생성 쿼리 ──
        print("\n" + "─" * 50)
        print("✍️ [Step 6] 통합 포스트 생성 쿼리")
        print("─" * 50)

        response = nlm_query(notebook_id, QUERY_PROMPT, timeout=300)
        if not response:
            print("   ❌ NLM 쿼리 실패 — 종료")
            return

        print(f"   ✅ 응답 수신 ({len(response):,}자)")

        # ── Step 7: 파싱 & 저장 ──
        print("\n" + "─" * 50)
        print("💾 [Step 7] 포스트 파싱 & 저장")
        print("─" * 50)

        file_path = parse_and_save_post(response, date_str, now_kst)

        # ── Step 8: 처리 완료 마킹 ──
        for art in rss_articles:
            mark_processed("rss", art["id"])
        for sender, letters in gmail_groups.items():
            for letter in letters:
                mark_processed("gmail", letter["id"])
        print(f"   ✅ 상태 마킹 완료 (RSS {rss_count}건, Gmail {gmail_count}건)")

    finally:
        # ── 정리: 노트북 삭제 (선택) ──
        print("\n" + "─" * 50)
        print("🧹 [정리] 임시 노트북 삭제")
        print("─" * 50)
        nlm_delete_notebook(notebook_id)
        print(f"   ✅ 노트북 '{notebook_title}' 삭제 완료")

    print("\n" + "=" * 60)
    print(f"🎉 NLM 데일리 다이제스트 완료! (Gemini API: 0회)")
    print("=" * 60)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="NotebookLM 기반 AI 데일리 다이제스트")
    parser.add_argument("--skip-research", action="store_true", help="웹 리서치 생략 (수집 데이터만 사용)")
    parser.add_argument("--deep", action="store_true", help="딥 리서치 모드 (~5분, ~40개 소스)")
    args = parser.parse_args()

    run_nlm_pipeline(skip_research=args.skip_research, deep_mode=args.deep)
