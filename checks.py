import os
import re

# ==========================================
# CONFIG
# ==========================================

FOLDER = r"D:\Dataset"

# ==========================================
# REGEX
# ==========================================

# Matches:
# filename (1).pdf

duplicate_pattern = re.compile(r'^(.*)\s\((\d+)\)(\.pdf)$', re.IGNORECASE)

# ==========================================
# PROCESS
# ==========================================

renamed = 0
skipped = 0

for filename in os.listdir(FOLDER):

    match = duplicate_pattern.match(filename)

    if not match:
        continue

    base_name = match.group(1)
    extension = match.group(3)

    new_filename = base_name + extension

    old_path = os.path.join(FOLDER, filename)
    new_path = os.path.join(FOLDER, new_filename)

    # Safety check
    if os.path.exists(new_path):

        print(f"[SKIP] Target already exists:")
        print(f"       {new_filename}")

        skipped += 1
        continue

    # Rename
    os.rename(old_path, new_path)

    print(f"[RENAMED]")
    print(f"  OLD: {filename}")
    print(f"  NEW: {new_filename}\n")

    renamed += 1

# ==========================================
# SUMMARY
# ==========================================

print("\n==============================")
print("SUMMARY")
print("==============================")

print(f"Renamed : {renamed}")
print(f"Skipped : {skipped}")