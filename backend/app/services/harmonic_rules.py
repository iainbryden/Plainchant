"""Harmonic rule checking for voice interactions."""

from app.models import VoiceLine, RuleViolation, Severity
from .intervals import is_perfect_consonance, calculate_interval
from .motion import motion_type, MotionType


def check_parallel_perfects(voice1: VoiceLine, voice2: VoiceLine) -> list[RuleViolation]:
    """Check for parallel perfect fifths and octaves."""
    violations = []
    min_len = min(len(voice1.notes), len(voice2.notes))
    
    for i in range(min_len - 1):
        prev_interval = calculate_interval(voice1.notes[i].pitch, voice2.notes[i].pitch)
        curr_interval = calculate_interval(voice1.notes[i + 1].pitch, voice2.notes[i + 1].pitch)
        
        if is_perfect_consonance(prev_interval) and is_perfect_consonance(curr_interval):
            motion = motion_type(
                voice1.notes[i].pitch, voice1.notes[i + 1].pitch,
                voice2.notes[i].pitch, voice2.notes[i + 1].pitch
            )
            
            if motion == MotionType.PARALLEL:
                interval_name = "octave" if curr_interval % 12 == 0 else "fifth"
                violations.append(RuleViolation(
                    rule_code="PARALLEL_PERFECTS",
                    description=f"Parallel perfect {interval_name}s at index {i}",
                    voice_indices=[voice1.voice_index, voice2.voice_index],
                    note_indices=[i, i + 1],
                    severity=Severity.ERROR
                ))
    
    return violations


def check_hidden_perfects(bass: VoiceLine, soprano: VoiceLine) -> list[RuleViolation]:
    """Check for hidden (direct) fifths and octaves in outer voices."""
    violations = []
    min_len = min(len(bass.notes), len(soprano.notes))
    
    for i in range(min_len - 1):
        curr_interval = calculate_interval(bass.notes[i + 1].pitch, soprano.notes[i + 1].pitch)
        
        if is_perfect_consonance(curr_interval):
            motion = motion_type(
                bass.notes[i].pitch, bass.notes[i + 1].pitch,
                soprano.notes[i].pitch, soprano.notes[i + 1].pitch
            )
            
            if motion == MotionType.SIMILAR:
                # Check if soprano leaps
                soprano_interval = abs(soprano.notes[i + 1].pitch.midi - soprano.notes[i].pitch.midi)
                if soprano_interval > 2:  # Leap (more than a step)
                    interval_name = "octave" if curr_interval % 12 == 0 else "fifth"
                    violations.append(RuleViolation(
                        rule_code="HIDDEN_PERFECTS",
                        description=f"Hidden perfect {interval_name} at index {i + 1}",
                        voice_indices=[bass.voice_index, soprano.voice_index],
                        note_indices=[i, i + 1],
                        severity=Severity.WARNING
                    ))
    
    return violations


def check_voice_crossing(voices: list[VoiceLine]) -> list[RuleViolation]:
    """Check for voice crossing (lower voice goes above higher voice)."""
    violations = []
    
    if len(voices) < 2:
        return violations
    
    # Sort voices by index (assuming lower index = higher voice)
    sorted_voices = sorted(voices, key=lambda v: v.voice_index)
    
    for i in range(len(sorted_voices) - 1):
        upper = sorted_voices[i]
        lower = sorted_voices[i + 1]
        min_len = min(len(upper.notes), len(lower.notes))
        
        for j in range(min_len):
            if lower.notes[j].pitch.midi > upper.notes[j].pitch.midi:
                violations.append(RuleViolation(
                    rule_code="VOICE_CROSSING",
                    description=f"Voice {lower.voice_index} crosses above voice {upper.voice_index} at index {j}",
                    voice_indices=[upper.voice_index, lower.voice_index],
                    note_indices=[j],
                    severity=Severity.ERROR
                ))
    
    return violations


def check_voice_overlap(voices: list[VoiceLine]) -> list[RuleViolation]:
    """Check for voice overlap (voice moves into previous range of another voice)."""
    violations = []
    
    if len(voices) < 2:
        return violations
    
    sorted_voices = sorted(voices, key=lambda v: v.voice_index)
    
    for i in range(len(sorted_voices) - 1):
        upper = sorted_voices[i]
        lower = sorted_voices[i + 1]
        min_len = min(len(upper.notes), len(lower.notes))
        
        for j in range(1, min_len):
            # Check if lower voice's current note is higher than upper voice's previous note
            if lower.notes[j].pitch.midi > upper.notes[j - 1].pitch.midi:
                violations.append(RuleViolation(
                    rule_code="VOICE_OVERLAP",
                    description=f"Voice {lower.voice_index} overlaps voice {upper.voice_index} at index {j}",
                    voice_indices=[upper.voice_index, lower.voice_index],
                    note_indices=[j],
                    severity=Severity.WARNING
                ))
    
    return violations


def check_spacing(voices: list[VoiceLine], max_interval: int = 12) -> list[RuleViolation]:
    """Check for reasonable spacing between adjacent voices."""
    violations = []
    
    if len(voices) < 2:
        return violations
    
    sorted_voices = sorted(voices, key=lambda v: v.voice_index)
    
    for i in range(len(sorted_voices) - 1):
        upper = sorted_voices[i]
        lower = sorted_voices[i + 1]
        min_len = min(len(upper.notes), len(lower.notes))
        
        for j in range(min_len):
            interval = calculate_interval(lower.notes[j].pitch, upper.notes[j].pitch)
            if interval > max_interval:
                violations.append(RuleViolation(
                    rule_code="EXCESSIVE_SPACING",
                    description=f"Spacing of {interval} semitones between voices at index {j}",
                    voice_indices=[upper.voice_index, lower.voice_index],
                    note_indices=[j],
                    severity=Severity.WARNING
                ))
    
    return violations
