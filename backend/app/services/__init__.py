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
from .species_rules import (
    check_first_species_consonances,
    check_first_species_start,
    check_first_species_end,
    check_first_species_penultimate,
    FirstSpeciesValidator,
    evaluate_first_species,
)
from .cf_generator import generate_cantus_firmus
from .first_species_generator import generate_first_species

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
    "check_first_species_consonances",
    "check_first_species_start",
    "check_first_species_end",
    "check_first_species_penultimate",
    "FirstSpeciesValidator",
    "evaluate_first_species",
    "generate_cantus_firmus",
    "generate_first_species",
]
