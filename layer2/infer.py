# layer2/infer.py

def _eval_protected_mode(pm_evidence):
    """
    Decide whether protected mode is justified based on
    strength-weighted evidence.
    """
    strong = sum(1 for e in pm_evidence if e["strength"] == "strong")
    medium = sum(1 for e in pm_evidence if e["strength"] == "medium")
    weak = sum(1 for e in pm_evidence if e["strength"] == "weak")

    # Thresholds:
    # - any strong evidence
    # - or multiple corroborating weaker signals
    if strong >= 1:
        return True
    if medium >= 2:
        return True
    if weak >= 3:
        return True

    return False


def infer_requirements(scan, inspection):
    result = {
        "platforms": [],
        "cpu_class": {
            "minimum": "unknown",
            "confidence": 0.0
        },
        "memory_model": "unknown",

        # IMPORTANT:
        # graphics & sound are NOT asserted in Layer 2
        "graphics": ["text"],
        "sound": [],

        "constraints": {},
        "negative": []
    }

    # --------------------------------------
    # Platform inference
    # --------------------------------------
    if inspection["pe_exe"]:
        result["platforms"].append(("windows", 0.9))
        result["platforms"].append(("dos", 0.1))
        result["negative"].extend(["not_dos", "not_linux"])
        return result

    # Default assumption: DOS primary
    result["platforms"].append(("dos", 0.85))
    result["platforms"].append(("windows", 0.15))
    result["negative"].append("not_linux")

    # --------------------------------------
    # CPU & memory inference
    # --------------------------------------
    pm_evidence = inspection.get("pm_evidence", [])

    if _eval_protected_mode(pm_evidence):
        # Protected mode implies >= 386
        result["memory_model"] = "protected"
        result["cpu_class"] = {
            "minimum": "386",
            "confidence": 0.7
        }
        result["constraints"]["requires_dos_extender"] = True
        result["negative"].append("not_windows_nt")

    else:
        # No protected-mode commitment
        result["memory_model"] = "unknown"
        result["constraints"]["requires_dos_extender"] = False

        # Very weak heuristic: large EXE implies >8086
        max_size = max(inspection.get("exe_sizes", {}).values(), default=0)

        if max_size > 300_000:
            result["cpu_class"] = {
                "minimum": "286",
                "confidence": 0.3
            }
        else:
            result["cpu_class"] = {
                "minimum": "8086",
                "confidence": 0.3
            }

    return result
