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
    # --------------------------------------
    # Platform candidates
    # --------------------------------------
    platforms = [
        PlatformCandidate(platform=p, confidence=c)
        for p, c in inference["platforms"]
    ]

    # --------------------------------------
    # Entry points
    # --------------------------------------
    entry_points = [
        EntryPoint(
            path=p,
            confidence=entry_confidence(p, inspection)
        )
        for p in candidates
    ]

    # --------------------------------------
    # Raw evidence (for audit & Layer 3)
    # --------------------------------------
    evidence = {
        "pm_evidence": inspection.get("pm_evidence", []),
        "graphics_evidence": inspection.get("graphics_evidence", []),
        "sound_evidence": inspection.get("sound_evidence", [])
    }

    # --------------------------------------
    # Execution-relevant evidence
    # (only derived from confident inference)
    # --------------------------------------
    execution_evidence = {}

    if inference["memory_model"] == "protected":
        execution_evidence["requires_386"] = list({
            e["file"] for e in inspection.get("pm_evidence", [])
        })

    # --------------------------------------
    # Final SystemProfile
    # --------------------------------------
    return SystemProfile(
        artifact_root=artifact.normalized_path,
        platform_candidates=platforms,

        cpu_class=inference["cpu_class"],
        memory_model=inference["memory_model"],

        # Layer 2 assertions are conservative
        graphics=["text"],
        sound=[],

        # Evidence-only fields
        graphics_evidence=inspection.get("graphics_evidence", []),
        sound_evidence=inspection.get("sound_evidence", []),

        entry_points=entry_points,

        constraints=inference["constraints"],
        negative_constraints=inference["negative"],

        evidence=evidence,
        execution_evidence=execution_evidence
    )
