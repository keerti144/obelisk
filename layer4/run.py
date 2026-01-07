from layer4.runners.dosbox import DOSBoxRunner
from layer4.profiler import ExecutionProfiler

def run_layer4(plans):
    runner = DOSBoxRunner()
    profiler = ExecutionProfiler()

    profiles = []
    for plan in plans:
        profiles.append(profiler.profile(plan, runner))

    return profiles
