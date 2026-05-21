const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

async function convertToPdf() {
    const bookDir = __dirname;
    const mdPath = path.join(bookDir, "digital_marketing_lies_integrated.md");
    const pdfPath = path.join(bookDir, "digital_marketing_lies_preview.pdf");

    if (!fs.existsSync(mdPath)) {
        console.error(`에러: ${mdPath} 파일이 존재하지 않습니다.`);
        process.exit(1);
    }

    const markdownText = fs.readFileSync(mdPath, 'utf-8');

    // Puppeteer 브라우저에서 실행할 HTML 뼈대 작성
    // marked.js CDN과 Google Fonts 및 예쁜 책 스타일 CSS 추가
    const htmlContent = `
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>마케팅 데이터의 거짓말</title>
        <!-- marked.js Markdown 파서 로드 -->
        <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
        <!-- Google Fonts: Noto Sans KR, Nanum Myeongjo 로드 -->
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700;800&family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
        <style>
            @page {
                size: A4;
                margin: 20mm 20mm 20mm 20mm;
            }
            body {
                font-family: 'Noto Sans KR', sans-serif;
                font-size: 14px;
                line-height: 1.8;
                color: #2c3e50;
                padding: 10px;
            }
            /* 책 본문 스타일링 */
            h1, h2, h3, h4, h5, h6 {
                color: #1a252f;
                font-family: 'Noto Sans KR', sans-serif;
                page-break-after: avoid;
            }
            h1 {
                font-size: 28px;
                border-bottom: 2px solid #34495e;
                padding-bottom: 8px;
                margin-top: 40px;
                margin-bottom: 24px;
                font-weight: 700;
            }
            /* 각 챕터(📍 프롤로그 등) h1 앞에는 페이지 넘김 설정 */
            .chapter-title {
                page-break-before: always;
            }
            h2 {
                font-size: 20px;
                margin-top: 30px;
                margin-bottom: 16px;
                border-bottom: 1px solid #ecf0f1;
                padding-bottom: 6px;
                font-weight: 700;
            }
            h3 {
                font-size: 16px;
                margin-top: 24px;
                margin-bottom: 12px;
                font-weight: 700;
            }
            p {
                margin-bottom: 16px;
                text-align: justify;
            }
            blockquote {
                border-left: 4px solid #3498db;
                padding: 12px 20px;
                margin: 20px 0;
                background-color: #f8f9fa;
                font-style: italic;
                color: #555;
                font-family: 'Nanum Myeongjo', serif;
                line-height: 1.7;
            }
            blockquote strong {
                font-family: 'Noto Sans KR', sans-serif;
            }
            ul, ol {
                margin-bottom: 16px;
                padding-left: 24px;
            }
            li {
                margin-bottom: 8px;
            }
            code {
                font-family: monospace;
                background-color: #f1f2f6;
                padding: 2px 6px;
                border-radius: 4px;
                font-size: 13px;
            }
            hr {
                border: 0;
                border-top: 1px solid #ddd;
                margin: 40px 0;
            }
            /* 테이블 스타일 */
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 24px;
                font-size: 13px;
            }
            th, td {
                border: 1px solid #dcdde1;
                padding: 10px;
                text-align: left;
            }
            th {
                background-color: #f5f6fa;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div id="content"></div>
        <script>
            // 마크다운 파싱 옵션 설정
            marked.setOptions({
                gfm: true,
                breaks: true
            });
            
            // Raw Markdown 전달
            const rawMarkdown = \`${markdownText.replace(/`/g, '\\`').replace(/\${/g, '\\${')}\`;
            
            // 챕터별로 h1에 page-break를 주기 위해 처리
            let html = marked.parse(rawMarkdown);
            
            // H1 중에서 프롤로그, 장, 에필로그로 시작하는 H1에 클래스 추가해 페이지 나누기 적용
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const h1s = doc.querySelectorAll('h1');
            h1s.forEach((h1, index) => {
                if (index > 0) { // 책 대제목 제외
                    h1.classList.add('chapter-title');
                }
            });
            
            document.getElementById('content').innerHTML = doc.body.innerHTML;
        </script>
    </body>
    </html>
    `;

    console.log("Puppeteer 브라우저 기동 중...");
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    
    console.log("HTML 컨텐츠 바인딩 및 렌더링 대기 중...");
    await page.setContent(htmlContent, { waitUntil: 'networkidle0' });
    
    console.log("PDF 파일 생성 중...");
    await page.pdf({
        path: pdfPath,
        format: 'A4',
        margin: {
            top: '25mm',
            bottom: '25mm',
            left: '25mm',
            right: '25mm'
        },
        displayHeaderFooter: true,
        headerTemplate: '<div style="font-size: 8px; width: 100%; text-align: center; color: #bbb; font-family: sans-serif;">마케팅 데이터의 거짓말 - 프리뷰 초안</div>',
        footerTemplate: '<div style="font-size: 8px; width: 100%; text-align: center; color: #bbb; font-family: sans-serif;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
        printBackground: true
    });

    console.log(`성공! PDF 프리뷰 파일이 생성되었습니다: ${pdfPath}`);
    await browser.close();
}

convertToPdf().catch(err => {
    console.error("PDF 변환 오류 발생:", err);
    process.exit(1);
});
