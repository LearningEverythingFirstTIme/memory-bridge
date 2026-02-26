import fs from "fs";
import path from "path";

const MEMORY_DIR = path.join(process.cwd(), "memory");
const ROOT_DIR = process.cwd();

export interface FileItem {
  name: string;
  path: string;
  category: string;
  lastModified: string;
  size?: number;
}

function getCategoryFromPath(filePath: string, isRoot: boolean = false): string {
  const parts = filePath.split("/");
  const filename = parts[parts.length - 1];
  
  // Root-level documentation files
  if (isRoot) {
    if (filename === "SESSION-STATE.md") return "state";
    if (filename === "MEMORY.md") return "memory";
    return "docs";
  }
  
  // Memory folder files
  if (filename === "SESSION-STATE.md") return "state";
  if (filename === "MEMORY.md") return "memory";
  if (filePath.startsWith("journal/")) return "journal";
  if (filePath.startsWith("capture/")) return "capture";
  if (filePath.startsWith("scripts/")) return "scripts";
  if (filePath.startsWith("reports/")) return "reports";
  return "notes";
}

function getAllFilesRecursive(dir: string, basePath: string = "", isRoot: boolean = false): FileItem[] {
  const files: FileItem[] = [];
  
  try {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      const relativePath = basePath ? `${basePath}/${entry.name}` : entry.name;
      
      if (entry.isDirectory()) {
        // Skip node_modules and hidden directories
        if (entry.name.startsWith(".") || entry.name === "node_modules") continue;
        files.push(...getAllFilesRecursive(fullPath, relativePath, isRoot));
      } else if (entry.name.endsWith(".md") || entry.name.endsWith(".py") || entry.name.endsWith(".sh")) {
        const stats = fs.statSync(fullPath);
        files.push({
          name: entry.name,
          path: relativePath.replace(/\.md$/, "").replace(/\.py$/, "").replace(/\.sh$/, ""),
          category: getCategoryFromPath(relativePath, isRoot),
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

function getRootDocs(): FileItem[] {
  const files: FileItem[] = [];
  const docFiles = ["AGENTS.md", "HEARTBEAT.md", "IDENTITY.md", "MEMORY-QUICKREF.md", "SOUL.md", "TOOLS.md", "USER.md"];
  
  for (const filename of docFiles) {
    const fullPath = path.join(ROOT_DIR, filename);
    if (fs.existsSync(fullPath)) {
      const stats = fs.statSync(fullPath);
      files.push({
        name: filename,
        path: filename.replace(".md", ""),
        category: "docs",
        lastModified: stats.mtime.toISOString(),
        size: stats.size,
      });
    }
  }
  
  return files;
}

function getScripts(): FileItem[] {
  const scriptsDir = path.join(ROOT_DIR, "scripts");
  const files: FileItem[] = [];
  
  try {
    if (fs.existsSync(scriptsDir)) {
      const entries = fs.readdirSync(scriptsDir, { withFileTypes: true });
      for (const entry of entries) {
        if (entry.isFile() && (entry.name.endsWith(".py") || entry.name.endsWith(".sh"))) {
          const fullPath = path.join(scriptsDir, entry.name);
          const stats = fs.statSync(fullPath);
          files.push({
            name: entry.name,
            path: `scripts/${entry.name.replace(/\.py$/, "").replace(/\.sh$/, "")}`,
            category: "scripts",
            lastModified: stats.mtime.toISOString(),
            size: stats.size,
          });
        }
      }
    }
  } catch (e) {
    console.error("Error reading scripts directory:", e);
  }
  
  return files;
}

function getReports(): FileItem[] {
  const reportsDir = path.join(ROOT_DIR, "reports");
  const files: FileItem[] = [];
  
  try {
    if (fs.existsSync(reportsDir)) {
      const entries = fs.readdirSync(reportsDir, { withFileTypes: true });
      for (const entry of entries) {
        if (entry.isFile() && (entry.name.endsWith(".md") || entry.name.endsWith(".json"))) {
          const fullPath = path.join(reportsDir, entry.name);
          const stats = fs.statSync(fullPath);
          files.push({
            name: entry.name,
            path: `reports/${entry.name.replace(/\.md$/, "").replace(/\.json$/, "")}`,
            category: "reports",
            lastModified: stats.mtime.toISOString(),
            size: stats.size,
          });
        }
      }
    }
  } catch (e) {
    console.error("Error reading reports directory:", e);
  }
  
  return files;
}

export function getAllFiles(): FileItem[] {
  const memoryFiles = getAllFilesRecursive(MEMORY_DIR);
  const rootDocs = getRootDocs();
  const scripts = getScripts();
  const reports = getReports();
  
  const allFiles = [...memoryFiles, ...rootDocs, ...scripts, ...reports];
  
  // Sort by category then by name (descending for dates)
  return allFiles.sort((a, b) => {
    if (a.category !== b.category) {
      return a.category.localeCompare(b.category);
    }
    return b.name.localeCompare(a.name);
  });
}

export function getFileContent(filePath: string): string | null {
  try {
    // Try multiple locations
    const possiblePaths = [
      path.join(MEMORY_DIR, `${filePath}.md`),
      path.join(MEMORY_DIR, `${filePath}.py`),
      path.join(MEMORY_DIR, `${filePath}.sh`),
      path.join(MEMORY_DIR, `${filePath}.json`),
      path.join(ROOT_DIR, `${filePath}.md`),
      path.join(ROOT_DIR, `${filePath}.py`),
      path.join(ROOT_DIR, `${filePath}.sh`),
      path.join(ROOT_DIR, `${filePath}.json`),
      path.join(ROOT_DIR, `${filePath}`), // For scripts/reports subdirs
    ];
    
    for (const fullPath of possiblePaths) {
      if (fs.existsSync(fullPath)) {
        return fs.readFileSync(fullPath, "utf-8");
      }
    }
    
    return null;
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
