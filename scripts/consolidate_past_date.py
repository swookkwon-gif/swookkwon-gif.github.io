import os
import sys
import json
import time
import re
from google import genai
from google.genai import types

sys.path.insert(0, os.path.dirname(__file__))

# Setup environment
import dotenv
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.local'))

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

POSTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'content', 'posts', 'AI News')

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

def clean_json_response(text: str) -> str:
    text = text.strip()
    if text.startswith("```json"):
        text = text[len("```json"):].strip()
    if text.endswith("```"):
        text = text[:-len("```")].strip()
    return text

def call_llm(prompt: str) -> dict:
    for model_name in MODELS_TO_TRY:
        try:
            print(f"Calling {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    response_mime_type="application/json",
                    response_schema=DIGEST_SCHEMA
                )
            )
            raw_text = clean_json_response(response.text)
            return json.loads(raw_text)
        except Exception as e:
            print(f"Error with {model_name}: {e}")
            continue
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python consolidate_past_date.py YYYY-MM-DD")
        sys.exit(1)
    date_str = sys.argv[1]
    files = [f for f in os.listdir(POSTS_DIR) if f.startswith(date_str)]
    
    print(f"Found {len(files)} files for {date_str}: {files}")
    if not files:
        return

    content_dump = ""
    for file in files:
        path = os.path.join(POSTS_DIR, file)
        with open(path, 'r', encoding='utf-8') as f:
            content_dump += f"\n\n--- FILE: {file} ---\n{f.read()}"

    prompt = f"""
당신은 AI 데일리 다이제스트 수석 편집장입니다.
아래는 수집된 여러 AI 뉴스 기사들(마크다운 원본)입니다.
이를 하나의 통합 일간 뉴스 포스트(마크다운 본문)로 재구성하세요.

[원본 기사 내용들]
{content_dump}

[통합 규칙]
0. **URL 위생 규칙**: 원문 링크로 `substack.com/redirect/...`, `google.com/url?...`, `t.co/...` 등 리다이렉트/트래커 URL을 절대 사용하지 마세요. 반드시 최종 목적지 URL만 사용합니다.
0. **엄격한 팩트 준수**: 제공된 원본 데이터에 없는 외부 지식을 절대로 덧붙이거나 상상해서 지어내지 마세요.
1. **중복 뉴스 병합**: 같은 사건/발표를 다루는 기사들을 하나로 합침.
   - 병합 시 소스 이름을 "소스: A · B" 형태로 표기
2. **중요도 기반 선별**: 여러 기사 중 가장 중요한 메인 뉴스들을 선별하여 작성. 아이콘(이모지)을 절대 사용하지 마세요.
3. **메인 뉴스 포맷**:
   - 포스트 최상단에 전체 메인 제목(H1, `# 제목`)을 절대 쓰지 마세요.
   - 각 뉴스: `## 순번. 제목`
   - 본문 2-4문장 + 핵심 수치가 있으면 불릿으로 강조
   - 출처 표기:
     `<br><small style="color: #888;">소스: 소스명 &nbsp;|&nbsp; 🔗 [원문 보기](URL)</small>`
   - 각 기사 끝에는 빈 줄 + `---` 구분선 + 빈 줄
4. **post_title**: 날짜나 'AI 데일리 다이제스트' 등의 단어 없이, **가장 중요한 상위 3개 뉴스의 핵심 요약 제목**을 콤마(,)로 연결하여 작성하세요. (예: "오픈AI 새 모델 발표, 메타 라마3 오픈소스 공개, 애플 AI 전략")
5. **top_topics**: 상위 3개 토픽 키워드 배열
"""

    print("Generating integrated post...")
    data = call_llm(prompt)
    if not data:
        print("Failed to generate.")
        return

    result_md = data.get("markdown_content", "")
    post_title = data.get("post_title", "AI 데일리 다이제스트")

    title = f"[{date_str[-5:-3]}월 {date_str[-2:]}일] AI 데일리 다이제스트 — {post_title}"
    
    # Excerpt 생성
    clean_content = re.sub(r'<[^>]+>', '', result_md)
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
    filename = f"{date_str}-{slug}.md"
    file_path = os.path.join(POSTS_DIR, filename)

    print(f"Saving to {filename}...")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter + result_md + "\n\n")

    print("Deleting old files...")
    for file in files:
        if file != filename:
            os.remove(os.path.join(POSTS_DIR, file))
            print(f"Deleted {file}")

if __name__ == "__main__":
    main()
