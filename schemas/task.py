from enum import StrEnum

from pydantic import BaseModel, Field


class AgentRole(StrEnum):
    SUPERVISOR = "supervisor"
    ANALYST = "analyst"
    VERIFIER = "verifier"
    CRITIC = "critic"


class Task(BaseModel):
    task_id: str
    agent: AgentRole
    objective: str
    inputs: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    parent_task_id: str | None = None
