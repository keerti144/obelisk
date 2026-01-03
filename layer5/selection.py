# layer5/selection.py

from layer5.models import EvaluatedConfiguration


def satisfies_requirements(observation, requirements):
    """
    Check whether a configuration satisfies all required features.
    """
    violations = []

    for req in requirements:
        if req.status == "required":
            value = observation.features.get(req.feature)
            if not value:
                violations.append(f"{req.feature} required")

    return (len(violations) == 0), violations


def score_configuration(observation):
    """
    Lower score is better.
    Policy-based scoring (PCem-safe).
    """

    score = 0.0

    # Prefer sound only if required (sound itself has no penalty)
    # Penalize unnecessary complexity

    if observation.features.get("video") == "svga":
        score += 1.0

    if observation.features.get("timing") == "adaptive":
        score += 0.5

    return score


def evaluate_configurations(observations, requirements):
    """
    Evaluate and rank all configurations.
    """

    evaluated = []

    for obs in observations:
        if not obs.stable:
            continue  # Hard discard

        ok, violations = satisfies_requirements(obs, requirements)

        score = score_configuration(obs) if ok else float("inf")

        evaluated.append(
            EvaluatedConfiguration(
                variant=obs.variant,
                stable=obs.stable,
                satisfies_requirements=ok,
                score=score,
                violations=violations,
            )
        )

    evaluated.sort(key=lambda c: c.score)
    return evaluated


def select_canonical(evaluated):
    """
    Select the best configuration.
    """
    for cfg in evaluated:
        if cfg.satisfies_requirements:
            return cfg
    return None
