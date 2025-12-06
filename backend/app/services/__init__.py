"""Services for counterpoint generation and analysis."""

from .intervals import (
    calculate_interval,
    interval_to_scale_degree,
    is_perfect_consonance,
    is_imperfect_consonance,
    is_consonant,
    is_dissonant,
)
from .motion import motion_type, MotionType
from .melodic_rules import (
    check_range,
    check_leap_size,
    check_leap_compensation,
    check_step_preference,
    check_repeated_notes,
    check_melodic_climax,
    check_no_augmented_intervals,
    check_no_melodic_tritones,
    check_start_end_degrees,
)
from .harmonic_rules import (
    check_parallel_perfects,
    check_hidden_perfects,
    check_voice_crossing,
    check_voice_overlap,
    check_spacing,
)

__all__ = [
    "calculate_interval",
    "interval_to_scale_degree",
    "is_perfect_consonance",
    "is_imperfect_consonance",
    "is_consonant",
    "is_dissonant",
    "motion_type",
    "MotionType",
    "check_range",
    "check_leap_size",
    "check_leap_compensation",
    "check_step_preference",
    "check_repeated_notes",
    "check_melodic_climax",
    "check_no_augmented_intervals",
    "check_no_melodic_tritones",
    "check_start_end_degrees",
    "check_parallel_perfects",
    "check_hidden_perfects",
    "check_voice_crossing",
    "check_voice_overlap",
    "check_spacing",
]
