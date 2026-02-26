import fs from "fs";
import path from "path";
import { getAllFiles, getFileContent } from "./github";

export interface SearchResult {
  path: string;
  name: string;
  category: string;
  excerpt: string;
  matches: number;
}

// Build search index at build time
export function buildSearchIndex(): SearchIndex {
  const files = getAllFiles();
  const documents: SearchDocument[] = [];
  
  for (const file of files) {
    const content = getFileContent(file.path);
    if (content) {
      documents.push({
        path: file.path,
        name: file.name,
        category: file.category,
        content: content.toLowerCase(),
      });
    }
  }
  
  return new SearchIndex(documents);
}

interface SearchDocument {
  path: string;
  name: string;
  category: string;
  content: string;
}

class SearchIndex {
  constructor(private documents: SearchDocument[]) {}
  
  search(query: string): SearchResult[] {
    const normalizedQuery = query.toLowerCase().trim();
    if (!normalizedQuery) return [];
    
    const results: SearchResult[] = [];
    
    for (const doc of this.documents) {
      const matches = this.countMatches(doc.content, normalizedQuery);
      
      if (matches > 0) {
        results.push({
          path: doc.path,
          name: doc.name,
          category: doc.category,
          excerpt: this.generateExcerpt(doc.content, normalizedQuery),
          matches,
        });
      }
    }
    
    // Sort by relevance (most matches first)
    return results.sort((a, b) => b.matches - a.matches);
  }
  
  private countMatches(content: string, query: string): number {
    let count = 0;
    let pos = 0;
    while ((pos = content.indexOf(query, pos)) !== -1) {
      count++;
      pos += query.length;
    }
    return count;
  }
  
  private generateExcerpt(content: string, query: string): string {
    const queryPos = content.indexOf(query);
    if (queryPos === -1) return content.slice(0, 150) + "...";
    
    // Find start of excerpt (100 chars before query, or start of content)
    let start = Math.max(0, queryPos - 100);
    // Adjust to start at word boundary
    while (start > 0 && content[start] !== ' ' && content[start] !== '\n') {
      start--;
    }
    
    // Find end of excerpt (200 chars total)
    let end = Math.min(content.length, start + 200);
    // Adjust to end at word boundary
    while (end < content.length && content[end] !== ' ' && content[end] !== '\n') {
      end++;
    }
    
    let excerpt = content.slice(start, end).trim();
    if (start > 0) excerpt = "..." + excerpt;
    if (end < content.length) excerpt = excerpt + "...";
    
    return excerpt;
  }
}

// Singleton instance for static generation
let searchIndex: SearchIndex | null = null;

export function getSearchIndex(): SearchIndex {
  if (!searchIndex) {
    searchIndex = buildSearchIndex();
  }
  return searchIndex;
}
