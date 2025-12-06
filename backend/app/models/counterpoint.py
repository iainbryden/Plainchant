"""Counterpoint problem and solution models."""

from enum import Enum
from pydantic import BaseModel, Field
from .voice import VoiceLine, SpeciesType
from .scale import Key


class Severity(str, Enum):
    """Severity levels for rule violations."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class RuleViolation(BaseModel):
    """Represents a violation of a counterpoint rule."""
    
    rule_code: str = Field(..., description="Unique code for the rule (e.g., 'PARALLEL_FIFTH')")
    description: str = Field(..., description="Human-readable description of the violation")
    voice_indices: list[int] = Field(default_factory=list, description="Indices of voices involved")
    note_indices: list[int] = Field(default_factory=list, description="Indices of notes involved")
    severity: Severity = Field(default=Severity.ERROR, description="Severity of the violation")
    
    def __str__(self) -> str:
        return f"[{self.severity.value.upper()}] {self.rule_code}: {self.description}"


class CounterpointProblem(BaseModel):
    """Defines a counterpoint generation problem."""
    
    key: Key = Field(..., description="Musical key for the composition")
    cantus_firmus: VoiceLine = Field(..., description="The cantus firmus voice line")
    num_voices: int = Field(..., ge=2, le=4, description="Total number of voices (2-4)")
    species_per_voice: list[SpeciesType] = Field(
        ..., 
        description="Species type for each voice (excluding CF)"
    )
    
    def __init__(self, **data):
        super().__init__(**data)
        # Validate species_per_voice length
        expected_len = self.num_voices - 1  # Exclude CF
        if len(self.species_per_voice) != expected_len:
            raise ValueError(
                f"species_per_voice must have {expected_len} elements "
                f"(got {len(self.species_per_voice)})"
            )


class CounterpointSolution(BaseModel):
    """Represents a complete counterpoint solution."""
    
    voice_lines: list[VoiceLine] = Field(..., description="All voice lines including CF")
    diagnostics: list[RuleViolation] = Field(
        default_factory=list,
        description="Rule violations and warnings"
    )
    success: bool = Field(default=True, description="Whether generation succeeded")
    message: str = Field(default="", description="Additional information about the solution")
    
    def has_errors(self) -> bool:
        """Check if solution has any error-level violations."""
        return any(v.severity == Severity.ERROR for v in self.diagnostics)
    
    def has_warnings(self) -> bool:
        """Check if solution has any warnings."""
        return any(v.severity == Severity.WARNING for v in self.diagnostics)
