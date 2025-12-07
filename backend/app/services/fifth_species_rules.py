"""Fifth species counterpoint rules (florid - mixed rhythms)."""

from app.models import VoiceLine, RuleViolation, Severity, Duration
from .intervals import is_consonant, calculate_interval


def check_mixed_rhythm(counterpoint: VoiceLine) -> list[RuleViolation]:
    """Check that counterpoint uses mixed rhythms appropriately."""
    violations = []
    
    # Check for variety in durations
    durations = set(n.duration for n in counterpoint.notes)
    if len(durations) < 2:
        violations.append(RuleViolation(
            rule_code="INSUFFICIENT_RHYTHMIC_VARIETY",
            description="Fifth species should use varied note durations",
            voice_indices=[counterpoint.voice_index],
            note_indices=[],
            severity=Severity.WARNING
        ))
    
    return violations


def check_downbeat_consonance(counterpoint: VoiceLine, cantus: VoiceLine) -> list[RuleViolation]:
    """Check that downbeats (measure starts) are consonant."""
    violations = []
    
    # Track position in beats (assuming 4/4 time, whole note = 4 beats)
    beat_pos = 0.0
    cf_idx = 0
    
    for i, note in enumerate(counterpoint.notes):
        # Check if on downbeat
        if beat_pos % 4.0 == 0:
            if cf_idx < len(cantus.notes):
                interval = calculate_interval(cantus.notes[cf_idx].pitch, note.pitch)
                if not is_consonant(interval):
                    violations.append(RuleViolation(
                        rule_code="DOWNBEAT_DISSONANCE",
                        description=f"Downbeat at index {i} should be consonant",
                        voice_indices=[cantus.voice_index, counterpoint.voice_index],
                        note_indices=[i],
                        severity=Severity.ERROR
                    ))
        
        # Update position
        beat_pos += note.duration.to_beats()
        if beat_pos >= 4.0:
            beat_pos = 0.0
            cf_idx += 1
    
    return violations


def check_stepwise_predominance(counterpoint: VoiceLine) -> list[RuleViolation]:
    """Check that melody is predominantly stepwise."""
    violations = []
    
    if len(counterpoint.notes) < 2:
        return violations
    
    stepwise_count = 0
    total_intervals = 0
    
    for i in range(1, len(counterpoint.notes)):
        interval = abs(counterpoint.notes[i].pitch.midi - counterpoint.notes[i-1].pitch.midi)
        total_intervals += 1
        if interval <= 2:
            stepwise_count += 1
    
    if total_intervals > 0:
        stepwise_ratio = stepwise_count / total_intervals
        if stepwise_ratio < 0.6:
            violations.append(RuleViolation(
                rule_code="INSUFFICIENT_STEPWISE_MOTION",
                description=f"Only {stepwise_ratio:.1%} stepwise motion (should be ≥60%)",
                voice_indices=[counterpoint.voice_index],
                note_indices=[],
                severity=Severity.WARNING
            ))
    
    return violations


def evaluate_fifth_species(cantus: VoiceLine, counterpoint: VoiceLine) -> list[RuleViolation]:
    """Evaluate fifth species counterpoint against cantus firmus."""
    violations = []
    
    violations.extend(check_mixed_rhythm(counterpoint))
    violations.extend(check_downbeat_consonance(counterpoint, cantus))
    violations.extend(check_stepwise_predominance(counterpoint))
    
    return violations
