"""Voice line and voice range definitions."""

from enum import Enum
from pydantic import BaseModel, Field
from .note import Note


class SpeciesType(str, Enum):
    """Species counterpoint types."""
    FIRST = "first"      # Note against note
    SECOND = "second"    # Two notes against one
    THIRD = "third"      # Four notes against one
    FOURTH = "fourth"    # Syncopation/suspensions
    FIFTH = "fifth"      # Florid (mixed)


class VoiceRange(str, Enum):
    """Standard SATB voice ranges."""
    SOPRANO = "soprano"
    ALTO = "alto"
    TENOR = "tenor"
    BASS = "bass"
    
    def get_range(self) -> tuple[int, int]:
        """Get MIDI range (min, max) for this voice."""
        ranges = {
            VoiceRange.SOPRANO: (60, 79),   # C4 to G5
            VoiceRange.ALTO: (55, 74),      # G3 to D5
            VoiceRange.TENOR: (48, 67),     # C3 to G4
            VoiceRange.BASS: (40, 60),      # E2 to C4
        }
        return ranges[self]


class VoiceLine(BaseModel):
    """Represents a complete voice line in counterpoint."""
    
    notes: list[Note] = Field(..., description="Sequence of notes in the voice")
    voice_index: int = Field(..., ge=0, description="Index of this voice (0-based)")
    voice_range: VoiceRange = Field(..., description="Voice range classification")
    species: SpeciesType = Field(default=SpeciesType.FIRST, description="Species type")
    
    def get_midi_range(self) -> tuple[int, int]:
        """Get the actual MIDI range used in this voice line."""
        if not self.notes:
            return (0, 0)
        midi_values = [note.pitch.midi for note in self.notes]
        return (min(midi_values), max(midi_values))
    
    def __len__(self) -> int:
        return len(self.notes)
