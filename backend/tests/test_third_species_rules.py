"""Tests for third species rules."""

from app.models import Pitch, Note, Duration, VoiceLine, VoiceRange
from app.services.third_species_rules import (
    check_beat_hierarchy,
    check_third_species_rhythm,
    check_third_species_length,
    evaluate_third_species
)


def test_beat_hierarchy_valid():
    """Test that consonant strong beats pass."""
    cf = VoiceLine(
        notes=[Note(pitch=Pitch.from_midi(60), duration=Duration.WHOLE)],
        voice_index=0,
        voice_range=VoiceRange.ALTO
    )
    # C4, D4, E4, F4 (all consonant with C4)
    cp = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(60), duration=Duration.QUARTER),  # Beat 1: P1
            Note(pitch=Pitch.from_midi(62), duration=Duration.QUARTER),  # Beat 2: M2
            Note(pitch=Pitch.from_midi(64), duration=Duration.QUARTER),  # Beat 3: M3
            Note(pitch=Pitch.from_midi(65), duration=Duration.QUARTER),  # Beat 4: P4
        ],
        voice_index=1,
        voice_range=VoiceRange.SOPRANO
    )
    
    violations = check_beat_hierarchy(cp, cf)
    assert len(violations) == 0


def test_beat_hierarchy_dissonant():
    """Test that dissonant strong beats are detected."""
    cf = VoiceLine(
        notes=[Note(pitch=Pitch.from_midi(60), duration=Duration.WHOLE)],
        voice_index=0,
        voice_range=VoiceRange.ALTO
    )
    # C4, C#4, D4, D#4 (C#4 and D#4 dissonant)
    cp = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(60), duration=Duration.QUARTER),  # Beat 1: P1
            Note(pitch=Pitch.from_midi(61), duration=Duration.QUARTER),  # Beat 2: m2 (dissonant)
            Note(pitch=Pitch.from_midi(62), duration=Duration.QUARTER),  # Beat 3: M2 (dissonant)
            Note(pitch=Pitch.from_midi(63), duration=Duration.QUARTER),  # Beat 4: m3
        ],
        voice_index=1,
        voice_range=VoiceRange.SOPRANO
    )
    
    violations = check_beat_hierarchy(cp, cf)
    assert len(violations) == 1  # Beat 3 is dissonant


def test_third_species_rhythm():
    """Test rhythm validation."""
    cp = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(60), duration=Duration.QUARTER),
            Note(pitch=Pitch.from_midi(62), duration=Duration.HALF),  # Wrong duration
            Note(pitch=Pitch.from_midi(64), duration=Duration.QUARTER),
            Note(pitch=Pitch.from_midi(65), duration=Duration.QUARTER),
        ],
        voice_index=1,
        voice_range=VoiceRange.SOPRANO
    )
    
    violations = check_third_species_rhythm(cp)
    assert len(violations) == 1


def test_third_species_length():
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
        notes=[Note(pitch=Pitch.from_midi(60), duration=Duration.QUARTER)] * 7,  # Should be 8
        voice_index=1,
        voice_range=VoiceRange.SOPRANO
    )
    
    violations = check_third_species_length(cp, cf)
    assert len(violations) == 1


def test_evaluate_third_species():
    """Test complete evaluation."""
    cf = VoiceLine(
        notes=[Note(pitch=Pitch.from_midi(60), duration=Duration.WHOLE)],
        voice_index=0,
        voice_range=VoiceRange.ALTO
    )
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
    
    violations = evaluate_third_species(cf, cp)
    assert len(violations) == 0
