import { getSortedPostsData } from "@/lib/posts";
import SidebarNav from "./SidebarNav";

export default function Sidebar() {
  const posts = getSortedPostsData();
  
  // 포스트들을 카테고리별로 그룹핑
  const categoriesMap = posts.reduce((acc, post) => {
    const cat = post.category || "Insight";
    if (!acc[cat]) {
      acc[cat] = [];
    }
    acc[cat].push({
      slug: post.slug,
      title: post.title,
      date: post.date,
      category: post.category,
    });
    return acc;
  }, {} as Record<string, { slug: string; title: string; date: string; category: string }[]>);

  // 카테고리 데이터를 배열로 변환 (backups 등 비공개 카테고리 제외)
  const excludedCategories = new Set(['backups']);
  const categories = Object.entries(categoriesMap)
    .filter(([name]) => !excludedCategories.has(name.toLowerCase()))
    .map(([name, posts]) => ({
    name,
    slug: name.toLowerCase().replace(/\s+/g, '-'),
    posts,
  }));

  return (
    <aside className="hidden md:block w-[340px] shrink-0">
      <div className="md:sticky md:top-6 md:max-h-[calc(100vh-3rem)] md:overflow-y-auto no-scrollbar pt-2">
        <SidebarNav categories={categories} />
      </div>
    </aside>
  );
}
