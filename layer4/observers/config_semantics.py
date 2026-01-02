def parse_dosbox_config(conf_path):
    semantics = {
        "timing_mode": "unknown",
        "sound_enabled": False,
        "graphics_mode": "unknown"
    }

    try:
        text = open(conf_path, "r", errors="ignore").read().lower()
    except Exception:
        return semantics

    # Timing
    if "cycles=auto" in text:
        semantics["timing_mode"] = "adaptive"
    elif "cycles=" in text:
        semantics["timing_mode"] = "fixed"

    # Sound
    if "sbtype=" in text and "sbtype=none" not in text:
        semantics["sound_enabled"] = True

    # Graphics
    if "svga" in text:
        semantics["graphics_mode"] = "svga"
    elif "vga" in text:
        semantics["graphics_mode"] = "vga"

    return semantics
