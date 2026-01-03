# layer5/run.py

import json
from pathlib import Path
from dataclasses import asdict

from layer5.analysis import analyze_all
from layer5.inference import infer_all_requirements
from layer5.selection import evaluate_configurations, select_canonical
from layer5.explanation import build_explanation
from layer5.models import Layer5Result


def run_layer5(execution_profiles, output_dir="layer5_output"):
    """
    Run Layer 5 end-to-end.

    Inputs:
      - execution_profiles: List of Layer 4 ExecutionProfile objects

    Outputs:
      - Layer5Result object
      - Writes artifact_result.json
    """

    # 1. Normalize execution profiles
    observations = analyze_all(execution_profiles)

    # 2. Infer requirements
    requirements = infer_all_requirements(observations)

    # 3. Evaluate & rank configurations
    evaluated = evaluate_configurations(observations, requirements)

    # 4. Select canonical configuration
    canonical = select_canonical(evaluated)
    if canonical is None:
        raise RuntimeError("Layer 5 failed: no viable configuration found")

    # 5. Build explanation
    explanation = build_explanation(canonical, requirements, observations)

    # 6. Construct final result
    result = Layer5Result(
        chosen_variant=canonical.variant,
        inferred_requirements=requirements,
        ranked_variants=evaluated,
        explanation=explanation,
    )

    # 7. Persist result
    out_dir = Path(output_dir)
    out_dir.mkdir(exist_ok=True)

    out_file = out_dir / "artifact_result.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(asdict(result), f, indent=2)

    return result
