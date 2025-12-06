"""Note representation with pitch and duration."""

from enum import Enum
from pydantic import BaseModel, Field
from .pitch import Pitch


class Duration(str, Enum):
    """Note duration values."""
    WHOLE = "whole"
    HALF = "half"
    QUARTER = "quarter"
    EIGHTH = "eighth"
    SIXTEENTH = "sixteenth"
    
    def to_beats(self) -> float:
        """Convert duration to beats (assuming whole note = 4 beats)."""
        durations = {
            Duration.WHOLE: 4.0,
            Duration.HALF: 2.0,
            Duration.QUARTER: 1.0,
            Duration.EIGHTH: 0.5,
            Duration.SIXTEENTH: 0.25,
        }
        return durations[self]


class Note(BaseModel):
    """Represents a musical note with pitch and duration."""
    
    pitch: Pitch = Field(..., description="The pitch of the note")
    duration: Duration = Field(..., description="The duration of the note")
    accent: bool = Field(default=False, description="Whether the note is accented")
    tie: bool = Field(default=False, description="Whether the note is tied to the next")
    
    def __str__(self) -> str:
        return f"{self.pitch} ({self.duration.value})"
    
    def __repr__(self) -> str:
        return f"Note({self.pitch}, {self.duration.value})"
