# layer5/analysis.py

from layer5.models import ExecutionObservation


def analyze_execution(profile) -> ExecutionObservation:
    """
    Normalize a Layer 4 ExecutionProfile into an ExecutionObservation.
    """

    phases = profile.phases

    stable = bool(phases.get("stability_window_reached"))
    unstable = bool(phases.get("control_transferred")) and not stable

    features = {
        "sound": profile.config.get("sound_enabled"),
        "video": profile.config.get("graphics_mode"),
        "timing": profile.config.get("timing_mode"),
    }

    return ExecutionObservation(
        emulator=profile.emulator,
        variant=profile.variant,
        entry_point=profile.entry_point,

        stable=stable,
        unstable=unstable,

        features=features,
        sound_outcome=profile.sound_outcome,

        host_telemetry=profile.host_telemetry,
    )


def analyze_all(profiles):
    """
    Batch version.
    """
    return [analyze_execution(p) for p in profiles]
