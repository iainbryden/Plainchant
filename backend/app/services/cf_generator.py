"""Cantus Firmus generator using backtracking."""

import random
from typing import Optional
from app.models import Pitch, Note, Duration, VoiceLine, VoiceRange, Key
from .melodic_rules import (
    check_range, check_leap_size, check_step_preference,
    check_melodic_climax, check_no_melodic_tritones, check_start_end_degrees
)


def generate_cantus_firmus(
    key: Key,
    length: int,
    voice_range: VoiceRange,
    seed: Optional[int] = None,
    max_attempts: int = 1000
) -> Optional[VoiceLine]:
    """Generate a valid cantus firmus using backtracking."""
    if seed is not None:
        random.seed(seed)
    
    min_midi, max_midi = voice_range.get_range()
    scale_degrees = key.get_scale_degrees()
    
    for _ in range(max_attempts):
        notes = _generate_cf_backtrack(key, length, min_midi, max_midi, scale_degrees)
        if notes:
            return VoiceLine(
                notes=notes,
                voice_index=0,
                voice_range=voice_range
            )
    
    return None


def _generate_cf_backtrack(
    key: Key,
    length: int,
    min_midi: int,
    max_midi: int,
    scale_degrees: list[int]
) -> Optional[list[Note]]:
    """Backtracking algorithm for CF generation."""
    notes = []
    
    # Start on tonic
    tonic_midi = _find_tonic_in_range(key.tonic, min_midi, max_midi)
    if tonic_midi is None:
        return None
    
    notes.append(Note(pitch=Pitch.from_midi(tonic_midi), duration=Duration.WHOLE))
    
    if _backtrack(notes, length, key, min_midi, max_midi, scale_degrees):
        return notes
    
    return None


def _backtrack(
    notes: list[Note],
    length: int,
    key: Key,
    min_midi: int,
    max_midi: int,
    scale_degrees: list[int]
) -> bool:
    """Recursive backtracking."""
    if len(notes) == length:
        return _is_valid_cf(notes, key, min_midi, max_midi)
    
    candidates = _get_candidates(notes, key, min_midi, max_midi, scale_degrees, length)
    random.shuffle(candidates)
    
    for midi in candidates:
        notes.append(Note(pitch=Pitch.from_midi(midi), duration=Duration.WHOLE))
        
        if _backtrack(notes, length, key, min_midi, max_midi, scale_degrees):
            return True
        
        notes.pop()
    
    return False


def _get_candidates(
    notes: list[Note],
    key: Key,
    min_midi: int,
    max_midi: int,
    scale_degrees: list[int],
    length: int
) -> list[int]:
    """Get valid candidate pitches for next note."""
    last_midi = notes[-1].pitch.midi
    candidates = []
    
    # Last note must be tonic
    if len(notes) == length - 1:
        for octave in range(12):
            midi = key.tonic + octave * 12
            if min_midi <= midi <= max_midi:
                candidates.append(midi)
        return candidates
    
    # Prefer stepwise motion
    for interval in [1, 2, -1, -2, 3, -3, 4, -4, 5, -5, 7, -7]:
        midi = last_midi + interval
        if min_midi <= midi <= max_midi and midi % 12 in scale_degrees:
            candidates.append(midi)
    
    return candidates


def _is_valid_cf(notes: list[Note], key: Key, min_midi: int, max_midi: int) -> bool:
    """Check if CF satisfies all rules."""
    voice_line = VoiceLine(
        notes=notes,
        voice_index=0,
        voice_range=VoiceRange.SOPRANO
    )
    
    # Check all melodic rules
    if check_leap_size(voice_line, max_leap=12):
        return False
    if check_step_preference(voice_line, min_stepwise=0.6):
        return False
    if check_melodic_climax(voice_line):
        return False
    if check_no_melodic_tritones(voice_line):
        return False
    if check_start_end_degrees(voice_line, key):
        return False
    
    return True


def _find_tonic_in_range(tonic_pc: int, min_midi: int, max_midi: int) -> Optional[int]:
    """Find tonic pitch within range."""
    for octave in range(12):
        midi = tonic_pc + octave * 12
        if min_midi <= midi <= max_midi:
            return midi
    return None
