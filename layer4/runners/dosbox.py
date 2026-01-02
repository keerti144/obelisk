import subprocess
from pathlib import Path

from pathlib import Path


DOSBOX_PATH = r"C:\Program Files (x86)\DOSBox-0.74-3\DOSBox.exe"

class DOSBoxRunner:
    def launch(self, plan):
        LOG_DIR = Path("layer4_output/logs")
        LOG_DIR.mkdir(parents=True, exist_ok=True)

        log_path = LOG_DIR / f"{plan.variant}_dosbox.log"

        proc = subprocess.Popen(
            [
                DOSBOX_PATH,
                "-conf", plan.config_path,
                "-logfile", str(log_path)
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        return proc, log_path
