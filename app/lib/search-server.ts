// Server-side search document builder
// Only import this in server components (page.tsx)

import { getAllFiles, getFileContent } from "./github";
import { SearchDocument } from "./search";

export type { SearchDocument } from "./search";

// Build search documents at build time (serializable)
export function buildSearchDocuments(): SearchDocument[] {
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
  
  return documents;
}
