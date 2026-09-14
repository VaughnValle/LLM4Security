from pydantic import BaseModel, Field
class Finding(BaseModel):
    finding_id: str
    title: str
    description: str
    confidence: float = Field(ge=0.0, le=1.0)
    evidence_ids: list[str] = Field(default_factory=list)
    affected_files: list[str] = Field(default_factory=list)
    status: str = 'candidate'
