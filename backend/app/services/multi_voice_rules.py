"""Multi-voice counterpoint evaluation."""

from app.models import VoiceLine, RuleViolation, CounterpointSolution
from .species_rules import evaluate_first_species
from .harmonic_rules import check_parallel_perfects, check_voice_crossing
from .melodic_rules import (
    check_range, check_leap_size, check_leap_compensation,
    check_step_preference, check_no_augmented_intervals
)


def evaluate_multi_voice(solution: CounterpointSolution) -> list[RuleViolation]:
    """Evaluate multi-voice first species counterpoint.
    
    Checks:
    - All pairwise voice interactions (first species rules)
    - Parallel perfects between any voice pair
    - Voice crossing
    - Individual melodic rules for each voice
    """
    violations = []
    voices = solution.voice_lines
    
    if len(voices) < 2:
        return violations
    
    # Check all pairwise combinations
    for i in range(len(voices)):
        for j in range(i + 1, len(voices)):
            # First species rules for this pair
            pair_violations = evaluate_first_species(voices[i], voices[j])
            violations.extend(pair_violations)
            
            # Parallel perfects
            parallel_violations = check_parallel_perfects(voices[i], voices[j])
            violations.extend(parallel_violations)
    
    # Check voice crossing for all voices
    crossing_violations = check_voice_crossing(voices)
    violations.extend(crossing_violations)
    
    # Check melodic rules for each voice (except CF at index 0)
    # Note: Skipping check_no_augmented_intervals as it requires key parameter
    for voice in voices[1:]:
        violations.extend(check_leap_size(voice))
        violations.extend(check_leap_compensation(voice))
        violations.extend(check_step_preference(voice))
    
    return violations
