import time
from pathlib import Path

from layer4.models import ExecutionProfile
from layer4.phases import PHASES
from layer4.observers.config_semantics import parse_dosbox_config
from layer4.observers.telemetry import sample_cpu


class ExecutionProfiler:
    def profile(self, plan, runner):
        # ---- Phase initialization ----
        phases = {p: False for p in PHASES}

        # ---- Resolve artifact root (mounted as C:) ----
        artifact_root = Path(plan.artifact_root)

        # ---- CLEANUP (MUST BE BEFORE LAUNCH) ----
        for fname in ["STARTED.TXT", "ERRLVL.TXT", "FINISH.TXT"]:
            f = artifact_root / fname
            if f.exists():
                f.unlink()

        # ---- Launch emulator ----
        proc, _ = runner.launch(plan)
        phases["emulator_started"] = True

        # ---- Allow AUTOEXEC to begin ----
        time.sleep(1)
        phases["filesystem_mounted"] = True

        # ---- Observation window ----
        OBSERVATION_WINDOW = 8
        time.sleep(OBSERVATION_WINDOW)

        # ---- Sentinel files (ground truth) ----
        started = (artifact_root / "STARTED.TXT").exists()
        finished = (artifact_root / "FINISH.TXT").exists()

        errorlevel = None
        err_file = artifact_root / "ERRLVL.TXT"
        if err_file.exists():
            try:
                errorlevel = int(err_file.read_text().strip())
            except ValueError:
                errorlevel = None  # valid DOS behavior

        # ---- Phase logic (NO inference) ----
        phases["entrypoint_invoked"] = started
        phases["control_transferred"] = started

        phases["stability_window_reached"] = (
            started and (
                not finished or
                (finished and errorlevel == 0)
            )
        )

        # ---- Optional diagnostics ----
        host_telemetry = sample_cpu(proc)

        # ---- Cleanup emulator ----
        try:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                except Exception:
                    proc.kill()
        except Exception:
            pass

        # ---- Config metadata (input, not execution) ----
        config = parse_dosbox_config(plan.config_path)

        # ---- Build final profile ----
        return ExecutionProfile(
            emulator="dosbox",
            variant=plan.variant,
            entry_point=plan.entry_point,
            phases=phases,
            sentinels={
                "started": started,
                "finished": finished,
                "errorlevel": errorlevel
            },
            config=config,
            host_telemetry=host_telemetry
        )
