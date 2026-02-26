// Client-side search functions only
// This file can be imported by both server and client components

export interface SearchResult {
  path: string;
  name: string;
  category: string;
  excerpt: string;
  matches: number;
}

export interface SearchDocument {
  path: string;
  name: string;
  category: string;
  content: string;
}

// Client-side search function
export function searchDocuments(documents: SearchDocument[], query: string): SearchResult[] {
  const normalizedQuery = query.toLowerCase().trim();
  if (!normalizedQuery) return [];
  
  const results: SearchResult[] = [];
  
  for (const doc of documents) {
    const matches = countMatches(doc.content, normalizedQuery);
    
    if (matches > 0) {
      results.push({
        path: doc.path,
        name: doc.name,
        category: doc.category,
        excerpt: generateExcerpt(doc.content, normalizedQuery),
        matches,
      });
    }
  }
  
  // Sort by relevance (most matches first)
  return results.sort((a, b) => b.matches - a.matches);
}

function countMatches(content: string, query: string): number {
  let count = 0;
  let pos = 0;
  while ((pos = content.indexOf(query, pos)) !== -1) {
    count++;
    pos += query.length;
  }
  return count;
}

function generateExcerpt(content: string, query: string): string {
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
