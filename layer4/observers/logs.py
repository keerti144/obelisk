def parse_dosbox_log(log_path):
    facts = {
        "sound_detected": None,
        "xms_detected": None,
        "errors": []
    }

    if not log_path.exists():
        return facts

    text = log_path.read_text(errors="ignore").lower()

    if "sound blaster detected" in text:
        facts["sound_detected"] = True
    if "no sound card detected" in text:
        facts["sound_detected"] = False

    if "xms" in text:
        facts["xms_detected"] = True

    for line in text.splitlines():
        if "error" in line or "illegal" in line:
            facts["errors"].append(line.strip())

    return facts
