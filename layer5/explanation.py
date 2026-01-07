# layer5/explanation.py

def build_explanation(canonical, requirements, observations):
    """
    Generate a human-readable explanation for the selected configuration.
    """

    lines = []

    # Explain inferred requirements
    for req in requirements:
        if req.status == "required":
            lines.append(
                f"{req.feature.capitalize()} support is required for stable execution."
            )
        elif req.status == "optional":
            lines.append(
                f"{req.feature.capitalize()} configuration does not affect stability."
            )

    # Explain selection
    lines.append(
        f"The '{canonical.variant}' configuration was selected as it satisfies all "
        f"inferred requirements while minimizing hardware and timing complexity."
    )

    return " ".join(lines)
