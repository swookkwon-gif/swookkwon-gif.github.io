import re

file_path = "content/posts/AI News/2026-05-08-ai-daily-anthropic-openai-eu-act.md"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Separate frontmatter and body
match = re.match(r"(---.*?---\n+)(.*)", text, re.DOTALL)
if match:
    frontmatter = match.group(1)
    body = match.group(2)
    
    # Fix missing newlines before '---'
    body = re.sub(r'(?<!\n)---', r'\n\n---\n\n', body)
    # Fix missing newlines before '##'
    body = re.sub(r'(?<!\n)## ', r'\n\n## ', body)
    # Fix missing newlines before '###'
    body = re.sub(r'(?<!\n)### ', r'\n\n### ', body)
    # Fix missing newlines before '* '
    body = re.sub(r'(?<!\n)\* \*\*', r'\n* **', body)
    # Clean up excessive newlines
    body = re.sub(r'\n{3,}', r'\n\n', body)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(frontmatter + body)
    print("Fixed markdown formatting.")
else:
    print("Could not find frontmatter.")
