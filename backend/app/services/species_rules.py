"""Species-specific counterpoint rules."""

from app.models import VoiceLine, RuleViolation, Severity
from .intervals import calculate_interval, is_consonant, is_perfect_consonance


def check_first_species_consonances(cantus: VoiceLine, counterpoint: VoiceLine) -> list[RuleViolation]:
    """Check that all intervals are consonant in first species."""
    violations = []
    min_len = min(len(cantus.notes), len(counterpoint.notes))
    
    # Determine if cantus is the bass (lower voice)
    is_bass = cantus.voice_index > counterpoint.voice_index
    
    for i in range(min_len):
        interval = calculate_interval(cantus.notes[i].pitch, counterpoint.notes[i].pitch)
        if not is_consonant(interval, is_bass):
            violations.append(RuleViolation(
                rule_code="FIRST_SPECIES_DISSONANCE",
                description=f"Dissonant interval at index {i}",
                voice_indices=[cantus.voice_index, counterpoint.voice_index],
                note_indices=[i],
                severity=Severity.ERROR
            ))
    
    return violations


def check_first_species_start(cantus: VoiceLine, counterpoint: VoiceLine) -> list[RuleViolation]:
    """Check that first species starts with perfect consonance (P1, P5, P8)."""
    violations = []
    
    if len(cantus.notes) == 0 or len(counterpoint.notes) == 0:
        return violations
    
    interval = calculate_interval(cantus.notes[0].pitch, counterpoint.notes[0].pitch)
    
    if not is_perfect_consonance(interval):
        violations.append(RuleViolation(
            rule_code="FIRST_SPECIES_START",
            description="First species must start with perfect consonance (P1, P5, or P8)",
            voice_indices=[cantus.voice_index, counterpoint.voice_index],
            note_indices=[0],
            severity=Severity.ERROR
        ))
    
    return violations


def check_first_species_end(cantus: VoiceLine, counterpoint: VoiceLine) -> list[RuleViolation]:
    """Check that first species ends with perfect unison or octave."""
    violations = []
    
    if len(cantus.notes) == 0 or len(counterpoint.notes) == 0:
        return violations
    
    min_len = min(len(cantus.notes), len(counterpoint.notes))
    interval = calculate_interval(cantus.notes[min_len - 1].pitch, counterpoint.notes[min_len - 1].pitch)
    
    # Must be unison or octave (0 or 12 semitones, mod 12)
    if interval % 12 != 0:
        violations.append(RuleViolation(
            rule_code="FIRST_SPECIES_END",
            description="First species must end with unison or octave",
            voice_indices=[cantus.voice_index, counterpoint.voice_index],
            note_indices=[min_len - 1],
            severity=Severity.ERROR
        ))
    
    return violations


def check_first_species_penultimate(cantus: VoiceLine, counterpoint: VoiceLine) -> list[RuleViolation]:
    """Check penultimate measure approaches final correctly (6-8 or 3-1 motion)."""
    violations = []
    
    min_len = min(len(cantus.notes), len(counterpoint.notes))
    if min_len < 2:
        return violations
    
    # Get penultimate and final intervals
    penult_interval = calculate_interval(cantus.notes[min_len - 2].pitch, counterpoint.notes[min_len - 2].pitch)
    final_interval = calculate_interval(cantus.notes[min_len - 1].pitch, counterpoint.notes[min_len - 1].pitch)
    
    # Penultimate should be M6 or m6 (8 or 9 semitones) or M3 or m3 (3 or 4 semitones)
    # Final should be octave or unison (0 mod 12)
    penult_mod = penult_interval % 12
    final_mod = final_interval % 12
    
    valid_penult = penult_mod in [3, 4, 8, 9]  # 3rd or 6th
    valid_final = final_mod == 0  # Unison or octave
    
    if not (valid_penult and valid_final):
        violations.append(RuleViolation(
            rule_code="FIRST_SPECIES_PENULTIMATE",
            description="Penultimate should be 3rd or 6th resolving to unison/octave",
            voice_indices=[cantus.voice_index, counterpoint.voice_index],
            note_indices=[min_len - 2, min_len - 1],
            severity=Severity.WARNING
        ))
    
    return violations


class FirstSpeciesValidator:
    """Validator for first species counterpoint."""
    
    @staticmethod
    def validate(cantus: VoiceLine, counterpoint: VoiceLine) -> list[RuleViolation]:
        """Run all first species checks."""
        violations = []
        
        violations.extend(check_first_species_consonances(cantus, counterpoint))
        violations.extend(check_first_species_start(cantus, counterpoint))
        violations.extend(check_first_species_end(cantus, counterpoint))
        violations.extend(check_first_species_penultimate(cantus, counterpoint))
        
        return violations


def evaluate_first_species(cantus: VoiceLine, counterpoint: VoiceLine) -> list[RuleViolation]:
    """Evaluate a first species counterpoint solution."""
    return FirstSpeciesValidator.validate(cantus, counterpoint)
