def global_scan(artifact):
    signals = {
        "exe": 0,
        "com": 0,
        "bat": 0,
        "dll": 0,
        "pyd": 0,
        "boot": 0
    }

    for f in artifact.files:
        name = f.path.lower()
        if name.endswith(".exe"):
            signals["exe"] += 1
        elif name.endswith(".com"):
            signals["com"] += 1
        elif name.endswith(".bat"):
            signals["bat"] += 1
        elif name.endswith(".dll"):
            signals["dll"] += 1
        elif name.endswith(".pyd"):
            signals["pyd"] += 1

    return signals
