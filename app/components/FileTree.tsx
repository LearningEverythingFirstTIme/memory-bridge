"use client";

import { useState } from "react";
import { ChevronRight, ChevronDown, FileText } from "lucide-react";

interface FileItem {
  name: string;
  path: string;
  category: string;
  lastModified: string;
}

interface Category {
  id: string;
  label: string;
  files: FileItem[];
}

interface FileTreeProps {
  categories: Category[];
}

export function FileTree({ categories }: FileTreeProps) {
  const [expanded, setExpanded] = useState<Set<string>>(
    () => new Set(categories.map(c => c.id))
  );

  const toggleCategory = (id: string) => {
    setExpanded((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  return (
    <nav className="flex-1 overflow-y-auto p-2">
      <ul className="space-y-1">
        {categories.map((category) => (
          <li key={category.id}>
            <button
              onClick={() => toggleCategory(category.id)}
              className="w-full flex items-center gap-2 px-2 py-1.5 text-sm font-medium text-muted-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground rounded-md transition-colors"
            >
              {expanded.has(category.id) ? (
                <ChevronDown className="w-4 h-4" />
              ) : (
                <ChevronRight className="w-4 h-4" />
              )}
              <span>{category.label}</span>
              <span className="ml-auto text-xs text-muted-foreground">
                {category.files.length}
              </span>
            </button>
            
            {expanded.has(category.id) && category.files.length > 0 && (
              <ul className="ml-4 mt-1 space-y-0.5">
                {category.files.map((file) => (
                  <li key={file.path}>
                    <a
                      href={`/view/${file.path}/`}
                      className="flex items-center gap-2 px-2 py-1.5 text-sm text-muted-foreground hover:text-sidebar-foreground hover:bg-sidebar-accent rounded-md transition-colors"
                    >
                      <FileText className="w-3.5 h-3.5 flex-shrink-0" />
                      <span className="truncate">{file.name}</span>
                    </a>
                  </li>
                ))}
              </ul>
            )}
          </li>
        ))}
      </ul>
    </nav>
  );
}
