"""Unit tests for first species counterpoint generator."""

import pytest
from app.models import Key, Mode, VoiceRange, CounterpointProblem, SpeciesType
from app.services import generate_cantus_firmus, generate_first_species, evaluate_first_species


class TestFirstSpeciesGenerator:
    """Tests for first species counterpoint generation."""
    
    def test_generate_basic(self):
        """Test basic first species generation."""
        key = Key(tonic=0, mode=Mode.IONIAN)
        cf = generate_cantus_firmus(key, length=8, voice_range=VoiceRange.ALTO, seed=42)
        
        problem = CounterpointProblem(
            key=key,
            cantus_firmus=cf,
            num_voices=2,
            species_per_voice=[SpeciesType.FIRST]
        )
        
        solution = generate_first_species(problem, seed=42)
        
        assert solution is not None
        assert len(solution.voice_lines) == 2
        assert len(solution.voice_lines[1].notes) == len(cf.notes)
    
    def test_generate_valid_counterpoint(self):
        """Test that generated counterpoint passes validation."""
        key = Key(tonic=0, mode=Mode.IONIAN)
        cf = generate_cantus_firmus(key, length=8, voice_range=VoiceRange.ALTO, seed=42)
        
        problem = CounterpointProblem(
            key=key,
            cantus_firmus=cf,
            num_voices=2,
            species_per_voice=[SpeciesType.FIRST]
        )
        
        solution = generate_first_species(problem, seed=42)
        
        assert solution is not None
        violations = evaluate_first_species(cf, solution.voice_lines[1])
        assert len(violations) == 0
    
    def test_generate_different_keys(self):
        """Test generation in different keys."""
        for tonic in [0, 2, 5, 7]:
            key = Key(tonic=tonic, mode=Mode.IONIAN)
            cf = generate_cantus_firmus(key, length=8, voice_range=VoiceRange.ALTO, seed=42)
            
            problem = CounterpointProblem(
                key=key,
                cantus_firmus=cf,
                num_voices=2,
                species_per_voice=[SpeciesType.FIRST]
            )
            
            solution = generate_first_species(problem, seed=42)
            assert solution is not None
    
    def test_generate_different_modes(self):
        """Test generation in different modes."""
        for mode in [Mode.IONIAN, Mode.DORIAN, Mode.AEOLIAN]:
            key = Key(tonic=0, mode=mode)
            cf = generate_cantus_firmus(key, length=8, voice_range=VoiceRange.ALTO, seed=42)
            
            problem = CounterpointProblem(
                key=key,
                cantus_firmus=cf,
                num_voices=2,
                species_per_voice=[SpeciesType.FIRST]
            )
            
            solution = generate_first_species(problem, seed=42)
            assert solution is not None
    
    def test_generate_different_lengths(self):
        """Test generation with different CF lengths."""
        key = Key(tonic=0, mode=Mode.IONIAN)
        
        for length in [6, 8, 10]:
            cf = generate_cantus_firmus(key, length=length, voice_range=VoiceRange.ALTO, seed=42)
            
            problem = CounterpointProblem(
                key=key,
                cantus_firmus=cf,
                num_voices=2,
                species_per_voice=[SpeciesType.FIRST]
            )
            
            solution = generate_first_species(problem, seed=42)
            assert solution is not None
            assert len(solution.voice_lines[1].notes) == length
