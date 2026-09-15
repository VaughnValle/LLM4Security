import os
from pathlib import Path


def resolve_guide_root(explicit: str | Path | None = None) -> Path:
    # An invalid explicit setting must never silently select another benchmark checkout.
    configured = explicit if explicit is not None else os.getenv("GUIDE_ROOT")
    root = Path(configured).expanduser() if configured else Path.cwd().parent / "GUIDE"
    root = root.resolve()
    if root.is_dir() and ((root / ".git").exists() or (root / ".gitmodules").is_file()):
        return root
    raise FileNotFoundError(f"Could not find GUIDE at {root}. Set GUIDE_ROOT.")


def guide_file(root: Path, relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("Sources must be relative paths inside GUIDE_ROOT")
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root) or not resolved.is_file():
        raise ValueError(f"Source is missing or escapes GUIDE_ROOT: {relative}")
    if resolved.suffix.lower() not in (".v", ".sv", ".vh", ".svh"):
        raise ValueError("Only Verilog/SystemVerilog source and header files are accepted")
    return resolved
