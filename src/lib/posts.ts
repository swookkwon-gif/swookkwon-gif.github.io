import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

const postsDirectory = path.join(process.cwd(), 'content/posts');

export interface PostData {
  slug: string;
  title: string;
  date: string;
  excerpt: string;
  category: string;
  content: string;
  author?: string;
  tags?: string[];
  related?: string[];
  relatedPosts?: { slug: string; title: string; date: string; category: string; excerpt: string }[];
  categoryTotalCount?: number;
}

function getAllMarkdownFiles(dirPath: string, arrayOfFiles: string[] = []) {
  if (!fs.existsSync(dirPath)) return arrayOfFiles;
  const files = fs.readdirSync(dirPath);
  files.forEach(function (file) {
    const fullPath = path.join(dirPath, file);
    if (fs.statSync(fullPath).isDirectory()) {
      arrayOfFiles = getAllMarkdownFiles(fullPath, arrayOfFiles);
    } else {
      if (file.endsWith('.md')) {
        arrayOfFiles.push(fullPath);
      }
    }
  });
  return arrayOfFiles;
}

function generateExcerpt(content: string, length: number = 150): string {
  // 마크다운 헤딩, 이미지, 링크 제거 및 줄바꿈을 공백으로 변경하여 순수 텍스트만 추출
  let text = content
    .replace(/^#+\s+.*/gm, '') // 헤딩 제거
    .replace(/!\[.*?\]\(.*?\)/g, '') // 이미지 제거
    .replace(/\[(.*?)\]\(.*?\)/g, '$1') // 링크는 텍스트만 남김
    .replace(/<[^>]*>/g, '') // HTML 태그 제거
    .replace(/[\r\n]+/g, ' ') // 줄바꿈을 공백으로
    .trim();
  
  if (text.length <= length) return text;
  return text.substring(0, length).trim() + '...';
}

export function getSortedPostsData(lang: string = 'ko'): PostData[] {
  const allFiles = getAllMarkdownFiles(postsDirectory);
  
  const fileMap = new Map<string, { en?: string, ko?: string }>();
  allFiles.forEach(file => {
    const fileName = path.basename(file);
    const slug = fileName.replace(/\.(en|ko)?\.?md$/, '');
    if (!fileMap.has(slug)) fileMap.set(slug, {});
    
    if (fileName.endsWith('.en.md')) {
      fileMap.get(slug)!.en = file;
    } else if (fileName.endsWith('.md')) {
      fileMap.get(slug)!.ko = file;
    }
  });

  const filteredFiles: string[] = [];
  fileMap.forEach(langs => {
    if (lang === 'en') {
      if (langs.en) filteredFiles.push(langs.en);
      // No fallback to Korean — only real .en.md files
    } else {
      if (langs.ko) filteredFiles.push(langs.ko);
    }
  });

  const allPostsData = filteredFiles.map((fullPath) => {
    const fileName = path.basename(fullPath);
    const slug = fileName.replace(/\.(en|ko)?\.?md$/, '');
    const fileContents = fs.readFileSync(fullPath, 'utf8');
    const { data, content } = matter(fileContents);
    
    // 부모 폴더 이름에서 카테고리 추출 (예: "AI News" -> "AI News")
    const parentFolder = path.basename(path.dirname(fullPath));
    const derivedCategory = parentFolder !== 'posts' 
      ? parentFolder.replace(/^\d+\.\s*/, '') 
      : (data.category || 'Insight');

    let postDateStr = '';
    let sortTimestamp = 0;
    try {
      const rawDate = data.date || new Date();
      // gray-matter parses valid dates into Date objects
      const d = rawDate instanceof Date ? rawDate : new Date(String(rawDate));
      
      if (!isNaN(d.getTime())) {
        sortTimestamp = d.getTime();
        // Format to YYYY-MM-DD (KST)
        const kstDate = new Date(d.getTime() + (9 * 60 * 60 * 1000));
        const yyyy = kstDate.getUTCFullYear();
        const mm = String(kstDate.getUTCMonth() + 1).padStart(2, '0');
        const dd = String(kstDate.getUTCDate()).padStart(2, '0');
        postDateStr = `${yyyy}-${mm}-${dd}`;
      } else {
        postDateStr = String(data.date).split('T')[0];
      }
    } catch (e) {
      postDateStr = String(data.date).split('T')[0];
    }

    return {
      ...data,
      slug,
      content,
      title: data.title,
      date: postDateStr,
      author: data.author || 'Antigravity',
      _sortTimestamp: sortTimestamp, // 내부 정렬용 필드
      excerpt: data.excerpt || generateExcerpt(content),
      category: derivedCategory,
    } as PostData & { _sortTimestamp: number };
  });

  return allPostsData.sort((a, b) => (a._sortTimestamp < b._sortTimestamp ? 1 : -1));
}

export function getPostData(slug: string, lang: string = 'ko'): PostData {
  const allFiles = getAllMarkdownFiles(postsDirectory);
  
  let targetFile = allFiles.find(file => {
    const fileName = path.basename(file);
    const fileSlug = fileName.replace(/\.(en|ko)?\.?md$/, '');
    if (fileSlug !== slug) return false;
    
    if (lang === 'en') return fileName.endsWith('.en.md');
    return fileName.endsWith('.md') && !fileName.endsWith('.en.md');
  });
  
  // Fallback to Korean if English file doesn't exist
  if (!targetFile && lang === 'en') {
    targetFile = allFiles.find(file => {
      const fileName = path.basename(file);
      const fileSlug = fileName.replace(/\.(en|ko)?\.?md$/, '');
      return fileSlug === slug && fileName.endsWith('.md') && !fileName.endsWith('.en.md');
    });
  }
  
  if (!targetFile) {
    throw new Error(`Post not found for slug: ${slug}`);
  }

  const fileContents = fs.readFileSync(targetFile, 'utf8');
  const { data, content } = matter(fileContents);
  
  const parentFolder = path.basename(path.dirname(targetFile));
  const derivedCategory = parentFolder !== 'posts' 
    ? parentFolder.replace(/^\d+\.\s*/, '') 
    : (data.category || 'Insight');

  // Related & Navigation Logic
  const allPosts = getSortedPostsData(lang); // sorted desc by date
  const categoryPosts = allPosts.filter(p => p.category === derivedCategory);
  
  let relatedPosts: { slug: string; title: string; date: string; category: string; excerpt: string }[] = [];
  
  if (data.related && Array.isArray(data.related)) {
    relatedPosts = allPosts
      .filter(p => data.related.includes(p.slug))
      .map(p => ({ slug: p.slug, title: p.title, date: p.date, category: p.category, excerpt: p.excerpt }));
  } else {
    // 명시된 관련 글이 없으면 같은 카테고리의 최신 글을 최대 7개 추천 (현재 글 제외)
    relatedPosts = categoryPosts
      .filter(p => p.slug !== slug)
      .slice(0, 7)
      .map(p => ({ slug: p.slug, title: p.title, date: p.date, category: p.category, excerpt: p.excerpt }));
  }

  let postDateStr = '';
  try {
    const rawDate = data.date || new Date();
    const d = rawDate instanceof Date ? rawDate : new Date(String(rawDate));
    
    if (!isNaN(d.getTime())) {
      const kstDate = new Date(d.getTime() + (9 * 60 * 60 * 1000));
      const yyyy = kstDate.getUTCFullYear();
      const mm = String(kstDate.getUTCMonth() + 1).padStart(2, '0');
      const dd = String(kstDate.getUTCDate()).padStart(2, '0');
      postDateStr = `${yyyy}-${mm}-${dd}`;
    } else {
      postDateStr = String(data.date).split('T')[0];
    }
  } catch (e) {
    postDateStr = String(data.date).split('T')[0];
  }

  return {
    ...data,
    slug,
    content,
    title: data.title,
    date: postDateStr,
    author: data.author || 'Antigravity',
    excerpt: data.excerpt || generateExcerpt(content),
    category: derivedCategory,
    relatedPosts,
    categoryTotalCount: categoryPosts.length
  } as PostData;
}
