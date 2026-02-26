import { notFound } from "next/navigation";
import { FileTree } from "../../components/FileTree";
import { MarkdownViewer } from "../../components/MarkdownViewer";
import { Breadcrumbs } from "../../components/Breadcrumbs";
import { SearchBox } from "../../components/SearchBox";
import { ThemeToggle } from "../../components/ThemeToggle";
import { getAllFiles, getFileContent, getLastSynced } from "../../lib/github";
import { buildSearchDocuments } from "../../lib/search-server";

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
  const searchDocuments = buildSearchDocuments();

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
    <div className="flex min-h-screen bg-background">
      {/* Sidebar */}
      <aside className="w-72 bg-sidebar border-r border-sidebar-border flex flex-col fixed h-full">
        <div className="p-4 border-b border-sidebar-border flex items-center justify-between">
          <div>
            <a href="/" className="block">
              <h1 className="text-lg font-semibold text-sidebar-foreground">Memory Bridge</h1>
            </a>
            <p className="text-xs text-muted-foreground mt-1">Archival memory viewer</p>
          </div>
          <ThemeToggle />
        </div>
        <div className="p-4 border-b border-sidebar-border">
          <SearchBox documents={searchDocuments} />
        </div>
        <FileTree categories={categories} />
        <div className="p-4 border-t border-sidebar-border text-xs text-muted-foreground">
          Last synced: {lastSynced}
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 ml-72 p-8">
        <div className="max-w-4xl mx-auto">
          <Breadcrumbs path={filePath} />
          
          <div className="bg-card rounded-lg border border-border p-8">
            <MarkdownViewer content={content} />
          </div>
        </div>
      </main>
    </div>
  );
}
