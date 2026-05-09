import os

def fix_dir(d):
    for root, _, files in os.walk(d):
        for f in files:
            if f.endswith('.py'):
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Check if file has `|` for types (like `dict | list` or `str | None`)
                # To be safe, just add it if not already there and if there are type hints.
                if 'from __future__ import annotations' not in content:
                    # Find where to insert (after shebang and docstring)
                    lines = content.split('\n')
                    insert_idx = 0
                    if lines and lines[0].startswith('#!'):
                        insert_idx = 1
                    
                    # Skip docstrings
                    if len(lines) > insert_idx and lines[insert_idx].startswith('"""'):
                        for i in range(insert_idx + 1, len(lines)):
                            if '"""' in lines[i]:
                                insert_idx = i + 1
                                break
                    
                    lines.insert(insert_idx, 'from __future__ import annotations')
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write('\n'.join(lines))

fix_dir('scripts')
