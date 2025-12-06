"""Melodic rule checking for individual voice lines."""

from app.models import VoiceLine, VoiceRange, RuleViolation, Severity, Key


def check_range(voice_line: VoiceLine, voice_range: VoiceRange) -> list[RuleViolation]:
    """Check if all notes are within the specified voice range."""
    violations = []
    min_midi, max_midi = voice_range.get_range()
    
    for i, note in enumerate(voice_line.notes):
        if note.pitch.midi < min_midi or note.pitch.midi > max_midi:
            violations.append(RuleViolation(
                rule_code="RANGE_VIOLATION",
                description=f"Note {note.pitch} at index {i} outside {voice_range.value} range",
                voice_indices=[voice_line.voice_index],
                note_indices=[i],
                severity=Severity.ERROR
            ))
    
    return violations


def check_leap_size(voice_line: VoiceLine, max_leap: int = 12) -> list[RuleViolation]:
    """Check for excessively large leaps (default max: octave)."""
    violations = []
    
    for i in range(len(voice_line.notes) - 1):
        interval = abs(voice_line.notes[i + 1].pitch.midi - voice_line.notes[i].pitch.midi)
        if interval > max_leap:
            violations.append(RuleViolation(
                rule_code="EXCESSIVE_LEAP",
                description=f"Leap of {interval} semitones exceeds maximum of {max_leap}",
                voice_indices=[voice_line.voice_index],
                note_indices=[i, i + 1],
                severity=Severity.ERROR
            ))
    
    return violations


def check_leap_compensation(voice_line: VoiceLine, large_leap: int = 7) -> list[RuleViolation]:
    """Check that large leaps are followed by stepwise motion in opposite direction."""
    violations = []
    
    for i in range(len(voice_line.notes) - 2):
        leap = voice_line.notes[i + 1].pitch.midi - voice_line.notes[i].pitch.midi
        
        if abs(leap) >= large_leap:
            next_motion = voice_line.notes[i + 2].pitch.midi - voice_line.notes[i + 1].pitch.midi
            
            # Check if next motion is stepwise (≤2 semitones) and in opposite direction
            if abs(next_motion) > 2 or (leap * next_motion > 0):
                violations.append(RuleViolation(
                    rule_code="UNCOMPENSATED_LEAP",
                    description=f"Large leap at index {i} not followed by stepwise contrary motion",
                    voice_indices=[voice_line.voice_index],
                    note_indices=[i, i + 1, i + 2],
                    severity=Severity.WARNING
                ))
    
    return violations


def check_step_preference(voice_line: VoiceLine, min_stepwise: float = 0.6) -> list[RuleViolation]:
    """Check that at least 60-70% of motion is stepwise."""
    violations = []
    
    if len(voice_line.notes) < 2:
        return violations
    
    stepwise_count = 0
    total_intervals = len(voice_line.notes) - 1
    
    for i in range(total_intervals):
        interval = abs(voice_line.notes[i + 1].pitch.midi - voice_line.notes[i].pitch.midi)
        if interval <= 2:  # Step (1-2 semitones)
            stepwise_count += 1
    
    stepwise_ratio = stepwise_count / total_intervals
    
    if stepwise_ratio < min_stepwise:
        violations.append(RuleViolation(
            rule_code="INSUFFICIENT_STEPWISE_MOTION",
            description=f"Only {stepwise_ratio:.1%} stepwise motion (minimum {min_stepwise:.0%})",
            voice_indices=[voice_line.voice_index],
            note_indices=[],
            severity=Severity.WARNING
        ))
    
    return violations


def check_repeated_notes(voice_line: VoiceLine, max_repetitions: int = 3) -> list[RuleViolation]:
    """Check for excessive repeated notes."""
    violations = []
    
    if len(voice_line.notes) < 2:
        return violations
    
    current_pitch = voice_line.notes[0].pitch.midi
    repeat_count = 1
    start_index = 0
    
    for i in range(1, len(voice_line.notes)):
        if voice_line.notes[i].pitch.midi == current_pitch:
            repeat_count += 1
        else:
            if repeat_count > max_repetitions:
                violations.append(RuleViolation(
                    rule_code="EXCESSIVE_REPETITION",
                    description=f"{repeat_count} repeated notes starting at index {start_index}",
                    voice_indices=[voice_line.voice_index],
                    note_indices=list(range(start_index, i)),
                    severity=Severity.WARNING
                ))
            current_pitch = voice_line.notes[i].pitch.midi
            repeat_count = 1
            start_index = i
    
    # Check final sequence
    if repeat_count > max_repetitions:
        violations.append(RuleViolation(
            rule_code="EXCESSIVE_REPETITION",
            description=f"{repeat_count} repeated notes starting at index {start_index}",
            voice_indices=[voice_line.voice_index],
            note_indices=list(range(start_index, len(voice_line.notes))),
            severity=Severity.WARNING
        ))
    
    return violations


def check_melodic_climax(voice_line: VoiceLine) -> list[RuleViolation]:
    """Check for a single melodic high point."""
    violations = []
    
    if len(voice_line.notes) == 0:
        return violations
    
    max_midi = max(note.pitch.midi for note in voice_line.notes)
    high_points = [i for i, note in enumerate(voice_line.notes) if note.pitch.midi == max_midi]
    
    if len(high_points) > 1:
        # Allow if high points are adjacent
        if not all(high_points[i] + 1 == high_points[i + 1] for i in range(len(high_points) - 1)):
            violations.append(RuleViolation(
                rule_code="MULTIPLE_CLIMAXES",
                description=f"Multiple non-adjacent high points at indices {high_points}",
                voice_indices=[voice_line.voice_index],
                note_indices=high_points,
                severity=Severity.WARNING
            ))
    
    return violations


def check_no_augmented_intervals(voice_line: VoiceLine, key: Key) -> list[RuleViolation]:
    """Check for augmented intervals (e.g., augmented 2nd)."""
    violations = []
    scale_degrees = set(key.get_scale_degrees())
    
    for i in range(len(voice_line.notes) - 1):
        interval = abs(voice_line.notes[i + 1].pitch.midi - voice_line.notes[i].pitch.midi)
        pc1 = voice_line.notes[i].pitch.pitch_class
        pc2 = voice_line.notes[i + 1].pitch.pitch_class
        
        # Augmented 2nd: 3 semitones between scale degrees that should be adjacent
        if interval == 3 and pc1 in scale_degrees and pc2 in scale_degrees:
            violations.append(RuleViolation(
                rule_code="AUGMENTED_INTERVAL",
                description=f"Augmented interval at index {i}",
                voice_indices=[voice_line.voice_index],
                note_indices=[i, i + 1],
                severity=Severity.ERROR
            ))
    
    return violations


def check_no_melodic_tritones(voice_line: VoiceLine) -> list[RuleViolation]:
    """Check for melodic tritones (augmented 4th/diminished 5th)."""
    violations = []
    
    for i in range(len(voice_line.notes) - 1):
        interval = abs(voice_line.notes[i + 1].pitch.midi - voice_line.notes[i].pitch.midi)
        if interval % 12 == 6:  # Tritone
            violations.append(RuleViolation(
                rule_code="MELODIC_TRITONE",
                description=f"Melodic tritone at index {i}",
                voice_indices=[voice_line.voice_index],
                note_indices=[i, i + 1],
                severity=Severity.ERROR
            ))
    
    return violations


def check_start_end_degrees(voice_line: VoiceLine, key: Key) -> list[RuleViolation]:
    """Check that voice starts and ends on stable scale degrees (tonic)."""
    violations = []
    
    if len(voice_line.notes) == 0:
        return violations
    
    # Check start
    start_pc = voice_line.notes[0].pitch.pitch_class
    if start_pc != key.tonic:
        violations.append(RuleViolation(
            rule_code="UNSTABLE_START",
            description=f"Voice starts on {start_pc} instead of tonic {key.tonic}",
            voice_indices=[voice_line.voice_index],
            note_indices=[0],
            severity=Severity.WARNING
        ))
    
    # Check end
    end_pc = voice_line.notes[-1].pitch.pitch_class
    if end_pc != key.tonic:
        violations.append(RuleViolation(
            rule_code="UNSTABLE_END",
            description=f"Voice ends on {end_pc} instead of tonic {key.tonic}",
            voice_indices=[voice_line.voice_index],
            note_indices=[len(voice_line.notes) - 1],
            severity=Severity.ERROR
        ))
    
    return violations
