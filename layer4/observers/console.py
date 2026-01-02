ILLEGAL_PATTERNS = [
    "illegal command",
    "bad command",
    "file not found"
]

def analyze_console_output(stdout: str, stderr: str):
    output = (stdout or "") + (stderr or "")
    lowered = output.lower()

    illegal = any(pat in lowered for pat in ILLEGAL_PATTERNS)

    return {
        "illegal_command": illegal,
        "raw_output": output[:500]
    }
