# layer2/infer.py
def infer_requirements(scan, inspection):
    result = {
        "platforms": [],
        "cpu_class": "unknown",
        "memory_model": "unknown",
        "graphics": [],
        "sound": [],
        "constraints": {},
        "negative": []
    }

    # --- Platform inference ---
    if inspection["pe_exe"]:
        result["platforms"].append(("windows", 0.9))
        result["platforms"].append(("dos", 0.1))
        result["negative"].append("not_dos")
        result["negative"].append("not_linux")
        return result

    # Default: DOS dominant
    result["platforms"].append(("dos", 0.85))
    result["platforms"].append(("windows", 0.15))
    result["negative"].append("not_linux")

    # --- CPU & memory inference ---
    if inspection["dos_extender"]:
        result["cpu_class"] = "386"
        result["memory_model"] = "protected"
        result["constraints"]["requires_dos_extender"] = True
        result["negative"].append("not_windows_nt")
    else:
        # Heuristic: large EXE likely not 8086-only
        max_size = max(inspection["exe_sizes"].values(), default=0)

        if max_size > 300_000:
            result["cpu_class"] = "286"
            result["memory_model"] = "real"
        else:
            result["cpu_class"] = "8086"
            result["memory_model"] = "real"

        result["constraints"]["requires_dos_extender"] = False

    # --- Graphics & sound ---
    result["graphics"] = inspection["graphics"]
    result["sound"] = inspection["sound"]

    return result
