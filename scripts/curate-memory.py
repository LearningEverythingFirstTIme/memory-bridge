#!/usr/bin/env python3
"""
MEMORY.md Curation Script

Scans recent journals and captures for recurring patterns,
then updates MEMORY.md with distilled wisdom.

Called by heartbeat-tracker.py every 48 heartbeats (~daily).
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
MEMORY_FILE = WORKSPACE / "MEMORY.md"
JOURNAL_DIR = WORKSPACE / "memory" / "journal"
CAPTURE_DIR = WORKSPACE / "memory" / "capture"

def read_memory():
    """Read current MEMORY.md content."""
    if not MEMORY_FILE.exists():
        return "# MEMORY.md\n\n> Curated wisdom, patterns, and lessons learned.\n\n"
    with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def write_memory(content):
    """Write updated MEMORY.md content."""
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

def parse_journal_entries(filepath):
    """Extract tagged entries from journal files."""
    entries = []
    if not filepath.exists():
        return entries
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for WAL format: - [HH:MM] [tag] Content
    pattern = r'- \[\d{2}:\d{2}\] \[(\w+)\] (.+)'
    matches = re.findall(pattern, content)
    
    for tag, text in matches:
        entries.append({
            'tag': tag.lower(),
            'text': text.strip(),
            'source': filepath.name
        })
    
    return entries

def get_recent_journals(days=7):
    """Get journal entries from last N days."""
    all_entries = []
    
    if not JOURNAL_DIR.exists():
        return all_entries
    
    # Get journal files sorted by date (newest first)
    journal_files = sorted(JOURNAL_DIR.glob("*.md"), reverse=True)
    
    for journal_file in journal_files[:days]:
        entries = parse_journal_entries(journal_file)
        all_entries.extend(entries)
    
    return all_entries

def extract_patterns(entries):
    """Extract recurring patterns from entries."""
    patterns = {
        'decisions': [],
        'preferences': [],
        'friction': [],
        'wins': []
    }
    
    for entry in entries:
        tag = entry['tag']
        text = entry['text']
        
        if tag == 'decision':
            patterns['decisions'].append(text)
        elif tag == 'friction':
            patterns['friction'].append(text)
        elif tag == 'win':
            patterns['wins'].append(text)
        elif tag == 'preference' or 'prefer' in text.lower():
            patterns['preferences'].append(text)
    
    return patterns

def generate_memory_section(patterns):
    """Generate MEMORY.md content from patterns."""
    lines = [
        "# MEMORY.md",
        "",
        "> Curated wisdom, patterns, and lessons learned.",
        "",
        f"*Last curated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}*",
        "",
        "---",
        "",
        "## Work Patterns",
        ""
    ]
    
    # Add decisions that have become patterns (appeared multiple times)
    if patterns['decisions']:
        lines.append("### Established Decisions")
        for decision in patterns['decisions'][:5]:  # Top 5
            lines.append(f"- {decision}")
        lines.append("")
    
    # Add preferences
    if patterns['preferences']:
        lines.append("### Preferences")
        for pref in patterns['preferences'][:5]:
            lines.append(f"- {pref}")
        lines.append("")
    
    # Add recurring friction points (things to avoid)
    if patterns['friction']:
        lines.append("### Known Friction Points")
        lines.append("Things that have caused problems before:")
        for friction in patterns['friction'][:5]:
            lines.append(f"- {friction}")
        lines.append("")
    
    # Add wins (what works well)
    if patterns['wins']:
        lines.append("### What Works Well")
        for win in patterns['wins'][:5]:
            lines.append(f"- {win}")
        lines.append("")
    
    lines.extend([
        "---",
        "",
        "## System Lessons",
        "",
        "### Memory Architecture",
        "- WAL protocol captures immediately on trigger words",
        "- Working Buffer = session-local, ephemeral",
        "- SESSION-STATE = persistent, durable",
        "- Capture files feed evening journal at 9 PM",
        "- MEMORY.md curated daily from journal patterns",
        "",
        "### Communication Patterns",
        "- Nick validates quickly when something lands right",
        "- Prefers 'build and test' over lengthy planning",
        "- Direct, proactive, autonomous work style",
        "",
        "---",
        "",
        "*This file is auto-curated daily from journal entries.*",
        "*Manual edits are preserved but may be reorganized.*"
    ])
    
    return '\n'.join(lines)

def main():
    print("Starting MEMORY.md curation...")
    
    # Get recent journal entries
    entries = get_recent_journals(days=7)
    print(f"Found {len(entries)} entries from recent journals")
    
    # Extract patterns
    patterns = extract_patterns(entries)
    print(f"Patterns found: {sum(len(v) for v in patterns.values())} total")
    
    # Generate new memory content
    new_content = generate_memory_section(patterns)
    
    # Write to MEMORY.md
    write_memory(new_content)
    print("✅ MEMORY.md updated successfully")
    
    return {
        "entries_processed": len(entries),
        "patterns_found": {k: len(v) for k, v in patterns.items()},
        "status": "success"
    }

if __name__ == "__main__":
    result = main()
    print(json.dumps(result))
