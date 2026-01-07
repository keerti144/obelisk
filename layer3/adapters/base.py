from abc import ABC, abstractmethod
from typing import List
from layer3.canonical import CanonicalMachine
from layer3.launchplan import LaunchPlan

class EmulatorAdapter(ABC):

    @abstractmethod
    def generate_variants(
        self,
        machine: CanonicalMachine,
        entry_point: str
    ) -> List[LaunchPlan]:
        pass
