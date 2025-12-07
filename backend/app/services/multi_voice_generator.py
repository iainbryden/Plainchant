"""Multi-voice first species counterpoint generator (3-4 voices)."""

import random
from typing import Optional
from app.models import Pitch, Note, Duration, VoiceLine, VoiceRange, CounterpointProblem, CounterpointSolution
from .intervals import is_consonant, calculate_interval, is_perfect_consonance
from .motion import motion_type, MotionType


def generate_multi_voice_first_species(
    problem: CounterpointProblem,
    num_voices: int = 3,
    seed: Optional[int] = None,
    max_attempts: int = 10000,
    use_bass: bool = False
) -> Optional[CounterpointSolution]:
    """Generate 3-4 voice first species counterpoint.
    
    Args:
        problem: Counterpoint problem with cantus firmus
        num_voices: Total voices including CF (3 or 4)
        seed: Random seed for reproducibility
        max_attempts: Maximum generation attempts
        use_bass: For 3 voices, use SAB instead of SAT (default False)
    
    Returns:
        CounterpointSolution with all voices or None if generation fails
    """
    if num_voices < 3 or num_voices > 4:
        raise ValueError("num_voices must be 3 or 4")
    
    if seed is not None:
        random.seed(seed)
    
    cf = problem.cantus_firmus
    key = problem.key
    
    # Determine voice ranges based on CF voice_range
    cf_range = cf.voice_range
    
    if num_voices == 3:
        if use_bass:
            # 3 voices with bass: SAB or ATB combinations
            if cf_range == VoiceRange.BASS:
                ranges = [VoiceRange.SOPRANO, VoiceRange.ALTO]  # SAB
            elif cf_range == VoiceRange.TENOR:
                ranges = [VoiceRange.SOPRANO, VoiceRange.BASS]  # STB
            elif cf_range == VoiceRange.ALTO:
                ranges = [VoiceRange.SOPRANO, VoiceRange.BASS]  # SAB
            else:  # SOPRANO
                ranges = [VoiceRange.ALTO, VoiceRange.BASS]  # SAB
        else:
            # 3 voices default: SAT or ATB combinations
            if cf_range == VoiceRange.BASS:
                ranges = [VoiceRange.ALTO, VoiceRange.TENOR]  # ATB
            elif cf_range == VoiceRange.TENOR:
                ranges = [VoiceRange.SOPRANO, VoiceRange.ALTO]  # SAT
            elif cf_range == VoiceRange.ALTO:
                ranges = [VoiceRange.SOPRANO, VoiceRange.TENOR]  # SAT
            else:  # SOPRANO
                ranges = [VoiceRange.ALTO, VoiceRange.TENOR]  # SAT
    else:  # 4 voices (SATB)
        if cf_range == VoiceRange.BASS:
            ranges = [VoiceRange.TENOR, VoiceRange.ALTO, VoiceRange.SOPRANO]
        elif cf_range == VoiceRange.TENOR:
            ranges = [VoiceRange.BASS, VoiceRange.ALTO, VoiceRange.SOPRANO]
        elif cf_range == VoiceRange.ALTO:
            ranges = [VoiceRange.SOPRANO, VoiceRange.TENOR, VoiceRange.BASS]
        else:  # SOPRANO
            ranges = [VoiceRange.ALTO, VoiceRange.TENOR, VoiceRange.BASS]
    
    for _ in range(max_attempts):
        voices = _generate_all_voices(cf, key, ranges)
        if voices and len(voices) == num_voices:
            return CounterpointSolution(voice_lines=voices)
    
    return None


def _generate_all_voices(
    cf: VoiceLine,
    key,
    ranges: list[VoiceRange]
) -> Optional[list[VoiceLine]]:
    """Generate all counterpoint voices sequentially with retry."""
    from .melodic_rules import check_step_preference
    
    voices = [cf]
    scale_degrees = key.get_scale_degrees()
    
    for voice_idx, voice_range in enumerate(ranges, start=1):
        # Try multiple times for the last voice (hardest to generate)
        max_retries = 3 if voice_idx == len(ranges) else 1
        
        for retry in range(max_retries):
            notes = _generate_voice(voices, key, voice_range, voice_idx, scale_degrees)
            if notes and len(notes) == len(cf.notes):
                voice_line = VoiceLine(notes=notes, voice_index=voice_idx, voice_range=voice_range)
                # Validate melodic rules (must have ≥60% stepwise motion)
                if not check_step_preference(voice_line):
                    voices.append(voice_line)
                    break
        else:
            return None
    
    return voices


def _generate_voice(
    existing_voices: list[VoiceLine],
    key,
    voice_range: VoiceRange,
    voice_idx: int,
    scale_degrees: list[int]
) -> Optional[list[Note]]:
    """Generate a single counterpoint voice."""
    min_midi, max_midi = voice_range.get_range()
    cf = existing_voices[0]
    notes = []
    
    for idx, cf_note in enumerate(cf.notes):
        if idx == 0:
            candidates = _get_multi_start_candidates(
                existing_voices, idx, min_midi, max_midi, scale_degrees
            )
        elif idx == len(cf.notes) - 1:
            candidates = _get_multi_end_candidates(
                existing_voices, notes[-1], idx, min_midi, max_midi, key.tonic
            )
        else:
            candidates = _get_multi_candidates(
                existing_voices, notes, idx, min_midi, max_midi, scale_degrees
            )
        
        if not candidates:
            return None
        
        random.shuffle(candidates)
        notes.append(Note(pitch=Pitch.from_midi(candidates[0]), duration=Duration.WHOLE))
    
    return notes


def _get_multi_start_candidates(
    existing_voices: list[VoiceLine],
    idx: int,
    min_midi: int,
    max_midi: int,
    scale_degrees: list[int]
) -> list[int]:
    """Get candidates for first note (consonant with all voices)."""
    candidates = []
    cf = existing_voices[0]
    
    for midi in range(min_midi, max_midi + 1):
        if midi % 12 not in scale_degrees:
            continue
        
        # Check consonance with all existing voices and avoid exact unisons
        valid = True
        for voice in existing_voices:
            # Avoid starting on exact same note (unison)
            if voice.notes[idx].pitch.midi == midi:
                valid = False
                break
            interval = calculate_interval(voice.notes[idx].pitch, Pitch.from_midi(midi))
            if not is_consonant(interval):
                valid = False
                break
        
        # Check no voice crossing
        for voice in existing_voices:
            if voice.voice_index < len(existing_voices):  # Lower voice
                if midi < voice.notes[idx].pitch.midi:
                    valid = False
                    break
        
        if valid:
            candidates.append(midi)
    
    return candidates


def _get_multi_end_candidates(
    existing_voices: list[VoiceLine],
    prev_note: Note,
    idx: int,
    min_midi: int,
    max_midi: int,
    tonic: int
) -> list[int]:
    """Get candidates for last note (tonic, consonant, stepwise, no repeat)."""
    preferred = []
    fallback = []
    cf = existing_voices[0]
    prev_midi = prev_note.pitch.midi
    
    for octave in range(12):
        midi = tonic + octave * 12
        if not (min_midi <= midi <= max_midi):
            continue
        
        # Avoid repeated notes
        if midi == prev_midi:
            continue
        
        # Check consonance with all voices
        valid = True
        for voice in existing_voices:
            interval = calculate_interval(voice.notes[idx].pitch, Pitch.from_midi(midi))
            if not is_consonant(interval):
                valid = False
                break
        
        if not valid:
            continue
        
        # Check parallel perfects (strict for octaves/unisons, relaxed for fifths)
        for voice in existing_voices:
            prev_vert = calculate_interval(voice.notes[idx - 1].pitch, prev_note.pitch)
            curr_vert = calculate_interval(voice.notes[idx].pitch, Pitch.from_midi(midi))
            
            if is_perfect_consonance(prev_vert) and is_perfect_consonance(curr_vert):
                motion = motion_type(
                    voice.notes[idx - 1].pitch, voice.notes[idx].pitch,
                    prev_note.pitch, Pitch.from_midi(midi)
                )
                if motion == MotionType.PARALLEL:
                    prev_type = prev_vert % 12
                    curr_type = curr_vert % 12
                    # NEVER allow parallel octaves/unisons (same perfect type)
                    if prev_type == 0 and curr_type == 0:
                        valid = False
                        break
                    # NEVER allow parallel fifths of same type
                    if prev_type == 7 and curr_type == 7:
                        valid = False
                        break
        
        if not valid:
            continue
        
        # Categorize by quality (prefer stepwise, allow small leaps)
        step_dist = abs(midi - prev_midi)
        if step_dist <= 2:
            preferred.append(midi)  # Best: stepwise
        elif step_dist <= 5:
            fallback.append(midi)  # OK: small leap (3rd/4th)
        # Reject large leaps at cadence (>5 semitones)
    
    return preferred + fallback


def _get_multi_candidates(
    existing_voices: list[VoiceLine],
    notes: list[Note],
    idx: int,
    min_midi: int,
    max_midi: int,
    scale_degrees: list[int]
) -> list[int]:
    """Get valid candidates for next note."""
    candidates = []
    preferred = []
    prev_midi = notes[-1].pitch.midi
    cf = existing_voices[0]
    is_penultimate = (idx == len(cf.notes) - 2)
    
    # Prefer stepwise, then small leaps
    for interval in [2, -2, 1, -1, 3, -3, 4, -4, 5, -5]:
        midi = prev_midi + interval
        if not (min_midi <= midi <= max_midi and midi % 12 in scale_degrees):
            continue
        
        # Check consonance with all existing voices
        valid = True
        for voice in existing_voices:
            vert_interval = calculate_interval(voice.notes[idx].pitch, Pitch.from_midi(midi))
            if not is_consonant(vert_interval):
                valid = False
                break
        
        if not valid:
            continue
        
        # Check no parallel perfects with any voice
        for voice in existing_voices:
            if len(notes) >= 1:
                prev_vert = calculate_interval(voice.notes[idx - 1].pitch, notes[-1].pitch)
                curr_vert = calculate_interval(voice.notes[idx].pitch, Pitch.from_midi(midi))
                
                if is_perfect_consonance(prev_vert) and is_perfect_consonance(curr_vert):
                    motion = motion_type(
                        voice.notes[idx - 1].pitch, voice.notes[idx].pitch,
                        notes[-1].pitch, Pitch.from_midi(midi)
                    )
                    if motion == MotionType.PARALLEL:
                        valid = False
                        break
        
        if not valid:
            continue
        
        # Penultimate: prefer 3rd or 6th with CF
        if is_penultimate:
            cf_interval = calculate_interval(cf.notes[idx].pitch, Pitch.from_midi(midi))
            penult_mod = cf_interval % 12
            if penult_mod in [3, 4, 8, 9]:
                preferred.append(midi)
            else:
                candidates.append(midi)
        else:
            candidates.append(midi)
    
    # Shuffle each group
    if preferred:
        random.shuffle(preferred)
    random.shuffle(candidates)
    return preferred + candidates if preferred else candidates
