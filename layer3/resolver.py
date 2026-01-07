from layer3.canonical import CanonicalMachine

CPU_ORDER = ["286", "386", "486"]

def escalate_cpu(min_cpu: str) -> str:
    if min_cpu not in CPU_ORDER:
        return "386"
    i = CPU_ORDER.index(min_cpu)
    return CPU_ORDER[min(i + 1, len(CPU_ORDER) - 1)]


def resolve_machine(system_profile) -> CanonicalMachine:
    # ---- CPU ----
    cpu_info = system_profile.cpu_class
    min_cpu = cpu_info.get("minimum", "286")

    cpu = (
        escalate_cpu(min_cpu)
        if cpu_info.get("confidence", 0) < 0.5
        else min_cpu
    )

    # ---- Memory / DOS extender ----
    requires_ext = system_profile.constraints.get(
        "requires_dos_extender", False
    )

    memory_mb = 32 if requires_ext else 16
    dos_extender = requires_ext

    # ---- Graphics ----
    if "svga" in system_profile.graphics:
        graphics = "svga"
    elif "vga" in system_profile.graphics or "text" in system_profile.graphics:
        graphics = "vga"
    else:
        graphics = "vga"

    # ---- Sound ----
    if "sb16" in system_profile.sound_evidence:
        sound = ["sb16"]
    elif "adlib" in system_profile.sound_evidence:
        sound = ["adlib"]
    else:
        sound = []

    return CanonicalMachine(
        cpu=cpu,
        memory_mb=memory_mb,
        graphics=graphics,
        sound=sound,
        dos_extender=dos_extender
    )
