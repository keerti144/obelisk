# layer5/models.py

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ExecutionObservation:
    """
    Normalized, emulator-agnostic view of one execution attempt.
    """
    emulator: str
    variant: str
    entry_point: str

    stable: bool
    unstable: bool

    features: Dict[str, object]      # sound, video, timing, cpu (later)
    sound_outcome: Optional[str]

    host_telemetry: Dict[str, object]


@dataclass
class InferredRequirement:
    """
    Result of correlating features with outcomes.
    """
    feature: str                     # e.g. "sound"
    status: str                      # required | optional | forbidden | unknown
    confidence: float
    evidence: List[str]


@dataclass
class EvaluatedConfiguration:
    """
    One configuration after inference + policy evaluation.
    """
    variant: str
    stable: bool
    satisfies_requirements: bool
    score: float
    violations: List[str]


@dataclass
class Layer5Result:
    """
    Final output of Layer 5.
    """
    chosen_variant: str
    inferred_requirements: List[InferredRequirement]
    ranked_variants: List[EvaluatedConfiguration]
    explanation: str

# layer5/models.py (small extension)

@dataclass
class InferredRequirement:
    feature: str
    status: str              # required | optional | forbidden | preferred | unknown
    confidence: float
    evidence: List[str]
    preferred_value: object = None

