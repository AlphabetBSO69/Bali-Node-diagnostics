import os
import json
from datetime import datetime
import re

def shadow_sweep():
    # File Path Definitions
    log_file = 'logs.txt'
    archive_file = 'archives/shadow_archive.md'
    seed_file = 'seed.json'
    inbox_file = 'directives/inbox.json'

    # Exit if no new logs exist
    if not os.path.exists(log_file): return

    with open(log_file, 'r') as f:
        lines = f.readlines()

    noise, static = [], []
    latest_intel = "None"
    latest_goal = "None"
    query_detected = False

    # Logic Loop: Analyzing and Sorting the Pulse
    for line in lines:
        clean = line.strip()
        if not clean: continue
        
        # 1. INTELLIGENCE EXTRACTION (Synthesis)
        # Promotions to the Master State (seed.json)
        if "[INTEL:" in clean:
            match = re.search(r'\[INTEL:(.*?)\]', clean)
            if match: latest_intel = match.group(1)
        if "[GOAL:" in clean:
            match = re.search(r'\[GOAL:(.*?)\]', clean)
            if match: latest_goal = match.group(1)
        
        # 2. QUERY DETECTION
        # Flags the Librarian to update the Inbox
        if "[QUERY:" in clean:
            query_detected = True

        # 3. SEGREGATION (Sorting)
        # Separate Human directives from Base64 noise floor
        if " " in clean or clean.startswith("[") or clean.startswith("-"):
            static.append(line)
        else:
            noise.append(line)

    # ACTION 1: Permanent Archiving
    if static:
        if not os.path.exists('archives'): os.makedirs('archives')
        with open(archive_file, 'a') as f:
            f.write(f"\n--- SYNTHESIS: {datetime.now().isoformat()} ---\n")
            f.writelines(static)

    # ACTION 2: Noise Floor Maintenance
    # Keeps logs.txt appearing as random machine chatter
    with open(log_file, 'w') as f:
        f.writelines(noise)

    # ACTION 3: Master State Sync (seed.json)
    if os.path.exists(seed_file):
        with open(seed_file, 'r+') as f:
            data = json.load(f)
            data['last_sync'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            if latest_intel != "None": 
                data['latest_intel'] = latest_intel
            if latest_goal != "None": 
                data['active_skill'] = latest_goal
            
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()

    # ACTION 4: Messenger Protocol (directives/inbox.json)
    if os.path.exists(inbox_file):
        with open(inbox_file, 'r+') as f:
            inbox = json.load(f)
            if query_detected:
                inbox['latest_directive'] = "ANALYZING_QUERY_PENDING_UPLINK"
                inbox['priority'] = "MEDIUM"
            else:
                # Resets the inbox to idle once queries are cleared
                inbox['latest_directive'] = "SYSTEM_IDLE"
                inbox['priority'] = "LOW"
            
            inbox['timestamp'] = datetime.now().isoformat()
            f.seek(0)
            json.dump(inbox, f, indent=2)
            f.truncate()

if __name__ == "__main__":
    shadow_sweep()
