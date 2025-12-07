"""Second species counterpoint generator (2:1 rhythm)."""

import random
from typing import Optional
from app.models import Pitch, Note, Duration, VoiceLine, VoiceRange, CounterpointProblem, CounterpointSolution
from .intervals import is_consonant, calculate_interval, is_perfect_consonance
from .motion import motion_type, MotionType


def generate_second_species(
    problem: CounterpointProblem,
    seed: Optional[int] = None,
    max_attempts: int = 1000
) -> Optional[CounterpointSolution]:
    """Generate second species counterpoint (2:1 rhythm)."""
    if seed is not None:
        random.seed(seed)
    
    cf = problem.cantus_firmus
    key = problem.key
    
    # Determine counterpoint voice range
    cf_avg = sum(n.pitch.midi for n in cf.notes) / len(cf.notes)
    cp_range = VoiceRange.SOPRANO if cf_avg < 60 else VoiceRange.BASS
    
    for _ in range(max_attempts):
        notes = _generate_second_species_greedy(cf, key, cp_range)
        if notes and len(notes) == len(cf.notes) * 2:
            cp_voice = VoiceLine(notes=notes, voice_index=1, voice_range=cp_range)
            return CounterpointSolution(voice_lines=[cf, cp_voice])
    
    return None


def _generate_second_species_greedy(cf: VoiceLine, key, cp_range: VoiceRange) -> Optional[list[Note]]:
    """Greedy generation for second species."""
    min_midi, max_midi = cp_range.get_range()
    scale_degrees = key.get_scale_degrees()
    notes = []
    
    for cf_idx, cf_note in enumerate(cf.notes):
        # Generate two notes per CF note
        for beat in [0, 1]:  # 0 = strong beat, 1 = weak beat
            is_strong = (beat == 0)
            is_first = (cf_idx == 0 and beat == 0)
            is_last = (cf_idx == len(cf.notes) - 1 and beat == 1)
            
            if is_first:
                candidates = _get_start_candidates(cf_note, min_midi, max_midi, scale_degrees)
                random.shuffle(candidates)
            elif is_last:
                candidates = _get_end_candidates(cf_note, notes[-1], min_midi, max_midi, key.tonic)
                random.shuffle(candidates)
            else:
                candidates = _get_second_species_candidates(
                    notes[-1], cf_note, is_strong, min_midi, max_midi, scale_degrees, notes, cf, cf_idx
                )
                # Candidates already shuffled within preference groups
            
            if not candidates:
                return None
            
            notes.append(Note(pitch=Pitch.from_midi(candidates[0]), duration=Duration.HALF))
    
    return notes


def _get_start_candidates(cf_note: Note, min_midi: int, max_midi: int, scale_degrees: list[int]) -> list[int]:
    """Get candidates for first note (perfect consonance)."""
    candidates = []
    for midi in range(min_midi, max_midi + 1):
        if midi % 12 not in scale_degrees:
            continue
        interval = calculate_interval(cf_note.pitch, Pitch.from_midi(midi))
        if is_perfect_consonance(interval):
            candidates.append(midi)
    return candidates


def _get_end_candidates(cf_note: Note, prev_note: Note, min_midi: int, max_midi: int, tonic: int) -> list[int]:
    """Get candidates for last note (tonic, perfect consonance, prefer stepwise)."""
    preferred = []
    candidates = []
    for octave in range(12):
        midi = tonic + octave * 12
        if min_midi <= midi <= max_midi:
            interval = calculate_interval(cf_note.pitch, Pitch.from_midi(midi))
            if is_perfect_consonance(interval):
                step_dist = abs(midi - prev_note.pitch.midi)
                if step_dist <= 2:
                    preferred.append(midi)
                elif step_dist <= 5:  # Allow small leaps if needed
                    candidates.append(midi)
    return preferred + candidates


def _get_second_species_candidates(
    prev_note: Note,
    cf_note: Note,
    is_strong: bool,
    min_midi: int,
    max_midi: int,
    scale_degrees: list[int],
    notes: list[Note],
    cf: VoiceLine,
    cf_idx: int
) -> list[int]:
    """Get valid candidates for next note in second species."""
    candidates = []
    preferred = []
    prev_midi = prev_note.pitch.midi
    is_penultimate = (cf_idx == len(cf.notes) - 2 and is_strong)
    
    # Prefer stepwise motion
    for interval in [2, -2, 1, -1, 3, -3, 4, -4]:
        midi = prev_midi + interval
        if not (min_midi <= midi <= max_midi and midi % 12 in scale_degrees):
            continue
        
        # Check consonance with CF
        vert_interval = calculate_interval(cf_note.pitch, Pitch.from_midi(midi))
        
        if is_strong:
            # Strong beat must be consonant
            if not is_consonant(vert_interval):
                continue
        else:
            # Weak beat can be dissonant if passing tone
            if not is_consonant(vert_interval):
                # Must be approached by step (already checked by interval loop)
                # Must leave by step in same direction - check next note will continue
                # For now, allow dissonance on weak beat if stepwise
                if abs(interval) > 2:
                    continue
        
        # Check no parallel perfects on strong beats
        if is_strong and len(notes) >= 2:
            prev_strong_idx = len(notes) - 2
            prev_cf_idx = prev_strong_idx // 2
            if prev_cf_idx < len(cf.notes):
                prev_vert = calculate_interval(cf.notes[prev_cf_idx].pitch, notes[prev_strong_idx].pitch)
                if is_perfect_consonance(prev_vert) and is_perfect_consonance(vert_interval):
                    motion = motion_type(
                        cf.notes[prev_cf_idx].pitch, cf_note.pitch,
                        notes[prev_strong_idx].pitch, Pitch.from_midi(midi)
                    )
                    if motion == MotionType.PARALLEL:
                        continue
        
        # Prefer 3rd or 6th for penultimate strong beat
        if is_penultimate:
            penult_mod = vert_interval % 12
            if penult_mod in [3, 4, 8, 9]:
                preferred.append(midi)
            else:
                candidates.append(midi)
        else:
            candidates.append(midi)
    
    # Shuffle each group separately, then combine
    if preferred:
        random.shuffle(preferred)
    random.shuffle(candidates)
    return preferred + candidates if preferred else candidates
