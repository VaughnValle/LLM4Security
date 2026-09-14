from enum import StrEnum

from pydantic import BaseModel, Field


class VerificationStatus(StrEnum):
    PROVED = "proved"
    DISPROVED = "disproved"
    INCONCLUSIVE = "inconclusive"
    ERROR = "error"


class VerificationResult(BaseModel):
    task_id: str
    status: VerificationStatus
    evidence_ids: list[str] = Field(default_factory=list)
    notes: str = ""
