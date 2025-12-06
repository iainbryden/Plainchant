"""Unit tests for harmonic rule checking."""

import pytest
from app.models import Pitch, Note, Duration, VoiceLine, VoiceRange
from app.services import (
    check_parallel_perfects,
    check_hidden_perfects,
    check_voice_crossing,
    check_voice_overlap,
    check_spacing,
)


def create_voice_line(midi_values: list[int], voice_index: int = 0) -> VoiceLine:
    """Helper to create a voice line from MIDI values."""
    notes = [Note(pitch=Pitch.from_midi(m), duration=Duration.WHOLE) for m in midi_values]
    return VoiceLine(notes=notes, voice_index=voice_index, voice_range=VoiceRange.SOPRANO)


class TestHarmonicRules:
    """Tests for harmonic rule checking."""
    
    def test_parallel_perfects_valid(self):
        """Test no parallel perfects with valid motion."""
        v1 = create_voice_line([60, 62, 64], voice_index=0)
        v2 = create_voice_line([64, 65, 67], voice_index=1)
        violations = check_parallel_perfects(v1, v2)
        assert len(violations) == 0
    
    def test_parallel_fifths(self):
        """Test detection of parallel fifths."""
        v1 = create_voice_line([60, 62], voice_index=0)
        v2 = create_voice_line([67, 69], voice_index=1)  # P5 to P5
        violations = check_parallel_perfects(v1, v2)
        assert len(violations) == 1
        assert violations[0].rule_code == "PARALLEL_PERFECTS"
    
    def test_parallel_octaves(self):
        """Test detection of parallel octaves."""
        v1 = create_voice_line([60, 62], voice_index=0)
        v2 = create_voice_line([72, 74], voice_index=1)  # P8 to P8
        violations = check_parallel_perfects(v1, v2)
        assert len(violations) == 1
        assert violations[0].rule_code == "PARALLEL_PERFECTS"
    
    def test_hidden_perfects_valid(self):
        """Test no hidden perfects with stepwise soprano."""
        bass = create_voice_line([48, 50], voice_index=1)
        soprano = create_voice_line([60, 62], voice_index=0)  # Stepwise
        violations = check_hidden_perfects(bass, soprano)
        assert len(violations) == 0
    
    def test_hidden_perfects_invalid(self):
        """Test detection of hidden perfects with soprano leap."""
        bass = create_voice_line([48, 53], voice_index=1)  # C3 to F3 (up 5 semitones)
        soprano = create_voice_line([60, 72], voice_index=0)  # C4 to C5 (leap up 12 to octave)
        violations = check_hidden_perfects(bass, soprano)
        assert len(violations) == 1
        assert violations[0].rule_code == "HIDDEN_PERFECTS"
    
    def test_voice_crossing_valid(self):
        """Test no voice crossing with proper ordering."""
        v1 = create_voice_line([67, 69, 71], voice_index=0)  # Upper
        v2 = create_voice_line([60, 62, 64], voice_index=1)  # Lower
        violations = check_voice_crossing([v1, v2])
        assert len(violations) == 0
    
    def test_voice_crossing_invalid(self):
        """Test detection of voice crossing."""
        v1 = create_voice_line([67, 60, 71], voice_index=0)  # Upper goes low
        v2 = create_voice_line([60, 65, 64], voice_index=1)  # Lower goes high
        violations = check_voice_crossing([v1, v2])
        assert len(violations) >= 1
        assert any(v.rule_code == "VOICE_CROSSING" for v in violations)
    
    def test_voice_overlap_valid(self):
        """Test no voice overlap with proper motion."""
        v1 = create_voice_line([67, 69, 71], voice_index=0)
        v2 = create_voice_line([60, 62, 64], voice_index=1)
        violations = check_voice_overlap([v1, v2])
        assert len(violations) == 0
    
    def test_voice_overlap_invalid(self):
        """Test detection of voice overlap."""
        v1 = create_voice_line([67, 60, 62], voice_index=0)  # Upper drops
        v2 = create_voice_line([60, 65, 64], voice_index=1)  # Lower jumps above prev
        violations = check_voice_overlap([v1, v2])
        assert len(violations) >= 1
        assert any(v.rule_code == "VOICE_OVERLAP" for v in violations)
    
    def test_spacing_valid(self):
        """Test reasonable spacing between voices."""
        v1 = create_voice_line([67, 69], voice_index=0)
        v2 = create_voice_line([60, 62], voice_index=1)  # 7 semitones apart
        violations = check_spacing([v1, v2])
        assert len(violations) == 0
    
    def test_spacing_excessive(self):
        """Test detection of excessive spacing."""
        v1 = create_voice_line([79, 81], voice_index=0)  # Very high
        v2 = create_voice_line([60, 62], voice_index=1)  # Low (19 semitones)
        violations = check_spacing([v1, v2], max_interval=12)
        assert len(violations) == 2
        assert all(v.rule_code == "EXCESSIVE_SPACING" for v in violations)
