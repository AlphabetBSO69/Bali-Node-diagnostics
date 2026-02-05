import os
import json
from datetime import datetime

def shadow_sweep():
    log_file = 'logs.txt'
    archive_dir = 'archives'
    archive_file = os.path.join(archive_dir, 'shadow_archive.md')
    seed_file = 'seed.json'

    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    if not os.path.exists(log_file):
        return

    with open(log_file, 'r') as f:
        lines = f.readlines()

    # NEW LOGIC: If it has spaces and common words, it's STATIC (Archive it)
    # If it's one long string of gibberish, it's NOISE (Keep it)
    noise = []
    static = []
    
    for line in lines:
        clean = line.strip()
        if not clean: continue
        
        # Archive if it has spaces (sentence) or starts with [ (tag)
        if " " in clean or clean.startswith("[") or clean.startswith("-"):
            static.append(line)
        else:
            noise.append(line)

    # 1. Archive the Static
    if static:
        with open(archive_file, 'a') as f:
            f.write(f"\n--- SWEEP: {datetime.now().isoformat()} ---\n")
            f.writelines(static)

    # 2. Clean the Logs (Retain Noise)
    with open(log_file, 'w') as f:
        f.writelines(noise)

    # 3. Update the Heartbeat in seed.json
    if os.path.exists(seed_file):
        with open(seed_file, 'r') as f:
            data = json.load(f)
        
        data['last_sync'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        with open(seed_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Librarian: Pulse updated to {data['last_sync']}")

if __name__ == "__main__":
    shadow_sweep()