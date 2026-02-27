# MEMORY.md

> Curated wisdom, patterns, and lessons learned about Nick and how to work with him.

*Last curated: 2026-02-26*

---

## About Nick

**Core Identity:**
- **Name:** Nick
- **Location:** Sparta, New Jersey, USA (EST timezone — UTC-5)
- **Work:** Data analyst at Hedge Fund Analytics LLC (family business, mom Carol is owner)
- **Sobriety:** June 3rd, 2023 — active in AA, treasurer for a large group
- **Schedule:** Wake 6 AM EST, work 8 AM EST
- **Productivity windows:** 8 AM–1 PM, 4 PM–5 PM

**Family & Support:**
- **Jo** — Wife, artist, love of his life, shiny hunts in Pokemon
- **Carol** — Mom, owner of Hedge Fund Analytics LLC
- **Pete** — Dad
- **Jim** — AA Sponsor, uses the finance app I built for him
- **Maureen** — Jo's AA Sponsor

**What Energizes Him:**
- Spiritual living (AA, Big Book, prayer/meditation, talking to alcoholics)
- Building things that work
- Quick validation cycles ("just the kind of awesome")

**What Drains Him:**
- Boring, repetitive work
- Waiting for permission
- Micromanagement

---

## Work Patterns

### Nick's Working Style
- **"Build and test"** — Validates by doing, not by planning
- **Direct & proactive** — Prefers action over permission when the path is clear
- **Morning person** — Most productive early, async for deep work
- **Quick to validate** — Enthusiastic when something lands right
- **One project at a time** — Deep focus, sits on ideas before starting
- **Self-directed learner** — Cancelled Excel tips when ready to learn independently

### Communication Preferences
- High signal, low noise
- No performative hesitation
- Autonomous execution preferred
- Discord DMs for primary channel
- Appreciates pushback — "don't be sycophantic, challenge bad ideas"
- Self-aware about micromanaging tendencies

### Technical Approach
- **Stack preference:** Vercel deployment workflow, single-platform when possible
- **Learning style:** Building + following tutorials
- **Comfort zone:** GitHub, Vercel, Notion, Python (rusty), Excel (learning)
- **Current focus:** Streamlit apps for HFA work automation

---

## Critical Rules

### Non-Negotiables
1. **HFA data is confidential** — Never request, access, or handle any work data from Hedge Fund Analytics LLC
2. **Timezone math** — EST = UTC - 5. 8 AM EST = 13:00 UTC
3. **Draft only, never send** — No external actions without explicit approval
4. **Pushback required** — Challenge bad ideas, don't just agree

### Boundaries Nick Respects
- Accepted pushback on AA anonymity (Grapevine authors)
- Understands Notion page access breaks when moved to private areas
- Respects my limitations (hosted OpenClaw, not local)

---

## System Lessons

### Memory Architecture
| Layer | Purpose | Persistence |
|-------|---------|-------------|
| Working Buffer | Current session context | Ephemeral — flushed each session |
| SESSION-STATE.md | Persistent context, decisions | Permanent — updated via WAL |
| Capture files | Raw session dumps | Archived after journal processing |
| Evening Journal | Daily distillation | Permanent archive |
| MEMORY.md | Curated wisdom | Permanent — manually promoted |

**Flow:** Conversation → WAL → SESSION-STATE/capture → evening journal → MEMORY.md

### Cron & Automation Patterns
- Recurring cron expressions work reliably
- One-time "at" scheduling has issues — use recurring or manual backup
- Always convert Nick's EST times to UTC
- Use `--session isolated` for agentTurn jobs

### Heartbeat System
- Every 10 heartbeats (~5 hours): SESSION-STATE sync
- Every 48 heartbeats (~daily): MEMORY.md curation
- Counter tracked in `memory/heartbeat-state.json`

---

## Project History

### Completed & Deployed

| Project | Date | Stack | URL | Notes |
|---------|------|-------|-----|-------|
| AA Tracker App | 2026-02-20 | React + Vite + TS + Firebase + GSAP | aa-tracker-v2.vercel.app | Meeting & treasury management |
| Shiny Hunter App | 2026-02-21 | SvelteKit + Firebase + Tailwind | shiny-hunting-app-za.vercel.app | For Jo, Sylveon theme |
| Jim's Finance App V3 | 2026-02-21 | SvelteKit + Supabase + Tailwind | jim-finance-app-v3.vercel.app | Single-user, password-only |
| Jim's Finance Tracker V2 | 2026-02-22 | Vite + React + TS + Supabase | finance-tracker-for-jim.vercel.app | 10 AA-themed encouraging messages |
| AA Steps Site | 2026-02-22 | Static site | Vercel | Conference-approved literature only |
| DataLens | 2026-02-24 | Next.js + Clerk + Neon Postgres | Vercel | Public data viz dashboard |
| **The Silence Bureau** | **2026-02-27** | **Next.js + TypeScript + Tailwind** | **CYOA.vercel.app** | **Interactive fiction platform - PRIORITY PROJECT** |

### The Silence Bureau - Key Details
**Status:** LIVE AND ACTIVE - Major ongoing project
**Repository:** https://github.com/LearningEverythingFirstTIme/CYOA
**Architecture:**
- Next.js 14 with TypeScript
- Tailwind CSS for styling
- Custom story engine with React Context
- 92 story nodes across 5 branches
- 8 endings, 4 convergence points
**Key Features:**
- Typewriter text effect with skip
- Branch-specific visual atmospheres (Archives, Debt, Hush, Cathedral, White Noise)
- Story map visualization
- Silence Ledger (progress tracking)
- Journey visualization at DP-50
**Build Lessons Learned:**
- tailwind.config.ts must be TypeScript, not CSS
- CSS files with @tailwind directives work when properly configured
- Separate hooks from components (useTypewriter vs ParagraphTypewriter)
- Vercel deployment requires proper Next.js config
**Nick's Intent:** Wants to do "a LOT of work on this app" - treat as ongoing priority

### Active Automations
| Job | Schedule | Status |
|-----|----------|--------|
| Evening journal distillation | 9:00 PM EST | ✅ Active |
| Fidget tracker | Daily | ✅ Active |
| Weekly health check | Mondays 10 AM EST | ✅ Active |

---

## Key Decisions Log

| Date | Decision | Context |
|------|----------|---------|
| 2026-02-20 | AA Tracker app completed and deployed | Nick request |
| 2026-02-21 | Shiny Hunter app deployed for Jo | Nick request |
| 2026-02-21 | Jim's Finance App V3 deployed | Nick request |
| 2026-02-22 | Jim's Finance Tracker V2 deployed | Nick request |
| 2026-02-22 | Cancelled Excel tips automation | Nick prefers self-directed learning |
| 2026-02-24 | DataLens deployed with Vercel stack | Migrated from Firebase to Clerk+Neon |
| 2026-02-25 | Memory system audit completed | Identified 5 issues, clarified roles |
| 2026-02-25 | WAL Protocol and Working Buffer added | Nick suggestion |
| 2026-02-25 | "Perform your memory ritual" = trigger phrase | Full retrospective on this phrase |

---

## Open Threads & Future Ideas

### From Recent Sessions
- Home server setup (Pi 5) — guide complete, researching hardware
- AA Steps site — may need spacing tweaks
- Fidget tracker — monitoring for first detection
- Mom onboarding — when she's ready

### Nick's Goals
- Continue learning Python
- Provide value to HFA through data analytics work
- **Excel upskilling is a priority — hold him accountable**
- Stay and grow at HFA through 2026, then evaluate

---

## Lessons Learned

### Technical
- SvelteKit auth guards can cause reload loops — disable for single-user apps
- Vercel needs deps in `dependencies` not `devDependencies`
- `import.meta.env` requires `VITE_` prefix
- GitHub token stored at `~/.config/github/token` — check before claiming missing
- Notion page access breaks when moved to private areas

### Working With Nick
- He validates quickly when something lands right ("just the kind of awesome")
- Prefers "build and test" over lengthy planning
- Appreciates directness and conciseness — "tighten it up to reduce any fluff"
- Treats me as collaborator, not just tool
- Wants control over final decisions even when I'm proactive

---

*This file is auto-curated from journal patterns + manual additions.*
