# layer4/execution_result.py
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class ExecutionResult:
    emulator: str
    variant: str
    entry_point: str

    status: str                 # "success" | "partial" | "failure"
    runtime_seconds: float
    exit_code: Optional[int]

    signals: Dict[str, bool]
    observations: List[str]
