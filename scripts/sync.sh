#!/bin/bash

# Memory Bridge Sync Script
# Syncs memory files from VPS to the memory/ folder for GitHub deployment

set -e

WORKSPACE="/root/.openclaw/workspace"
MEMORY_DIR="$(dirname "$0")/../memory"

echo "🔄 Syncing memory files..."

# Create directories
mkdir -p "$MEMORY_DIR/journal"
mkdir -p "$MEMORY_DIR/capture"

# Sync root files
if [ -f "$WORKSPACE/SESSION-STATE.md" ]; then
    cp "$WORKSPACE/SESSION-STATE.md" "$MEMORY_DIR/"
    echo "✓ SESSION-STATE.md"
fi

if [ -f "$WORKSPACE/MEMORY.md" ]; then
    cp "$WORKSPACE/MEMORY.md" "$MEMORY_DIR/"
    echo "✓ MEMORY.md"
fi

# Sync journal files
if [ -d "$WORKSPACE/memory/journal" ]; then
    cp "$WORKSPACE/memory/journal/"*.md "$MEMORY_DIR/journal/" 2>/dev/null || true
    echo "✓ Journal files"
fi

# Sync capture files
if [ -d "$WORKSPACE/memory/capture" ]; then
    cp "$WORKSPACE/memory/capture/"*.md "$MEMORY_DIR/capture/" 2>/dev/null || true
    echo "✓ Capture files"
fi

# Sync daily notes (root of memory folder)
if [ -d "$WORKSPACE/memory" ]; then
    for file in "$WORKSPACE/memory/"*.md; do
        if [ -f "$file" ]; then
            cp "$file" "$MEMORY_DIR/"
        fi
    done
    echo "✓ Daily notes"
fi

echo ""
echo "✅ Sync complete!"
echo "Run 'git add memory/' and commit to update the archive."
