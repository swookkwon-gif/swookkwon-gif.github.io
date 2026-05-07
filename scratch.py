import json
import subprocess
from datetime import datetime, timezone, timedelta
import os

nb_id = "aa8651b2-c13b-445f-b134-4b1ae99ca212"
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
   - 소스 기준으로 그룹화하여 아래 포맷으로 작성하세요.
     ### 🔹 소스: [소스 이름](해당 소스 URL)
     * **기사 제목 1**: 요약 한 줄
5. 출력은 순수 마크다운 포맷(백틱 ``` 없이)으로만 출력하세요."""

print("Querying NotebookLM...")
res = subprocess.run(["nlm", "query", "notebook", nb_id, query_prompt, "--json"], capture_output=True, text=True)
try:
    data = json.loads(res.stdout)
    post_content = data.get("answer", "").strip()
    if post_content.startswith("```markdown"):
        post_content = post_content[len("```markdown"):].strip()
    if post_content.endswith("```"):
        post_content = post_content[:-3].strip()
    
    with open("temp_post.md", "w") as f:
        f.write(post_content)
    print("Saved to temp_post.md")
except Exception as e:
    print("Error:", e, res.stdout)
