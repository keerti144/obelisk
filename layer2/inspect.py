import os

DEBUG_DUMP_STRINGS = True
DEBUG_OUTPUT_DIR = "layer2_debug"

DOS_EXTENDER_SIGNATURES = [
    # Rational / Watcom
    "dos/4gw",
    "dos4gw",
    "dos/16m",
    "dos16m",
    "dos16m.386",

    # DPMI / VCPI
    "dpmi",
    "vcpi",

    # CWSDPMI / PMODE
    "cwsdpmi",
    "pmode/w",

    # Explicit protected-mode declarations
    "protected mode",
    "general protection fault",
    "page fault",
    "gdt",
    "ldt",
    "selector"
]

SOUND_SIGNATURES = {
    "sb16": ["blaster", "sb16", "sbport", "sbdma", "sbirq"],
    "adlib": ["adlib"],
    "pc_speaker": ["pc speaker", "speaker"],
    "gus": ["gravis", "ultrasound", "gus"]
}

GRAPHICS_SIGNATURES = {
    "vga": ["vga", "320x200"],
    "ega": ["ega"],
    "cga": ["cga"]
}

SCAN_LIMIT = 64 * 1024  # 64 KB

def inspect_candidates(artifact, candidates):
    results = {
        "dos_extender": [],
        "protected_mode_evidence": set(),   # NEW
        "sound": set(),
        "graphics": set(),
        "mz_only": [],
        "pe_exe": [],
        "exe_sizes": {}
    }

    for rel in candidates:
        full = os.path.join(artifact.normalized_path, rel)

        try:
            size = os.path.getsize(full)
            results["exe_sizes"][rel] = size

            with open(full, "rb") as f:
                data = f.read(SCAN_LIMIT)
                if DEBUG_DUMP_STRINGS:
                    os.makedirs(DEBUG_OUTPUT_DIR, exist_ok=True)

                    out_path = os.path.join(
                        DEBUG_OUTPUT_DIR,
                        rel.replace(os.sep, "_") + ".strings.txt"
                    )

                    strings = extract_printable_strings(data)

                    with open(out_path, "w", encoding="utf-8", errors="ignore") as out:
                        out.write(f"--- STRINGS EXTRACTED FROM {rel} ---\n\n")
                        for s in strings:
                            out.write(s + "\n")

        except Exception:
            continue

        # Header inspection
        if data.startswith(b"MZ"):
            if b"PE\0\0" in data:
                results["pe_exe"].append(rel)
            else:
                results["mz_only"].append(rel)

        text = data.lower().decode(errors="ignore")

        # DOS extender detection
        for sig in DOS_EXTENDER_SIGNATURES:
            if sig in text:
                results["dos_extender"].append(sig)
                results["protected_mode_evidence"].add(rel)

        # Sound detection
        for device, tokens in SOUND_SIGNATURES.items():
            for t in tokens:
                if t in text:
                    results["sound"].add(device)

        # Graphics detection
        for mode, tokens in GRAPHICS_SIGNATURES.items():
            for t in tokens:
                if t in text:
                    results["graphics"].add(mode)

    # Normalize sets → lists
    results["sound"] = list(results["sound"])
    results["graphics"] = list(results["graphics"])
    results["protected_mode_evidence"] = list(results["protected_mode_evidence"])

    return results

def extract_printable_strings(data, min_len=4):
    result = []
    current = []

    for b in data:
        if 32 <= b <= 126:  # printable ASCII
            current.append(chr(b))
        else:
            if len(current) >= min_len:
                result.append("".join(current))
            current = []

    if len(current) >= min_len:
        result.append("".join(current))

    return result
