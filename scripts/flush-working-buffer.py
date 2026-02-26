#!/usr/bin/env python3
"""
Working Buffer Auto-Flush Script

Checks if working-buffer.md is stale (>24h old) and flushes it to capture file.
Run this before evening journal generation or during health checks.
"""

import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
WORKING_BUFFER = WORKSPACE / "working-buffer.md"
CAPTURE_DIR = WORKSPACE / "memory" / "capture"

STALE_HOURS = 24


def parse_working_buffer():
    """Extract WAL entries from working buffer."""
    if not WORKING_BUFFER.exists():
        return []
    
    content = WORKING_BUFFER.read_text(encoding='utf-8')
    entries = []
    
    # Find Recent WAL Entries section
    wal_match = re.search(r'## Recent WAL Entries\n(.+?)(?=\n##|\Z)', content, re.DOTALL)
    if wal_match:
        section = wal_match.group(1)
        # Parse entries like: - [HH:MM] [tag] Content
        pattern = r'- \[(\d{2}:\d{2})\] \[(\w+)\] (.+)'
        matches = re.findall(pattern, section)
        for time_str, tag, content_text in matches:
            entries.append({
                'time': time_str,
                'tag': tag,
                'content': content_text.strip()
            })
    
    return entries


def is_buffer_stale():
    """Check if working buffer is older than STALE_HOURS."""
    if not WORKING_BUFFER.exists():
        return False
    
    mtime = datetime.fromtimestamp(WORKING_BUFFER.stat().st_mtime, tz=timezone.utc)
    age = datetime.now(timezone.utc) - mtime
    return age.total_seconds() > (STALE_HOURS * 3600)


def flush_to_capture(entries):
    """Append entries to today's capture file."""
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    capture_file = CAPTURE_DIR / f"{today}.md"
    
    # Create capture file if it doesn't exist
    CAPTURE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Append entries
    with open(capture_file, 'a', encoding='utf-8') as f:
        f.write("\n# Auto-flushed from Working Buffer\n")
        for entry in entries:
            f.write(f"- [{entry['time']}] [{entry['tag']}] {entry['content']}\n")
    
    return capture_file


def reset_working_buffer():
    """Reset working buffer to template."""
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    now = datetime.now(timezone.utc).strftime('%H:%M')
    
    template = f"""# Working Buffer — {today}

> Active session context. Flush to capture file when context switches or session ends.

## Current Task

## Session Timeline

## Blockers

## Decisions Pending

## What Would Help Right Now

## Open Loops

## Recent WAL Entries

---

*Flush to memory/capture/{today}.md when session ends or context switches*
"""
    
    WORKING_BUFFER.write_text(template, encoding='utf-8')


def main():
    try:
        print(f"Working Buffer Auto-Flush Check")
        print(f"Buffer file: {WORKING_BUFFER}")
        print(f"Stale threshold: {STALE_HOURS} hours")
        print()
        
        if not WORKING_BUFFER.exists():
            print("❌ Working buffer does not exist")
            return 1
        
        mtime = datetime.fromtimestamp(WORKING_BUFFER.stat().st_mtime, tz=timezone.utc)
        age = datetime.now(timezone.utc) - mtime
        print(f"Buffer age: {age.total_seconds() / 3600:.1f} hours")
        
        if not is_buffer_stale():
            print(f"✅ Buffer is fresh (not stale)")
            return 0
        
        print(f"⚠️  Buffer is stale (>{STALE_HOURS}h old)")
        print()
        
        # Parse entries
        entries = parse_working_buffer()
        
        if not entries:
            print("No WAL entries found in buffer")
            print("Resetting buffer...")
            reset_working_buffer()
            print("✅ Buffer reset")
            return 0
        
        print(f"Found {len(entries)} WAL entries to flush")
        
        # Flush to capture
        capture_file = flush_to_capture(entries)
        print(f"✅ Flushed to {capture_file}")
        
        # Reset buffer
        reset_working_buffer()
        print(f"✅ Working buffer reset")
        
        print()
        print("Flush complete!")
        return 0
        
    except Exception as e:
        print(f"❌ Error flushing working buffer: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
