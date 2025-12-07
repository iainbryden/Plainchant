"""Tests for fifth species counterpoint generator."""

from app.models import Key, Mode, VoiceRange, CounterpointProblem, SpeciesType
from app.services import generate_cantus_firmus
from app.services.fifth_species_generator import generate_fifth_species
from app.services.fifth_species_rules import evaluate_fifth_species


def test_generate_fifth_species():
    """Test basic fifth species generation."""
    key = Key(tonic=0, mode=Mode.IONIAN)
    cf = generate_cantus_firmus(key, length=8, voice_range=VoiceRange.ALTO, seed=42)
    
    problem = CounterpointProblem(
        key=key,
        cantus_firmus=cf,
        num_voices=2,
        species_per_voice=[SpeciesType.FIFTH]
    )
    
    solution = generate_fifth_species(problem, seed=42)
    
    assert solution is not None
    assert len(solution.voice_lines) == 2
    # Fifth species has variable length due to mixed rhythms
    assert len(solution.voice_lines[1].notes) >= len(cf.notes)


def test_fifth_species_different_keys():
    """Test generation in different keys."""
    for tonic in [0, 2, 5]:
        key = Key(tonic=tonic, mode=Mode.IONIAN)
        cf = generate_cantus_firmus(key, length=8, voice_range=VoiceRange.ALTO, seed=42)
        
        problem = CounterpointProblem(
            key=key,
            cantus_firmus=cf,
            num_voices=2,
            species_per_voice=[SpeciesType.FIFTH]
        )
        
        solution = generate_fifth_species(problem, seed=42)
        assert solution is not None


def test_fifth_species_evaluation():
    """Test that generated fifth species passes validation."""
    key = Key(tonic=0, mode=Mode.IONIAN)
    cf = generate_cantus_firmus(key, length=8, voice_range=VoiceRange.ALTO, seed=42)
    
    problem = CounterpointProblem(
        key=key,
        cantus_firmus=cf,
        num_voices=2,
        species_per_voice=[SpeciesType.FIFTH]
    )
    
    solution = generate_fifth_species(problem, seed=42)
    assert solution is not None
    
    violations = evaluate_fifth_species(cf, solution.voice_lines[1])
    errors = [v for v in violations if v.severity.value == "error"]
    assert len(errors) == 0


def test_fifth_species_reproducibility():
    """Test that same seed produces same result."""
    key = Key(tonic=0, mode=Mode.IONIAN)
    cf = generate_cantus_firmus(key, length=8, voice_range=VoiceRange.ALTO, seed=42)
    
    problem = CounterpointProblem(
        key=key,
        cantus_firmus=cf,
        num_voices=2,
        species_per_voice=[SpeciesType.FIFTH]
    )
    
    solution1 = generate_fifth_species(problem, seed=100)
    solution2 = generate_fifth_species(problem, seed=100)
    
    assert solution1 is not None
    assert solution2 is not None
    
    notes1 = [n.pitch.midi for n in solution1.voice_lines[1].notes]
    notes2 = [n.pitch.midi for n in solution2.voice_lines[1].notes]
    
    assert notes1 == notes2
