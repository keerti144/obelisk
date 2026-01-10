#V1.0 - Layer 1 (Artifact Extraction)

from layer1.ingest import ingest
from dataclasses import asdict
import json

artifact = ingest("input/MarioGG")
artifact_dict = asdict(artifact)
with open("artifact_descriptor.txt", "w", encoding="utf-8") as f:
    json.dump(artifact_dict, f, indent=2)

print("Artifact descriptor written to artifact_descriptor.txt")

#V2.0 - Layer 2 (System Inference)

from layer2.analyze import analyze

profile = analyze(artifact)
output = json.dumps(asdict(profile), indent=2)

with open("artifact_profile.txt", "w", encoding="utf-8") as f:
    f.write(output)
print("Possible configuration written to artifact_profile.txt")

print(output)

# V3.0 – Layer 3 (Configuration Synthesis)

from layer3.synthesize import synthesize

plans = synthesize(profile)   # List[LaunchPlan]

layer3_output = [
    asdict(plan) for plan in plans
]

with open("artifact_launch_plans.txt", "w", encoding="utf-8") as f:
    json.dump(layer3_output, f, indent=2)

print("Launch plans written to artifact_launch_plans.txt")

print("\n=== Layer 3 Launch Plans ===")
for plan in plans:
    print(
        f"- variant={plan.variant:15} "
        f"priority={plan.priority} "
        f"emulator={plan.emulator} "
        f"entry={plan.entry_point}"
    )

# V4.0 – Layer 4 (Execution & Validation)

from layer4.run import run_layer4
from pathlib import Path

profiles = run_layer4(plans)

print("\n=== Layer 4 Execution Profiles ===\n")

for profile in profiles:
    print(json.dumps(asdict(profile), indent=2))

out_dir = Path("layer4_output")
out_dir.mkdir(exist_ok=True)


for profile in profiles:
    out_file = out_dir / f"{profile.variant}_execution_profile.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(asdict(profile), f, indent=2)

# V5.0 – Layer 5 (Telemetry & Reasoning)

from layer5.run import run_layer5

layer5_result = run_layer5(profiles)

print("\n=== Layer 5 Final Result ===\n")
print("Chosen configuration:", layer5_result.chosen_variant)
print("\nExplanation:")
print(layer5_result.explanation)


