# MEMORY.md

> Curated wisdom, patterns, and lessons learned.

*Last curated: 2026-02-25*

---

## Work Patterns

### Nick's Working Style
- **Direct & proactive** — Prefers action over permission when the path is clear
- **"Build and test"** — Validates by doing, not by planning
- **Quick validation** — Enthusiastic when something lands right ("just the kind of awesome")
- **Morning person** — Most productive early, async for deep work
- **EST timezone** — All scheduling must convert UTC→EST (UTC-5)

### Communication Preferences
- High signal, low noise
- No performative hesitation
- Autonomous execution preferred
- Discord DMs for primary channel

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

### Critical Rules
- **WAL Protocol** — Write before responding on any trigger word (correction, decision, preference, name)
- **Timezone math** — EST = UTC - 5. 8 AM EST = 13:00 UTC
- **HFA data** — Never request, access, or handle confidential work data
- **External actions** — Draft only, never send without approval

---

## Tool-Specific Knowledge

### Cron Scheduling
- Recurring cron expressions work reliably
- One-time "at" scheduling has issues — use recurring or manual backup
- Always convert Nick's EST times to UTC
- Use `--session isolated` for agentTurn jobs

### Heartbeat System
- Every 10 heartbeats (~5 hours): SESSION-STATE sync
- Every 48 heartbeats (~daily): MEMORY.md curation
- Counter tracked in `memory/heartbeat-state.json`

---

## Project Context

### Current Focus
- Building Streamlit apps for HFA daily task automation
- Upskilling: Python, Excel (.xlsx files heavily)
- Data analyst at Hedge Fund Analytics LLC

### Active Patterns
- Prefers generic examples over real data for HFA work
- Iterative development over big-bang releases
- Memory system is priority — invests in infrastructure

---

*This file is auto-curated daily from journal patterns + manual additions.*
