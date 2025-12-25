from dataclasses import dataclass
from typing import List, Dict


# --------------------------------------
# Platform likelihoods
# --------------------------------------

@dataclass
class PlatformCandidate:
    platform: str          # "dos", "windows", "unknown"
    confidence: float      # 0.0 – 1.0


# --------------------------------------
# Entry points
# --------------------------------------

@dataclass
class EntryPoint:
    path: str
    confidence: float      # likelihood this is a primary entry point


# --------------------------------------
# Final Layer-2 output
# --------------------------------------

@dataclass
class SystemProfile:
    # Platform inference
    artifact_root: str 
    platform_candidates: List[PlatformCandidate]

    # CPU & execution model (conservative)
    cpu_class: Dict        # {"minimum": "8086|286|386|unknown", "confidence": float}
    memory_model: str      # "real", "protected", "unknown"

    # Layer-2 assertions (minimal)
    graphics: List[str]    # always ["text"]
    sound: List[str]       # empty; sound is runtime-optional

    # Evidence only (non-binding)
    graphics_evidence: List[str]
    sound_evidence: List[str]

    # Execution candidates
    entry_points: List[EntryPoint]

    # Constraints inferred from strong evidence
    constraints: Dict[str, bool]
    negative_constraints: List[str]

    # Raw evidence & derived execution hints (for audit / Layer 3)
    evidence: Dict[str, list]
    execution_evidence: Dict[str, list]
