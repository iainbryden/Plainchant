"""Tests for third species counterpoint generator."""

from app.models import Key, Mode, VoiceRange, CounterpointProblem, SpeciesType, Duration
from app.services import generate_cantus_firmus
from app.services.third_species_generator import generate_third_species
from app.services.third_species_rules import evaluate_third_species


def test_generate_third_species():
    """Test basic third species generation."""
    key = Key(tonic=0, mode=Mode.IONIAN)
    cf = generate_cantus_firmus(key, length=8, voice_range=VoiceRange.ALTO, seed=42)
    
    problem = CounterpointProblem(
        key=key,
        cantus_firmus=cf,
        num_voices=2,
        species_per_voice=[SpeciesType.THIRD]
    )
    
    solution = generate_third_species(problem, seed=42)
    
    assert solution is not None
    assert len(solution.voice_lines) == 2
    assert len(solution.voice_lines[1].notes) == len(cf.notes) * 4
    assert all(n.duration == Duration.QUARTER for n in solution.voice_lines[1].notes)


def test_third_species_different_keys():
    """Test generation in different keys."""
    for tonic in [0, 2, 5]:
        key = Key(tonic=tonic, mode=Mode.IONIAN)
        cf = generate_cantus_firmus(key, length=8, voice_range=VoiceRange.ALTO, seed=42)
        
        problem = CounterpointProblem(
            key=key,
            cantus_firmus=cf,
            num_voices=2,
            species_per_voice=[SpeciesType.THIRD]
        )
        
        solution = generate_third_species(problem, seed=42)
        assert solution is not None


def test_third_species_evaluation():
    """Test that generated third species passes validation."""
    key = Key(tonic=0, mode=Mode.IONIAN)
    cf = generate_cantus_firmus(key, length=8, voice_range=VoiceRange.ALTO, seed=42)
    
    problem = CounterpointProblem(
        key=key,
        cantus_firmus=cf,
        num_voices=2,
        species_per_voice=[SpeciesType.THIRD]
    )
    
    solution = generate_third_species(problem, seed=42)
    assert solution is not None
    
    violations = evaluate_third_species(cf, solution.voice_lines[1])
    # Allow warnings, but no errors
    errors = [v for v in violations if v.severity.value == "error"]
    assert len(errors) == 0


def test_third_species_reproducibility():
    """Test that same seed produces same result."""
    key = Key(tonic=0, mode=Mode.IONIAN)
    cf = generate_cantus_firmus(key, length=8, voice_range=VoiceRange.ALTO, seed=42)
    
    problem = CounterpointProblem(
        key=key,
        cantus_firmus=cf,
        num_voices=2,
        species_per_voice=[SpeciesType.THIRD]
    )
    
    solution1 = generate_third_species(problem, seed=100)
    solution2 = generate_third_species(problem, seed=100)
    
    assert solution1 is not None
    assert solution2 is not None
    
    notes1 = [n.pitch.midi for n in solution1.voice_lines[1].notes]
    notes2 = [n.pitch.midi for n in solution2.voice_lines[1].notes]
    
    assert notes1 == notes2
