from google import genai
from google.genai import types

GEMINI_API_KEY = "YOUR_API_KEY_HERE"

def call_llm_with_retry(prompt, schema=None, label="LLM", use_search=False):
    \"\"\"
    과거 파이프라인에서 사용하던 Gemini의 Google Search Grounding 연동 코드 백업.
    use_search=True 일 경우 실시간 구글 검색을 통해 답변을 생성함.
    \"\"\"
    client = genai.Client(api_key=GEMINI_API_KEY)
    models_to_try = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash-latest']
    
    for attempt in range(3):
        for model_name in models_to_try:
            try:
                # 구글 검색 도구 활성화 부분
                tools = [types.Tool(google_search=types.GoogleSearch())] if use_search else None
                config = types.GenerateContentConfig(temperature=0.3)
                
                if schema:
                    config.response_mime_type = "application/json"
                    config.response_schema = schema
                if tools:
                    config.tools = tools

                print(f"[{label}] {model_name} 호출 중... (시도 {attempt+1}/3)")
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=config
                )
                return response.text
            except Exception as e:
                print(f"[{label}] {model_name} 실패 (시도 {attempt+1}/3): {e}")
                
    return None
