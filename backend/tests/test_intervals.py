"""Unit tests for interval and motion detection."""

import pytest
from app.models import Pitch, Key, Mode
from app.services import (
    calculate_interval,
    is_perfect_consonance,
    is_imperfect_consonance,
    is_consonant,
    is_dissonant,
    motion_type,
    MotionType,
)


class TestIntervals:
    """Tests for interval calculations."""
    
    def test_calculate_interval(self):
        """Test interval calculation."""
        c4 = Pitch.from_midi(60)
        g4 = Pitch.from_midi(67)
        assert calculate_interval(c4, g4) == 7  # Perfect fifth
        
        c4 = Pitch.from_midi(60)
        c5 = Pitch.from_midi(72)
        assert calculate_interval(c4, c5) == 12  # Octave
    
    def test_perfect_consonances(self):
        """Test perfect consonance detection."""
        assert is_perfect_consonance(0)   # Unison
        assert is_perfect_consonance(7)   # Perfect fifth
        assert is_perfect_consonance(12)  # Octave
        assert is_perfect_consonance(19)  # Perfect fifth + octave
        assert not is_perfect_consonance(5)  # Perfect fourth
    
    def test_imperfect_consonances(self):
        """Test imperfect consonance detection."""
        assert is_imperfect_consonance(3)   # Minor third
        assert is_imperfect_consonance(4)   # Major third
        assert is_imperfect_consonance(8)   # Minor sixth
        assert is_imperfect_consonance(9)   # Major sixth
        assert not is_imperfect_consonance(7)  # Perfect fifth
    
    def test_consonance(self):
        """Test general consonance detection."""
        assert is_consonant(0)   # Unison
        assert is_consonant(3)   # Minor third
        assert is_consonant(4)   # Major third
        assert is_consonant(7)   # Perfect fifth
        assert is_consonant(8)   # Minor sixth
        assert is_consonant(9)   # Major sixth
        assert is_consonant(12)  # Octave
    
    def test_fourth_above_bass(self):
        """Test that perfect fourth above bass is dissonant."""
        assert not is_consonant(5, is_bass=True)   # P4 above bass
        assert is_consonant(5, is_bass=False)      # P4 between upper voices
    
    def test_dissonance(self):
        """Test dissonance detection."""
        assert is_dissonant(1)   # Minor second
        assert is_dissonant(2)   # Major second
        assert is_dissonant(6)   # Tritone
        assert is_dissonant(10)  # Minor seventh
        assert is_dissonant(11)  # Major seventh
        assert not is_dissonant(7)  # Perfect fifth


class TestMotion:
    """Tests for motion type detection."""
    
    def test_parallel_motion(self):
        """Test parallel motion detection."""
        # Both voices move up by same interval, maintaining same interval between them
        c4 = Pitch.from_midi(60)
        d4 = Pitch.from_midi(62)
        g4 = Pitch.from_midi(67)
        a4 = Pitch.from_midi(69)
        
        # C-G to D-A (both up by 2 semitones, maintaining perfect fifth)
        assert motion_type(c4, d4, g4, a4) == MotionType.PARALLEL
    
    def test_similar_motion(self):
        """Test similar motion detection."""
        c4 = Pitch.from_midi(60)
        d4 = Pitch.from_midi(62)
        e4 = Pitch.from_midi(64)
        g4 = Pitch.from_midi(67)
        
        # C-E to D-G (both up, but different intervals)
        assert motion_type(c4, d4, e4, g4) == MotionType.SIMILAR
    
    def test_contrary_motion(self):
        """Test contrary motion detection."""
        c4 = Pitch.from_midi(60)
        d4 = Pitch.from_midi(62)
        e4 = Pitch.from_midi(64)
        d4_2 = Pitch.from_midi(62)
        
        # C-E to D-D (one up, one down)
        assert motion_type(c4, d4, e4, d4_2) == MotionType.CONTRARY
    
    def test_oblique_motion(self):
        """Test oblique motion detection."""
        c4 = Pitch.from_midi(60)
        c4_2 = Pitch.from_midi(60)
        e4 = Pitch.from_midi(64)
        f4 = Pitch.from_midi(65)
        
        # C-E to C-F (one static, one moves)
        assert motion_type(c4, c4_2, e4, f4) == MotionType.OBLIQUE
    
    def test_no_motion(self):
        """Test when both voices are static."""
        c4 = Pitch.from_midi(60)
        e4 = Pitch.from_midi(64)
        
        # Both voices stay the same
        assert motion_type(c4, c4, e4, e4) == MotionType.OBLIQUE
