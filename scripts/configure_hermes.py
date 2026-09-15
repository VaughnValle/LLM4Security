"""Configure the local Hermes research client only after endpoint validation.

Run inside the guest: uv run --env-file .env python scripts/configure_hermes.py
"""

import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import yaml

from integrations.guide.paths import resolve_guide_root
from integrations.inference.client import InferenceClient


def main():
    key = os.environ.get("OPENAI_API_KEY")
    if not key or key == "local":
        raise SystemExit("Load the guest's private .env with a configured API key")
    repo = Path(__file__).resolve().parents[1]
    guide = resolve_guide_root()
    endpoint = os.environ.get("OPENAI_BASE_URL", "http://127.0.0.1:8000/v1")
    client = InferenceClient()
    try:
        response = client.http.get("models")
        response.raise_for_status()
        model = next(m for m in response.json()["data"] if m["id"] == client.model)
        context = int(model["max_model_len"])
        if context < 64000:
            raise SystemExit(
                "Hermes needs a real >=64,000-token endpoint; refusing metadata override"
            )
    finally:
        client.close()
    config_path = Path.home() / ".hermes/config.yaml"
    config = yaml.safe_load(config_path.read_text()) or {}
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = config_path.with_name(f"config.yaml.before-llm4security-{stamp}")
    shutil.copyfile(config_path, backup)
    backup.chmod(0o600)
    config.setdefault("model", {}).update(
        default=client.model,
        provider="custom",
        base_url=endpoint,
        api_key=key,
        context_length=context,
        streaming=False,
    )
    config.setdefault("agent", {}).update(max_turns=8, reasoning_effort="none")
    config.setdefault("platform_toolsets", {})["cli"] = ["guide-eda-mcp"]
    config.setdefault("mcp_servers", {})["guide-eda-mcp"] = {
        "command": str(repo / ".venv/bin/guide-eda-mcp"),
        "timeout": 420,
        "supports_parallel_tool_calls": False,
        "env": {
            "GUIDE_ROOT": str(guide),
            "EDA_ARTIFACT_ROOT": str(repo / "results/eda"),
            "EDA_IMAGE": os.environ.get("EDA_IMAGE", "llm4security-eda:phase1"),
        },
    }
    with tempfile.NamedTemporaryFile("w", dir=config_path.parent, delete=False) as out:
        yaml.safe_dump(config, out, sort_keys=False)
        temporary = Path(out.name)
    temporary.chmod(0o600)
    temporary.replace(config_path)
    print(f"Hermes configured: {client.model}, actual context {context}, GUIDE {guide}")
    print(f"Private configuration backup: {backup}")


if __name__ == "__main__":
    main()
