from layer2.models import SystemProfile, PlatformCandidate, EntryPoint

def entry_confidence(path, inspection):
    score = 0.3

    size = inspection.get("exe_sizes", {}).get(path, 0)

    if size > 300_000:
        score += 0.4

    name = path.lower()
    if not any(k in name for k in ["setup", "readme", "install", "config"]):
        score += 0.2

    return min(score, 0.95)


def synthesize(artifact, scan, candidates, inspection, inference):
    platforms = [
        PlatformCandidate(p, c) for p, c in inference["platforms"]
    ]

    entry_points = [
        EntryPoint(
            path=p,
            confidence=entry_confidence(p, inspection)
        )
        for p in candidates
    ]

    evidence = {
        "dos_extender": inspection["dos_extender"],
        "graphics": inspection["graphics"],
        "sound": inspection["sound"]
    }

    execution_evidence = {}

    if inspection.get("dos_extender"):
        execution_evidence["protected_mode"] = inspection.get(
            "protected_mode_evidence", []
        )
        execution_evidence["requires_386"] = inspection.get(
            "protected_mode_evidence", []
        )

    return SystemProfile(
        platform_candidates=platforms,
        cpu_class=inference["cpu_class"],
        memory_model=inference["memory_model"],
        graphics=inference["graphics"],
        sound=inference["sound"],
        entry_points=entry_points,
        constraints=inference["constraints"],
        negative_constraints=inference["negative"],
        evidence=evidence,
        execution_evidence=execution_evidence
    )
