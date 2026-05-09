import json
import re

# Read the generated markdown from output.txt
output_path = "/Users/wook/.gemini/antigravity/brain/f466cb15-70ed-4a12-aaca-0f4469c7dafd/.system_generated/steps/1196/output.txt"
with open(output_path, "r", encoding="utf-8") as f:
    data = json.load(f)
    
new_content = data.get("answer", "")
if new_content.startswith("```markdown"):
    new_content = new_content[11:].strip()
if new_content.endswith("```"):
    new_content = new_content[:-3].strip()

# Read the target markdown file
md_path = "content/posts/AI News/2026-05-08-ai-daily-anthropic-openai-eu-act.md"
with open(md_path, "r", encoding="utf-8") as f:
    text = f.read()

# Extract frontmatter
match = re.match(r"(---.*?---\n+)(.*)", text, re.DOTALL)
if match:
    frontmatter = match.group(1)
    
    # Prepend the intro block
    intro = "> 📊 오늘의 AI 트렌드: NotebookLM 딥 리서치 파이프라인을 통해 수집 및 심층 분석된 결과입니다.\n\n---\n\n"
    
    final_text = frontmatter + intro + new_content + "\n"
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(final_text)
    print("Successfully applied new formatting to the markdown file.")
else:
    print("Could not find frontmatter.")
