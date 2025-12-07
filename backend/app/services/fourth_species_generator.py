"""Fourth species counterpoint generator (syncopated with suspensions)."""

import random
from typing import Optional
from app.models import Pitch, Note, Duration, VoiceLine, VoiceRange, CounterpointProblem, CounterpointSolution
from .intervals import is_consonant, calculate_interval, is_perfect_consonance


def generate_fourth_species(
    problem: CounterpointProblem,
    seed: Optional[int] = None,
    max_attempts: int = 5000
) -> Optional[CounterpointSolution]:
    """Generate fourth species counterpoint (syncopated with suspensions)."""
    if seed is not None:
        random.seed(seed)
    
    cf = problem.cantus_firmus
    key = problem.key
    
    cf_avg = sum(n.pitch.midi for n in cf.notes) / len(cf.notes)
    cp_range = VoiceRange.SOPRANO if cf_avg < 60 else VoiceRange.BASS
    
    for _ in range(max_attempts):
        notes = _generate_fourth_species_greedy(cf, key, cp_range)
        if notes and len(notes) == len(cf.notes) * 2:
            cp_voice = VoiceLine(notes=notes, voice_index=1, voice_range=cp_range)
            return CounterpointSolution(voice_lines=[cf, cp_voice])
    
    return None


def _generate_fourth_species_greedy(cf: VoiceLine, key, cp_range: VoiceRange) -> Optional[list[Note]]:
    """Greedy generation for fourth species (simplified - syncopated consonances)."""
    """Greedy generation for fourth species."""
    min_midi, max_midi = cp_range.get_range()
    scale_degrees = key.get_scale_degrees()
    notes = []
    
    for cf_idx, cf_note in enumerate(cf.notes):
        is_first = (cf_idx == 0)
        is_last = (cf_idx == len(cf.notes) - 1)
        
        if is_first:
            # First measure: start with consonance
            candidates = _get_start_candidates(cf_note, min_midi, max_midi, scale_degrees)
            random.shuffle(candidates)
            if not candidates:
                return None
            midi = candidates[0]
            notes.append(Note(pitch=Pitch.from_midi(midi), duration=Duration.HALF))
            
            # Second half: any consonance with next CF
            if len(cf.notes) > 1:
                next_cf = cf.notes[1]
                prep_candidates = []
                for test_midi in range(min_midi, max_midi + 1):
                    if test_midi % 12 not in scale_degrees:
                        continue
                    prep_interval = calculate_interval(next_cf.pitch, Pitch.from_midi(test_midi))
                    if is_consonant(prep_interval):
                        prep_candidates.append(test_midi)
                
                if not prep_candidates:
                    return None
                random.shuffle(prep_candidates)
                notes.append(Note(pitch=Pitch.from_midi(prep_candidates[0]), duration=Duration.HALF))
        
        elif is_last:
            # Last: resolve to tonic
            prev_midi = notes[-1].pitch.midi
            candidates = []
            for octave in range(12):
                midi = key.tonic + octave * 12
                if min_midi <= midi <= max_midi:
                    interval = calculate_interval(cf_note.pitch, Pitch.from_midi(midi))
                    if is_perfect_consonance(interval):
                        step = midi - prev_midi
                        if -2 <= step <= 2:  # Prefer stepwise
                            candidates.append(midi)
            if not candidates:
                return None
            random.shuffle(candidates)
            notes.append(Note(pitch=Pitch.from_midi(candidates[0]), duration=Duration.HALF))
        
        else:
            # Middle: resolution then preparation
            prev_midi = notes[-1].pitch.midi
            
            # Resolution: step down
            res_candidates = []
            for step in [-2, -1, 0]:  # Allow same note
                midi = prev_midi + step
                if min_midi <= midi <= max_midi and midi % 12 in scale_degrees:
                    interval = calculate_interval(cf_note.pitch, Pitch.from_midi(midi))
                    if is_consonant(interval):
                        res_candidates.append(midi)
            
            if not res_candidates:
                return None
            
            random.shuffle(res_candidates)
            res_midi = res_candidates[0]
            notes.append(Note(pitch=Pitch.from_midi(res_midi), duration=Duration.HALF))
            
            # Preparation
            if cf_idx < len(cf.notes) - 1:
                next_cf = cf.notes[cf_idx + 1]
                prep_candidates = []
                
                for test_midi in range(min_midi, max_midi + 1):
                    if test_midi % 12 not in scale_degrees:
                        continue
                    prep_interval = calculate_interval(next_cf.pitch, Pitch.from_midi(test_midi))
                    if is_consonant(prep_interval):
                        prep_candidates.append(test_midi)
                
                if not prep_candidates:
                    return None
                
                random.shuffle(prep_candidates)
                notes.append(Note(pitch=Pitch.from_midi(prep_candidates[0]), duration=Duration.HALF))
    
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
    """Get candidates for last note (tonic, perfect consonance, stepwise down)."""
    candidates = []
    for octave in range(12):
        midi = tonic + octave * 12
        if min_midi <= midi <= max_midi:
            interval = calculate_interval(cf_note.pitch, Pitch.from_midi(midi))
            if is_perfect_consonance(interval):
                step = midi - prev_note.pitch.midi
                if -2 <= step <= 0:  # Stepwise down or same
                    candidates.append(midi)
    return candidates
