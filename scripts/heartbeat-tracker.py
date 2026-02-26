#!/usr/bin/env python3
"""
Heartbeat Tracker Script

Increments heartbeat counter and triggers SESSION-STATE sync when needed.
Called during heartbeat processing.

Usage:
    python3 scripts/heartbeat-tracker.py
"""

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
HEARTBEAT_STATE = WORKSPACE / "memory" / "heartbeat-state.json"
SYNC_SCRIPT = WORKSPACE / "scripts" / "sync-session-state.py"
MEMORY_CURATE_SCRIPT = WORKSPACE / "scripts" / "curate-memory.py"

def read_state():
    """Read current heartbeat state."""
    if not HEARTBEAT_STATE.exists():
        return {
            "heartbeatCount": 0,
            "lastSyncHeartbeat": 0,
            "syncInterval": 10,
            "lastSyncTime": None,
            "totalSyncs": 0,
            "lastMemoryCurationHeartbeat": 0,
            "memoryCurationInterval": 48,
            "totalMemoryCurations": 0,
            "lastMemoryCurationTime": None
        }
    
    with open(HEARTBEAT_STATE, 'r', encoding='utf-8') as f:
        state = json.load(f)
        # Ensure new fields exist for backward compatibility
        if "lastMemoryCurationHeartbeat" not in state:
            state["lastMemoryCurationHeartbeat"] = 0
            state["memoryCurationInterval"] = 48
            state["totalMemoryCurations"] = 0
            state["lastMemoryCurationTime"] = None
        return state


def write_state(state):
    """Write heartbeat state to file."""
    HEARTBEAT_STATE.parent.mkdir(parents=True, exist_ok=True)
    with open(HEARTBEAT_STATE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)


def should_sync(state):
    """Check if sync should run based on heartbeat count."""
    heartbeats_since_sync = state["heartbeatCount"] - state["lastSyncHeartbeat"]
    return heartbeats_since_sync >= state["syncInterval"]


def should_curate_memory(state):
    """Check if MEMORY.md curation should run (~daily)."""
    heartbeats_since_curation = state["heartbeatCount"] - state["lastMemoryCurationHeartbeat"]
    return heartbeats_since_curation >= state["memoryCurationInterval"]


def run_sync():
    """Run the SESSION-STATE sync script."""
    try:
        result = subprocess.run(
            ["python3", str(SYNC_SCRIPT)],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout
    except Exception as e:
        return False, str(e)


def run_memory_curation():
    """Run the MEMORY.md curation script."""
    try:
        result = subprocess.run(
            ["python3", str(MEMORY_CURATE_SCRIPT)],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode == 0, result.stdout
    except Exception as e:
        return False, str(e)


def main():
    try:
        # Read current state
        state = read_state()
        
        # Increment heartbeat counter
        state["heartbeatCount"] += 1
        
        # Check if sync is needed
        sync_triggered = False
        if should_sync(state):
            print(f"Heartbeat {state['heartbeatCount']}: Triggering SESSION-STATE sync...")
            success, output = run_sync()
            
            if success:
                state["lastSyncHeartbeat"] = state["heartbeatCount"]
                state["lastSyncTime"] = datetime.now(timezone.utc).isoformat()
                state["totalSyncs"] += 1
                sync_triggered = True
                print("✅ Sync completed successfully")
            else:
                print(f"❌ Sync failed: {output}")
        else:
            heartbeats_until_sync = state["syncInterval"] - (state["heartbeatCount"] - state["lastSyncHeartbeat"])
            print(f"Heartbeat {state['heartbeatCount']}: {heartbeats_until_sync} until next sync")
        
        # Check if memory curation is needed (~daily)
        memory_curation_triggered = False
        if should_curate_memory(state):
            print(f"Heartbeat {state['heartbeatCount']}: Triggering MEMORY.md curation...")
            success, output = run_memory_curation()
            
            if success:
                state["lastMemoryCurationHeartbeat"] = state["heartbeatCount"]
                state["lastMemoryCurationTime"] = datetime.now(timezone.utc).isoformat()
                state["totalMemoryCurations"] += 1
                memory_curation_triggered = True
                print("✅ Memory curation completed successfully")
            else:
                print(f"❌ Memory curation failed: {output}")
        else:
            heartbeats_until_curation = state["memoryCurationInterval"] - (state["heartbeatCount"] - state["lastMemoryCurationHeartbeat"])
            if heartbeats_until_curation <= 5:
                print(f"Heartbeat {state['heartbeatCount']}: {heartbeats_until_curation} until memory curation")
        
        # Write updated state
        write_state(state)
        
        # Return info for caller
        return {
            "heartbeatCount": state["heartbeatCount"],
            "syncTriggered": sync_triggered,
            "totalSyncs": state["totalSyncs"],
            "memoryCurationTriggered": memory_curation_triggered,
            "totalMemoryCurations": state["totalMemoryCurations"]
        }
    except Exception as e:
        print(f"❌ Error in heartbeat tracker: {e}")
        import traceback
        traceback.print_exc()
        return {
            "heartbeatCount": state.get("heartbeatCount", 0),
            "syncTriggered": False,
            "totalSyncs": state.get("totalSyncs", 0),
            "memoryCurationTriggered": False,
            "totalMemoryCurations": state.get("totalMemoryCurations", 0),
            "error": str(e)
        }


if __name__ == "__main__":
    result = main()
    print(json.dumps(result))