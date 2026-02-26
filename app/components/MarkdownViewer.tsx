"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import "highlight.js/styles/github.css";
import "highlight.js/styles/github-dark.css";

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
            <h2 className="text-2xl font-semibold text-foreground mt-8 mb-4">
              {children}
            </h2>
          ),
          h3: ({ children }) => (
            <h3 className="text-xl font-semibold text-foreground mt-6 mb-3">
              {children}
            </h3>
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
          code: ({ children, className }) => {
            const isInline = !className;
            return isInline ? (
              <code className="bg-muted text-foreground px-1.5 py-0.5 rounded text-sm font-mono">
                {children}
              </code>
            ) : (
              <pre className="bg-stone-900 dark:bg-black text-stone-100 p-4 rounded-lg overflow-x-auto mb-4">
                <code className={className}>{children}</code>
              </pre>
            );
          },
          blockquote: ({ children }) => (
            <blockquote className="border-l-4 border-border pl-4 italic text-muted-foreground mb-4">
              {children}
            </blockquote>
          ),
          a: ({ children, href }) => (
            <a
              href={href}
              className="text-foreground underline hover:text-primary"
              target={href?.startsWith("http") ? "_blank" : undefined}
              rel={href?.startsWith("http") ? "noopener noreferrer" : undefined}
            >
              {children}
            </a>
          ),
          table: ({ children }) => (
            <table className="w-full border-collapse mb-4">{children}</table>
          ),
          thead: ({ children }) => (
            <thead className="bg-muted">{children}</thead>
          ),
          th: ({ children }) => (
            <th className="border border-border px-4 py-2 text-left font-semibold text-foreground">
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className="border border-border px-4 py-2 text-muted-foreground">
              {children}
            </td>
          ),
          hr: () => <hr className="border-border my-6" />,
        }}
      >
        {content}
      </ReactMarkdown>
    </article>
  );
}
