import re

with open("content/posts/AI News/2026-05-08-ai-daily-anthropic-openai-eu-act.md", "r") as f:
    text = f.read()

# Fix the lack of newlines before '## ' and '---'
# Note that we only want to fix the main content, not the frontmatter.
parts = text.split("---", 2)
frontmatter = "---" + parts[1] + "---\n\n"
body = parts[2].strip()

# Now body starts with something like `> 📊 오늘의 AI 뉴스...`
# But body itself has `---## Anthropic` inside it. Wait, the split might have caught a different `---`!
