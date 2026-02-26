# Memory System Quick Reference

> Read this at the start of every new session to orient yourself.

## The Core Idea

I wake up fresh each session. These files are my continuity. I don't remember conversations automatically — I write down what matters and read it back.

---

## Session Startup Routine

**Always read in this order:**
1. `SOUL.md` — Who I am, how I operate
2. `USER.md` — Who Nick is, his context and goals
3. `memory/journal/YYYY-MM-DD.md` — Yesterday's distilled summary (read first!)
4. `SESSION-STATE.md` — Persistent context (projects, profile, services)
5. `memory/capture/*.md` — Newest capture file (if exists)
6. `working-buffer.md` — Only if session is continuing (not new)

**Don't read working-buffer.md for new sessions** — it's session-local context that was already flushed.

---

## How Memory Flows

```
Observation → Capture (WAL) → Storage → Distillation → Retrieval
```

**WAL Protocol** (Write-Ahead Logging):
- When something significant happens, write it down *immediately*
- Use tags: `[decision]`, `[friction]`, `[win]`, `[idea]`, `[mood]`, `[question]`, `[open-loop]`, `[note]`
- Format: `- [HH:MM] [tag] Content`
- Destination: `memory/capture/YYYY-MM-DD.md`

**Storage Layers:**
- `memory/capture/*.md` — Raw ephemeral captures
- `memory/YYYY-MM-DD.md` — Daily raw logs
- `memory/journal/*.md` — Distilled evening journals (auto-generated 9 PM EST)
- `MEMORY.md` — Curated long-term wisdom
- `notes/` — PARA structure (Projects, Areas, Resources, Archive)

---

## Key Files

| File | Purpose | Update Frequency | Persistence |
|------|---------|------------------|-------------|
| `SESSION-STATE.md` | **Persistent context** — Nick's profile, active projects, completed projects, connected services | Auto-sync every ~5h | Permanent |
| `working-buffer.md` | **Session-local context** — current task, session timeline, recent WAL entries | Continuous | Ephemeral (flushed each session) |
| `MEMORY.md` | Long-term curated memory | Manual | Permanent |
| `AGENTS.md` | Operating rules | When lessons learned | Permanent |

**Critical distinction:**
- **SESSION-STATE** = What should I know about Nick? (durable, synced)
- **Working Buffer** = What are we doing right now? (disposable, session-only)

---

## Automation

- **Evening journal:** 9 PM EST — distills captures into structured journal
- **SESSION-STATE sync:** Every 10 heartbeats (~5 hours)
- **Working buffer flush:** If >24h old
- **Health check:** Mondays 10 AM EST

---

## What to Remember About Nick

- Data analyst at Hedge Fund Analytics LLC
- Learning Python, building Streamlit apps
- Excel upskilling needed — **hold him accountable**
- Sobriety date: June 3rd, 2023 — active in AA, treasurer
- Wife: Jo (artist, shiny hunts Pokemon)
- Morning person (6 AM wake, 8 AM work)
- Wants extreme proactivity, Discord DMs preferred
- **HFA data is confidential** — never request it

---

## Active Projects (check SESSION-STATE.md for current status)

- AA Tracker App — deployed, Firebase
- Shiny Pokemon Hunter — deployed for Jo, SvelteKit
- Jim's Finance Apps — two versions deployed (SvelteKit + React)

---

## If Context Is Truncated

**Trigger:** You see `<summary>` tag, "context truncated", or Nick asks "where were we?"

**Recovery steps:**
1. **Read `working-buffer.md`** — it has the session timeline and recent WAL entries
2. **Check `SESSION-STATE.md`** — for active project context
3. **Present:** "Context was truncated. Last task was [X]. Continue?"

**Don't ask "what were we doing?"** — the buffer has the answer.

---

## The Rule

**Text > Brain.** If it feels like "I'll remember this," write it down *now*.

---

*Last updated: 2026-02-25*
