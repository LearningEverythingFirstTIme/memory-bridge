import { FileTree } from "./components/FileTree";
import { SearchBox } from "./components/SearchBox";
import { getAllFiles, getLastSynced } from "./lib/github";
import { buildSearchDocuments } from "./lib/search-server";

export default function Home() {
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
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <aside className="w-72 bg-stone-100 border-r border-stone-200 flex flex-col fixed h-full">
        <div className="p-4 border-b border-stone-200">
          <h1 className="text-lg font-semibold text-stone-800">Memory Bridge</h1>
          <p className="text-xs text-stone-500 mt-1">Archival memory viewer</p>
        </div>
        <div className="p-4 border-b border-stone-200">
          <SearchBox documents={searchDocuments} />
        </div>
        <FileTree categories={categories} />
        <div className="p-4 border-t border-stone-200 text-xs text-stone-400">
          Last synced: {lastSynced}
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 ml-72 p-8">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl font-semibold text-stone-800 mb-6">Memory Archive</h2>
          
          <div className="grid gap-6">
            {categories.map((category) => (
              <section key={category.id} className="bg-white rounded-lg border border-stone-200 p-6">
                <h3 className="text-sm font-medium text-stone-500 uppercase tracking-wider mb-4">
                  {category.label}
                </h3>
                {category.files.length === 0 ? (
                  <p className="text-stone-400 text-sm italic">No files</p>
                ) : (
                  <ul className="space-y-2">
                    {category.files.slice(0, 5).map((file) => (
                      <li key={file.path}>
                        <a
                          href={`/view/${file.path}/`}
                          className="text-stone-700 hover:text-stone-900 hover:underline text-sm"
                        >
                          {file.name}
                        </a>
                        <span className="text-stone-400 text-xs ml-2">
                          {new Date(file.lastModified).toLocaleDateString()}
                        </span>
                      </li>
                    ))}
                    {category.files.length > 5 && (
                      <li className="text-stone-400 text-xs">
                        +{category.files.length - 5} more files
                      </li>
                    )}
                  </ul>
                )}
              </section>
            ))}
          </div>

          <div className="mt-12 p-6 bg-stone-100 rounded-lg border border-stone-200">
            <h3 className="text-sm font-medium text-stone-600 mb-2">About</h3>
            <p className="text-sm text-stone-500 leading-relaxed">
              Memory Bridge is a read-only archive of Kimi Claw&apos;s memory system. 
              Files are synced daily from the VPS to GitHub and rendered here as Markdown.
              Use the sidebar to navigate between different categories of memory files.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
