MAGIC_BYTES = {
    b"MZ": "exe",
    b"PK\x03\x04": "zip",
    b"\xEB\x3C\x90": "boot_sector",
    b"\x55\xAA": "boot_signature"
}

def detect_magic(path: str) -> str:
    try:
        with open(path, "rb") as f:
            header = f.read(4)
        for magic, ftype in MAGIC_BYTES.items():
            if header.startswith(magic):
                return ftype
    except Exception:
        pass
    return "unknown"

def detect_extension(filename: str) -> str:
    name = filename.lower()
    if name.endswith(".exe"):
        return "exe"
    if name.endswith(".com"):
        return "com"
    if name.endswith(".img") or name.endswith(".iso"):
        return "disk_image"
    if name.endswith(".zip"):
        return "zip"
    if name.endswith(".dll"):
        return "dll"
    if name.endswith(".pyd"):
        return "pyd"
    return "unknown"

def detect_file_type(path: str) -> str:
    magic = detect_magic(path)
    if magic != "unknown":
        return magic
    return detect_extension(path)
