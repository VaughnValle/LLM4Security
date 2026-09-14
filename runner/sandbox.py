from dataclasses import dataclass
from pathlib import Path
@dataclass(slots=True)
class SandboxSpec:
    workdir: Path
    image: str
    cpu_limit: float = 4.0
    memory_limit_gb: int = 8
    network_enabled: bool = False
class Sandbox:
    def __init__(self, spec: SandboxSpec): self.spec=spec
    def run(self, argv: list[str]) -> int: raise NotImplementedError('TODO: container-backed execution')
