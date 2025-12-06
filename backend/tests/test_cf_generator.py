"""Unit tests for cantus firmus generator."""

import pytest
from app.models import Key, Mode, VoiceRange
from app.services import generate_cantus_firmus


class TestCFGenerator:
    """Tests for CF generation."""
    
    def test_generate_cf_basic(self):
        """Test basic CF generation."""
        key = Key(tonic=0, mode=Mode.IONIAN)
        cf = generate_cantus_firmus(key, length=8, voice_range=VoiceRange.SOPRANO, seed=42)
        
        assert cf is not None
        assert len(cf.notes) == 8
        assert cf.notes[0].pitch.pitch_class == 0  # Starts on tonic
        assert cf.notes[-1].pitch.pitch_class == 0  # Ends on tonic
    
    def test_generate_cf_different_lengths(self):
        """Test CF generation with different lengths."""
        key = Key(tonic=0, mode=Mode.IONIAN)
        
        for length in [6, 8, 10, 12]:
            cf = generate_cantus_firmus(key, length=length, voice_range=VoiceRange.SOPRANO, seed=42)
            assert cf is not None
            assert len(cf.notes) == length
    
    def test_generate_cf_different_keys(self):
        """Test CF generation in different keys."""
        for tonic in [0, 2, 4, 5, 7]:  # C, D, E, F, G
            key = Key(tonic=tonic, mode=Mode.IONIAN)
            cf = generate_cantus_firmus(key, length=8, voice_range=VoiceRange.SOPRANO, seed=42)
            
            assert cf is not None
            assert cf.notes[0].pitch.pitch_class == tonic
            assert cf.notes[-1].pitch.pitch_class == tonic
    
    def test_generate_cf_different_modes(self):
        """Test CF generation in different modes."""
        for mode in [Mode.IONIAN, Mode.DORIAN, Mode.AEOLIAN]:
            key = Key(tonic=0, mode=mode)
            cf = generate_cantus_firmus(key, length=8, voice_range=VoiceRange.SOPRANO, seed=42)
            
            assert cf is not None
            assert len(cf.notes) == 8
    
    def test_generate_cf_different_ranges(self):
        """Test CF generation in different voice ranges."""
        key = Key(tonic=0, mode=Mode.IONIAN)
        
        for voice_range in [VoiceRange.SOPRANO, VoiceRange.ALTO, VoiceRange.TENOR, VoiceRange.BASS]:
            cf = generate_cantus_firmus(key, length=8, voice_range=voice_range, seed=42)
            
            assert cf is not None
            min_midi, max_midi = voice_range.get_range()
            for note in cf.notes:
                assert min_midi <= note.pitch.midi <= max_midi
    
    def test_generate_cf_reproducible(self):
        """Test that same seed produces same CF."""
        key = Key(tonic=0, mode=Mode.IONIAN)
        
        cf1 = generate_cantus_firmus(key, length=8, voice_range=VoiceRange.SOPRANO, seed=123)
        cf2 = generate_cantus_firmus(key, length=8, voice_range=VoiceRange.SOPRANO, seed=123)
        
        assert cf1 is not None
        assert cf2 is not None
        assert len(cf1.notes) == len(cf2.notes)
        for n1, n2 in zip(cf1.notes, cf2.notes):
            assert n1.pitch.midi == n2.pitch.midi
