import os
import glob
import re

post_dir = "/Users/wook/WookAi/Booklog/content/posts/**/*.md"
files = glob.glob(post_dir, recursive=True)

modified_files = []

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    in_code_block = False
    has_h1 = False
    
    # Pass 1: Check if true H1 exists outside of code blocks
    for line in lines:
        if line.startswith("```"):
            in_code_block = not in_code_block
        elif not in_code_block and re.match(r'^#\s', line):
            has_h1 = True
            break
            
    if not has_h1:
        continue
        
    # Pass 2: Demote all true headings
    new_lines = []
    in_code_block = False
    
    for line in lines:
        if line.startswith("```"):
            in_code_block = not in_code_block
            new_lines.append(line)
        elif not in_code_block and re.match(r'^(#+)\s', line):
            # Demote heading by adding one '#'
            new_line = "#" + line
            new_lines.append(new_line)
        else:
            new_lines.append(line)
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    modified_files.append(os.path.basename(filepath))

print(f"Total modified: {len(modified_files)}")
for mf in modified_files:
    print(f"- {mf}")
