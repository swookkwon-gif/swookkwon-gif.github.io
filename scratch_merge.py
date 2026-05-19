import os, glob, re
from datetime import datetime

def parse_md(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fm_match = re.search(r'^---\s*(.*?)\s*^---', content, re.MULTILINE | re.DOTALL)
    if not fm_match: return {}, content
    
    fm_str = fm_match.group(1)
    body = content[fm_match.end():].strip()
    
    metadata = {}
    for line in fm_str.split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            metadata[k.strip()] = v.strip().strip('"').strip("'")
            
    return metadata, body

def merge_files(files, target_filename, new_title, category, date, author):
    merged_body = ""
    tags = set()
    
    for f in files:
        meta, body = parse_md(f)
        if 'tags' in meta:
            t_str = meta['tags'].strip('[]')
            tags.update([t.strip().strip('"').strip("'") for t in t_str.split(',') if t.strip()])
        
        # Add original title as heading if not the first file or always
        orig_title = meta.get('title', 'Section')
        merged_body += f"\n\n## {orig_title}\n\n{body}"
        
    tag_str = "[" + ", ".join([f'"{t}"' for t in tags]) + "]"
    
    frontmatter = f"""---
title: "{new_title}"
date: {date}
category: "{category}"
author: "{author}"
tags: {tag_str}
---
"""
    
    with open(target_filename, 'w', encoding='utf-8') as f:
        f.write(frontmatter + merged_body)
        
    for f in files:
        os.system(f'git rm "{f}"')
        
    os.system(f'git add "{target_filename}"')
    print(f"Merged {len(files)} files into {target_filename}")

# 1. Claude Mythos
f1 = ['content/posts/AI Learnings/2026-05-01-claude-mythos-doomsday-scenario.md',
      'content/posts/AI Learnings/2026-05-01-claude-mythos-cybersecurity-impact.md']
merge_files(f1, 'content/posts/AI Learnings/2026-05-01-claude-mythos-comprehensive-impact-analysis.md',
            '클로드 미토스(Claude Mythos) 종합 분석: 글로벌 보안 위기와 다중 산업 파급력',
            'AI Learnings', '2026-05-01', 'Wook')

# 2. NotebookLM
f2 = sorted(glob.glob('content/posts/AI Learnings/2026-05-03-notebooklm-guide-part*.md'))
merge_files(f2, 'content/posts/AI Learnings/2026-05-03-notebooklm-comprehensive-master-guide.md',
            '구글 NotebookLM 100% 실전 활용 가이드 (통합본)',
            'AI Learnings', '2026-05-03', 'Wook')

# 3. Gemini CLI / Antigravity
f3 = ['content/posts/AI Learnings/2026-05-08-antigravity-vs-gemini-cli-guide.md',
      'content/posts/AI Learnings/2026-05-09-gemini-cli-yolo-mode-chunking.md',
      'content/posts/AI Learnings/2026-05-10-gemini-cli-skills-for-developers.md']
merge_files(f3, 'content/posts/AI Learnings/2026-05-10-gemini-cli-antigravity-master-guide.md',
            'Gemini CLI & Antigravity 에이전트 완벽 가이드: 개발자 생산성 극대화 (통합본)',
            'AI Learnings', '2026-05-10', 'Wook')

