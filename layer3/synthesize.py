from layer3.resolver import resolve_machine
from layer3.adapters.dosbox import DOSBoxAdapter
from layer3.adapters.pcem import PCemAdapter   # NEW

def synthesize(system_profile):
    machine = resolve_machine(system_profile)

    # -------------------------------------------------
    # PROGRAM EXECUTION (DOSBox path – unchanged)
    # -------------------------------------------------
    if system_profile.execution_mode == "program":
        entry = max(
            system_profile.entry_points,
            key=lambda e: e.confidence
        ).path

        adapter = DOSBoxAdapter()
        plans = adapter.generate_variants(
            machine,
            entry,
            system_profile.artifact_root,
            system_profile
        )

        return sorted(plans, key=lambda p: p.priority)

    # -------------------------------------------------
    # BOOTABLE OS EXECUTION (PCem path)
    # -------------------------------------------------
    elif system_profile.execution_mode == "bootable_os":
        adapter = PCemAdapter()
        plans = adapter.generate_variants(
            machine,
            system_profile.artifact_root,
            system_profile
        )

        return sorted(plans, key=lambda p: p.priority)

    # -------------------------------------------------
    # UNKNOWN EXECUTION MODE
    # -------------------------------------------------
    else:
        return []