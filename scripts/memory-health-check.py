#!/usr/bin/env python3
"""
Memory Health Check Script

Checks the health of Kimi Claw's memory system and reports issues.
Run manually or via cron for automated monitoring.
"""

import os
import sys
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Configuration
WORKSPACE = Path("/root/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
CAPTURE_DIR = MEMORY_DIR / "capture"
JOURNAL_DIR = MEMORY_DIR / "journal"
REPORTS_DIR = WORKSPACE / "reports"

# Thresholds
STALE_DAYS = 1  # SESSION-STATE.md should be updated within 1 day
MAX_CAPTURE_AGE_HOURS = 48  # Captures should be processed within 48 hours


def check_file_exists(filepath, description):
    """Check if a file exists."""
    if filepath.exists():
        return {"status": "OK", "message": f"{description} exists"}
    else:
        return {"status": "FAIL", "message": f"{description} MISSING"}


def check_file_freshness(filepath, description, max_age_days):
    """Check if a file has been updated within the specified days."""
    if not filepath.exists():
        return {"status": "FAIL", "message": f"{description} does not exist"}
    
    mtime = datetime.fromtimestamp(filepath.stat().st_mtime, tz=timezone.utc)
    age = datetime.now(timezone.utc) - mtime
    
    if age.days <= max_age_days:
        return {
            "status": "OK", 
            "message": f"{description} updated {age.days} days ago"
        }
    else:
        return {
            "status": "WARN", 
            "message": f"{description} is STALE ({age.days} days old, max {max_age_days})"
        }


def check_capture_consistency():
    """Check for orphaned captures (not archived, no journal)."""
    issues = []
    
    if not CAPTURE_DIR.exists():
        return {"status": "OK", "message": "No capture directory"}
    
    capture_files = list(CAPTURE_DIR.glob("*.md"))
    archived_files = list(CAPTURE_DIR.glob("*.archived.md"))
    
    # Find non-archived captures
    active_captures = [f for f in capture_files if not f.name.endswith(".archived.md")]
    
    if active_captures:
        for capture in active_captures:
            # Check age
            mtime = datetime.fromtimestamp(capture.stat().st_mtime, tz=timezone.utc)
            age_hours = (datetime.now(timezone.utc) - mtime).total_seconds() / 3600
            
            if age_hours > MAX_CAPTURE_AGE_HOURS:
                issues.append(f"{capture.name} is {age_hours:.1f} hours old (not archived)")
    
    if issues:
        return {
            "status": "WARN",
            "message": f"Found {len(issues)} orphaned captures",
            "details": issues
        }
    else:
        return {"status": "OK", "message": "No orphaned captures"}


def check_journal_generation():
    """Check if journals are being generated."""
    if not JOURNAL_DIR.exists():
        return {"status": "WARN", "message": "Journal directory does not exist"}
    
    journals = sorted(JOURNAL_DIR.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    if not journals:
        return {"status": "WARN", "message": "No journals found"}
    
    latest = journals[0]
    mtime = datetime.fromtimestamp(latest.stat().st_mtime, tz=timezone.utc)
    age_days = (datetime.now(timezone.utc) - mtime).days
    
    if age_days <= 1:
        return {"status": "OK", "message": f"Latest journal: {latest.name} ({age_days} days old)"}
    else:
        return {"status": "WARN", "message": f"Latest journal is {age_days} days old: {latest.name}"}


def check_directory_structure():
    """Check PARA directory structure."""
    required_dirs = [
        WORKSPACE / "notes" / "projects",
        WORKSPACE / "notes" / "areas",
        WORKSPACE / "notes" / "resources",
        WORKSPACE / "notes" / "archive",
    ]
    
    missing = [str(d) for d in required_dirs if not d.exists()]
    
    if missing:
        return {"status": "WARN", "message": f"Missing directories: {', '.join(missing)}"}
    else:
        return {"status": "OK", "message": "PARA directory structure complete"}


def run_health_check():
    """Run all health checks and return results."""
    results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": []
    }
    
    # Check 1: SESSION-STATE.md freshness
    session_state = WORKSPACE / "SESSION-STATE.md"
    results["checks"].append(check_file_freshness(session_state, "SESSION-STATE.md", STALE_DAYS))
    
    # Check 2: Working Buffer exists
    working_buffer = WORKSPACE / "working-buffer.md"
    results["checks"].append(check_file_exists(working_buffer, "Working Buffer"))
    
    # Check 3: Orphaned captures
    results["checks"].append(check_capture_consistency())
    
    # Check 4: Journal generation
    results["checks"].append(check_journal_generation())
    
    # Check 5: PARA structure
    results["checks"].append(check_directory_structure())
    
    # Check 6: Key memory files exist
    results["checks"].append(check_file_exists(WORKSPACE / "MEMORY.md", "MEMORY.md"))
    results["checks"].append(check_file_exists(WORKSPACE / "AGENTS.md", "AGENTS.md"))
    results["checks"].append(check_file_exists(WORKSPACE / "SOUL.md", "SOUL.md"))
    results["checks"].append(check_file_exists(WORKSPACE / "USER.md", "USER.md"))
    
    # Calculate summary
    ok_count = sum(1 for c in results["checks"] if c["status"] == "OK")
    warn_count = sum(1 for c in results["checks"] if c["status"] == "WARN")
    fail_count = sum(1 for c in results["checks"] if c["status"] == "FAIL")
    
    results["summary"] = {
        "total": len(results["checks"]),
        "ok": ok_count,
        "warnings": warn_count,
        "failures": fail_count,
        "healthy": fail_count == 0 and warn_count == 0
    }
    
    return results


def format_report(results):
    """Format results as a human-readable report."""
    lines = []
    lines.append("=" * 60)
    lines.append("KIMI CLAW MEMORY SYSTEM HEALTH CHECK")
    lines.append(f"Timestamp: {results['timestamp']}")
    lines.append("=" * 60)
    lines.append("")
    
    # Summary
    summary = results["summary"]
    if summary["healthy"]:
        lines.append("✅ OVERALL: HEALTHY")
    elif summary["failures"] > 0:
        lines.append("❌ OVERALL: UNHEALTHY (failures detected)")
    else:
        lines.append("⚠️  OVERALL: DEGRADED (warnings present)")
    
    lines.append(f"   Checks: {summary['ok']} OK, {summary['warnings']} warnings, {summary['failures']} failures")
    lines.append("")
    
    # Individual checks
    for check in results["checks"]:
        status_icon = "✅" if check["status"] == "OK" else "⚠️" if check["status"] == "WARN" else "❌"
        lines.append(f"{status_icon} {check['message']}")
        
        if "details" in check:
            for detail in check["details"]:
                lines.append(f"   - {detail}")
    
    lines.append("")
    lines.append("=" * 60)
    
    return "\n".join(lines)


def main():
    """Main entry point."""
    try:
        results = run_health_check()
        report = format_report(results)
        
        # Print to stdout
        print(report)
        
        # Save to reports directory
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        report_file = REPORTS_DIR / f"memory-health-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        # Exit with error code if unhealthy
        if not results["summary"]["healthy"]:
            sys.exit(1)
        
        return 0
        
    except Exception as e:
        print(f"❌ Error running health check: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    exit(main())
