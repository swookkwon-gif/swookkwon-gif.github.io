import os
import re
from datetime import datetime
from google import genai
from google.genai import types

def main():
    # 1. 이슈 내용 읽기
    try:
        with open('issue_title.txt', 'r', encoding='utf-8') as f:
            issue_title = f.read().strip()
        with open('issue_body.txt', 'r', encoding='utf-8') as f:
            issue_body = f.read().strip()
    except FileNotFoundError:
        print("Issue content files not found.")
        return

    if not issue_body:
        print("Issue body is empty. Nothing to do.")
        return

    # 2. Gemini API 호출 준비
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY is missing.")
        return

    client = genai.Client(api_key=api_key)

    prompt = f"""
다음은 사용자가 NotebookLM을 통해 작성한 딥리서치 초안 텍스트입니다.
이 텍스트를 바탕으로 아주 깔끔하고 전문적인 마크다운 형식의 블로그 포스트를 작성해 주세요.

[요구사항]
1. 반드시 Jekyll/Hugo 호환 Frontmatter를 최상단에 포함할 것.
   - title: "{issue_title}" (이슈 제목을 참고하되 더 매력적으로 변경 가능, 딥리서치 태그 제거)
   - date: YYYY-MM-DD HH:MM:SS (현재 시간으로 포맷팅)
   - categories: "Marketing" 또는 "Data" 중 내용에 가장 잘 맞는 것 하나 선택 (배열 형태)
   - tags: 내용에 맞는 핵심 키워드 3~5개 추출 (배열 형태)
2. 내용은 수정/삭제하지 말고, 원본 텍스트의 인사이트를 모두 살려서 구조만 예쁘게 다듬을 것.
3. 소제목, 인용구(>), 볼드체, 리스트 등을 적극적으로 활용하여 가독성을 극대화할 것.
4. "참고자료" 섹션이 있다면 마크다운 하단에 정리해 줄 것.
5. 응답은 마크다운(Frontmatter 포함) 코드블록(```markdown ... ```)으로만 출력할 것.

[원본 딥리서치 텍스트]
{issue_body}
"""

    print("Generating blog post via Gemini API...")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.7,
        )
    )

    result_text = response.text

    # 3. Markdown 추출
    match = re.search(r'```(?:markdown)?\s*(.*?)\s*```', result_text, re.DOTALL)
    if match:
        markdown_content = match.group(1).strip()
    else:
        markdown_content = result_text.strip()

    # 카테고리 판별하여 폴더 지정
    folder_name = "Marketing"
    if "categories: [\"Data\"]" in markdown_content or "categories: ['Data']" in markdown_content or "categories:\n  - Data" in markdown_content:
        folder_name = "Data"

    # 4. 파일 저장 (현재 시간 기준 파일명)
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    
    # 영문 슬러그 생성 (간단히)
    safe_title = re.sub(r'[^a-zA-Z0-9가-힣]+', '-', issue_title.lower()).strip('-')
    keywords_to_remove = ["blog", "post", "포스트", "포스팅", "블로그"]
    for kw in keywords_to_remove:
        safe_title = safe_title.replace(kw, "")
    safe_title = re.sub(r'-+', '-', safe_title).strip('-')

    if not safe_title:
        safe_title = "ai-generated-post"
        
    filename = f"{date_str}-{safe_title}.md"
    filepath = f"content/posts/{folder_name}/{filename}"

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
        
    print(f"Successfully created blog post at {filepath}")

if __name__ == "__main__":
    main()
