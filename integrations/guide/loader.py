from pathlib import Path
from .paths import resolve_guide_root
KNOWN_SECURITY_PATHS={'GHOST':'GHOST','ATTRITION':'ATTRITION','NOODLE':'NOODLE','LockForge':'LockForge','TrojanLoc':'TrojanLoc','SALAD':'SALAD','Trust-Hub':'benchmark/Trust-Hub'}
def discover_security_components(guide_root: str | Path | None = None) -> dict[str, Path]:
    root=resolve_guide_root(guide_root); found={}
    for name, rel in KNOWN_SECURITY_PATHS.items():
        p=root/rel
        if p.exists(): found[name]=p
    return found
