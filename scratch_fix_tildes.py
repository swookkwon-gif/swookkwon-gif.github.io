import os
import re

directory = 'content/posts/'

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    new_text = text
    
    # 1. " ~ " -> " - "
    new_text = new_text.replace(' ~ ', ' - ')
    
    # 2. Approx "~" -> "약 " (if at start of word and followed by digit or $)
    new_text = re.sub(r'(^|[\s\(\[\{])\~(?=[\d\$])', r'\1약 ', new_text)
    
    # 3. Ranges "A~B" -> "A-B"
    # A is Korean, English, Digit, or %. B is Korean, English, Digit, or $.
    # This avoids matching "~/" or "http://.../~user"
    new_text = re.sub(r'([가-힣A-Za-z0-9%])\~([가-힣A-Za-z0-9\$])', r'\1-\2', new_text)
    
    if new_text != text:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_text)
        return True
    return False

modified_count = 0
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.md'):
            if process_file(os.path.join(root, file)):
                modified_count += 1

print(f"Modified {modified_count} files.")
