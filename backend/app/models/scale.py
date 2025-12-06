"""Scale, mode, and key definitions."""

from enum import Enum
from pydantic import BaseModel, Field


class Mode(str, Enum):
    """Modal scales for counterpoint."""
    IONIAN = "ionian"          # Major scale
    DORIAN = "dorian"
    PHRYGIAN = "phrygian"
    LYDIAN = "lydian"
    MIXOLYDIAN = "mixolydian"
    AEOLIAN = "aeolian"        # Natural minor
    LOCRIAN = "locrian"


class Scale(BaseModel):
    """Represents a diatonic scale pattern."""
    
    # Semitone intervals from root (e.g., [0, 2, 4, 5, 7, 9, 11] for major)
    intervals: list[int] = Field(..., description="Semitone intervals from root")
    mode: Mode = Field(..., description="Mode name")
    
    @classmethod
    def from_mode(cls, mode: Mode) -> "Scale":
        """Create a scale from a mode."""
        mode_intervals = {
            Mode.IONIAN: [0, 2, 4, 5, 7, 9, 11],      # W-W-H-W-W-W-H
            Mode.DORIAN: [0, 2, 3, 5, 7, 9, 10],      # W-H-W-W-W-H-W
            Mode.PHRYGIAN: [0, 1, 3, 5, 7, 8, 10],    # H-W-W-W-H-W-W
            Mode.LYDIAN: [0, 2, 4, 6, 7, 9, 11],      # W-W-W-H-W-W-H
            Mode.MIXOLYDIAN: [0, 2, 4, 5, 7, 9, 10],  # W-W-H-W-W-H-W
            Mode.AEOLIAN: [0, 2, 3, 5, 7, 8, 10],     # W-H-W-W-H-W-W
            Mode.LOCRIAN: [0, 1, 3, 5, 6, 8, 10],     # H-W-W-H-W-W-W
        }
        return cls(intervals=mode_intervals[mode], mode=mode)


class Key(BaseModel):
    """Represents a musical key (tonic + mode)."""
    
    tonic: int = Field(..., ge=0, le=11, description="Tonic pitch class (0-11, C=0)")
    mode: Mode = Field(..., description="Mode of the key")
    
    def get_scale_degrees(self) -> list[int]:
        """Get all pitch classes in this key."""
        scale = Scale.from_mode(self.mode)
        return [(self.tonic + interval) % 12 for interval in scale.intervals]
    
    def __str__(self) -> str:
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        return f"{note_names[self.tonic]} {self.mode.value}"
