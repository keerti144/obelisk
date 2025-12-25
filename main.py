#V1.0 - Layer 1 (Artifact Extraction)

from layer1.ingest import ingest
from dataclasses import asdict
import json

artifact = ingest("input/Mario")
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

from layer4.execute import execute

results = execute(plans)

layer4_output = [asdict(r) for r in results]

with open("artifact_execution_results.txt", "w", encoding="utf-8") as f:
    json.dump(layer4_output, f, indent=2)

print("\n=== Layer 4 Execution Results ===")
print(json.dumps(layer4_output, indent=2))