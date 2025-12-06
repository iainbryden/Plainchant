"""Unit tests for species-specific rules."""

import pytest
from app.models import Pitch, Note, Duration, VoiceLine, VoiceRange
from app.services import (
    check_first_species_consonances,
    check_first_species_start,
    check_first_species_end,
    check_first_species_penultimate,
    FirstSpeciesValidator,
    evaluate_first_species,
)


def create_voice_line(midi_values: list[int], voice_index: int = 0) -> VoiceLine:
    """Helper to create a voice line from MIDI values."""
    notes = [Note(pitch=Pitch.from_midi(m), duration=Duration.WHOLE) for m in midi_values]
    return VoiceLine(notes=notes, voice_index=voice_index, voice_range=VoiceRange.SOPRANO)


class TestFirstSpeciesRules:
    """Tests for first species counterpoint rules."""
    
    def test_consonances_all_consonant(self):
        """Test all consonant intervals pass."""
        cantus = create_voice_line([60, 62, 64, 65, 67], voice_index=1)
        counterpoint = create_voice_line([64, 65, 67, 69, 71], voice_index=0)  # Thirds and fourths
        violations = check_first_species_consonances(cantus, counterpoint)
        assert len(violations) == 0
    
    def test_consonances_with_dissonance(self):
        """Test dissonant interval is detected."""
        cantus = create_voice_line([60, 62], voice_index=1)
        counterpoint = create_voice_line([61, 63], voice_index=0)  # Minor 2nd (dissonant)
        violations = check_first_species_consonances(cantus, counterpoint)
        assert len(violations) == 2
        assert all(v.rule_code == "FIRST_SPECIES_DISSONANCE" for v in violations)
    
    def test_start_perfect_consonance(self):
        """Test starting with perfect consonance."""
        cantus = create_voice_line([60, 62], voice_index=1)
        counterpoint = create_voice_line([67, 69], voice_index=0)  # Starts with P5
        violations = check_first_species_start(cantus, counterpoint)
        assert len(violations) == 0
    
    def test_start_imperfect_consonance(self):
        """Test starting with imperfect consonance fails."""
        cantus = create_voice_line([60, 62], voice_index=1)
        counterpoint = create_voice_line([64, 65], voice_index=0)  # Starts with M3
        violations = check_first_species_start(cantus, counterpoint)
        assert len(violations) == 1
        assert violations[0].rule_code == "FIRST_SPECIES_START"
    
    def test_start_unison(self):
        """Test starting with unison (perfect consonance)."""
        cantus = create_voice_line([60, 62], voice_index=1)
        counterpoint = create_voice_line([60, 62], voice_index=0)  # Unison
        violations = check_first_species_start(cantus, counterpoint)
        assert len(violations) == 0
    
    def test_start_octave(self):
        """Test starting with octave (perfect consonance)."""
        cantus = create_voice_line([60, 62], voice_index=1)
        counterpoint = create_voice_line([72, 74], voice_index=0)  # Octave
        violations = check_first_species_start(cantus, counterpoint)
        assert len(violations) == 0
    
    def test_end_unison(self):
        """Test ending with unison."""
        cantus = create_voice_line([60, 62, 60], voice_index=1)
        counterpoint = create_voice_line([64, 65, 60], voice_index=0)  # Ends on unison
        violations = check_first_species_end(cantus, counterpoint)
        assert len(violations) == 0
    
    def test_end_octave(self):
        """Test ending with octave."""
        cantus = create_voice_line([60, 62, 60], voice_index=1)
        counterpoint = create_voice_line([64, 65, 72], voice_index=0)  # Ends on octave
        violations = check_first_species_end(cantus, counterpoint)
        assert len(violations) == 0
    
    def test_end_not_perfect(self):
        """Test ending without unison/octave fails."""
        cantus = create_voice_line([60, 62, 60], voice_index=1)
        counterpoint = create_voice_line([64, 65, 67], voice_index=0)  # Ends on P5
        violations = check_first_species_end(cantus, counterpoint)
        assert len(violations) == 1
        assert violations[0].rule_code == "FIRST_SPECIES_END"
    
    def test_penultimate_sixth_to_octave(self):
        """Test valid 6-8 cadence."""
        cantus = create_voice_line([62, 60], voice_index=1)  # D-C
        counterpoint = create_voice_line([70, 72], voice_index=0)  # Bb-C (M6 to octave)
        violations = check_first_species_penultimate(cantus, counterpoint)
        assert len(violations) == 0
    
    def test_penultimate_third_to_unison(self):
        """Test valid 3-1 cadence."""
        cantus = create_voice_line([62, 60], voice_index=1)  # D-C
        counterpoint = create_voice_line([65, 60], voice_index=0)  # F-C (P4 to P5, but checking as 4 to 0)
        violations = check_first_species_penultimate(cantus, counterpoint)
        # Actually let's use a proper minor third
        cantus2 = create_voice_line([59, 60], voice_index=1)  # B-C
        counterpoint2 = create_voice_line([62, 60], voice_index=0)  # D-C (m3 to unison)
        violations2 = check_first_species_penultimate(cantus2, counterpoint2)
        assert len(violations2) == 0
    
    def test_penultimate_invalid(self):
        """Test invalid penultimate approach."""
        cantus = create_voice_line([62, 60], voice_index=1)
        counterpoint = create_voice_line([67, 72], voice_index=0)  # P5 to octave (not 3rd or 6th)
        violations = check_first_species_penultimate(cantus, counterpoint)
        assert len(violations) == 1
        assert violations[0].rule_code == "FIRST_SPECIES_PENULTIMATE"
    
    def test_validator_valid_example(self):
        """Test complete valid first species example."""
        # Simple valid first species: C-D-E-D-C with G-A-C-B-C
        cantus = create_voice_line([60, 62, 64, 62, 60], voice_index=1)
        counterpoint = create_voice_line([67, 69, 72, 71, 72], voice_index=0)
        violations = FirstSpeciesValidator.validate(cantus, counterpoint)
        # Should have no errors, possibly warnings
        errors = [v for v in violations if v.severity.value == "error"]
        assert len(errors) == 0
    
    def test_validator_invalid_example(self):
        """Test complete invalid first species example."""
        cantus = create_voice_line([60, 62], voice_index=1)
        counterpoint = create_voice_line([64, 63], voice_index=0)  # Starts with 3rd, ends with 3rd
        violations = FirstSpeciesValidator.validate(cantus, counterpoint)
        assert len(violations) >= 2  # At least start and end violations
    
    def test_evaluate_first_species(self):
        """Test evaluate_first_species function."""
        cantus = create_voice_line([60, 62, 60], voice_index=1)
        counterpoint = create_voice_line([72, 74, 72], voice_index=0)  # Octaves throughout
        violations = evaluate_first_species(cantus, counterpoint)
        # Should be valid
        errors = [v for v in violations if v.severity.value == "error"]
        assert len(errors) == 0
