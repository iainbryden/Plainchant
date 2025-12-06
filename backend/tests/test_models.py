"""Unit tests for core data models."""

import pytest
from app.models import (
    Pitch, Scale, Mode, Key, Duration, Note,
    VoiceLine, VoiceRange, SpeciesType,
    CounterpointProblem, CounterpointSolution, RuleViolation, Severity
)


class TestPitch:
    """Tests for Pitch model."""
    
    def test_from_midi(self):
        """Test creating pitch from MIDI number."""
        pitch = Pitch.from_midi(60)  # Middle C
        assert pitch.midi == 60
        assert pitch.pitch_class == 0
        assert pitch.octave == 4
        assert pitch.spelling == 'C'
    
    def test_pitch_validation(self):
        """Test pitch validation."""
        with pytest.raises(ValueError):
            Pitch(midi=60, pitch_class=5, octave=4, spelling='C')  # Wrong pitch class
    
    def test_pitch_string(self):
        """Test pitch string representation."""
        pitch = Pitch.from_midi(61, 'C#')
        assert str(pitch) == 'C#4'


class TestScale:
    """Tests for Scale and Key models."""
    
    def test_ionian_scale(self):
        """Test Ionian (major) scale."""
        scale = Scale.from_mode(Mode.IONIAN)
        assert scale.intervals == [0, 2, 4, 5, 7, 9, 11]
    
    def test_key_scale_degrees(self):
        """Test getting scale degrees from key."""
        key = Key(tonic=0, mode=Mode.IONIAN)  # C major
        degrees = key.get_scale_degrees()
        assert degrees == [0, 2, 4, 5, 7, 9, 11]
    
    def test_key_string(self):
        """Test key string representation."""
        key = Key(tonic=2, mode=Mode.DORIAN)  # D Dorian
        assert 'D' in str(key) and 'dorian' in str(key)


class TestNote:
    """Tests for Note and Duration models."""
    
    def test_note_creation(self):
        """Test creating a note."""
        pitch = Pitch.from_midi(60)
        note = Note(pitch=pitch, duration=Duration.WHOLE)
        assert note.pitch.midi == 60
        assert note.duration == Duration.WHOLE
        assert not note.accent
        assert not note.tie
    
    def test_duration_to_beats(self):
        """Test duration conversion to beats."""
        assert Duration.WHOLE.to_beats() == 4.0
        assert Duration.HALF.to_beats() == 2.0
        assert Duration.QUARTER.to_beats() == 1.0


class TestVoice:
    """Tests for VoiceLine and VoiceRange models."""
    
    def test_voice_range(self):
        """Test voice range MIDI values."""
        soprano_range = VoiceRange.SOPRANO.get_range()
        assert soprano_range == (60, 79)
        
        bass_range = VoiceRange.BASS.get_range()
        assert bass_range == (40, 60)
    
    def test_voice_line(self):
        """Test voice line creation."""
        notes = [
            Note(pitch=Pitch.from_midi(60), duration=Duration.WHOLE),
            Note(pitch=Pitch.from_midi(62), duration=Duration.WHOLE),
        ]
        voice = VoiceLine(
            notes=notes,
            voice_index=0,
            voice_range=VoiceRange.SOPRANO,
            species=SpeciesType.FIRST
        )
        assert len(voice) == 2
        assert voice.get_midi_range() == (60, 62)


class TestCounterpoint:
    """Tests for Counterpoint models."""
    
    def test_rule_violation(self):
        """Test rule violation creation."""
        violation = RuleViolation(
            rule_code="PARALLEL_FIFTH",
            description="Parallel perfect fifths detected",
            voice_indices=[0, 1],
            note_indices=[2, 3],
            severity=Severity.ERROR
        )
        assert violation.rule_code == "PARALLEL_FIFTH"
        assert violation.severity == Severity.ERROR
    
    def test_counterpoint_problem(self):
        """Test counterpoint problem creation."""
        cf_notes = [Note(pitch=Pitch.from_midi(60), duration=Duration.WHOLE)]
        cf = VoiceLine(
            notes=cf_notes,
            voice_index=0,
            voice_range=VoiceRange.BASS,
            species=SpeciesType.FIRST
        )
        key = Key(tonic=0, mode=Mode.IONIAN)
        
        problem = CounterpointProblem(
            key=key,
            cantus_firmus=cf,
            num_voices=2,
            species_per_voice=[SpeciesType.FIRST]
        )
        assert problem.num_voices == 2
        assert len(problem.species_per_voice) == 1
    
    def test_counterpoint_solution(self):
        """Test counterpoint solution."""
        cf_notes = [Note(pitch=Pitch.from_midi(60), duration=Duration.WHOLE)]
        cf = VoiceLine(
            notes=cf_notes,
            voice_index=0,
            voice_range=VoiceRange.BASS
        )
        
        solution = CounterpointSolution(
            voice_lines=[cf],
            diagnostics=[],
            success=True
        )
        assert solution.success
        assert not solution.has_errors()
        assert not solution.has_warnings()
