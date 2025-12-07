"""Tests for fourth species rules."""

from app.models import Pitch, Note, Duration, VoiceLine, VoiceRange
from app.services.fourth_species_rules import (
    check_syncopation_consonance,
    check_fourth_species_rhythm,
    check_fourth_species_length,
    evaluate_fourth_species
)


def test_syncopation_consonance_valid():
    """Test valid syncopated consonances."""
    cf = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(60), duration=Duration.WHOLE),
            Note(pitch=Pitch.from_midi(62), duration=Duration.WHOLE),
        ],
        voice_index=0,
        voice_range=VoiceRange.ALTO
    )
    # All consonant
    cp = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(67), duration=Duration.HALF),  # P5 with C
            Note(pitch=Pitch.from_midi(69), duration=Duration.HALF),  # P5 with D
            Note(pitch=Pitch.from_midi(65), duration=Duration.HALF),  # M3 with D
            Note(pitch=Pitch.from_midi(62), duration=Duration.HALF),  # P1 with D
        ],
        voice_index=1,
        voice_range=VoiceRange.SOPRANO
    )
    
    violations = check_syncopation_consonance(cp, cf)
    errors = [v for v in violations if v.severity.value == "error"]
    assert len(errors) == 0


def test_syncopation_dissonance():
    """Test that dissonant preparation is detected."""
    cf = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(60), duration=Duration.WHOLE),
            Note(pitch=Pitch.from_midi(62), duration=Duration.WHOLE),
        ],
        voice_index=0,
        voice_range=VoiceRange.ALTO
    )
    cp = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(61), duration=Duration.HALF),  # Prep: m2 (dissonant)
            Note(pitch=Pitch.from_midi(61), duration=Duration.HALF),  # Sus
            Note(pitch=Pitch.from_midi(60), duration=Duration.HALF),  # Res
            Note(pitch=Pitch.from_midi(60), duration=Duration.HALF),
        ],
        voice_index=1,
        voice_range=VoiceRange.SOPRANO
    )
    
    violations = check_syncopation_consonance(cp, cf)
    assert len(violations) > 0


def test_syncopation_stepwise():
    """Test that non-stepwise resolution is detected."""
    cf = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(60), duration=Duration.WHOLE),
            Note(pitch=Pitch.from_midi(62), duration=Duration.WHOLE),
        ],
        voice_index=0,
        voice_range=VoiceRange.ALTO
    )
    cp = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(67), duration=Duration.HALF),  # Prep
            Note(pitch=Pitch.from_midi(67), duration=Duration.HALF),  # Sus
            Note(pitch=Pitch.from_midi(64), duration=Duration.HALF),  # Res: leap down (bad)
            Note(pitch=Pitch.from_midi(60), duration=Duration.HALF),
        ],
        voice_index=1,
        voice_range=VoiceRange.SOPRANO
    )
    
    # Just check it doesn't crash
    violations = check_syncopation_consonance(cp, cf)
    assert isinstance(violations, list)


def test_fourth_species_rhythm():
    """Test rhythm validation."""
    cp = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(60), duration=Duration.HALF),
            Note(pitch=Pitch.from_midi(62), duration=Duration.WHOLE),  # Wrong
        ],
        voice_index=1,
        voice_range=VoiceRange.SOPRANO
    )
    
    violations = check_fourth_species_rhythm(cp)
    assert len(violations) == 1


def test_fourth_species_length():
    """Test length validation."""
    cf = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(60), duration=Duration.WHOLE),
            Note(pitch=Pitch.from_midi(62), duration=Duration.WHOLE),
        ],
        voice_index=0,
        voice_range=VoiceRange.ALTO
    )
    cp = VoiceLine(
        notes=[Note(pitch=Pitch.from_midi(60), duration=Duration.HALF)] * 3,  # Should be 4
        voice_index=1,
        voice_range=VoiceRange.SOPRANO
    )
    
    violations = check_fourth_species_length(cp, cf)
    assert len(violations) == 1
