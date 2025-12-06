"""Unit tests for melodic rule checking."""

import pytest
from app.models import Pitch, Note, Duration, VoiceLine, VoiceRange, Key, Mode
from app.services import (
    check_range,
    check_leap_size,
    check_leap_compensation,
    check_step_preference,
    check_repeated_notes,
    check_melodic_climax,
    check_no_augmented_intervals,
    check_no_melodic_tritones,
    check_start_end_degrees,
)


def create_voice_line(midi_values: list[int], voice_range: VoiceRange = VoiceRange.SOPRANO) -> VoiceLine:
    """Helper to create a voice line from MIDI values."""
    notes = [Note(pitch=Pitch.from_midi(m), duration=Duration.WHOLE) for m in midi_values]
    return VoiceLine(notes=notes, voice_index=0, voice_range=voice_range)


class TestMelodicRules:
    """Tests for melodic rule checking."""
    
    def test_check_range_valid(self):
        """Test range check with valid notes."""
        voice = create_voice_line([60, 62, 64], VoiceRange.SOPRANO)
        violations = check_range(voice, VoiceRange.SOPRANO)
        assert len(violations) == 0
    
    def test_check_range_invalid(self):
        """Test range check with out-of-range notes."""
        voice = create_voice_line([40, 42, 44], VoiceRange.SOPRANO)  # Too low
        violations = check_range(voice, VoiceRange.SOPRANO)
        assert len(violations) == 3
        assert all(v.rule_code == "RANGE_VIOLATION" for v in violations)
    
    def test_check_leap_size_valid(self):
        """Test leap size with acceptable leaps."""
        voice = create_voice_line([60, 65, 67])  # P4, M3
        violations = check_leap_size(voice)
        assert len(violations) == 0
    
    def test_check_leap_size_excessive(self):
        """Test leap size with excessive leap."""
        voice = create_voice_line([60, 74])  # Octave + M2
        violations = check_leap_size(voice, max_leap=12)
        assert len(violations) == 1
        assert violations[0].rule_code == "EXCESSIVE_LEAP"
    
    def test_check_leap_compensation_valid(self):
        """Test leap compensation with proper recovery."""
        voice = create_voice_line([60, 67, 65])  # P5 up, M2 down
        violations = check_leap_compensation(voice)
        assert len(violations) == 0
    
    def test_check_leap_compensation_invalid(self):
        """Test leap compensation without proper recovery."""
        voice = create_voice_line([60, 67, 72])  # P5 up, P5 up (no compensation)
        violations = check_leap_compensation(voice)
        assert len(violations) == 1
        assert violations[0].rule_code == "UNCOMPENSATED_LEAP"
    
    def test_check_step_preference_valid(self):
        """Test step preference with mostly stepwise motion."""
        voice = create_voice_line([60, 62, 64, 65, 67, 69])  # Mostly steps
        violations = check_step_preference(voice)
        assert len(violations) == 0
    
    def test_check_step_preference_invalid(self):
        """Test step preference with too many leaps."""
        voice = create_voice_line([60, 65, 69, 72])  # All leaps
        violations = check_step_preference(voice)
        assert len(violations) == 1
        assert violations[0].rule_code == "INSUFFICIENT_STEPWISE_MOTION"
    
    def test_check_repeated_notes_valid(self):
        """Test repeated notes with acceptable repetition."""
        voice = create_voice_line([60, 60, 62, 64])
        violations = check_repeated_notes(voice)
        assert len(violations) == 0
    
    def test_check_repeated_notes_excessive(self):
        """Test repeated notes with excessive repetition."""
        voice = create_voice_line([60, 60, 60, 60, 62])  # 4 repetitions
        violations = check_repeated_notes(voice, max_repetitions=3)
        assert len(violations) == 1
        assert violations[0].rule_code == "EXCESSIVE_REPETITION"
    
    def test_check_melodic_climax_single(self):
        """Test melodic climax with single high point."""
        voice = create_voice_line([60, 62, 67, 65, 64])  # Single peak at 67
        violations = check_melodic_climax(voice)
        assert len(violations) == 0
    
    def test_check_melodic_climax_multiple(self):
        """Test melodic climax with multiple high points."""
        voice = create_voice_line([60, 67, 62, 67, 60])  # Two peaks at 67
        violations = check_melodic_climax(voice)
        assert len(violations) == 1
        assert violations[0].rule_code == "MULTIPLE_CLIMAXES"
    
    def test_check_melodic_climax_adjacent(self):
        """Test melodic climax with adjacent high points (allowed)."""
        voice = create_voice_line([60, 62, 67, 67, 65])  # Adjacent peaks
        violations = check_melodic_climax(voice)
        assert len(violations) == 0
    
    def test_check_no_melodic_tritones_valid(self):
        """Test no tritones with valid intervals."""
        voice = create_voice_line([60, 62, 64, 65])
        violations = check_no_melodic_tritones(voice)
        assert len(violations) == 0
    
    def test_check_no_melodic_tritones_invalid(self):
        """Test no tritones with tritone present."""
        voice = create_voice_line([60, 66])  # Tritone (6 semitones)
        violations = check_no_melodic_tritones(voice)
        assert len(violations) == 1
        assert violations[0].rule_code == "MELODIC_TRITONE"
    
    def test_check_start_end_degrees_valid(self):
        """Test start/end on tonic."""
        key = Key(tonic=0, mode=Mode.IONIAN)  # C major
        voice = create_voice_line([60, 62, 64, 60])  # C-D-E-C
        violations = check_start_end_degrees(voice, key)
        assert len(violations) == 0
    
    def test_check_start_end_degrees_invalid_end(self):
        """Test ending not on tonic."""
        key = Key(tonic=0, mode=Mode.IONIAN)  # C major
        voice = create_voice_line([60, 62, 64, 65])  # C-D-E-F
        violations = check_start_end_degrees(voice, key)
        assert len(violations) == 1
        assert violations[0].rule_code == "UNSTABLE_END"
