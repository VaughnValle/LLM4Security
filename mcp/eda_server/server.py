from dataclasses import dataclass
from pathlib import Path
@dataclass(slots=True)
class ToolResult:
    ok: bool
    summary: str
    artifact_paths: list[str]
def compile_rtl(sources: list[Path], top: str | None = None) -> ToolResult:
    raise NotImplementedError('TODO: sandboxed Icarus/Verilator backend')
def synthesize(sources: list[Path], top: str) -> ToolResult:
    raise NotImplementedError('TODO: sandboxed Yosys backend')
def prove_property(sources: list[Path], property_text: str) -> ToolResult:
    raise NotImplementedError('TODO: SymbiYosys backend')
