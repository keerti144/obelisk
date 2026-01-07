# layer4/execute.py
from layer4.runners.dosbox import DOSBoxRunner

def execute(plans):
    """
    Execute LaunchPlans in priority order.
    Stops early on first success.
    """
    results = []
    runner = DOSBoxRunner()
    print()

    for plan in plans:
        print(f"[Layer 4] Running variant={plan.variant} priority={plan.priority}")
        result = runner.launch(plan)
        results.append(result)

        print(f"[Layer 4] Result={result.status} runtime={result.runtime_seconds}s")

        #if result.status == "success":
        #    print("[Layer 4] Success achieved, stopping execution")  #Uncomment this later for optimal running
        #    break

    return results
