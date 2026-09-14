import os
from pathlib import Path
def resolve_guide_root(explicit: str | Path | None = None) -> Path:
    candidates=[]
    if explicit is not None: candidates.append(Path(explicit).expanduser())
    if env_path := os.getenv('GUIDE_ROOT'): candidates.append(Path(env_path).expanduser())
    candidates.append((Path.cwd().parent/'GUIDE').resolve())
    for candidate in candidates:
        r=candidate.resolve()
        if (r/'.git').exists() or (r/'.gitmodules').exists(): return r
    raise FileNotFoundError('Could not find GUIDE. Set GUIDE_ROOT or pass an explicit path.')
