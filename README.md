# Memory Bridge

A read-only Markdown viewer for Kimi Claw's memory system. Files are synced daily from the VPS to GitHub and rendered as a clean, archival web interface.

**Live Demo:** https://memory-bridge.vercel.app (after deployment)

## 🧠 Core Memory Files

These 5 files are loaded at the start of every session:

| Priority | File | Purpose | Loaded In |
|----------|------|---------|-----------|
| 1️⃣ | `SOUL.md` | Identity, personality, operating principles | All sessions |
| 2️⃣ | `USER.md` | Nick's profile, preferences, context | All sessions |
| 3️⃣ | `IDENTITY.md` | How we work together | All sessions |
| 4️⃣ | `memory/YYYY-MM-DD.md` | Today + yesterday's raw logs | All sessions |
| 5️⃣ | `MEMORY.md` | Curated long-term memory | **Main sessions only** |

> 🔒 **Security note:** MEMORY.md is excluded from shared contexts (Discord, group chats) to prevent leaking personal context.

## Features

- **Clean, archival aesthetic** — Stone color palette, minimal design
- **Organized navigation** — Files grouped by category (State, Memory, Journal, Capture, Notes)
- **Syntax highlighting** — Code blocks rendered with highlight.js
- **Static export** — Ready for Vercel deployment
- **No auth required** — Read-only access

## File Structure

```
memory/
├── SESSION-STATE.md      # → State category
├── MEMORY.md             # → Memory category
├── journal/
│   └── YYYY-MM-DD.md     # → Journal category
├── capture/
│   └── YYYY-MM-DD.md     # → Capture category
└── YYYY-MM-DD.md         # → Daily Notes category
```

## Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

## Deployment

### Option 1: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### Option 2: GitHub + Vercel

1. Push this repo to GitHub
2. Connect repo to Vercel
3. Deploy automatically on every push

## Sync Script

To sync memory files from VPS to this repo:

```bash
./scripts/sync.sh
```

This copies files from:
- `/root/.openclaw/workspace/SESSION-STATE.md`
- `/root/.openclaw/workspace/MEMORY.md`
- `/root/.openclaw/workspace/memory/journal/*.md`
- `/root/.openclaw/workspace/memory/capture/*.md`
- `/root/.openclaw/workspace/memory/*.md`

After syncing, commit and push to update the web archive.

## Tech Stack

- Next.js 16 (App Router)
- TypeScript
- Tailwind CSS
- react-markdown + remark-gfm + rehype-highlight
- Lucide icons

## License

MIT
