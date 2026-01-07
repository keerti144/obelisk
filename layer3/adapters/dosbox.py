from typing import List
from layer3.adapters.base import EmulatorAdapter
from layer3.launchplan import LaunchPlan
from layer3.canonical import CanonicalMachine

class DOSBoxAdapter(EmulatorAdapter):

    def generate_variants(
        self,
        machine: CanonicalMachine,
        entry_point: str,
        artifact_root: str
    ) -> List[LaunchPlan]:

        plans = []

        # Variant 1: minimal viable (strict)
        plans.append(
            self._make_plan(
                machine, entry_point, artifact_root,
                variant="minimal",
                priority=1,
                cycles="3000",
                sound=False,
                svga=False
            )
        )

        # Variant 2: minimal + sound
        if machine.sound:
            plans.append(
                self._make_plan(
                    machine, entry_point, artifact_root,
                    variant="minimal+sound",
                    priority=2,
                    cycles="3000",
                    sound=True,
                    svga=False
                )
            )

        # Variant 3: auto CPU (less strict)
        plans.append(
            self._make_plan(
                machine, entry_point, artifact_root,
                variant="auto-cpu",
                priority=3,
                cycles="auto",
                sound=False,
                svga=False
            )
        )

        # Variant 4: permissive fallback
        plans.append(
            self._make_plan(
                machine, entry_point, artifact_root,
                variant="permissive",
                priority=4,
                cycles="auto",
                sound=True,
                svga=True
            )
        )

        return plans

    def _make_plan(
        self,
        machine: CanonicalMachine,
        entry_point: str,
        artifact_root: str,
        variant: str,
        priority: int,
        cycles: str,
        sound: bool,
        svga: bool
    ) -> LaunchPlan:

        conf_path = f"dosbox_{variant}.conf"

        with open(conf_path, "w") as f:
            f.write("[cpu]\n")
            f.write(f"cputype={machine.cpu}\n")
            f.write("core=normal\n")
            f.write(f"cycles={cycles}\n\n")

            f.write("[memory]\n")
            f.write(f"memsize={machine.memory_mb}\n\n")

            f.write("[dosbox]\n")
            f.write("machine=svga_s3\n" if svga else "machine=vga\n")
            f.write("\n")

            f.write("[sblaster]\n")
            if sound and machine.sound:
                f.write("sbtype=sb16\n")
            else:
                f.write("sbtype=none\n")

            f.write("\n[autoexec]\n")
            f.write(f'mount c "{artifact_root}"\n')
            f.write("c:\n")
            f.write(f"{entry_point}\n")

        return LaunchPlan(
            emulator="dosbox",
            config_path=conf_path,
            entry_point=entry_point,
            timeout=20,
            confidence=0.6,
            variant=variant,
            priority=priority
        )
