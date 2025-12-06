"""Interval calculation and consonance/dissonance classification."""

from app.models import Pitch, Key


def calculate_interval(pitch1: Pitch, pitch2: Pitch) -> int:
    """
    Calculate the interval between two pitches in semitones.
    
    Args:
        pitch1: First pitch
        pitch2: Second pitch
    
    Returns:
        Absolute interval in semitones
    """
    return abs(pitch2.midi - pitch1.midi)


def interval_to_scale_degree(interval: int, key: Key) -> int:
    """
    Map an interval in semitones to a scale degree (1-8).
    
    Args:
        interval: Interval in semitones
        key: Musical key context
    
    Returns:
        Scale degree (1-8, where 8 is octave)
    """
    # Reduce to within one octave
    interval_mod = interval % 12
    
    # Map semitones to generic intervals
    # This is approximate - exact mapping depends on key
    semitone_to_degree = {
        0: 1,   # Unison
        1: 2,   # Minor 2nd
        2: 2,   # Major 2nd
        3: 3,   # Minor 3rd
        4: 3,   # Major 3rd
        5: 4,   # Perfect 4th
        6: 5,   # Tritone (augmented 4th/diminished 5th)
        7: 5,   # Perfect 5th
        8: 6,   # Minor 6th
        9: 6,   # Major 6th
        10: 7,  # Minor 7th
        11: 7,  # Major 7th
    }
    
    degree = semitone_to_degree.get(interval_mod, 1)
    
    # Add octaves
    octaves = interval // 12
    if octaves > 0:
        degree += octaves * 7
    
    return degree


def is_perfect_consonance(interval: int) -> bool:
    """
    Check if an interval is a perfect consonance.
    
    Perfect consonances: unison (P1), perfect fifth (P5), octave (P8), and compounds.
    
    Args:
        interval: Interval in semitones
    
    Returns:
        True if perfect consonance
    """
    interval_mod = interval % 12
    return interval_mod in [0, 7]  # Unison/octave or perfect fifth


def is_imperfect_consonance(interval: int) -> bool:
    """
    Check if an interval is an imperfect consonance.
    
    Imperfect consonances: major/minor 3rd, major/minor 6th, and compounds.
    
    Args:
        interval: Interval in semitones
    
    Returns:
        True if imperfect consonance
    """
    interval_mod = interval % 12
    return interval_mod in [3, 4, 8, 9]  # Minor 3rd, major 3rd, minor 6th, major 6th


def is_consonant(interval: int, is_bass: bool = False) -> bool:
    """
    Check if an interval is consonant.
    
    Args:
        interval: Interval in semitones
        is_bass: Whether the lower voice is the bass (affects 4th treatment)
    
    Returns:
        True if consonant
    """
    interval_mod = interval % 12
    
    # Perfect 4th (5 semitones)
    if interval_mod == 5:
        # P4 above bass is dissonant, but consonant between upper voices
        return not is_bass
    
    return is_perfect_consonance(interval) or is_imperfect_consonance(interval)


def is_dissonant(interval: int, is_bass: bool = False) -> bool:
    """
    Check if an interval is dissonant.
    
    Args:
        interval: Interval in semitones
        is_bass: Whether the lower voice is the bass (affects 4th treatment)
    
    Returns:
        True if dissonant
    """
    return not is_consonant(interval, is_bass)
