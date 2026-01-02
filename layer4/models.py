from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ExecutionProfile:
    # Identity
    emulator: str
    variant: str
    entry_point: str

    # Execution phases (facts derived from sentinels + time)
    phases: Dict[str, bool]

    # Ground-truth execution evidence (OS-level)
    sentinels: Dict[str, Optional[int]]

    # Configuration metadata (input, not inference)
    config: Dict[str, str]

    # Optional diagnostics (non-semantic)
    host_telemetry: Dict[str, object]
