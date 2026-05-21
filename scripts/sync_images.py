import os
import re

# 원본 및 타겟 디렉토리 경로 정의
base_dir = "/Users/wook/WookAi/Booklog"
manuscript_dir = os.path.join(base_dir, ".manuscript/digital-marketing-lies")
posts_dir = os.path.join(base_dir, "content/posts")

# 챕터 파일과 블로그 포스트의 매핑 관계 정의
# (블로그 포스트 경로는 posts_dir 하위의 상대 경로)
MAPPING = {
    "prologue.md": [
        "2026-05-19-who-is-the-patsy-in-digital-marketing.ko.md",
        "Marketing/2026-05-12-does-advertising-increase-sales.md"
    ],
    "chapter-01.md": [
        "Marketing/2026-04-29-global-ad-market-size-estimates-gap.md",
        "Marketing/2026-05-17-korea-digital-ad-market-size-analysis.md",
        "Marketing/2026-05-17-korea-digital-ad-market-size-analysis.en.md",
        "Marketing/2026-05-18-innovative-adtech-b2b-selling-strategies.md"
    ],
    "chapter-02.md": [
        "Marketing/2026-05-10-attribution-models-dilemma-dda.md",
        "Marketing/2026-05-10-digital-analytics-web-vs-app-mmp.md"
    ],
    "chapter-03.md": [
        "2026-05-19-uber-100m-attribution-fraud-case.ko.md",
        "Marketing/2026-05-12-does-advertising-increase-sales.md",
        "Marketing/2026-05-09-ad-fraud-click-farm.md",
        "Marketing/2026-05-12-book-review-avoiding-ad-fraud.md",
        "2026-05-20-latest-global-ad-fraud-scandals-2024-2026.ko.md",
        "Marketing/2026-05-12-adtech-ad-fraud-brand-safety.md"
    ],
    "chapter-04.md": [
        "Marketing/2026-04-23-never-bid-brand-keywords.md",
        "Marketing/2026-04-25-tadelis-paid-search.md",
        "Marketing/2026-05-09-google-performance-max-analysis.md",
        "Marketing/2026-05-10-pmax-blackbox-exodus.md",
        "2026-05-20-ad-tech-machine-learning-invalid-learning-loop.ko.md",
        "Marketing/2026-05-10-uac-app-fraud-defense.md",
        "Marketing/2026-05-10-uac-fraud-placement-audit.md",
        "Marketing/2026-05-09-ad-fraud-mfa.md",
        "2026-05-19-youtube-kids-channel-advertising-performance-illusion.ko.md"
    ],
    "chapter-05.md": [
        "2026-05-19-meta-facebook-advertising-fraud-blackbox.ko.md",
        "2026-05-20-ad-tech-machine-learning-invalid-learning-loop.ko.md",
        "Marketing/2026-05-09-retargeting-marketing-deep-dive.md",
        "Marketing/2026-05-10-targeting-trap-bias.md"
    ],
    "chapter-06.md": [
        "2026-05-19-analytics-measurement-discrepancy.ko.md",
        "Marketing/2026-05-10-first-party-data-server-side-capi.md",
        "Marketing/2026-05-10-capi-mmm-cookieless-infrastructure.md"
    ],
    "chapter-07.md": [
        "2026-05-19-boeing-sears-financial-metrics-failure.ko.md",
        "Marketing/2026-05-18-anchoring-effect-recommender-system.md",
        "Marketing/2026-05-13-marketing-quiz-3-statistics.md",
        "Marketing/2026-05-13-marketing-quiz-4-vanity-metrics.md",
        "Marketing/2026-05-12-social-desirability-bias-survey-flaws.md",
        "Data/2026-04-30-abraham-wald-survivorship-bias.md",
        "Data/2026-04-30-simpsons-paradox-uc-berkeley.md",
        "Data/2026-05-10-ab-testing-p-value-srm.md"
    ],
    "chapter-08.md": [
        "Marketing/2026-05-13-marketing-quiz-1-causality.md",
        "Marketing/2026-05-09-mmm-resurgence-limitations.md",
        "Data/2026-04-30-spurious-correlation-nicolas-cage.md"
    ],
    "chapter-09.md": [
        "Marketing/2026-05-18-innovative-adtech-b2b-selling-strategies.md",
        "Marketing/2026-05-10-data-signal-design-capi-cleanroom.md",
        "Marketing/2026-05-10-capi-mmm-cookieless-infrastructure.md",
        "2026-05-20-global-digital-ad-spend-waste-estimates.ko.md"
    ],
    "epilogue.md": []
}

img_pattern = re.compile(r'\!\[(.*?)\]\((.*?)\)')

def get_images_from_post(post_rel_path):
    post_path = os.path.join(posts_dir, post_rel_path)
    if not os.path.exists(post_path):
        print(f"  [경고] 블로그 포스트를 찾을 수 없습니다: {post_rel_path}")
        return []
    
    with open(post_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 이미지 링크 매칭 추출 (alt text, image src)
    matches = img_pattern.findall(content)
    return matches

def sync_images_to_chapters():
    print("=== 블로그 이미지 -> 책 챕터 동기화 작업 시작 ===")
    
    for chapter_file, posts in MAPPING.items():
        chapter_path = os.path.join(manuscript_dir, chapter_file)
        if not os.path.exists(chapter_path):
            print(f"[경고] 챕터 파일이 존재하지 않습니다: {chapter_file}")
            continue
            
        print(f"\nProcessing {chapter_file}...")
        
        # 1. 포스트들로부터 모든 이미지 추출
        all_images = []
        for post in posts:
            imgs = get_images_from_post(post)
            for alt, src in imgs:
                # 중복 수집 방지
                if (alt, src) not in all_images:
                    all_images.append((alt, src))
                    
        if not all_images:
            print("  가져올 이미지가 없습니다.")
            continue
            
        # 2. 챕터 파일 열어 기존 내용 확인
        with open(chapter_path, 'r', encoding='utf-8') as f:
            chapter_content = f.read()
            
        # 3. 중복 삽입 방지 필터링
        new_images = []
        for alt, src in all_images:
            if src not in chapter_content:
                new_images.append((alt, src))
                
        if not new_images:
            print("  이미 모든 이미지가 원고에 삽입되어 있습니다.")
            continue
            
        print(f"  새로 삽입할 이미지 {len(new_images)}개 감지.")
        
        # 4. 삽입할 텍스트 빌드
        img_section = "\n\n## 🖼️ 시각 자료 (참고 블로그)\n\n"
        for alt, src in new_images:
            img_section += f"![{alt}]({src})\n"
            
        # 5. 삽입할 위치 탐색 (참고 자료 바로 위 또는 파일의 가장 마지막)
        if "## 📚 참고자료" in chapter_content:
            parts = chapter_content.split("## 📚 참고자료")
            new_content = parts[0] + img_section + "\n## 📚 참고자료" + parts[1]
        else:
            new_content = chapter_content.rstrip() + img_section
            
        # 6. 저장
        with open(chapter_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  {chapter_file}에 이미지 삽입 완료!")

if __name__ == "__main__":
    sync_images_to_chapters()
