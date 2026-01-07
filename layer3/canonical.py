from dataclasses import dataclass
from typing import List

@dataclass
class CanonicalMachine:
    """
    Emulator-agnostic description of the minimum viable machine.
    """
    cpu: str              # "286", "386", "486"
    memory_mb: int
    graphics: str         # "text", "vga", "svga"
    sound: List[str]      # ["adlib"], ["sb16"]
    dos_extender: bool
