from dataclasses import dataclass
@dataclass(slots=True)
class QueueConfig:
    redis_url: str
@dataclass(slots=True)
class StateConfig:
    database_url: str
