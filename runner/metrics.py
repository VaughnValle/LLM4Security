from dataclasses import dataclass, field


@dataclass(slots=True)
class RunMetrics:
    input_tokens: int = 0
    output_tokens: int = 0
    tool_calls: int = 0
    delegations: int = 0
    wall_clock_seconds: float = 0.0
    custom: dict[str, float] = field(default_factory=dict)
