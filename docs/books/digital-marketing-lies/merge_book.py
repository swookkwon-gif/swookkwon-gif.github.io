import os

def merge_drafts():
    book_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(book_dir, "digital_marketing_lies_integrated.md")
    
    # 챕터 순서 정의
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
        # 책 표지 및 간단한 안내 메타데이터 작성
        outfile.write("# 도서 초안 통합본: 마케팅 데이터의 거짓말\n\n")
        outfile.write("> *본 파일은 프롤로그부터 9장, 에필로그까지의 초안 원고를 하나로 합친 파일입니다. 구글 드라이브에 업로드한 후 'Google 문서'로 열어 편집하시거나 구글 독스에 복사하여 사용하실 수 있습니다.*\n\n")
        outfile.write("---\n\n")
        
        for i, chapter_file in enumerate(chapters):
            file_path = os.path.join(book_dir, chapter_file)
            if not os.path.exists(file_path):
                print(f"경고: {chapter_file} 파일을 찾을 수 없습니다. 건너뜁니다.")
                continue
                
            print(f"병합 중: {chapter_file}")
            
            # 각 챕터 구분선 추가 (첫 장 제외)
            if i > 0:
                outfile.write("\n\n<!-- PAGE_BREAK -->\n\n---\n\n")
                
            with open(file_path, "r", encoding="utf-8") as infile:
                content = infile.read()
                outfile.write(content)
                outfile.write("\n")
                
    print(f"\n성공적으로 병합되었습니다! 저장 위치: {output_path}")

if __name__ == "__main__":
    merge_drafts()
