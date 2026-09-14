from enum import StrEnum

from pydantic import BaseModel, Field


class EvidenceType(StrEnum):
    STATIC_ANALYSIS = "static_analysis"
    SIMULATION = "simulation"
    SYNTHESIS = "synthesis"
    FORMAL = "formal"
    WAVEFORM = "waveform"
    BENCHMARK_METADATA = "benchmark_metadata"


class Evidence(BaseModel):
    evidence_id: str
    evidence_type: EvidenceType
    summary: str
    artifact_paths: list[str] = Field(default_factory=list)
    tool_name: str | None = None
    tool_version: str | None = None
    reproducible: bool = False
