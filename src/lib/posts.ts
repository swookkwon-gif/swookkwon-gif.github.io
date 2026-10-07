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
  tags?: string[];
  readingTime?: number;
}

function getAllMarkdownFiles(dirPath: string, arrayOfFiles: string[] = []): string[] {
  if (!fs.existsSync(dirPath)) return arrayOfFiles;
  const files = fs.readdirSync(dirPath);
  files.forEach((file) => {
    const fullPath = path.join(dirPath, file);
    if (fs.statSync(fullPath).isDirectory()) {
      arrayOfFiles = getAllMarkdownFiles(fullPath, arrayOfFiles);
    } else if (file.endsWith('.md')) {
      arrayOfFiles.push(fullPath);
    }
  });
  return arrayOfFiles;
}

function generateExcerpt(content: string, length: number = 160): string {
  const text = content
    .replace(/^#+\s+.*/gm, '') // 헤딩 제거
    .replace(/!\[.*?\]\(.*?\)/g, '') // 이미지 제거
    .replace(/\[(.*?)\]\(.*?\)/g, '$1') // 링크 텍스트만 유지
    .replace(/<[^>]*>/g, '') // HTML 태그 제거
    .replace(/```[\s\S]*?```/g, '') // 코드블록 제거
    .replace(/[\r\n]+/g, ' ')
    .trim();

  if (text.length <= length) return text;
  return text.substring(0, length).trim() + '...';
}

function calculateReadingTime(content: string): number {
  const wordsPerMinute = 200;
  const words = content.trim().split(/\s+/).length;
  return Math.max(1, Math.ceil(words / wordsPerMinute));
}

function formatDate(rawDate?: string | Date): string {
  if (!rawDate) return new Date().toISOString().split('T')[0];
  try {
    const d = rawDate instanceof Date ? rawDate : new Date(String(rawDate));
    if (!isNaN(d.getTime())) {
      const kstDate = new Date(d.getTime() + 9 * 60 * 60 * 1000);
      const yyyy = kstDate.getUTCFullYear();
      const mm = String(kstDate.getUTCMonth() + 1).padStart(2, '0');
      const dd = String(kstDate.getUTCDate()).padStart(2, '0');
      return `${yyyy}-${mm}-${dd}`;
    }
    return String(rawDate).split('T')[0];
  } catch {
    return String(rawDate).split('T')[0];
  }
}

export function getSortedPostsData(): PostData[] {
  if (!fs.existsSync(postsDirectory)) {
    return [];
  }

  const allFiles = getAllMarkdownFiles(postsDirectory);
  if (allFiles.length === 0) return [];

  const allPostsData = allFiles.map((fullPath) => {
    const fileName = path.basename(fullPath);
    const slug = fileName.replace(/\.md$/, '');
    const fileContents = fs.readFileSync(fullPath, 'utf8');
    const { data, content } = matter(fileContents);

    const parentFolder = path.basename(path.dirname(fullPath));
    const category = parentFolder !== 'posts' && parentFolder !== 'content'
      ? parentFolder
      : (data.category || 'Research');

    const formattedDate = formatDate(data.date);
    const sortTimestamp = data.date ? new Date(data.date).getTime() : 0;

    return {
      slug,
      content,
      title: data.title || slug,
      date: formattedDate,
      excerpt: data.excerpt || generateExcerpt(content),
      category,
      tags: Array.isArray(data.tags) ? data.tags : [],
      readingTime: calculateReadingTime(content),
      _sortTimestamp: sortTimestamp,
    };
  });

  return allPostsData.sort((a, b) => (a._sortTimestamp < b._sortTimestamp ? 1 : -1));
}

export function getPostData(slug: string): PostData {
  const allFiles = getAllMarkdownFiles(postsDirectory);
  const targetFile = allFiles.find((file) => {
    const fileName = path.basename(file);
    return fileName.replace(/\.md$/, '') === slug;
  });

  if (!targetFile) {
    throw new Error(`Post not found for slug: ${slug}`);
  }

  const fileContents = fs.readFileSync(targetFile, 'utf8');
  const { data, content } = matter(fileContents);

  const parentFolder = path.basename(path.dirname(targetFile));
  const category = parentFolder !== 'posts' && parentFolder !== 'content'
    ? parentFolder
    : (data.category || 'Research');

  return {
    slug,
    content,
    title: data.title || slug,
    date: formatDate(data.date),
    excerpt: data.excerpt || generateExcerpt(content),
    category,
    tags: Array.isArray(data.tags) ? data.tags : [],
    readingTime: calculateReadingTime(content),
  };
}
