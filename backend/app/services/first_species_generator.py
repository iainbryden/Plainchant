"""First species counterpoint generator using greedy algorithm."""

import random
from typing import Optional
from app.models import Pitch, Note, Duration, VoiceLine, VoiceRange, CounterpointProblem, CounterpointSolution
from .intervals import is_consonant, calculate_interval, is_perfect_consonance
from .motion import motion_type, MotionType


def generate_first_species(
    problem: CounterpointProblem,
    seed: Optional[int] = None,
    max_attempts: int = 1000
) -> Optional[CounterpointSolution]:
    """Generate first species counterpoint above or below CF."""
    if seed is not None:
        random.seed(seed)
    
    cf = problem.cantus_firmus
    key = problem.key
    
    # Determine counterpoint voice range
    cf_avg = sum(n.pitch.midi for n in cf.notes) / len(cf.notes)
    cp_range = VoiceRange.SOPRANO if cf_avg < 60 else VoiceRange.BASS
    
    for _ in range(max_attempts):
        notes = _generate_greedy(cf, key, cp_range)
        if notes and len(notes) == len(cf.notes):
            cp_voice = VoiceLine(notes=notes, voice_index=1, voice_range=cp_range)
            return CounterpointSolution(voice_lines=[cf, cp_voice])
    
    return None


def _generate_greedy(cf: VoiceLine, key, cp_range: VoiceRange) -> Optional[list[Note]]:
    """Greedy generation with randomization."""
    min_midi, max_midi = cp_range.get_range()
    scale_degrees = key.get_scale_degrees()
    notes = []
    
    for idx, cf_note in enumerate(cf.notes):
        if idx == 0:
            candidates = _get_start_candidates(cf_note, min_midi, max_midi, scale_degrees)
        elif idx == len(cf.notes) - 1:
            candidates = _get_end_candidates(cf_note, notes[-1], min_midi, max_midi, key.tonic)
        else:
            candidates = _get_candidates(notes[-1], cf_note, cf.notes, idx, min_midi, max_midi, scale_degrees, notes)
        
        if not candidates:
            return None
        
        random.shuffle(candidates)
        notes.append(Note(pitch=Pitch.from_midi(candidates[0]), duration=Duration.WHOLE))
    
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
    """Get candidates for last note (tonic, perfect consonance, stepwise)."""
    candidates = []
    for octave in range(12):
        midi = tonic + octave * 12
        if min_midi <= midi <= max_midi:
            interval = calculate_interval(cf_note.pitch, Pitch.from_midi(midi))
            if is_perfect_consonance(interval):
                step_dist = abs(midi - prev_note.pitch.midi)
                if step_dist <= 2:
                    candidates.append(midi)
    return candidates


def _get_candidates(
    prev_note: Note,
    cf_note: Note,
    cf_notes: list[Note],
    idx: int,
    min_midi: int,
    max_midi: int,
    scale_degrees: list[int],
    notes: list[Note]
) -> list[int]:
    """Get valid candidates for next note."""
    candidates = []
    prev_midi = prev_note.pitch.midi
    
    # Prefer stepwise, then small leaps
    for interval in [2, -2, 1, -1, 3, -3, 4, -4, 5, -5, 7, -7]:
        midi = prev_midi + interval
        if not (min_midi <= midi <= max_midi and midi % 12 in scale_degrees):
            continue
        
        # Check consonance
        vert_interval = calculate_interval(cf_note.pitch, Pitch.from_midi(midi))
        if not is_consonant(vert_interval):
            continue
        
        # Check no parallel perfects
        if len(notes) >= 1:
            prev_vert = calculate_interval(cf_notes[idx - 1].pitch, notes[-1].pitch)
            if is_perfect_consonance(prev_vert) and is_perfect_consonance(vert_interval):
                motion = motion_type(
                    cf_notes[idx - 1].pitch, cf_note.pitch,
                    notes[-1].pitch, Pitch.from_midi(midi)
                )
                if motion == MotionType.PARALLEL:
                    continue
        
        candidates.append(midi)
    
    return candidates
