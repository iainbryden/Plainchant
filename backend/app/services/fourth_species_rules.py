"""Fourth species counterpoint rules (suspensions with tied notes)."""

from app.models import VoiceLine, RuleViolation, Severity, Duration
from .intervals import is_consonant, calculate_interval


def check_syncopation_consonance(counterpoint: VoiceLine, cantus: VoiceLine) -> list[RuleViolation]:
    """Check that syncopated notes are consonant (simplified fourth species)."""
    violations = []
    
    # Check all notes are consonant (simplified - no true suspensions)
    for i in range(len(counterpoint.notes)):
        cf_idx = i // 2
        if cf_idx >= len(cantus.notes):
            break
        
        interval = calculate_interval(cantus.notes[cf_idx].pitch, counterpoint.notes[i].pitch)
        if not is_consonant(interval):
            violations.append(RuleViolation(
                rule_code="SYNCOPATION_DISSONANCE",
                description=f"Syncopated note at index {i} should be consonant",
                voice_indices=[cantus.voice_index, counterpoint.voice_index],
                note_indices=[i],
                severity=Severity.WARNING  # Warning not error for simplified version
            ))
    
    return violations


def check_fourth_species_rhythm(counterpoint: VoiceLine) -> list[RuleViolation]:
    """Check that counterpoint has proper syncopated rhythm (half notes)."""
    violations = []
    
    for i, note in enumerate(counterpoint.notes):
        if note.duration != Duration.HALF:
            violations.append(RuleViolation(
                rule_code="INVALID_DURATION",
                description=f"Note at index {i} should be half note, got {note.duration.value}",
                voice_indices=[counterpoint.voice_index],
                note_indices=[i],
                severity=Severity.ERROR
            ))
    
    return violations


def check_fourth_species_length(counterpoint: VoiceLine, cantus: VoiceLine) -> list[RuleViolation]:
    """Check that counterpoint has exactly 2x the notes of cantus firmus."""
    violations = []
    
    expected_length = len(cantus.notes) * 2
    if len(counterpoint.notes) != expected_length:
        violations.append(RuleViolation(
            rule_code="INVALID_LENGTH",
            description=f"Fourth species should have {expected_length} notes, got {len(counterpoint.notes)}",
            voice_indices=[cantus.voice_index, counterpoint.voice_index],
            note_indices=[],
            severity=Severity.ERROR
        ))
    
    return violations


def evaluate_fourth_species(cantus: VoiceLine, counterpoint: VoiceLine) -> list[RuleViolation]:
    """Evaluate fourth species counterpoint against cantus firmus."""
    violations = []
    
    violations.extend(check_fourth_species_rhythm(counterpoint))
    violations.extend(check_fourth_species_length(counterpoint, cantus))
    violations.extend(check_syncopation_consonance(counterpoint, cantus))
    
    return violations
