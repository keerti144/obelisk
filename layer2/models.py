from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class PlatformCandidate:
    platform: str          # "dos", "windows_9x", "windows_nt", "unknown"
    confidence: float

@dataclass
class EntryPoint:
    path: str
    confidence: float

@dataclass
class SystemProfile:
    platform_candidates: List[PlatformCandidate]

    cpu_class: str                  # "8086", "286", "386", "unknown"
    memory_model: str               # "real", "protected", "unknown"

    graphics: List[str]
    sound: List[str]

    entry_points: List[EntryPoint]

    constraints: Dict[str, bool]
    negative_constraints: List[str]

    evidence: Dict[str, List[str]]          # raw strings / tokens
    execution_evidence: Dict[str, List[str]]  # NEW

