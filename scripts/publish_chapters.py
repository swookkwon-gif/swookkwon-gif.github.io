import os
import re

base_dir = "/Users/wook/WookAi/Booklog"
manuscript_dir = os.path.join(base_dir, ".manuscript/digital-marketing-lies")
publish_dir = os.path.join(base_dir, "content/posts/digital-marketing-lies")

# 배포 설정 정의
CHAPTERS = [
    ("prologue.md", "prologue.md", "2026-05-21T01:00:00+09:00", ["프롤로그", "디지털마케팅", "북로그"]),
    ("chapter-01.md", "chapter-01.md", "2026-05-21T02:00:00+09:00", ["마케팅시장", "빅테크", "광고지출", "DigitalMarketingLies"]),
    ("chapter-02.md", "chapter-02.md", "2026-05-21T03:00:00+09:00", ["애드테크", "MMP", "과금모델", "AdTech"]),
    ("chapter-03.md", "chapter-03.md", "2026-05-21T04:00:00+09:00", ["광고사기", "우버", "AdFraud", "카니발라이제이션"]),
    ("chapter-04.md", "chapter-04.md", "2026-05-21T05:00:00+09:00", ["구글", "PerformanceMax", "블랙박스", "AI광고"]),
    ("chapter-05.md", "chapter-05.md", "2026-05-21T06:00:00+09:00", ["메타", "페이스북", "ROAS", "타겟팅"]),
    ("chapter-06.md", "chapter-06.md", "2026-05-21T07:00:00+09:00", ["데이터측정", "서버사이드", "CAPI", "GA4"]),
    ("chapter-07.md", "chapter-07.md", "2026-05-21T08:00:00+09:00", ["지표의함정", "굿하트의법칙", "심슨의역설", "생존자편향"]),
    ("chapter-08.md", "chapter-08.md", "2026-05-21T09:00:00+09:00", ["인과관계", "상관관계", "증분테스트", "MMM"]),
    ("chapter-09.md", "chapter-09.md", "2026-05-21T10:00:00+09:00", ["의사결정", "가드레일", "모니터링자동화", "n8n"]),
    ("epilogue.md", "epilogue.md", "2026-05-21T11:00:00+09:00", ["에필로그", "데이터리터러시", "Booklog"])
]

def publish():
    print("=== 챕터 블로그 포스트 공개 처리 시작 ===")
    
    # 1. 대상 디렉토리 생성
    if not os.path.exists(publish_dir):
        os.makedirs(publish_dir)
        print(f"디렉토리 생성 완료: {publish_dir}")
        
    for src_file, dest_file, date_str, tags in CHAPTERS:
        src_path = os.path.join(manuscript_dir, src_file)
        dest_path = os.path.join(publish_dir, dest_file)
        
        if not os.path.exists(src_path):
            print(f"[경고] 원본 원고가 존재하지 않습니다: {src_file}")
            continue
            
        with open(src_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 2. 첫 H1 제목 추출 및 제거
        # H1 매칭 정규식: 줄 시작 부분의 # 
        h1_match = re.search(r'^\s*#\s+(.*)', content)
        if h1_match:
            title = h1_match.group(1).strip()
            # H1 라인 전체 제거 (줄바꿈 포함)
            content = re.sub(r'^\s*#\s+.*?\n+', '', content, count=1)
        else:
            title = src_file.replace('.md', '').capitalize()
            print(f"[알림] {src_file}에서 H1 제목을 찾지 못해 파일명으로 대체합니다: {title}")
            
        # 3. YAML Frontmatter 생성
        frontmatter = f"""---
title: "{title}"
date: {date_str}
draft: false
tags: {str(tags).replace("'", '"')}
categories: ["Digital Marketing Lies"]
---

"""
        # 4. 결합 및 저장
        final_content = frontmatter + content.lstrip()
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
            
        print(f"  배포 완료: {dest_file} -> 타이틀: '{title}'")
        
    print("=== 블로그 공개용 포스트 배포 성공! ===")

if __name__ == "__main__":
    publish()
