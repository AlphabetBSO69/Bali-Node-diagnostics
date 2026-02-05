import os

def shadow_sweep():
    # 1. Define target paths relative to the repo root
    log_file = 'logs.txt'
    archive_dir = 'archives'
    archive_file = os.path.join(archive_dir, 'shadow_archive.md')

    # 2. Ensure the 'archives' directory exists (The "Safety Net")
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
        print(f"Librarian: Created missing directory -> {archive_dir}")

    # 3. Check if 'logs.txt' exists. If not, create an empty one to prevent errors.
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.write("")
        print("Librarian: logs.txt was missing. Created empty file.")
        return

    # 4. Read current log content
    with open(log_file, 'r') as f:
        lines = f.readlines()

    # 5. Filter Logic:
    # Noise = Random strings (Base64) usually over 20 chars, no brackets.
    # Static = Human text, timestamps, or bracketed headers.
    noise = [line for line in lines if not line.strip().startswith('[') and len(line.strip()) > 20]
    static = [line for line in lines if line not in noise and line.strip()]

    # 6. Append Static (Human readable) to the Shadow Archive
    if static:
        with open(archive_file, 'a') as f:
            f.writelines(static)
        print(f"Librarian: {len(static)} lines moved to Shadow Archive.")
    else:
        print("Librarian: No static found to archive.")

    # 7. Clear the logs.txt but RETAIN the Noise (Camouflage)
    with open(log_file, 'w') as f:
        f.writelines(noise)
    print(f"Librarian: {len(noise)} noise strings maintained in active logs.")

if __name__ == "__main__":
    print("Initiating Shadow Sweep Protocol...")
    shadow_sweep()
    print("Protocol [COMPLETE].")
