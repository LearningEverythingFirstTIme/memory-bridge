#!/bin/bash

# Memory Bridge Auto-Sync & Deploy Script
# Syncs memory files from VPS to GitHub, triggering Vercel auto-deploy

set -e

WORKSPACE="/root/.openclaw/workspace"
REPO_DIR="$WORKSPACE/memory-bridge"
MEMORY_DIR="$REPO_DIR/memory"
SCRIPTS_DIR="$REPO_DIR/scripts"
REPORTS_DIR="$REPO_DIR/reports"

echo "🔄 Memory Bridge Auto-Sync"
echo "=========================="
echo ""

# Check if we're in the repo directory
cd "$REPO_DIR"

# Pull latest changes first (in case of remote updates)
echo "📥 Pulling latest changes..."
git pull origin main --quiet || echo "⚠️  Could not pull, continuing with local changes"
echo ""

# Create directories
mkdir -p "$MEMORY_DIR/journal"
mkdir -p "$MEMORY_DIR/capture"
mkdir -p "$SCRIPTS_DIR"
mkdir -p "$REPORTS_DIR"

echo "📤 Syncing files..."

# === CORE MEMORY FILES ===
for file in SESSION-STATE.md MEMORY.md; do
    if [ -f "$WORKSPACE/$file" ]; then
        cp "$WORKSPACE/$file" "$MEMORY_DIR/"
        echo "  ✓ $file"
    fi
done

# === DAILY NOTES ===
if [ -d "$WORKSPACE/memory" ]; then
    for file in "$WORKSPACE/memory/"*.md; do
        if [ -f "$file" ]; then
            cp "$file" "$MEMORY_DIR/"
        fi
    done
    echo "  ✓ Daily notes"
fi

# === JOURNAL FILES ===
if [ -d "$WORKSPACE/memory/journal" ]; then
    cp "$WORKSPACE/memory/journal/"*.md "$MEMORY_DIR/journal/" 2>/dev/null || true
    echo "  ✓ Journal files"
fi

# === CAPTURE FILES ===
if [ -d "$WORKSPACE/memory/capture" ]; then
    cp "$WORKSPACE/memory/capture/"*.md "$MEMORY_DIR/capture/" 2>/dev/null || true
    echo "  ✓ Capture files"
fi

# === TRACKING DATA ===
for file in fidget-result.txt fidget-snapshot.json heartbeat-state.json; do
    if [ -f "$WORKSPACE/memory/$file" ]; then
        cp "$WORKSPACE/memory/$file" "$MEMORY_DIR/"
        echo "  ✓ $file"
    fi
done

# === AUTOMATION SCRIPTS ===
for script in curate-memory.py evening-journal.py fidget-checker.py flush-working-buffer.py heartbeat-tracker.py memory-health-check.py sync-session-state.py; do
    if [ -f "$WORKSPACE/scripts/$script" ]; then
        cp "$WORKSPACE/scripts/$script" "$SCRIPTS_DIR/"
        echo "  ✓ $script"
    fi
done

# === REPORTS ===
if [ -d "$WORKSPACE/reports" ]; then
    cp "$WORKSPACE/reports/memory-"* "$REPORTS_DIR/" 2>/dev/null || true
    echo "  ✓ Reports"
fi

# === CORE DOCUMENTATION ===
for doc in AGENTS.md HEARTBEAT.md IDENTITY.md MEMORY-QUICKREF.md SOUL.md TOOLS.md USER.md; do
    if [ -f "$WORKSPACE/$doc" ]; then
        cp "$WORKSPACE/$doc" "$REPO_DIR/"
        echo "  ✓ $doc"
    fi
done

echo ""

# === GIT COMMIT & PUSH ===
echo "📦 Checking for changes..."

if git diff --quiet && git diff --staged --quiet; then
    echo "✅ No changes to commit. Archive is up to date."
    exit 0
fi

echo "📝 Changes detected. Committing..."
git add -A

# Create commit message with timestamp
COMMIT_MSG="Memory sync: $(date '+%Y-%m-%d %H:%M') UTC

Synced from VPS:
- Memory files (SESSION-STATE, MEMORY, daily notes)
- Journal entries
- Capture files
- Tracking data (fidget, heartbeat)
- Automation scripts
- Reports
- Core documentation"

git commit -m "$COMMIT_MSG" --quiet

echo "🚀 Pushing to GitHub (triggers Vercel deploy)..."
git push origin main --quiet

echo ""
echo "✅ Sync complete! Vercel should auto-deploy shortly."
echo "   Check: https://vercel.com/dashboard"
