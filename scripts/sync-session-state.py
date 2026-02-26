#!/usr/bin/env python3
"""
SESSION-STATE Auto-Sync Script

Automatically updates SESSION-STATE.md based on recent activity.
Designed to run periodically (e.g., every N heartbeats).

Usage:
    python3 scripts/sync-session-state.py [--dry-run]
"""

import os
import re
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
CAPTURE_DIR = MEMORY_DIR / "capture"
JOURNAL_DIR = MEMORY_DIR / "journal"
SESSION_STATE = WORKSPACE / "SESSION-STATE.md"

# How far back to look for activity
LOOKBACK_DAYS = 2


def parse_wal_entries(filepath):
    """Extract WAL entries from a capture file."""
    entries = []
    if not filepath.exists():
        return entries
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match pattern: - [HH:MM] [tag] Content
    pattern = r'- \[(\d{2}:\d{2})\] \[(\w+)\] (.+)'
    matches = re.findall(pattern, content)
    
    for time_str, tag, content in matches:
        entries.append({
            'time': time_str,
            'tag': tag,
            'content': content.strip()
        })
    
    return entries


def extract_recent_decisions():
    """Extract recent decisions from captures and journals."""
    decisions = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=LOOKBACK_DAYS)
    
    # Check capture files
    for capture_file in CAPTURE_DIR.glob("*.md"):
        if capture_file.name.endswith('.archived.md'):
            continue
        
        mtime = datetime.fromtimestamp(capture_file.stat().st_mtime, tz=timezone.utc)
        if mtime < cutoff:
            continue
        
        entries = parse_wal_entries(capture_file)
        for entry in entries:
            if entry['tag'] == 'decision':
                decisions.append({
                    'date': capture_file.stem,
                    'time': entry['time'],
                    'content': entry['content']
                })
    
    # Check journal files
    for journal_file in JOURNAL_DIR.glob("*.md"):
        mtime = datetime.fromtimestamp(journal_file.stat().st_mtime, tz=timezone.utc)
        if mtime < cutoff:
            continue
        
        with open(journal_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract decisions section
        decisions_match = re.search(r'## Decisions\n\n(.+?)(?=\n##|\Z)', content, re.DOTALL)
        if decisions_match:
            section = decisions_match.group(1)
            for line in section.split('\n'):
                if line.strip().startswith('- '):
                    decisions.append({
                        'date': journal_file.stem,
                        'time': 'journal',
                        'content': line.strip()[2:]
                    })
    
    return decisions


def extract_open_loops():
    """Extract open loops from recent captures."""
    open_loops = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=LOOKBACK_DAYS)
    
    for capture_file in CAPTURE_DIR.glob("*.md"):
        if capture_file.name.endswith('.archived.md'):
            continue
        
        mtime = datetime.fromtimestamp(capture_file.stat().st_mtime, tz=timezone.utc)
        if mtime < cutoff:
            continue
        
        entries = parse_wal_entries(capture_file)
        for entry in entries:
            if entry['tag'] == 'open-loop':
                open_loops.append({
                    'date': capture_file.stem,
                    'content': entry['content']
                })
    
    return open_loops


def read_current_session_state():
    """Read current SESSION-STATE.md content."""
    if not SESSION_STATE.exists():
        return ""
    
    with open(SESSION_STATE, 'r', encoding='utf-8') as f:
        return f.read()


def update_session_state(dry_run=False):
    """Update SESSION-STATE.md with recent activity."""
    current_content = read_current_session_state()
    
    # Extract recent activity
    recent_decisions = extract_recent_decisions()
    open_loops = extract_open_loops()
    
    # Build updates
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    now = datetime.now(timezone.utc).strftime('%H:%M')
    
    updates = []
    updates.append(f"\n## Auto-Sync Update — {today} {now} UTC\n")
    
    # Add recent decisions
    if recent_decisions:
        updates.append("### Recent Decisions\n")
        for d in recent_decisions[-5:]:  # Last 5 decisions
            updates.append(f"- [{d['date']} {d['time']}] {d['content']}")
        updates.append("")
    
    # Add open loops
    if open_loops:
        updates.append("### Active Open Loops\n")
        for loop in open_loops[-5:]:
            updates.append(f"- [ ] {loop['date']}: {loop['content']}")
        updates.append("")
    
    # Update timestamp in header
    updated_content = re.sub(
        r'\*Last updated: .+?\*',
        f'*Last updated: {today} by auto-sync*',
        current_content
    )
    
    # Append updates before the final separator
    if '---\n\n*Last updated' in updated_content:
        parts = updated_content.rsplit('---\n\n*Last updated', 1)
        updated_content = parts[0] + ''.join(updates) + '---\n\n*Last updated' + parts[1]
    else:
        # Just append to end
        updated_content = updated_content.rstrip() + '\n' + ''.join(updates)
    
    if dry_run:
        print("=== DRY RUN ===")
        print("Would update SESSION-STATE.md with:")
        print(''.join(updates))
        return False
    
    # Write to temp file first, then atomic rename to prevent corruption
    temp_file = SESSION_STATE.with_suffix('.tmp')
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        temp_file.replace(SESSION_STATE)  # Atomic on Unix
        return True
    except Exception as e:
        print(f"❌ Error writing SESSION-STATE.md: {e}")
        if temp_file.exists():
            temp_file.unlink()
        return False


def main():
    try:
        parser = argparse.ArgumentParser(description='Auto-sync SESSION-STATE.md')
        parser.add_argument('--dry-run', action='store_true', help='Show what would change without writing')
        args = parser.parse_args()
        
        print(f"SESSION-STATE Auto-Sync")
        print(f"Looking back: {LOOKBACK_DAYS} days")
        print(f"Target: {SESSION_STATE}")
        print()
        
        success = update_session_state(dry_run=args.dry_run)
        
        if success:
            print(f"✅ SESSION-STATE.md updated successfully")
            return 0
        elif args.dry_run:
            print("\n(Dry run complete — no changes made)")
            return 0
        else:
            print(f"❌ Failed to update SESSION-STATE.md")
            return 1
    except Exception as e:
        print(f"❌ Error in sync-session-state: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
