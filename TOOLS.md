# TOOLS.md - Tool Configuration & Notes

> Document tool-specific configurations, gotchas, and credentials here.

---

## Credentials Location

All credentials stored in `.credentials/` (gitignored):
- `example-api.txt` — Example API key
- **Brave API Key** — `BSAhhb3HcsUtwP7EmHVmUCeHZCV4yLh` (for web_search tool)

---

## Cron Tool — CRITICAL IMPLEMENTATION RULES

**Status:** ⚠️ Has issues with one-time "at" scheduling — use workarounds

### THE PROBLEM

The cron scheduler's automatic wake/heartbeat **does not reliably fire one-time "at" scheduled jobs**. Recurring cron jobs work fine, but "at" jobs are often missed.

**Evidence:**
- Recurring jobs (daily-excel-tips, email-checks) execute correctly
- One-time "at" jobs frequently fail to fire automatically
- Manual `cron run` works, automatic scheduling doesn't

### WORKING SOLUTIONS

**Option 1: Use recurring cron expressions (MOST RELIABLE)**
```json
{
  "schedule": {
    "kind": "cron",
    "expr": "0 8 * * *",
    "tz": "America/New_York"
  }
}
```

**Option 2: For one-time reminders — manually trigger via `cron run`**
```bash
# After creating the job, immediately run it if needed soon
# OR check back and run manually when time arrives
```

**Option 3: Use external scheduling (cron job on host)**
Consider using the host's crontab to trigger reminders via API or messaging.

### IF YOU MUST USE "at" SCHEDULING

1. **Always verify `nextRunAtMs` in the response**
2. **Check back at the scheduled time and manually run if needed:**
   ```bash
   cron run --jobId <job-id>
   ```
3. **Set `deleteAfterRun: true` so they clean up after manual run**

### TIMEZONE HANDLING (Still Critical)

**Server runs on UTC. Nick is EST (UTC-5). ALWAYS convert.**
- EST = UTC - 5 hours (EST offset is -5)
- When Nick says "8 AM EST", schedule for `13:00:00Z`
- For "in X minutes": Current UTC time + X minutes

### CORRECT JOB STRUCTURE

```json
{
  "name": "descriptive-name",
  "schedule": {
    "kind": "cron",
    "expr": "0 8 * * *",
    "tz": "America/New_York"
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Use message tool with explicit target channel",
    "model": "kimi-coding/k2p5"
  },
  "delivery": {
    "channel": "discord",
    "mode": "announce",
    "to": "channel:1474399095279063150"
  },
  "notify": true
}
```

### Nick's Active Reminders (Recurring = Working)
- ✅ Daily Excel tips: 7 AM EST (cron)
- ✅ Email checks: 8/11/2/5 PM EST (cron)
- ⚠️ AA tablecloths: Sunday 9 AM EST (one-time — may need manual run)
- ⚠️ AA cake pickup: Friday 4 PM EST (one-time — may need manual run)

### RECOMMENDATION

**For important reminders:** Use recurring cron expressions or set a manual backup check. Don't rely solely on "at" scheduling for critical reminders.

---

## [Tool Name]

**Status:** ✅ Working | ⚠️ Issues | ❌ Not configured

**Configuration:**
```
Key details about how this tool is configured
```

**Gotchas:**
- Things that don't work as expected
- Workarounds discovered

**Common Operations:**
```bash
# Example command
tool-name --common-flag
```

---

## Writing Preferences

[Document any preferences about writing style, voice, etc.]

---

## What Goes Here

- Tool configurations and settings
- Credential locations (not the credentials themselves!)
- Gotchas and workarounds discovered
- Common commands and patterns
- Integration notes

## Why Separate?

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

---

*Add whatever helps you do your job. This is your cheat sheet.*
