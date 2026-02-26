"use client";

import { useState, useMemo } from "react";
import { SearchDocument, searchDocuments } from "../lib/search";

interface SearchBoxProps {
  documents: SearchDocument[];
}

export function SearchBox({ documents }: SearchBoxProps) {
  const [query, setQuery] = useState("");
  const [isOpen, setIsOpen] = useState(false);
  
  const filteredResults = useMemo(() => {
    if (!query.trim()) return [];
    return searchDocuments(documents, query).slice(0, 10);
  }, [query, documents]);
  
  const highlightMatch = (text: string, query: string) => {
    if (!query.trim()) return text;
    const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
    return text.replace(regex, '<mark class="bg-yellow-200 dark:bg-yellow-600">$1</mark>');
  };
  
  return (
    <div className="relative">
      <div className="relative">
        <svg 
          className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground"
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path 
            strokeLinecap="round" 
            strokeLinejoin="round" 
            strokeWidth={2} 
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" 
          />
        </svg>
        
        <input
          type="text"
          placeholder="Search memory..."
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setIsOpen(e.target.value.length > 0);
          }}
          onFocus={() => setIsOpen(query.length > 0)}
          className="w-full pl-10 pr-4 py-2 bg-card border border-border rounded-lg text-sm text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-ring"
        />
        {query && (
          <button
            onClick={() => {
              setQuery("");
              setIsOpen(false);
            }}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>
      
      {isOpen && filteredResults.length > 0 && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-card border border-border rounded-lg shadow-lg max-h-96 overflow-y-auto z-50">
          <div className="p-2 text-xs text-muted-foreground border-b border-border">
            {filteredResults.length} result{filteredResults.length !== 1 ? 's' : ''}
          </div>
          {filteredResults.map((result) => (
            <a
              key={result.path}
              href={`/view/${result.path}/`}
              onClick={() => setIsOpen(false)}
              className="block p-3 hover:bg-muted border-b border-border last:border-0"
            >
              <div className="flex items-center gap-2 mb-1">
                <span className="text-sm font-medium text-foreground"
                  dangerouslySetInnerHTML={{ 
                    __html: highlightMatch(result.name, query) 
                  }}
                />
                <span className="text-xs px-2 py-0.5 bg-muted text-muted-foreground rounded">
                  {result.category}
                </span>
                <span className="text-xs text-muted-foreground">
                  {result.matches} match{result.matches !== 1 ? 'es' : ''}
                </span>
              </div>
              <p 
                className="text-xs text-muted-foreground line-clamp-2"
                dangerouslySetInnerHTML={{ 
                  __html: highlightMatch(result.excerpt, query) 
                }}
              />
            </a>
          ))}
        </div>
      )}
      
      {isOpen && query && filteredResults.length === 0 && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-card border border-border rounded-lg shadow-lg p-4 text-center">
          <p className="text-sm text-muted-foreground">No results found for "{query}"</p>
        </div>
      )}
    </div>
  );
}
