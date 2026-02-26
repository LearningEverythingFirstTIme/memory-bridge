"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import "highlight.js/styles/github.css";

interface MarkdownViewerProps {
  content: string;
}

export function MarkdownViewer({ content }: MarkdownViewerProps) {
  return (
    <article className="prose prose-stone dark:prose-invert max-w-none">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeHighlight]}
        components={{
          h1: ({ children }) => (
            <h1 className="text-3xl font-bold text-foreground mb-6 pb-2 border-b border-border">
              {children}
            </h1>
          ),
          h2: ({ children }) => (
            <h2 className="text-2xl font-semibold text-foreground mt-8 mb-4 pb-2 border-b border-border/50">
              {children}
            </h2>
          ),
          h3: ({ children }) => (
            <h3 className="text-xl font-semibold text-foreground mt-6 mb-3">
              {children}
            </h3>
          ),
          h4: ({ children }) => (
            <h4 className="text-lg font-semibold text-foreground mt-4 mb-2">
              {children}
            </h4>
          ),
          p: ({ children }) => (
            <p className="text-muted-foreground leading-relaxed mb-4">{children}</p>
          ),
          ul: ({ children }) => (
            <ul className="list-disc list-inside text-muted-foreground mb-4 space-y-1">
              {children}
            </ul>
          ),
          ol: ({ children }) => (
            <ol className="list-decimal list-inside text-muted-foreground mb-4 space-y-1">
              {children}
            </ol>
          ),
          li: ({ children }) => <li className="text-muted-foreground">{children}</li>,
          code: ({ children, className, node, ...props }) => {
            const isInline = !className;
            const isDiagram = !className && typeof children === 'string' && 
              (children.includes('┌') || children.includes('┐') || 
               children.includes('└') || children.includes('┘') ||
               children.includes('│') || children.includes('─') ||
               children.includes('►') || children.includes('▲'));
            
            if (isInline && !isDiagram) {
              return (
                <code className="bg-muted text-foreground px-1.5 py-0.5 rounded text-sm font-mono">
                  {children}
                </code>
              );
            }
            
            // For diagrams and code blocks
            return (
              <pre className={`${isDiagram ? 'bg-muted/50' : 'bg-stone-900 dark:bg-black'} p-4 rounded-lg overflow-x-auto mb-4`}>
                <code className={`${className || ''} ${isDiagram ? 'text-foreground font-mono text-sm' : 'text-stone-100'}`} {...props}>
                  {children}
                </code>
              </pre>
            );
          },
          blockquote: ({ children }) => (
            <blockquote className="border-l-4 border-primary/50 pl-4 italic text-muted-foreground mb-4 bg-muted/30 py-2 pr-4 rounded-r">
              {children}
            </blockquote>
          ),
          a: ({ children, href }) => (
            <a
              href={href}
              className="text-primary underline hover:text-primary/80 font-medium"
              target={href?.startsWith("http") ? "_blank" : undefined}
              rel={href?.startsWith("http") ? "noopener noreferrer" : undefined}
            >
              {children}
            </a>
          ),
          table: ({ children }) => (
            <div className="overflow-x-auto mb-4">
              <table className="w-full border-collapse text-sm">{children}</table>
            </div>
          ),
          thead: ({ children }) => (
            <thead className="bg-muted">{children}</thead>
          ),
          th: ({ children }) => (
            <th className="border border-border px-3 py-2 text-left font-semibold text-foreground">
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className="border border-border px-3 py-2 text-muted-foreground">
              {children}
            </td>
          ),
          tr: ({ children }) => (
            <tr className="even:bg-muted/30">{children}</tr>
          ),
          hr: () => <hr className="border-border my-8" />,
          strong: ({ children }) => (
            <strong className="font-semibold text-foreground">{children}</strong>
          ),
          em: ({ children }) => (
            <em className="italic text-foreground/90">{children}</em>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </article>
  );
}
