#!/usr/bin/env python3
"""
Evening Journal Generator
Distills daily capture into structured journal entry for next-session context.
"""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta, timezone

# Valid WAL tags
VALID_TAGS = {'decision', 'friction', 'win', 'idea', 'mood', 'question', 'open-loop', 'note'}

def parse_capture_file(date_str):
    """Parse the day's capture file into structured entries."""
    capture_file = Path(f"/root/.openclaw/workspace/memory/capture/{date_str}.md")
    
    if not capture_file.exists():
        return []
    
    content = capture_file.read_text(encoding='utf-8')
    entries = []
    invalid_tags = []
    
    # Parse lines like: - [09:15] [tag] Content
    pattern = r'^- \[(\d{2}:\d{2})\] \[(\w+)\] (.+)$'
    
    for line in content.strip().split('\n'):
        match = re.match(pattern, line.strip())
        if match:
            time_str, tag, content_text = match.groups()
            # Validate tag
            if tag not in VALID_TAGS:
                invalid_tags.append((time_str, tag, content_text))
                tag = 'note'  # Default to note for invalid tags
            entries.append({
                'time': time_str,
                'tag': tag,
                'content': content_text
            })
    
    # Report invalid tags
    if invalid_tags:
        print(f"⚠️  Warning: Found {len(invalid_tags)} entries with invalid tags:")
        for time_str, tag, content in invalid_tags:
            print(f"   - [{time_str}] [{tag}] -> converted to [note]")
    
    return entries

def categorize_entries(entries):
    """Group entries by tag type."""
    categories = {
        'decision': [],
        'friction': [],
        'win': [],
        'idea': [],
        'mood': [],
        'question': [],
        'open-loop': [],
        'note': []
    }
    
    for entry in entries:
        tag = entry['tag']
        if tag in categories:
            categories[tag].append(entry)
        else:
            categories['note'].append(entry)
    
    return categories

def generate_journal(date_str, entries):
    """Generate structured journal markdown."""
    categories = categorize_entries(entries)
    
    lines = [
        f"# Evening Journal — {date_str}",
        ""
    ]
    
    # Decisions
    if categories['decision']:
        lines.append("## Decisions")
        for e in categories['decision']:
            lines.append(f"- {e['content']}")
        lines.append("")
    
    # Friction Points
    if categories['friction']:
        lines.append("## Friction Points")
        for e in categories['friction']:
            lines.append(f"- {e['content']}")
        lines.append("")
    
    # Wins
    if categories['win']:
        lines.append("## Wins")
        for e in categories['win']:
            lines.append(f"- {e['content']}")
        lines.append("")
    
    # Ideas Captured
    if categories['idea']:
        lines.append("## Ideas Captured")
        for e in categories['idea']:
            lines.append(f"- {e['content']}")
        lines.append("")
    
    # Mood & Context
    if categories['mood']:
        lines.append("## Mood & Context")
        for e in categories['mood']:
            lines.append(f"- {e['content']}")
        lines.append("")
    
    # Questions
    if categories['question']:
        lines.append("## Questions")
        for e in categories['question']:
            lines.append(f"- {e['content']}")
        lines.append("")
    
    # Open Loops
    if categories['open-loop']:
        lines.append("## Open Loops")
        for e in categories['open-loop']:
            lines.append(f"- [ ] {e['content']}")
        lines.append("")
    
    # Notes (untagged)
    if categories['note']:
        lines.append("## Notes")
        for e in categories['note']:
            lines.append(f"- {e['content']}")
        lines.append("")
    
    # Footer
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines.extend([
        "---",
        f"*Generated: {now}*"
    ])
    
    return "\n".join(lines)

def main():
    try:
        # Get yesterday's date (since this runs at 9 PM, we want today's captures)
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        
        print(f"[{datetime.now(timezone.utc).isoformat()}] Generating evening journal for {today}...")
        
        # Ensure directories exist
        journal_dir = Path("/root/.openclaw/workspace/memory/journal")
        capture_dir = Path("/root/.openclaw/workspace/memory/capture")
        journal_dir.mkdir(parents=True, exist_ok=True)
        capture_dir.mkdir(parents=True, exist_ok=True)
        
        # Parse capture file
        entries = parse_capture_file(today)
        
        if not entries:
            print(f"No capture entries found for {today}")
            # Still create empty journal to mark the day
            now = datetime.now(timezone.utc)
            journal_content = f"# Evening Journal — {today}\n\n*No captures recorded today.*\n\n---\n*Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}*"
        else:
            print(f"Found {len(entries)} capture entries")
            journal_content = generate_journal(today, entries)
        
        # Write journal file
        journal_file = journal_dir / f"{today}.md"
        journal_file.write_text(journal_content, encoding='utf-8')
        print(f"Journal written to {journal_file}")
        
        # Clear capture file (archive instead of delete)
        capture_file = capture_dir / f"{today}.md"
        if capture_file.exists():
            archive_file = capture_dir / f"{today}.archived.md"
            # Handle case where archive already exists (append timestamp)
            if archive_file.exists():
                timestamp = int(datetime.now(timezone.utc).timestamp())
                archive_file = capture_dir / f"{today}.{timestamp}.archived.md"
            capture_file.rename(archive_file)
            print(f"Capture file archived to {archive_file}")
        
        print("Done!")
        return 0
        
    except Exception as e:
        print(f"❌ Error generating journal: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
