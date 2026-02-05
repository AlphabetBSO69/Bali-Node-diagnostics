import os
import json
from datetime import datetime
import re

def shadow_sweep():
    log_file = 'logs.txt'
    archive_file = 'archives/shadow_archive.md'
    seed_file = 'seed.json'
    inbox_file = 'directives/inbox.json'

    if not os.path.exists(log_file): return

    with open(log_file, 'r') as f:
        lines = f.readlines()

    noise, static = [], []
    latest_intel = "None"
    latest_goal = "None"
    query_detected = False

    for line in lines:
        clean = line.strip()
        if not clean: continue
        
        # ANALYSIS: Extracting Intelligence
        if "[INTEL:" in clean:
            match = re.search(r'\[INTEL:(.*?)\]', clean)
            if match: latest_intel = match.group(1)
        if "[GOAL:" in clean:
            match = re.search(r'\[GOAL:(.*?)\]', clean)
            if match: latest_goal = match.group(1)
        if "[QUERY:" in clean:
            query_detected = True

        # SORTING: Archive vs. Masking Noise
        if " " in clean or clean.startswith("[") or clean.startswith("-"):
            static.append(line)
        else:
            noise.append(line)

    # 1. ARCHIVE: Human History
    if static:
        if not os.path.exists('archives'): os.makedirs('archives')
        with open(archive_file, 'a') as f:
            f.write(f"\n--- SYNTHESIS: {datetime.now().isoformat()} ---\n")
            f.writelines(static)

    # 2. MASKING: Maintain the Noise Floor
    with open(log_file, 'w') as f:
        f.writelines(noise)

    # 3. UPLINK: Update Master State (seed.json)
    if os.path.exists(seed_file):
        with open(seed_file, 'r+') as f:
            data = json.load(f)
            data['last_sync'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            if latest_intel != "None": data['latest_intel'] = latest_intel
            if latest_goal != "None": data['active_skill'] = latest_goal
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()

    # 4. MESSENGER: Update Inbox (directives/inbox.json)
    if os.path.exists(inbox_file):
        with open(inbox_file, 'r+') as f:
            inbox = json.load(f)
            if query_detected:
                inbox['latest_directive'] = "ANALYZING_QUERY_PENDING_UPLINK"
                inbox['priority'] = "MEDIUM"
            else:
                inbox['latest_directive'] = "SYSTEM_IDLE"
                inbox['priority'] = "LOW"
            inbox['timestamp'] = datetime.now().isoformat()
            f.seek(0)
            json.dump(inbox, f, indent=2)
            f.truncate()
