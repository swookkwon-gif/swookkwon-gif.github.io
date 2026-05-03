import os
import sys
import re
import json
import time
from datetime import datetime, timezone, timedelta
from google import genai
from google.genai import types
from dotenv import load_dotenv
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.local'))

POSTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'content', 'posts', '2. AI News')
STATE_FILE = os.path.join(os.path.dirname(__file__), 'state.json')

# ============ Utilities ============

def clean_url(url):
    """URL에서 utm_ 파라미터를 제거하고, ?amp 이후를 통째로 삭제한다."""
    try:
        if '?amp' in url:
            url = url.split('?amp')[0]
        elif '&amp' in url:
            url = url.split('&amp')[0]
        parsed = urlparse(url)
        query_params = parse_qsl(parsed.query, keep_blank_values=True)
        cleaned_params = [(k, v) for k, v in query_params if not k.lower().startswith('utm_') and not k.lower().startswith('amp')]
        cleaned_query = urlencode(cleaned_params)
        return urlunparse(parsed._replace(query=cleaned_query))
    except Exception:
        return url

def clean_all_urls_in_text(text):
    """마크다운 텍스트 내 모든 URL에서 utm 파라미터를 제거한다."""
    def _replace(match):
        return match.group(0).replace(match.group(1), clean_url(match.group(1)))
    return re.sub(r'\]\((https?://[^\)]+)\)', _replace, text)


def load_recent_covered_news(days=2):
    covered_news = []
    if not os.path.exists(STATE_FILE):
        return covered_news
    
    now_kst = datetime.now(timezone.utc) + timedelta(hours=9)
    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)
            
        evals = state.get("evaluations", {})
        for source, evals_list in evals.items():
            for ev in evals_list:
                ev_date_str = ev.get("date", "")
                if not ev_date_str: continue
                try:
                    ev_date = datetime.strptime(ev_date_str, "%Y-%m-%d").date()
                    if (now_kst.date() - ev_date).days <= days:
                        covered_news.append(ev.get("target", ""))
                except Exception:
                    pass
    except Exception as e:
        print(f"상태 파일 로드 중 오류: {e}")
        
    return list(set([news for news in covered_news if news]))

# ============ Main Pipeline ============

MODELS_TO_TRY = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash']

def call_gemini_streaming(client, prompt):
    """SDK 스트리밍 방식으로 Gemini를 호출한다. 타임아웃 문제를 근본적으로 해결."""
    for attempt in range(3):
        for model_name in MODELS_TO_TRY:
            try:
                print(f"      [{attempt+1}/3] '{model_name}' 스트리밍 호출 중...")
                response_text = ""
                for chunk in client.models.generate_content_stream(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.4,
                        tools=[types.Tool(google_search=types.GoogleSearch())],
                    ),
                ):
                    if chunk.text:
                        response_text += chunk.text
                
                if response_text:
                    print(f"      ✅ '{model_name}' 응답 완료 ({len(response_text):,}자)")
                    return response_text
                else:
                    print(f"      ⚠️ '{model_name}' 빈 응답. 다른 모델 시도...")
                    continue
                    
            except Exception as e:
                err_msg = str(e)
                if any(x in err_msg for x in ["429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE"]):
                    print(f"      ⚠️ '{model_name}' 할당량 초과/서버 에러. 다른 모델 시도...")
                    continue
                elif "timeout" in err_msg.lower() or "timed out" in err_msg.lower():
                    print(f"      ⚠️ '{model_name}' 타임아웃. 다른 모델 시도...")
                    continue
                else:
                    print(f"      ❌ '{model_name}' 예상 외 에러: {e}")
                    continue
        
        print(f"      [대기] 모든 모델 실패. 30초 후 재시도... ({attempt+1}/3)")
        time.sleep(30)
    
    return None


def run_gemini_search_blogger():
    print(f"==================================================")
    print(f"🚀 [Gemini 2.5 Auto Blogger] 자동 생성 파이프라인 시작")
    print(f"==================================================")
    
    # 1. 최근에 다룬 뉴스 리스트업 (중복 방지 메모리)
    recent_news = load_recent_covered_news(days=2)
    negative_prompt = ""
    if recent_news:
        recent_news = recent_news[:30] # Limit to 30 items to prevent prompt explosion
        print(f"✅ 최근 다룬 뉴스 {len(recent_news)}건 확인 완료 (중복 방지 적용)")
        negative_prompt = "\n\n[중복 방지 지침]\n아래 나열된 뉴스 기사/주제는 어제와 오늘 이미 다른 뉴스레터나 피드에서 다루었으므로, 이번 리서치에서 **절대 중복으로 포함하지 마세요**:\n"
        for idx, news in enumerate(recent_news, 1):
            negative_prompt += f"{idx}. {news}\n"
            
    # 2. 프롬프트 세팅
    now_kst = datetime.now(timezone.utc) + timedelta(hours=9)
    prompt = f"""
당신은 최고 수준의 테크 저널리스트이자 AI 트렌드 애널리스트입니다.
오늘({now_kst.strftime('%Y년 %m월 %d일')}) 기준으로 지난 24~48시간 동안 발생한 전 세계 AI 기술 및 산업 뉴스 중, 가장 파급력이 크고 중요한 10가지 뉴스를 구글 검색 기능을 활용하여 심층 리서치하세요.
주요 소스로 Hacker News, TechCrunch, The Verge, OpenAI/Anthropic/Google 공식 블로그 등을 참조하세요.
{negative_prompt}

리서치한 결과를 바탕으로 아래 가이드라인을 엄격히 준수하여 아주 상세한 기술 블로그 포스트를 한국어로 작성해 주세요.

[작성 가이드라인]
1. 메타 데이터 생성 (반드시 첫 두 줄에 작성):
   - 첫 번째 줄은 "TITLE: [제목]" 형식으로 작성하되, 대괄호 `[]`는 빼고 제목 텍스트만 적어. 제목은 가장 중요한 Top 3 뉴스의 핵심 팩트(키워드)만 콤마로 나열해 (예: TITLE: 구글 앤스로픽 400억 달러 투자, MS-오픈AI 계약 변경, 메타 AWS CPU 대규모 도입). '시사하는 바' 같은 주관적 문구는 절대 넣지 마.
   - 두 번째 줄은 "EXCERPT: [요약문]" 형식으로 전체 포스트를 2~3문장(약 100~150자)으로 요약한 프리뷰 텍스트를 적어.
2. 본문 서식: 가독성을 높이기 위해 텍스트 단락 구분을 명확히 하고, 적절한 줄바꿈을 사용할 것.
3. Top 3 심층 분석:
   - 10개의 뉴스 중 가장 중요한 3개의 뉴스를 각각 큰 소제목(##)으로 구분해.
   - 각 뉴스별로 소식의 핵심을 요약하고(2~3줄), 이어서 기술적 및 산업적 시사점을 깊이 있게 분석하여 줄글로 자연스럽게 작성해. (단, '[소식 요약]', '[시사점]' 같은 영역별 제목이나 괄호 표기는 절대 사용하지 말고 자연스러운 문단으로 구성할 것)
4. Top 10 주요 뉴스 및 중요도 평가 테이블 (반드시 마크다운 표 형식 사용):
   - 포스트 하단에 추출된 10개의 뉴스를 나열하는 마크다운 테이블(표)을 생성해. (컬럼: 순위, 기사 제목, 중요도 점수, 선정 사유)
   - 이 중 앞서 다룬 3가지가 왜 Top 3로 선정되었는지, 그리고 나머지 기사들은 왜 순위가 밀렸는지 '선정 사유'에 매우 구체적인 논거를 들어 기술해. (단순히 '중요하다'가 아니라, 예를 들어 '6천억 달러 규모의 펀딩 지연이 국방부의 일상적인 AI 도입 뉴스보다 산업적 파급력이 훨씬 크기 때문'과 같이 구체적인 비교 우위와 자본/기술적 파급력을 기준으로 중요도를 평가할 것). 텍스트가 깨지지 않도록 표 내부의 줄바꿈은 `<br>` 태그를 사용해.
5. **엄격한 팩트 준수**: 절대 배경 지식이나 상상으로 사실을 만들어내지 마세요. 오직 검색 결과에서 확인된 사실과 수치만 기재하세요.
6. 레퍼런스 및 주석:
   - 본문 내에서 참고한 기사를 인용할 때는 마크다운 표준 주석 문법인 `[^1]` 형태를 사용하여 클릭 시 하단으로 스크롤 되도록 작성해.
   - 포스트 가장 하단에는 본문에 사용된 주석 번호 1번부터 순서대로 정렬하여 `[^1]: [기사 제목](URL)` 형태의 목록으로 명확하게 제공해.
   - 만약 기사의 정확한 원본 URL을 찾을 수 없다면 억지로 생성하지 말고 `[^1]: 기사 제목` 형태로 링크 없이 표기해.
7. 어조: 해요체/하십시오체를 쓰지 말고 전문적인 테크 저널 목록형 어조(~이다, ~한다)를 사용할 것.
"""
    
    # 3. Gemini SDK 스트리밍 호출 (타임아웃 방지)
    print(f"\n[Step 2] Gemini + Google Search Grounding 스트리밍 호출 중...")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")
        return
    api_key = api_key.strip().strip('"').strip("'")
    
    client = genai.Client(api_key=api_key)
    article_content = call_gemini_streaming(client, prompt)
    
    if not article_content:
        print("❌ 모든 재시도 실패. 포스트 생성을 중단합니다.")
        return
        
    # 4. URL 정리 (utm 파라미터 제거)
    article_content = clean_all_urls_in_text(article_content)
    
    # 5. 마크다운 파일 저장
    print(f"\n[Step 3] 블로그 업로드용 파일 저장")
    slug_name = "daily-ai-top3-news"
    file_name = f"{now_kst.strftime('%Y-%m-%d')}-{slug_name}.md"
    file_path = os.path.join(POSTS_DIR, file_name)
    
    os.makedirs(POSTS_DIR, exist_ok=True)
    
    display_title = f"Daily Top 3: {now_kst.strftime('%m월 %d일')} 주요 AI 뉴스"
    display_excerpt = "오늘의 핵심 글로벌 AI 및 기술 뉴스 동향을 요약합니다."
    
    lines = article_content.split('\n')
    content_start_idx = 0
    
    for i in range(min(10, len(lines))):
        line = lines[i].strip()
        if line.startswith("TITLE:"):
            display_title = line.replace("TITLE:", "").replace("[", "").replace("]", "").strip()
            content_start_idx = max(content_start_idx, i + 1)
        elif line.startswith("EXCERPT:"):
            display_excerpt = line.replace("EXCERPT:", "").replace("[", "").replace("]", "").strip()
            content_start_idx = max(content_start_idx, i + 1)
            
    clean_article = '\n'.join(lines[content_start_idx:]).strip()

    frontmatter = f"""---
title: '{display_title.replace("'", "''")}'
date: {now_kst.strftime('%Y-%m-%dT%H:%M:%S+09:00')}
excerpt: '{display_excerpt.replace("'", "''")}'
categories:
  - AI News
tags:
  - Deep Research
  - Google Search Grounding
  - Daily Top 3
---

"""
    final_content = frontmatter + clean_article
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
        
    print(f"🎉 성공적으로 Gemini 무인 블로그 포스트가 생성되었습니다!")
    print(f"📁 위치: {file_path}")

if __name__ == "__main__":
    run_gemini_search_blogger()
