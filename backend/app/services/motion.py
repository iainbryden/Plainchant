"""Motion type detection between voices."""

from enum import Enum
from app.models import Pitch


class MotionType(str, Enum):
    """Types of motion between two voices."""
    PARALLEL = "parallel"      # Same direction, same interval
    SIMILAR = "similar"        # Same direction, different interval
    CONTRARY = "contrary"      # Opposite directions
    OBLIQUE = "oblique"        # One voice static


def motion_type(prev_p1: Pitch, curr_p1: Pitch, prev_p2: Pitch, curr_p2: Pitch) -> MotionType:
    """
    Determine the type of motion between two voices.
    
    Args:
        prev_p1: Previous pitch in voice 1
        curr_p1: Current pitch in voice 1
        prev_p2: Previous pitch in voice 2
        curr_p2: Current pitch in voice 2
    
    Returns:
        The type of motion
    """
    # Calculate motion in each voice
    motion1 = curr_p1.midi - prev_p1.midi
    motion2 = curr_p2.midi - prev_p2.midi
    
    # Oblique: one voice stays, other moves
    if motion1 == 0 and motion2 != 0:
        return MotionType.OBLIQUE
    if motion2 == 0 and motion1 != 0:
        return MotionType.OBLIQUE
    
    # No motion in either voice (both static)
    if motion1 == 0 and motion2 == 0:
        return MotionType.OBLIQUE  # Treat as oblique
    
    # Contrary: opposite directions
    if (motion1 > 0 and motion2 < 0) or (motion1 < 0 and motion2 > 0):
        return MotionType.CONTRARY
    
    # Same direction: check if intervals are the same
    prev_interval = abs(prev_p2.midi - prev_p1.midi)
    curr_interval = abs(curr_p2.midi - curr_p1.midi)
    
    if prev_interval == curr_interval:
        return MotionType.PARALLEL
    else:
        return MotionType.SIMILAR
