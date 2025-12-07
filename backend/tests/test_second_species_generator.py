"""Tests for second species generator."""

import pytest
from app.models import Key, Mode, VoiceRange, CounterpointProblem, SpeciesType
from app.services import generate_cantus_firmus
from app.services.second_species_generator import generate_second_species
from app.services.second_species_rules import evaluate_second_species


def test_generate_second_species():
    """Test basic second species generation."""
    key = Key(tonic=0, mode=Mode.IONIAN)
    cf = generate_cantus_firmus(key, length=8, voice_range=VoiceRange.ALTO, seed=42)
    
    problem = CounterpointProblem(
        key=key,
        cantus_firmus=cf,
        num_voices=2,
        species_per_voice=[SpeciesType.SECOND]
    )
    
    solution = generate_second_species(problem, seed=42)
    
    assert solution is not None
    assert len(solution.voice_lines) == 2
    assert len(solution.voice_lines[1].notes) == len(cf.notes) * 2


def test_second_species_different_keys():
    """Test second species in different keys."""
    for tonic in [0, 2, 5, 7]:
        key = Key(tonic=tonic, mode=Mode.IONIAN)
        cf = generate_cantus_firmus(key, length=6, voice_range=VoiceRange.ALTO, seed=42)
        
        problem = CounterpointProblem(
            key=key,
            cantus_firmus=cf,
            num_voices=2,
            species_per_voice=[SpeciesType.SECOND]
        )
        
        solution = generate_second_species(problem, seed=42)
        assert solution is not None


def test_second_species_evaluation():
    """Test that generated second species passes basic evaluation."""
    key = Key(tonic=0, mode=Mode.IONIAN)
    cf = generate_cantus_firmus(key, length=6, voice_range=VoiceRange.ALTO, seed=42)
    
    problem = CounterpointProblem(
        key=key,
        cantus_firmus=cf,
        num_voices=2,
        species_per_voice=[SpeciesType.SECOND]
    )
    
    solution = generate_second_species(problem, seed=42)
    assert solution is not None
    
    violations = evaluate_second_species(cf, solution.voice_lines[1])
    # Should have correct rhythm and length
    rhythm_errors = [v for v in violations if v.rule_code in ["INVALID_DURATION", "INVALID_LENGTH"]]
    assert len(rhythm_errors) == 0
    
    # Should have consonant strong beats
    strong_beat_errors = [v for v in violations if v.rule_code == "STRONG_BEAT_DISSONANCE"]
    assert len(strong_beat_errors) == 0


def test_second_species_reproducibility():
    """Test that same seed produces same result."""
    key = Key(tonic=0, mode=Mode.IONIAN)
    cf = generate_cantus_firmus(key, length=6, voice_range=VoiceRange.ALTO, seed=42)
    
    problem = CounterpointProblem(
        key=key,
        cantus_firmus=cf,
        num_voices=2,
        species_per_voice=[SpeciesType.SECOND]
    )
    
    solution1 = generate_second_species(problem, seed=100)
    solution2 = generate_second_species(problem, seed=100)
    
    assert solution1 is not None
    assert solution2 is not None
    
    notes1 = [n.pitch.midi for n in solution1.voice_lines[1].notes]
    notes2 = [n.pitch.midi for n in solution2.voice_lines[1].notes]
    assert notes1 == notes2
