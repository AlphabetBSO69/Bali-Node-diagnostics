import os
import json
from datetime import datetime
import re

def shadow_sweep():
    log_file = 'logs.txt'
    archive_file = 'archives/shadow_archive.md'
    seed_file = 'seed.json'

    if not os.path.exists(log_file): return

    with open(log_file, 'r') as f:
        lines = f.readlines()

    noise, static = [], []
    latest_intel = "None"
    latest_goal = "None"

    for line in lines:
        clean = line.strip()
        if not clean: continue
        
        # ANALYSIS: Extracting Intelligence for the Master State
        # This is where the Librarian 'thinks' and promotes data to the Seed
        if "[INTEL:" in clean:
            match = re.search(r'\[INTEL:(.*?)\]', clean)
            if match: latest_intel = match.group(1)
        if "[GOAL:" in clean:
            match = re.search(r'\[GOAL:(.*?)\]', clean)
            if match: latest_goal = match.group(1)

        # SORTING: Human sentences/directives vs. Machine noise
        if " " in clean or clean.startswith("[") or clean.startswith("-"):
            static.append(line)
        else:
            noise.append(line)

    # 1. Archive the Static data (Human History)
    if static:
        if not os.path.exists('archives'): os.makedirs('archives')
        with open(archive_file, 'a') as f:
            f.write(f"\n--- SYNTHESIS: {datetime.now().isoformat()} ---\n")
            f.writelines(static)

    # 2. Maintain the Noise Floor (Masking)
    with open(log_file, 'w') as f:
        f.writelines(noise)

    # 3. UPLINK: Synchronize the Master State (seed.json)
    if os.path.exists(seed_file):
        with open(seed_file, 'r+') as f:
            data = json.load(f)
            
            # Updating the global heartbeat
            data['last_sync'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            
            # Promoting local intel to global state
            if latest_intel != "None": 
                data['latest_intel'] = latest_intel
            if latest_goal != "None": 
                data['active_skill'] = latest_goal
            
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
