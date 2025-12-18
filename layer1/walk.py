import os

def walk_directory(root: str):
    entries = []
    for base, _, files in os.walk(root):
        for f in files:
            full = os.path.join(base, f)
            rel = os.path.relpath(full, root)
            entries.append((full, rel))
    return sorted(entries, key=lambda x: x[1])
