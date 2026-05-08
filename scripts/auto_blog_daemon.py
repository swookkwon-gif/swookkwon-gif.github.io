#!/usr/bin/env python3
import os
import re
import time
import json
import base64
import feedparser
import subprocess
from datetime import datetime, timezone, timedelta
from google import genai
from google.genai import types
from googleapiclient.discovery import build
from dotenv import load_dotenv
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

from state_manager import is_processed, mark_processed, save_evaluations
from auth import authenticate_gmail

load_dotenv(".env.local")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("⚠️ GEMINI_API_KEY is missing.")
    import sys; sys.exit(1)

POSTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'content', 'posts', 'AI News')
CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'config')
if not os.path.exists(POSTS_DIR): os.makedirs(POSTS_DIR)

TARGET_LABEL_NAME = "AI News"

# =============== UTILS ===============

def clean_url(url):
    try:
        if '?amp' in url: url = url.split('?amp')[0]
        elif '&amp' in url: url = url.split('&amp')[0]
        parsed = urlparse(url)
        query_params = parse_qsl(parsed.query, keep_blank_values=True)
        cleaned_params = [(k, v) for k, v in query_params if not k.lower().startswith('utm_') and not k.lower().startswith('amp')]
        return urlunparse(parsed._replace(query=urlencode(cleaned_params)))
    except Exception:
        return url

def clean_json_response(text):
    text = text.strip()
    if text.startswith("```json"): text = text[len("```json"):].strip()
    if text.endswith("```"): text = text[:-len("```")].strip()
    return text

def load_config():
    feeds_path = os.path.join(CONFIG_DIR, 'feeds.json')
    excl_path = os.path.join(CONFIG_DIR, 'exclusion_rules.json')
    feeds = []
    excl = {}
    if os.path.exists(feeds_path):
        with open(feeds_path, 'r', encoding='utf-8') as f:
            feeds = json.load(f)
    if os.path.exists(excl_path):
        with open(excl_path, 'r', encoding='utf-8') as f:
            excl = json.load(f)
    return feeds, excl

def create_markdown_post_file(filename_slug, post_title, content, category="AI News"):
    now_kst = datetime.now(timezone.utc) + timedelta(hours=9)
    date_str = now_kst.strftime("%Y-%m-%d")
    
    clean_content = re.sub(r'<[^>]+>', '', content)
    clean_content = re.sub(r'https?://[^\s]+', '', clean_content)
    clean_content = re.sub(r'[#*`\[\]\(\)]', '', clean_content)
    clean_content = re.sub(r'\s+', ' ', clean_content).strip()
    excerpt_text = clean_content[:120] + "..." if len(clean_content) > 120 else clean_content
    excerpt_text = excerpt_text.replace('"', "'").replace('\n', ' ')
    
    frontmatter = f"---\ntitle: '{post_title.replace(chr(39), chr(39)*2)}'\ndate: '{date_str}'\nexcerpt: '{excerpt_text.replace(chr(39), chr(39)*2)}'\ncategory: '{category}'\n---\n\n"
    filename = f"{date_str}-{filename_slug}.md"
    file_path = os.path.join(POSTS_DIR, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(frontmatter + content + "\n\n")

# =============== LLM CALLER ===============

def call_llm_with_retry(prompt, schema=None, label="LLM"):
    client = genai.Client(api_key=GEMINI_API_KEY)
    models_to_try = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash-latest']
    
    for attempt in range(3):
        for model_name in models_to_try:
            try:
                config = types.GenerateContentConfig(temperature=0.3)
                if schema:
                    config.response_mime_type = "application/json"
                    config.response_schema = schema
                    
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=config
                )
                if schema:
                    raw_text = clean_json_response(response.text)
                    return json.loads(raw_text)
                return response.text
            except Exception as e:
                err_msg = str(e)
                if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                    continue
                elif isinstance(e, json.JSONDecodeError):
                    print(f"      ❌ [{label}] JSON 에러. 재시도...")
                    time.sleep(10)
                    break
        print(f"      ⏳ [{label}] 대기 중... ({attempt+1}/3)")
        time.sleep(30)
    return None

EXTRACT_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "url": {"type": "string"},
            "summary": {"type": "string"}
        },
        "required": ["title", "url", "summary"]
    }
}

# =============== PHASE 1: COLLECTION ===============

def collect_rss_articles():
    feeds, exclusion_rules = load_config()
    all_rss_items = []
    
    for feed in feeds:
        print(f"\n🔍 [RSS] {feed['name']} 수집 중...")
        parsed = feedparser.parse(feed['url'])
        now = datetime.now(timezone.utc)
        
        feed_rules = exclusion_rules.get(feed['name'], {})
        global_rules = exclusion_rules.get('global', {})
        title_excludes = feed_rules.get('title_exclude', []) + global_rules.get('title_exclude', [])
        
        items_to_process = []
        for entry in parsed.entries:
            try:
                url_id = clean_url(entry.get('link', entry.get('id', '')))
                if not url_id or is_processed("rss", url_id): continue
                    
                dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc) if 'published_parsed' in entry and entry.published_parsed else now
                if (now - dt).days > 2: continue
                
                title = entry.get('title', 'No Title')
                if any(excl in title for excl in title_excludes): continue
                
                content = entry.get('content', [{'value': ''}])[0]['value'] if 'content' in entry else entry.get('summary', '')
                
                keywords = feed.get('keywords', [])
                if keywords:
                    combined_text = (title + " " + content).lower()
                    if not any(k.lower() in combined_text for k in keywords): continue
                
                items_to_process.append({"title": title, "url": url_id, "content": content[:3000]})
            except Exception: pass
            
        if not items_to_process:
            print(" └ 새 기사 없음.")
            continue
            
        # Chunking for LLM
        for i in range(0, len(items_to_process), 20):
            chunk = items_to_process[i:i+20]
            articles_text = ""
            for idx, item in enumerate(chunk):
                articles_text += f"\n[Article {idx}]\nTitle: {item['title']}\nURL: {item['url']}\nContent: {item['content'][:500]}\n"
                
            prompt = f"다음은 {feed['name']}의 RSS 기사들입니다. AI, 머신러닝, LLM 산업과 무관한 쓰레기 기사를 버리고 진짜 AI 뉴스만 추출하세요.\n{articles_text}"
            data = call_llm_with_retry(prompt, EXTRACT_SCHEMA, label=f"RSS-{feed['name']}")
            
            if data:
                for art in data:
                    all_rss_items.append({
                        "title": art["title"], "url": art["url"], "summary": art["summary"], 
                        "source_name": feed['name'], "content_raw": next((c["content"] for c in chunk if c["url"] == art["url"]), art["summary"])
                    })
            for item in chunk:
                mark_processed("rss", item["url"])
                
        print(f" └ {feed['name']}: {len(items_to_process)}개 중 {len(all_rss_items)}개 유효 기사 추출")
        
    return all_rss_items


def get_email_body(payload):
    text_content = ""
    def extract_text(part):
        nonlocal text_content
        mime_type = part.get('mimeType', '')
        if mime_type == 'text/plain':
            data = part.get('body', {}).get('data', '')
            if data: text_content += base64.urlsafe_b64decode(data).decode('utf-8', 'ignore') + "\n"
        elif mime_type == 'text/html':
            data = part.get('body', {}).get('data', '')
            if data:
                html_code = base64.urlsafe_b64decode(data).decode('utf-8', 'ignore')
                def _remove_utm_from_a(match): return f"{match.group(2)} (URL: {clean_url(match.group(1))})"
                html_code = re.sub(r'<a\s+[^>]*href=["\'](https?://[^"\']+)["\'][^>]*>(.*?)</a>', _remove_utm_from_a, html_code, flags=re.IGNORECASE|re.DOTALL)
                clean_text = re.sub(r'<[^>]+>', ' ', html_code)
                text_content += re.sub(r'\s+', ' ', clean_text).strip() + "\n"
        elif 'parts' in part:
            for subpart in part['parts']: extract_text(subpart)
    
    extract_text(payload)
    if not text_content:
        data = payload.get('body', {}).get('data', '')
        if data: text_content = base64.urlsafe_b64decode(data).decode('utf-8', 'ignore')
    return text_content[:10000]

def collect_gmail_articles():
    print("\n🔍 [Gmail] 뉴스레터 수집 중...")
    creds = authenticate_gmail(account="mail1")
    if not creds: return []
    service = build('gmail', 'v1', credentials=creds)
    res = service.users().labels().list(userId='me').execute()
    label_id = next((l['id'] for l in res.get('labels', []) if TARGET_LABEL_NAME.lower() in l['name'].lower()), None)
    if not label_id: return []
    
    last_week = datetime.now() - timedelta(days=7)
    results = service.users().messages().list(userId='me', q=f'after:{last_week.strftime("%Y/%m/%d")}', labelIds=[label_id], maxResults=50).execute()
    
    emails_by_sender = {}
    for msg in results.get('messages', []):
        msg_id = msg['id']
        if not is_processed("gmail", msg_id):
            full_msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
            headers = full_msg['payload'].get('headers', [])
            subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), "No Subject")
            sender_full = next((h['value'] for h in headers if h['name'].lower() == 'from'), "Unknown")
            sender = re.match(r'(.*?)\s*<.*?>', sender_full)
            sender = sender.group(1).strip().replace('"', '') if sender else sender_full
            body = get_email_body(full_msg['payload'])
            
            emails_by_sender.setdefault(sender, []).append({"id": msg_id, "subject": subject, "body": body})
            
    all_gmail_items = []
    for sender, letters in emails_by_sender.items():
        print(f" └ {sender} 메일 {len(letters)}개 파싱 중...")
        for letter in letters:
            prompt = f"다음 뉴스레터 본문에서 개별 AI 뉴스 기사를 모두 추출하세요. 광고나 쓸데없는 말은 무시하세요.\n[제목: {letter['subject']}]\n{letter['body']}"
            data = call_llm_with_retry(prompt, EXTRACT_SCHEMA, label=f"Gmail-{sender}")
            if data:
                for art in data:
                    all_gmail_items.append({
                        "title": art["title"], "url": art["url"], "summary": art["summary"], 
                        "source_name": sender, "content_raw": art["summary"]
                    })
            mark_processed("gmail", letter["id"])
            time.sleep(3)
            
    return all_gmail_items

def run_nlm(cmd_args):
    print(f" └ 실행: {' '.join(cmd_args)}")
    result = subprocess.run(cmd_args, capture_output=True, text=True)
    if result.returncode != 0:
        print(f" ❌ NLM 오류: {result.stderr}")
    return result.stdout

def merge_and_create_daily_digest(all_articles):
    if not all_articles:
        print("\n⚠️ 수집된 기사가 없습니다.")
        return
        
    print(f"\n🧠 [NotebookLM Phase] {len(all_articles)}개 기사 처리 및 노트북 생성 중...")
    
    now_kst = datetime.now(timezone.utc) + timedelta(hours=9)
    date_str = now_kst.strftime("%Y%m%d")
    
    sources_text = f"오늘({now_kst.strftime('%Y년 %m월 %d일')}) 수집된 AI 뉴스(RSS 및 이메일 뉴스레터) 기초 데이터입니다:\n\n"
    for idx, art in enumerate(all_articles):
        sources_text += f"[기사 {idx+1}]\n제목: {art['title']}\n출처: {art['source_name']}\nURL: {art['url']}\n요약: {art['summary']}\n\n"
        
    sources_file = os.path.join(POSTS_DIR, f"temp_sources_{date_str}.txt")
    with open(sources_file, "w", encoding="utf-8") as f:
        f.write(sources_text)
        
    nb_name = f"DailyNews_Archive_{date_str}"
    out = run_nlm(["nlm", "notebook", "create", nb_name])
    
    import re
    match = re.search(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', out)
    if not match:
        print("❌ 노트북 생성 실패")
        return
    nb_id = match.group(0)
    print(f" └ 생성된 노트북 ID: {nb_id}")
    
    run_nlm(["nlm", "source", "add", nb_id, "--file", sources_file, "--wait"])
    
    print(" └ 딥 리서치(Deep Research) 가동 중... (수 분 소요될 수 있습니다)")
    run_nlm(["nlm", "research", "start", "오늘 전 세계에서 가장 파급력이 큰 AI 산업 및 오픈소스 기술 동향 뉴스", "--mode", "fast", "--notebook-id", nb_id, "--auto-import"])
    
    print("\n✍️ [NotebookLM Phase] 요약본(포스트) 생성 중...")
    query_prompt = """당신은 최고 수준의 AI 뉴스 에디터입니다.
현재 이 노트북에 수집된 모든 소스(RSS/뉴스레터 기초 자료 + 딥 리서치 웹 자료)를 바탕으로, 오늘 가장 중요한 AI 뉴스 주제 Top 10을 클러스터링하고 블로그 포스트를 마크다운 형식으로 작성하세요.

[통합 규칙]
0. **엄격한 팩트 준수**: 노트북 소스에 없는 외부 지식을 덧붙이지 마세요.
1. **중복 뉴스 병합**: 같은 사건/발표를 다루는 기사들을 하나로 합치고 가장 상세한 내용을 기준으로 작성.
2. **중요도 기반 Top 10 선별**: 가장 중요한 상위 10개 기사만(Top 10) 메인 뉴스로 작성하세요. 이모지는 금지입니다.
3. **메인 뉴스(Top 10) 포맷**:
   - `## 1. 메타 로봇 스타트업 인수` (이런 형식으로 제목 작성)
   - 본문 2-4문장 + 핵심 수치 불릿 강조
   - 뉴스 하단 출처 표기 (본문 직후 줄 띄움 없이 `<br>` 사용):
     `<br><small style="color: #888;">소스: 7min.ai · AITimes &nbsp;|&nbsp; 🔗 [원문 보기](URL) · [원문 2](URL)</small>`
   - 각 기사가 끝난 후 빈 줄 추가, `---` 구분선, 빈 줄 추가.
4. **기타 뉴스 (소스별 그룹핑)**:
   - Top 10에 들어가지 못한 기사들은 하단의 `## 📌 기타 뉴스 모아보기` 섹션에 통합하세요.
   - 소스 기준으로 그룹화하여 아래 포맷으로 작성하세요. 소스 홈페이지 링크는 걸지 마세요.
     ### 🔹 소스: 소스 이름
     * **[기사 제목 1](해당 기사 URL)**: 요약 한 줄 (URL이 없는 기사는 제외하지 말고 링크 없이 텍스트로 기재할 것)
5. 출력은 순수 마크다운 포맷(백틱 ``` 없이)으로만 출력하세요."""

    query_out = run_nlm(["nlm", "query", "notebook", nb_id, query_prompt, "--json"])
    try:
        data = json.loads(query_out)
        if "error" in data or "answer" not in data:
            print(f" ❌ NotebookLM API 오류: {data}")
            return
            
        post_content = data.get("answer", "").strip()
        if not post_content:
            print(" ❌ 생성된 포스트 내용이 비어 있습니다.")
            return
            
        if post_content.startswith("```markdown"):
            post_content = post_content[len("```markdown"):].strip()
        if post_content.endswith("```"):
            post_content = post_content[:-3].strip()
    except Exception as e:
        print(f" ❌ NotebookLM Query 파싱 실패: {e}")
        return

    title_prompt = "방금 작성된 마크다운 내용에서 다루는 주요 주제 3가지를 콤마로 이어 매력적인 메인 제목을 만들어주세요. (예: 메타 새 모델 공개, 오픈AI 펀딩 확보). 출력은 백틱 없이 순수 텍스트 한 줄만 하세요."
    title_res = run_nlm(["nlm", "query", "notebook", nb_id, title_prompt, "--json"])
    try:
        post_title = json.loads(title_res).get("answer", "최신 AI 주요 동향").strip()
    except:
        post_title = "최신 AI 주요 동향"
        
    slug_prompt = "방금 작성된 마크다운 내용의 가장 핵심적인 주제를 나타내는 영문 단어 3~4개를 하이픈(-)으로 연결하여 출력하세요. (예: openai-ms-contract, pentagon-ai-contract). 영문 소문자와 하이픈만 사용해야 합니다."
    slug_res = run_nlm(["nlm", "query", "notebook", nb_id, slug_prompt, "--json"])
    try:
        topic_slug = json.loads(slug_res).get("answer", "news").strip().lower()
        topic_slug = __import__('re').sub(r'[^a-z0-9\-]', '', topic_slug)
        if topic_slug.startswith("ai-daily-"):
            topic_slug = topic_slug[len("ai-daily-"):]
        slug = f"ai-daily-{topic_slug}"
    except:
        slug = "ai-daily-news"
    title = f"[{now_kst.strftime('%m월 %d일')}] AI 데일리 다이제스트 — {post_title}"
    
    post_content = f"> 📊 오늘의 AI 트렌드: NotebookLM 딥 리서치 파이프라인을 통해 수집 및 심층 분석된 결과입니다.\n\n---\n\n{post_content}"
    
    create_markdown_post_file(slug, title, post_content, category="AI News")
    print(f"✅ 통합 다이제스트 포스트 완료: {title}")
    
    if os.path.exists(sources_file):
        os.remove(sources_file)

if __name__ == "__main__":
    print("=======================================================")
    print("🚀 [Auto Daemon v3.5] NotebookLM Deep Research 기반 AI 파이프라인")
    print("=======================================================")
    
    all_articles = []
    
    all_articles.extend(collect_rss_articles())
    all_articles.extend(collect_gmail_articles())
    
    merge_and_create_daily_digest(all_articles)
    
    print("\n=======================================================")
    print("🎉 자동 파싱 작업이 성공적으로 종료되었습니다.")
    print("=======================================================")
