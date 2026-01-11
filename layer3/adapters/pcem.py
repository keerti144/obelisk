from typing import List
from layer3.adapters.base import EmulatorAdapter
from layer3.launchplan import LaunchPlan
from layer3.canonical import CanonicalMachine

class PCemAdapter(EmulatorAdapter):

    def generate_variants(
        self,
        machine: CanonicalMachine,
        artifact_root: str,
        system_profile
    ) -> List[LaunchPlan]:

        # Stub: single conservative machine
        return [
            LaunchPlan(
                emulator="pcem",
                config_path="pcem_default.cfg",
                artifact_root=artifact_root,
                entry_point="",      # no entry point for OS boot
                timeout=300,         # PCem is slow
                confidence=0.5,
                variant="pcem-default",
                priority=1
            )
        ]
