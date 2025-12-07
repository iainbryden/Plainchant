"""Third species counterpoint rules (4:1 rhythm)."""

from app.models import VoiceLine, RuleViolation, Severity, Duration
from .intervals import is_consonant, calculate_interval


def check_beat_hierarchy(counterpoint: VoiceLine, cantus: VoiceLine) -> list[RuleViolation]:
    """Check that beats 1 and 3 (strong beats) are consonant."""
    violations = []
    
    # In 4:1, strong beats are at indices 0, 2, 4, 6, 8, 10... (indices 0, 2 mod 4)
    for i in range(0, len(counterpoint.notes), 4):
        cf_index = i // 4
        if cf_index >= len(cantus.notes):
            break
        
        # Check beat 1 (index i)
        interval = calculate_interval(cantus.notes[cf_index].pitch, counterpoint.notes[i].pitch)
        if not is_consonant(interval):
            violations.append(RuleViolation(
                rule_code="STRONG_BEAT_DISSONANCE",
                description=f"Dissonant interval on beat 1 at index {i}",
                voice_indices=[cantus.voice_index, counterpoint.voice_index],
                note_indices=[i],
                severity=Severity.ERROR
            ))
        
        # Check beat 3 (index i+2) if exists
        if i + 2 < len(counterpoint.notes):
            interval = calculate_interval(cantus.notes[cf_index].pitch, counterpoint.notes[i+2].pitch)
            if not is_consonant(interval):
                violations.append(RuleViolation(
                    rule_code="STRONG_BEAT_DISSONANCE",
                    description=f"Dissonant interval on beat 3 at index {i+2}",
                    voice_indices=[cantus.voice_index, counterpoint.voice_index],
                    note_indices=[i+2],
                    severity=Severity.ERROR
                ))
    
    return violations


def check_passing_tones(counterpoint: VoiceLine) -> list[RuleViolation]:
    """Check that dissonances are approached and left by step."""
    violations = []
    
    for i in range(1, len(counterpoint.notes) - 1):
        prev_interval = abs(counterpoint.notes[i].pitch.midi - counterpoint.notes[i-1].pitch.midi)
        next_interval = abs(counterpoint.notes[i+1].pitch.midi - counterpoint.notes[i].pitch.midi)
        
        # If not stepwise on both sides, could be problematic
        if prev_interval > 2 or next_interval > 2:
            # Allow neighbor tones (step-step in opposite directions)
            prev_dir = counterpoint.notes[i].pitch.midi - counterpoint.notes[i-1].pitch.midi
            next_dir = counterpoint.notes[i+1].pitch.midi - counterpoint.notes[i].pitch.midi
            
            if prev_interval <= 2 and next_interval <= 2 and prev_dir * next_dir < 0:
                continue  # Valid neighbor tone
            
            if prev_interval > 2 and next_interval > 2:
                violations.append(RuleViolation(
                    rule_code="LEAP_TO_FROM_NOTE",
                    description=f"Note at index {i} approached and left by leap",
                    voice_indices=[counterpoint.voice_index],
                    note_indices=[i-1, i, i+1],
                    severity=Severity.WARNING
                ))
    
    return violations


def check_third_species_rhythm(counterpoint: VoiceLine) -> list[RuleViolation]:
    """Check that counterpoint has proper 4:1 rhythm (all quarter notes)."""
    violations = []
    
    for i, note in enumerate(counterpoint.notes):
        if note.duration != Duration.QUARTER:
            violations.append(RuleViolation(
                rule_code="INVALID_DURATION",
                description=f"Note at index {i} should be quarter note, got {note.duration.value}",
                voice_indices=[counterpoint.voice_index],
                note_indices=[i],
                severity=Severity.ERROR
            ))
    
    return violations


def check_third_species_length(counterpoint: VoiceLine, cantus: VoiceLine) -> list[RuleViolation]:
    """Check that counterpoint has exactly 4x the notes of cantus firmus."""
    violations = []
    
    expected_length = len(cantus.notes) * 4
    if len(counterpoint.notes) != expected_length:
        violations.append(RuleViolation(
            rule_code="INVALID_LENGTH",
            description=f"Third species should have {expected_length} notes, got {len(counterpoint.notes)}",
            voice_indices=[cantus.voice_index, counterpoint.voice_index],
            note_indices=[],
            severity=Severity.ERROR
        ))
    
    return violations


def evaluate_third_species(cantus: VoiceLine, counterpoint: VoiceLine) -> list[RuleViolation]:
    """Evaluate third species counterpoint against cantus firmus."""
    violations = []
    
    violations.extend(check_third_species_rhythm(counterpoint))
    violations.extend(check_third_species_length(counterpoint, cantus))
    violations.extend(check_beat_hierarchy(counterpoint, cantus))
    violations.extend(check_passing_tones(counterpoint))
    
    return violations
