"""Pitch representation for musical notes."""

from pydantic import BaseModel, Field, field_validator


class Pitch(BaseModel):
    """Represents a musical pitch with MIDI number and spelling information."""
    
    midi: int = Field(..., ge=0, le=127, description="MIDI note number (0-127)")
    pitch_class: int = Field(..., ge=0, le=11, description="Pitch class (0-11, C=0)")
    octave: int = Field(..., ge=-1, le=9, description="Octave number")
    spelling: str = Field(..., description="Note spelling (e.g., 'C', 'C#', 'Db')")
    
    @field_validator('pitch_class')
    @classmethod
    def validate_pitch_class(cls, v: int, info) -> int:
        """Ensure pitch class matches MIDI number."""
        if 'midi' in info.data:
            expected = info.data['midi'] % 12
            if v != expected:
                raise ValueError(f"Pitch class {v} doesn't match MIDI {info.data['midi']}")
        return v
    
    @field_validator('octave')
    @classmethod
    def validate_octave(cls, v: int, info) -> int:
        """Ensure octave matches MIDI number."""
        if 'midi' in info.data:
            expected = (info.data['midi'] // 12) - 1
            if v != expected:
                raise ValueError(f"Octave {v} doesn't match MIDI {info.data['midi']}")
        return v
    
    @classmethod
    def from_midi(cls, midi: int, spelling: str = None) -> "Pitch":
        """Create a Pitch from a MIDI number."""
        pitch_class = midi % 12
        octave = (midi // 12) - 1
        
        if spelling is None:
            # Default to sharp spelling
            note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
            spelling = note_names[pitch_class]
        
        return cls(
            midi=midi,
            pitch_class=pitch_class,
            octave=octave,
            spelling=spelling
        )
    
    def __str__(self) -> str:
        return f"{self.spelling}{self.octave}"
    
    def __repr__(self) -> str:
        return f"Pitch({self.spelling}{self.octave}, MIDI={self.midi})"
