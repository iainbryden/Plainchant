"""Tests for second species rules."""

import pytest
from app.models import Key, Mode, Pitch, Note, Duration, VoiceLine, VoiceRange
from app.services.second_species_rules import (
    check_strong_beat_consonance,
    check_weak_beat_passing_tone,
    check_second_species_rhythm,
    check_second_species_length,
    evaluate_second_species
)


def test_strong_beat_consonance_valid():
    """Test that consonant strong beats pass."""
    key = Key(tonic=0, mode=Mode.IONIAN)
    
    # CF: C4, D4, E4, F4
    cf = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(60), duration=Duration.WHOLE),
            Note(pitch=Pitch.from_midi(62), duration=Duration.WHOLE),
            Note(pitch=Pitch.from_midi(64), duration=Duration.WHOLE),
            Note(pitch=Pitch.from_midi(65), duration=Duration.WHOLE),
        ],
        voice_index=0,
        voice_range=VoiceRange.ALTO
    )
    
    # CP: E4, F4, F4, G4, G4, A4, A4, C5 (strong beats: E4, F4, G4, A4 - all consonant)
    cp = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(64), duration=Duration.HALF),  # Strong: 3rd
            Note(pitch=Pitch.from_midi(65), duration=Duration.HALF),  # Weak
            Note(pitch=Pitch.from_midi(65), duration=Duration.HALF),  # Strong: 3rd
            Note(pitch=Pitch.from_midi(67), duration=Duration.HALF),  # Weak
            Note(pitch=Pitch.from_midi(67), duration=Duration.HALF),  # Strong: 3rd
            Note(pitch=Pitch.from_midi(69), duration=Duration.HALF),  # Weak
            Note(pitch=Pitch.from_midi(69), duration=Duration.HALF),  # Strong: 4th (consonant above bass)
            Note(pitch=Pitch.from_midi(72), duration=Duration.HALF),  # Weak
        ],
        voice_index=1,
        voice_range=VoiceRange.SOPRANO
    )
    
    violations = check_strong_beat_consonance(cp, cf)
    assert len(violations) == 0


def test_strong_beat_dissonance():
    """Test that dissonant strong beats are detected."""
    cf = VoiceLine(
        notes=[Note(pitch=Pitch.from_midi(60), duration=Duration.WHOLE)],
        voice_index=0,
        voice_range=VoiceRange.ALTO
    )
    
    # CP with dissonant strong beat (2nd)
    cp = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(62), duration=Duration.HALF),  # Strong: 2nd (dissonant)
            Note(pitch=Pitch.from_midi(64), duration=Duration.HALF),  # Weak
        ],
        voice_index=1,
        voice_range=VoiceRange.SOPRANO
    )
    
    violations = check_strong_beat_consonance(cp, cf)
    assert len(violations) == 1
    assert violations[0].rule_code == "STRONG_BEAT_DISSONANCE"


def test_weak_beat_passing_tone_valid():
    """Test valid passing tones on weak beats."""
    cf = VoiceLine(
        notes=[Note(pitch=Pitch.from_midi(60), duration=Duration.WHOLE)],
        voice_index=0,
        voice_range=VoiceRange.ALTO
    )
    
    # CP: C4, D4, E4 (D4 is passing tone, stepwise)
    cp = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(60), duration=Duration.HALF),  # Strong: unison
            Note(pitch=Pitch.from_midi(62), duration=Duration.HALF),  # Weak: 2nd (dissonant but passing)
            Note(pitch=Pitch.from_midi(64), duration=Duration.HALF),  # Next note
        ],
        voice_index=1,
        voice_range=VoiceRange.SOPRANO
    )
    
    violations = check_weak_beat_passing_tone(cp, cf)
    # Should have no violations if approached and left by step
    assert len([v for v in violations if v.rule_code == "WEAK_BEAT_NOT_PASSING"]) == 0


def test_weak_beat_leap_to_dissonance():
    """Test that leaping to weak beat dissonance is detected."""
    cf = VoiceLine(
        notes=[Note(pitch=Pitch.from_midi(60), duration=Duration.WHOLE)],
        voice_index=0,
        voice_range=VoiceRange.ALTO
    )
    
    # CP: C4, D4 (leap of 3rd to dissonance)
    cp = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(60), duration=Duration.HALF),  # Strong
            Note(pitch=Pitch.from_midi(62), duration=Duration.HALF),  # Weak: dissonant, but only 2 notes
            Note(pitch=Pitch.from_midi(67), duration=Duration.HALF),  # Leap away
        ],
        voice_index=1,
        voice_range=VoiceRange.SOPRANO
    )
    
    violations = check_weak_beat_passing_tone(cp, cf)
    assert len(violations) >= 1


def test_second_species_rhythm():
    """Test that all notes must be half notes."""
    cp = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(60), duration=Duration.HALF),
            Note(pitch=Pitch.from_midi(62), duration=Duration.WHOLE),  # Wrong duration
        ],
        voice_index=1,
        voice_range=VoiceRange.SOPRANO
    )
    
    violations = check_second_species_rhythm(cp)
    assert len(violations) == 1
    assert violations[0].rule_code == "INVALID_DURATION"


def test_second_species_length():
    """Test that CP must have 2x CF length."""
    cf = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(60), duration=Duration.WHOLE),
            Note(pitch=Pitch.from_midi(62), duration=Duration.WHOLE),
        ],
        voice_index=0,
        voice_range=VoiceRange.ALTO
    )
    
    # CP with wrong length (3 notes instead of 4)
    cp = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(64), duration=Duration.HALF),
            Note(pitch=Pitch.from_midi(65), duration=Duration.HALF),
            Note(pitch=Pitch.from_midi(67), duration=Duration.HALF),
        ],
        voice_index=1,
        voice_range=VoiceRange.SOPRANO
    )
    
    violations = check_second_species_length(cp, cf)
    assert len(violations) == 1
    assert violations[0].rule_code == "INVALID_LENGTH"


def test_evaluate_second_species():
    """Test complete second species evaluation."""
    cf = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(60), duration=Duration.WHOLE),
            Note(pitch=Pitch.from_midi(62), duration=Duration.WHOLE),
        ],
        voice_index=0,
        voice_range=VoiceRange.ALTO
    )
    
    # Valid second species
    cp = VoiceLine(
        notes=[
            Note(pitch=Pitch.from_midi(64), duration=Duration.HALF),  # Strong: 3rd
            Note(pitch=Pitch.from_midi(65), duration=Duration.HALF),  # Weak: 3rd
            Note(pitch=Pitch.from_midi(65), duration=Duration.HALF),  # Strong: 3rd
            Note(pitch=Pitch.from_midi(67), duration=Duration.HALF),  # Weak: 5th
        ],
        voice_index=1,
        voice_range=VoiceRange.SOPRANO
    )
    
    violations = evaluate_second_species(cf, cp)
    # Should have minimal violations for valid example
    assert len([v for v in violations if v.severity.value == "error"]) == 0
