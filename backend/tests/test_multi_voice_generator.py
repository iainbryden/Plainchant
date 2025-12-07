"""Tests for multi-voice first species generator."""

import pytest
from app.models import Key, Mode, Pitch, Note, Duration, VoiceLine, VoiceRange, CounterpointProblem, SpeciesType
from app.services.multi_voice_generator import generate_multi_voice_first_species
from app.services import generate_cantus_firmus


def test_generate_three_voice():
    """Test 3-voice generation."""
    key = Key(tonic=0, mode=Mode.IONIAN)
    cf = generate_cantus_firmus(key, length=8, voice_range=VoiceRange.ALTO, seed=42)
    
    problem = CounterpointProblem(
        key=key,
        cantus_firmus=cf,
        num_voices=3,
        species_per_voice=[SpeciesType.FIRST] * 2
    )
    
    solution = generate_multi_voice_first_species(problem, num_voices=3, seed=42)
    
    assert solution is not None
    assert len(solution.voice_lines) == 3
    assert all(len(v.notes) == len(cf.notes) for v in solution.voice_lines)


def test_generate_four_voice():
    """Test 4-voice generation."""
    key = Key(tonic=0, mode=Mode.IONIAN)
    cf = generate_cantus_firmus(key, length=8, voice_range=VoiceRange.TENOR, seed=100)
    
    problem = CounterpointProblem(
        key=key,
        cantus_firmus=cf,
        num_voices=4,
        species_per_voice=[SpeciesType.FIRST] * 3
    )
    
    solution = generate_multi_voice_first_species(problem, num_voices=4, seed=100, max_attempts=2000)
    
    assert solution is not None
    assert len(solution.voice_lines) == 4
    assert all(len(v.notes) == len(cf.notes) for v in solution.voice_lines)


def test_three_voice_different_keys():
    """Test 3-voice in different keys."""
    for tonic in [0, 2, 4, 5, 7]:
        key = Key(tonic=tonic, mode=Mode.IONIAN)
        cf = generate_cantus_firmus(key, length=8, voice_range=VoiceRange.ALTO, seed=42)
        
        problem = CounterpointProblem(
            key=key,
            cantus_firmus=cf,
            num_voices=3,
            species_per_voice=[SpeciesType.FIRST] * 2
        )
        
        solution = generate_multi_voice_first_species(problem, num_voices=3, seed=42)
        assert solution is not None


def test_invalid_num_voices():
    """Test that invalid num_voices raises error."""
    key = Key(tonic=0, mode=Mode.IONIAN)
    cf = generate_cantus_firmus(key, length=8, voice_range=VoiceRange.ALTO, seed=42)
    
    problem = CounterpointProblem(
        key=key,
        cantus_firmus=cf,
        num_voices=2,
        species_per_voice=[SpeciesType.FIRST] * 1
    )
    
    with pytest.raises(ValueError):
        generate_multi_voice_first_species(problem, num_voices=2, seed=42)
    
    with pytest.raises(ValueError):
        generate_multi_voice_first_species(problem, num_voices=5, seed=42)


def test_reproducibility():
    """Test that same seed produces same result."""
    key = Key(tonic=0, mode=Mode.IONIAN)
    cf = generate_cantus_firmus(key, length=8, voice_range=VoiceRange.ALTO, seed=42)
    
    problem = CounterpointProblem(
        key=key,
        cantus_firmus=cf,
        num_voices=3,
        species_per_voice=[SpeciesType.FIRST] * 2
    )
    
    solution1 = generate_multi_voice_first_species(problem, num_voices=3, seed=100)
    solution2 = generate_multi_voice_first_species(problem, num_voices=3, seed=100)
    
    assert solution1 is not None
    assert solution2 is not None
    
    for v1, v2 in zip(solution1.voice_lines, solution2.voice_lines):
        assert [n.pitch.midi for n in v1.notes] == [n.pitch.midi for n in v2.notes]
