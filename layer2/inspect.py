import os

DEBUG_DUMP_STRINGS = True
DEBUG_OUTPUT_DIR = "layer2_debug"

SCAN_LIMIT = 64 * 1024  # 64 KB


# ==============================
# Protected-mode evidence
# (split by strength)
# ==============================

STRONG_PM_SIGS = [
    # Rational / Watcom
    "dos/4gw",
    "dos4gw",
    "dos/16m",
    "dos16m",
    "dos16m.386",

    # CWSDPMI / PMODE
    "cwsdpmi",
    "pmode/w"
]

MEDIUM_PM_SIGS = [
    # DPMI / VCPI indicators
    "dpmi",
    "vcpi"
]

WEAK_PM_SIGS = [
    # Lexical / incidental tokens
    "protected mode",
    "general protection fault",
    "page fault",
    "gdt",
    "ldt",
    "selector"
]


# ==============================
# Graphics & sound evidence
# (evidence only, not assertions)
# ==============================

SOUND_SIGNATURES = {
    "sb16": ["blaster", "sb16", "sbport", "sbdma", "sbirq"],
    "adlib": ["adlib"],
    "pc_speaker": ["pc speaker", "speaker"],
    "gus": ["gravis", "ultrasound", "gus"]
}

SOUND_AWARE_TOKENS = [
    "sound",
    "music",
    "volume",
    "effects_volume",
    "music_volume",
    "digital sound"
]

GRAPHICS_SIGNATURES = {
    "vga": ["vga", "320x200"],
    "ega": ["ega"],
    "cga": ["cga"]
}


def inspect_candidates(artifact, candidates):
    results = {
        # Execution / format info
        "mz_only": [],
        "pe_exe": [],
        "exe_sizes": {},

        # Evidence (no conclusions here)
        "pm_evidence": [],           # list of {file, sig, strength}
        "graphics_evidence": set(),
        "sound_evidence": set(),
        "sound_awareness_evidence": set()
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

        # --------------------------
        # Header inspection
        # --------------------------
        if data.startswith(b"MZ"):
            if b"PE\0\0" in data:
                results["pe_exe"].append(rel)
            else:
                results["mz_only"].append(rel)

        text = data.lower().decode(errors="ignore")

        # --------------------------
        # Protected-mode evidence
        # --------------------------
        for sig in STRONG_PM_SIGS:
            if sig in text:
                results["pm_evidence"].append({
                    "file": rel,
                    "sig": sig,
                    "strength": "strong"
                })

        for sig in MEDIUM_PM_SIGS:
            if sig in text:
                results["pm_evidence"].append({
                    "file": rel,
                    "sig": sig,
                    "strength": "medium"
                })

        for sig in WEAK_PM_SIGS:
            if sig in text:
                results["pm_evidence"].append({
                    "file": rel,
                    "sig": sig,
                    "strength": "weak"
                })

        # --------------------------
        # Sound evidence (strings only)
        # --------------------------
        for device, tokens in SOUND_SIGNATURES.items():
            for t in tokens:
                if t in text:
                    results["sound_evidence"].add(device)

        # --------------------------
        # Graphics evidence (strings only)
        # --------------------------
        for mode, tokens in GRAPHICS_SIGNATURES.items():
            for t in tokens:
                if t in text:
                    results["graphics_evidence"].add(mode)

        for token in SOUND_AWARE_TOKENS:
            if token in text:
                results["sound_awareness_evidence"].add(token)

    # Normalize sets → lists
    results["sound_evidence"] = list(results["sound_evidence"])
    results["sound_awareness_evidence"] = list(results["sound_awareness_evidence"])
    results["graphics_evidence"] = list(results["graphics_evidence"])

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
