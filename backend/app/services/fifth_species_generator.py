"""Fifth species counterpoint generator (florid - mixed rhythms)."""

import random
from typing import Optional
from app.models import Pitch, Note, Duration, VoiceLine, VoiceRange, CounterpointProblem, CounterpointSolution
from .intervals import is_consonant, calculate_interval, is_perfect_consonance


def generate_fifth_species(
    problem: CounterpointProblem,
    seed: Optional[int] = None,
    max_attempts: int = 5000
) -> Optional[CounterpointSolution]:
    """Generate fifth species counterpoint (florid with mixed rhythms)."""
    if seed is not None:
        random.seed(seed)
    
    cf = problem.cantus_firmus
    key = problem.key
    
    cf_avg = sum(n.pitch.midi for n in cf.notes) / len(cf.notes)
    cp_range = VoiceRange.SOPRANO if cf_avg < 60 else VoiceRange.BASS
    
    for _ in range(max_attempts):
        notes = _generate_fifth_species_greedy(cf, key, cp_range)
        if notes:
            cp_voice = VoiceLine(notes=notes, voice_index=1, voice_range=cp_range)
            return CounterpointSolution(voice_lines=[cf, cp_voice])
    
    return None


def _generate_fifth_species_greedy(cf: VoiceLine, key, cp_range: VoiceRange) -> Optional[list[Note]]:
    """Greedy generation for fifth species."""
    min_midi, max_midi = cp_range.get_range()
    scale_degrees = key.get_scale_degrees()
    notes = []
    
    for cf_idx, cf_note in enumerate(cf.notes):
        is_first = (cf_idx == 0)
        is_last = (cf_idx == len(cf.notes) - 1)
        
        if is_first:
            # Start with whole note, perfect consonance
            candidates = _get_start_candidates(cf_note, min_midi, max_midi, scale_degrees)
            random.shuffle(candidates)
            if not candidates:
                return None
            notes.append(Note(pitch=Pitch.from_midi(candidates[0]), duration=Duration.WHOLE))
        
        elif is_last:
            # End with whole note, tonic
            candidates = _get_end_candidates(cf_note, notes[-1], min_midi, max_midi, key.tonic)
            random.shuffle(candidates)
            if not candidates:
                return None
            notes.append(Note(pitch=Pitch.from_midi(candidates[0]), duration=Duration.WHOLE))
        
        else:
            # Middle: mix of rhythms
            pattern = random.choice(['whole', 'two_halves', 'four_quarters'])
            
            if pattern == 'whole':
                # One whole note
                candidates = _get_consonant_candidates(cf_note, notes[-1], min_midi, max_midi, scale_degrees)
                if not candidates:
                    return None
                random.shuffle(candidates)
                notes.append(Note(pitch=Pitch.from_midi(candidates[0]), duration=Duration.WHOLE))
            
            elif pattern == 'two_halves':
                # Two half notes
                for _ in range(2):
                    candidates = _get_consonant_candidates(cf_note, notes[-1], min_midi, max_midi, scale_degrees)
                    if not candidates:
                        return None
                    random.shuffle(candidates)
                    notes.append(Note(pitch=Pitch.from_midi(candidates[0]), duration=Duration.HALF))
            
            else:  # four_quarters
                # Four quarter notes
                for _ in range(4):
                    candidates = _get_stepwise_candidates(notes[-1], cf_note, min_midi, max_midi, scale_degrees)
                    if not candidates:
                        return None
                    random.shuffle(candidates)
                    notes.append(Note(pitch=Pitch.from_midi(candidates[0]), duration=Duration.QUARTER))
    
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
    """Get candidates for last note (tonic, perfect consonance)."""
    candidates = []
    for octave in range(12):
        midi = tonic + octave * 12
        if min_midi <= midi <= max_midi:
            interval = calculate_interval(cf_note.pitch, Pitch.from_midi(midi))
            if is_perfect_consonance(interval):
                candidates.append(midi)
    return candidates


def _get_consonant_candidates(cf_note: Note, prev_note: Note, min_midi: int, max_midi: int, scale_degrees: list[int]) -> list[int]:
    """Get consonant candidates with stepwise preference."""
    candidates = []
    prev_midi = prev_note.pitch.midi
    
    # Prefer stepwise
    for interval in [2, -2, 1, -1, 3, -3, 4, -4, 5, -5]:
        midi = prev_midi + interval
        if min_midi <= midi <= max_midi and midi % 12 in scale_degrees:
            vert_interval = calculate_interval(cf_note.pitch, Pitch.from_midi(midi))
            if is_consonant(vert_interval):
                candidates.append(midi)
    
    return candidates


def _get_stepwise_candidates(prev_note: Note, cf_note: Note, min_midi: int, max_midi: int, scale_degrees: list[int]) -> list[int]:
    """Get stepwise candidates (for quarter note runs)."""
    candidates = []
    prev_midi = prev_note.pitch.midi
    
    for interval in [2, -2, 1, -1]:
        midi = prev_midi + interval
        if min_midi <= midi <= max_midi and midi % 12 in scale_degrees:
            vert_interval = calculate_interval(cf_note.pitch, Pitch.from_midi(midi))
            if is_consonant(vert_interval):
                candidates.append(midi)
    
    # If no stepwise consonances, allow any consonance
    if not candidates:
        for midi in range(min_midi, max_midi + 1):
            if midi % 12 in scale_degrees:
                vert_interval = calculate_interval(cf_note.pitch, Pitch.from_midi(midi))
                if is_consonant(vert_interval):
                    candidates.append(midi)
    
    return candidates
