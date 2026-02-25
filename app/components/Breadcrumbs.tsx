"use client";

import { ChevronRight, Home } from "lucide-react";

interface BreadcrumbsProps {
  path: string;
}

export function Breadcrumbs({ path }: BreadcrumbsProps) {
  const segments = path.split("/").filter(Boolean);

  return (
    <nav className="flex items-center gap-2 text-sm text-stone-500 mb-6">
      <a
        href="/"
        className="flex items-center gap-1 hover:text-stone-700 transition-colors"
      >
        <Home className="w-4 h-4" />
        <span>Home</span>
      </a>
      
      {segments.map((segment, index) => {
        const isLast = index === segments.length - 1;
        const href = "/" + segments.slice(0, index + 1).join("/") + "/";
        
        return (
          <div key={index} className="flex items-center gap-2">
            <ChevronRight className="w-4 h-4" />
            {isLast ? (
              <span className="text-stone-800 font-medium">{segment}</span>
            ) : (
              <a
                href={href}
                className="hover:text-stone-700 transition-colors"
              >
                {segment}
              </a>
            )}
          </div>
        );
      })}
    </nav>
  );
}
