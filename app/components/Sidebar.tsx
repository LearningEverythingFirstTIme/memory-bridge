"use client";

import { ThemeToggle } from "./ThemeToggle";
import { FileTree } from "./FileTree";
import { SearchBox } from "./SearchBox";
import { SearchDocument } from "../lib/search";

interface SidebarProps {
  searchDocuments: SearchDocument[];
  categories: { id: string; label: string; files: { path: string; name: string; lastModified: string; category: string }[] }[];
  lastSynced: string;
  showHomeLink?: boolean;
}

export function Sidebar({ searchDocuments, categories, lastSynced, showHomeLink }: SidebarProps) {
  return (
    <aside className="w-72 bg-sidebar border-r border-sidebar-border flex flex-col fixed h-full">
      <div className="p-4 border-b border-sidebar-border flex items-center justify-between">
        <div>
          {showHomeLink ? (
            <a href="/" className="block">
              <h1 className="text-lg font-semibold text-sidebar-foreground">Memory Bridge</h1>
            </a>
          ) : (
            <h1 className="text-lg font-semibold text-sidebar-foreground">Memory Bridge</h1>
          )}
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
  );
}
