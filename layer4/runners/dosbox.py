# layer4/runners/dosbox.py
import subprocess
import time
from layer4.execution_result import ExecutionResult

FATAL_PATTERNS = [
    "illegal opcode",
    "cpu requires",
    "abnormal program termination",
    "failed to initialize"
]

DOSBOX_PATH = "C:\\Program Files (x86)\\DOSBox-0.74-3\\DOSBox.exe"

class DOSBoxRunner:

    def launch(self, plan) -> ExecutionResult:
        start = time.time()
        observations = []
        signals = {
            "process_started": False,
            "alive_after_1s": False,
            "alive_after_10s": False,
            "fatal_error": False
        }

        try:
            proc = subprocess.Popen(
                [DOSBOX_PATH, "-conf", plan.config_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            signals["process_started"] = True
            observations.append("dosbox process started")

            time.sleep(1)
            if proc.poll() is None:
                signals["alive_after_1s"] = True

            time.sleep(9)
            if proc.poll() is None:
                signals["alive_after_10s"] = True

            # Collect output so far
            stdout, stderr = proc.communicate(timeout=1)
            output = (stdout or "") + (stderr or "")

            for pat in FATAL_PATTERNS:
                if pat.lower() in output.lower():
                    signals["fatal_error"] = True
                    observations.append(f"fatal pattern detected: {pat}")
                    break

        except subprocess.TimeoutExpired:
            observations.append("process exceeded observation window")

        except Exception as e:
            observations.append(f"exception during launch: {e}")

        finally:
            if 'proc' in locals() and proc.poll() is None:
                proc.terminate()

        runtime = time.time() - start
        exit_code = proc.poll() if 'proc' in locals() else None

        # ---- Classification ----
        if signals["alive_after_10s"] and not signals["fatal_error"]:
            status = "success"
        elif signals["process_started"]:
            status = "partial"
        else:
            status = "failure"

        return ExecutionResult(
            emulator="dosbox",
            variant=plan.variant,
            entry_point=plan.entry_point,
            status=status,
            runtime_seconds=round(runtime, 2),
            exit_code=exit_code,
            signals=signals,
            observations=observations
        )
