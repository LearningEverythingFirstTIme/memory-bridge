import { notFound } from "next/navigation";
import { FileTree } from "../../components/FileTree";
import { MarkdownViewer } from "../../components/MarkdownViewer";
import { Breadcrumbs } from "../../components/Breadcrumbs";
import { SearchBox } from "../../components/SearchBox";
import { getAllFiles, getFileContent, getLastSynced } from "../../lib/github";
import { buildSearchIndex } from "../../lib/search";

// Generate static params for all files at build time
export function generateStaticParams(): { slug: string[] }[] {
  const files = getAllFiles();
  
  return files.map((file) => ({
    slug: file.path.split("/"),
  }));
}

export default async function ViewerPage({
  params,
}: {
  params: Promise<{ slug: string[] }>;
}) {
  const { slug } = await params;
  const filePath = slug.join("/");
  
  const content = getFileContent(filePath);
  
  if (!content) {
    notFound();
  }

  const files = getAllFiles();
  const lastSynced = getLastSynced();
  const searchIndex = buildSearchIndex();
  const searchResults = searchIndex.search("");

  const categories = [
    { id: 'state', label: 'State', files: files.filter(f => f.category === 'state') },
    { id: 'memory', label: 'Memory', files: files.filter(f => f.category === 'memory') },
    { id: 'docs', label: 'Documentation', files: files.filter(f => f.category === 'docs') },
    { id: 'scripts', label: 'Scripts', files: files.filter(f => f.category === 'scripts') },
    { id: 'reports', label: 'Reports', files: files.filter(f => f.category === 'reports') },
    { id: 'journal', label: 'Journal', files: files.filter(f => f.category === 'journal') },
    { id: 'capture', label: 'Capture', files: files.filter(f => f.category === 'capture') },
    { id: 'notes', label: 'Daily Notes', files: files.filter(f => f.category === 'notes') },
  ];

  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <aside className="w-72 bg-stone-100 border-r border-stone-200 flex flex-col fixed h-full">
        <div className="p-4 border-b border-stone-200">
          <a href="/" className="block">
            <h1 className="text-lg font-semibold text-stone-800">Memory Bridge</h1>
          </a>
          <p className="text-xs text-stone-500 mt-1">Archival memory viewer</p>
        </div>
        <div className="p-4 border-b border-stone-200">
          <SearchBox results={searchResults} />
        </div>
        <FileTree categories={categories} />
        <div className="p-4 border-t border-stone-200 text-xs text-stone-400">
          Last synced: {lastSynced}
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 ml-72 p-8">
        <div className="max-w-4xl mx-auto">
          <Breadcrumbs path={filePath} />
          
          <div className="bg-white rounded-lg border border-stone-200 p-8">
            <MarkdownViewer content={content} />
          </div>
        </div>
      </main>
    </div>
  );
}
