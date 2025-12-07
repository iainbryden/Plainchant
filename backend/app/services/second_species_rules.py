"""Second species counterpoint rules (2:1 rhythm)."""

from app.models import VoiceLine, RuleViolation, Severity, Duration
from .intervals import is_consonant, calculate_interval


def check_strong_beat_consonance(counterpoint: VoiceLine, cantus: VoiceLine) -> list[RuleViolation]:
    """Check that all strong beats (odd indices) are consonant."""
    violations = []
    
    # In 2:1, strong beats are at indices 0, 2, 4, 6... (even indices in the CP voice)
    for i in range(0, len(counterpoint.notes), 2):
        cf_index = i // 2
        if cf_index >= len(cantus.notes):
            break
            
        interval = calculate_interval(cantus.notes[cf_index].pitch, counterpoint.notes[i].pitch)
        if not is_consonant(interval):
            violations.append(RuleViolation(
                rule_code="STRONG_BEAT_DISSONANCE",
                description=f"Dissonant interval on strong beat at index {i}",
                voice_indices=[cantus.voice_index, counterpoint.voice_index],
                note_indices=[i],
                severity=Severity.ERROR
            ))
    
    return violations


def check_weak_beat_passing_tone(counterpoint: VoiceLine, cantus: VoiceLine) -> list[RuleViolation]:
    """Check that weak beat dissonances are approached and left by step."""
    violations = []
    
    # Weak beats are at indices 1, 3, 5, 7... (odd indices)
    for i in range(1, len(counterpoint.notes), 2):
        cf_index = i // 2
        if cf_index >= len(cantus.notes):
            break
        
        interval = calculate_interval(cantus.notes[cf_index].pitch, counterpoint.notes[i].pitch)
        
        if not is_consonant(interval):
            # Dissonance on weak beat - must be passing tone
            if i == 0 or i >= len(counterpoint.notes) - 1:
                violations.append(RuleViolation(
                    rule_code="WEAK_BEAT_DISSONANCE_EDGE",
                    description=f"Dissonance on weak beat at edge (index {i})",
                    voice_indices=[cantus.voice_index, counterpoint.voice_index],
                    note_indices=[i],
                    severity=Severity.ERROR
                ))
                continue
            
            # Check stepwise approach and departure
            prev_interval = abs(counterpoint.notes[i].pitch.midi - counterpoint.notes[i-1].pitch.midi)
            next_interval = abs(counterpoint.notes[i+1].pitch.midi - counterpoint.notes[i].pitch.midi)
            
            if prev_interval > 2 or next_interval > 2:
                violations.append(RuleViolation(
                    rule_code="WEAK_BEAT_NOT_PASSING",
                    description=f"Weak beat dissonance not approached/left by step at index {i}",
                    voice_indices=[cantus.voice_index, counterpoint.voice_index],
                    note_indices=[i-1, i, i+1],
                    severity=Severity.ERROR
                ))
    
    return violations


def check_second_species_rhythm(counterpoint: VoiceLine) -> list[RuleViolation]:
    """Check that counterpoint has proper 2:1 rhythm (all half notes)."""
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


def check_second_species_length(counterpoint: VoiceLine, cantus: VoiceLine) -> list[RuleViolation]:
    """Check that counterpoint has exactly 2x the notes of cantus firmus."""
    violations = []
    
    expected_length = len(cantus.notes) * 2
    if len(counterpoint.notes) != expected_length:
        violations.append(RuleViolation(
            rule_code="INVALID_LENGTH",
            description=f"Second species should have {expected_length} notes, got {len(counterpoint.notes)}",
            voice_indices=[cantus.voice_index, counterpoint.voice_index],
            note_indices=[],
            severity=Severity.ERROR
        ))
    
    return violations


def evaluate_second_species(cantus: VoiceLine, counterpoint: VoiceLine) -> list[RuleViolation]:
    """Evaluate second species counterpoint against cantus firmus."""
    violations = []
    
    violations.extend(check_second_species_rhythm(counterpoint))
    violations.extend(check_second_species_length(counterpoint, cantus))
    violations.extend(check_strong_beat_consonance(counterpoint, cantus))
    violations.extend(check_weak_beat_passing_tone(counterpoint, cantus))
    
    return violations
