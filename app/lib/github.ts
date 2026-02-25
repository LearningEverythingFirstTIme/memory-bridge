import fs from "fs";
import path from "path";

const MEMORY_DIR = path.join(process.cwd(), "memory");

export interface FileItem {
  name: string;
  path: string;
  category: string;
  lastModified: string;
  size?: number;
}

function getCategoryFromPath(filePath: string): string {
  const parts = filePath.split("/");
  const filename = parts[parts.length - 1];
  
  if (filename === "SESSION-STATE.md") return "state";
  if (filename === "MEMORY.md") return "memory";
  if (filePath.startsWith("journal/")) return "journal";
  if (filePath.startsWith("capture/")) return "capture";
  return "notes";
}

function getAllFilesRecursive(dir: string, basePath: string = ""): FileItem[] {
  const files: FileItem[] = [];
  
  try {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      const relativePath = basePath ? `${basePath}/${entry.name}` : entry.name;
      
      if (entry.isDirectory()) {
        files.push(...getAllFilesRecursive(fullPath, relativePath));
      } else if (entry.name.endsWith(".md")) {
        const stats = fs.statSync(fullPath);
        files.push({
          name: entry.name,
          path: relativePath.replace(".md", ""),
          category: getCategoryFromPath(relativePath),
          lastModified: stats.mtime.toISOString(),
          size: stats.size,
        });
      }
    }
  } catch (e) {
    console.error(`Error reading directory ${dir}:`, e);
  }
  
  return files;
}

export function getAllFiles(): FileItem[] {
  const files = getAllFilesRecursive(MEMORY_DIR);
  
  // Sort by category then by name (descending for dates)
  return files.sort((a, b) => {
    if (a.category !== b.category) {
      return a.category.localeCompare(b.category);
    }
    return b.name.localeCompare(a.name);
  });
}

export function getFileContent(filePath: string): string | null {
  try {
    const fullPath = path.join(MEMORY_DIR, `${filePath}.md`);
    return fs.readFileSync(fullPath, "utf-8");
  } catch (e) {
    console.error(`Error reading file ${filePath}:`, e);
    return null;
  }
}

export function getLastSynced(): string {
  try {
    const stats = fs.statSync(MEMORY_DIR);
    return stats.mtime.toLocaleString();
  } catch (e) {
    return "Unknown";
  }
}
