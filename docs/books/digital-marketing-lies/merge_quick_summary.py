import os

def merge_quick_summary():
    book_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(book_dir, "quick-summary-v0.1.md")
    
    chapters = [
        "prologue.md",
        "chapter-01.md",
        "chapter-02.md",
        "chapter-03.md",
        "chapter-04.md",
        "chapter-05.md",
        "chapter-06.md",
        "chapter-07.md",
        "chapter-08.md",
        "chapter-09.md",
        "epilogue.md"
    ]
    
    with open(output_path, "w", encoding="utf-8") as outfile:
        # 맨 앞 커버 안내 페이지 없이, 프롤로그부터 바로 시작
        for i, chapter_file in enumerate(chapters):
            file_path = os.path.join(book_dir, chapter_file)
            if not os.path.exists(file_path):
                print(f"경고: {chapter_file} 파일을 찾을 수 없습니다. 건너뜁니다.")
                continue
                
            print(f"가공 및 병합 중: {chapter_file}")
            
            with open(file_path, "r", encoding="utf-8") as infile:
                content = infile.read()
                
            # '## 📚 참고자료' 영역 및 그 하위 내용 삭제
            if "## 📚 참고자료" in content:
                content = content.split("## 📚 참고자료")[0]
            
            # 우측/하단 공백 제거
            content = content.rstrip()
            
            # 각 챕터 구분선 추가 (첫 장 제외)
            if i > 0:
                outfile.write("\n\n<!-- PAGE_BREAK -->\n\n---\n\n")
                
            outfile.write(content)
            outfile.write("\n")
                
    print(f"\n성공적으로 병합되었습니다! 저장 위치: {output_path}")

if __name__ == "__main__":
    merge_quick_summary()
