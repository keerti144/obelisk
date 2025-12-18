def find_entry_points(artifact):
    points = []

    for f in artifact.files:
        name = f.path.lower()
        if name.endswith(".exe") or name.endswith(".com") or name.endswith(".bat"):
            points.append(f.path)

    return points
