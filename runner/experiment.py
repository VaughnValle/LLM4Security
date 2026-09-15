from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(slots=True)
class ExperimentConfig:
    name: str
    model: str
    agents: list[str]
    tools_enabled: bool
    context_tokens: int


def load_experiment(path: str | Path) -> ExperimentConfig:
    d = yaml.safe_load(Path(path).read_text())
    return ExperimentConfig(
        d["name"],
        d["model"],
        list(d.get("agents", [])),
        bool(d.get("tools_enabled", False)),
        int(d.get("context_tokens", 65536)),
    )


def run_experiment(config: ExperimentConfig) -> None:
    raise NotImplementedError("TODO: wire Hermes, broker, MCP clients, artifacts, and metrics")
