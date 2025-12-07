"""Tests for fifth species rules."""

from app.models import Pitch, Note, Duration, VoiceLine, VoiceRange
from app.services.fifth_species_rules import (
    check_mixed_rhythm,
    check_stepwise_predominance,
    evaluate_fifth_species
)


def test_mixed_rhythm_valid():
    """Test that mixed rhythms pass validation."""
    cp = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(60), duration=Duration.WHOLE),
            Note(pitch=Pitch.from_midi(62), duration=Duration.HALF),
            Note(pitch=Pitch.from_midi(64), duration=Duration.QUARTER),
        ],
        voice_index=1,
        voice_range=VoiceRange.SOPRANO
    )
    
    violations = check_mixed_rhythm(cp)
    assert len(violations) == 0


def test_mixed_rhythm_insufficient():
    """Test that single duration triggers warning."""
    cp = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(60), duration=Duration.WHOLE),
            Note(pitch=Pitch.from_midi(62), duration=Duration.WHOLE),
        ],
        voice_index=1,
        voice_range=VoiceRange.SOPRANO
    )
    
    violations = check_mixed_rhythm(cp)
    assert len(violations) == 1


def test_stepwise_predominance_valid():
    """Test that predominantly stepwise motion passes."""
    cp = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(60), duration=Duration.QUARTER),
            Note(pitch=Pitch.from_midi(62), duration=Duration.QUARTER),
            Note(pitch=Pitch.from_midi(64), duration=Duration.QUARTER),
            Note(pitch=Pitch.from_midi(65), duration=Duration.QUARTER),
        ],
        voice_index=1,
        voice_range=VoiceRange.SOPRANO
    )
    
    violations = check_stepwise_predominance(cp)
    assert len(violations) == 0


def test_stepwise_predominance_insufficient():
    """Test that too many leaps triggers warning."""
    cp = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(60), duration=Duration.QUARTER),
            Note(pitch=Pitch.from_midi(67), duration=Duration.QUARTER),  # Leap
            Note(pitch=Pitch.from_midi(72), duration=Duration.QUARTER),  # Leap
            Note(pitch=Pitch.from_midi(60), duration=Duration.QUARTER),  # Leap
        ],
        voice_index=1,
        voice_range=VoiceRange.SOPRANO
    )
    
    violations = check_stepwise_predominance(cp)
    assert len(violations) == 1
