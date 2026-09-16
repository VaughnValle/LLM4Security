"""Create sanitized, tracked Phase 1 evidence copies from ignored run output."""

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/evidence/phase1"

REPLACEMENTS = {
    "/home/researcher/LLM4Security": "<REPO_ROOT>",
    "/home/researcher/GUIDE": "<GUIDE_ROOT>",
}

FILES = {
    ROOT / "results/security-v1-agent-20260914/report.json": OUTPUT
    / "security-v1-agent-20260914/report.json",
    ROOT / "results/security-v1-agent-20260914/steps.md": OUTPUT
    / "security-v1-agent-20260914/steps.md",
    ROOT / "results/security-v1-tools-20260914/report.json": OUTPUT
    / "security-v1-tools-20260914/report.json",
    ROOT / "results/hermes-64k-acceptance-final.log": OUTPUT / "hermes-64k-acceptance-final.log",
}

FORBIDDEN = {
    "private IPv4 address": re.compile(r"\b(?:10|127\.0\.0\.1|192\.168)\.[0-9.]+\b"),
    "private home path": re.compile(r"/(?:home|Users)/[^/\s\"']+"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "API token": re.compile(r"\b(?:sk-[A-Za-z0-9_-]{20,}|github_pat_[A-Za-z0-9_]{20,})"),
    "authorization header": re.compile(r"(?i)Authorization[\"']?\s*[:=]\s*[\"']?Bearer"),
}


def sanitize(text: str, *, suffix: str) -> str:
    for private, public in REPLACEMENTS.items():
        text = text.replace(private, public)
    text = re.sub(r"(?m)^session_id:\s*\S+", "session_id: <REDACTED>", text)
    if suffix == ".json":
        payload = json.loads(text)
        payload["publication"] = {
            "source": "ignored local Phase 1 result",
            "sanitized": True,
            "replacements": [
                "VM repository path replaced with <REPO_ROOT>",
                "external GUIDE path replaced with <GUIDE_ROOT>",
            ],
        }
        text = json.dumps(payload, indent=2) + "\n"
    return text


def main() -> None:
    missing = [str(source.relative_to(ROOT)) for source in FILES if not source.is_file()]
    if missing:
        raise SystemExit(f"Missing source evidence: {', '.join(missing)}")

    checksums = {}
    for source, destination in FILES.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        text = sanitize(source.read_text(), suffix=source.suffix)
        matches = [name for name, pattern in FORBIDDEN.items() if pattern.search(text)]
        if matches:
            raise SystemExit(f"Refusing to publish {destination}: {', '.join(matches)}")
        destination.write_text(text)
        checksums[str(destination.relative_to(OUTPUT))] = hashlib.sha256(text.encode()).hexdigest()

    manifest = {
        "description": "Sanitized public copies of ignored Phase 1 execution evidence",
        "sanitization": [
            "VM repository and GUIDE home paths replaced with placeholders",
            "Hermes session identifier redacted",
            "credential and private-address scan required before output",
        ],
        "sha256": checksums,
    }
    (OUTPUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Published {len(FILES)} evidence files under {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
