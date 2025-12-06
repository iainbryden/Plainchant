"""
Core data models for species counterpoint generation.
"""

from .pitch import Pitch
from .scale import Scale, Mode, Key
from .note import Duration, Note
from .voice import VoiceLine, VoiceRange, SpeciesType
from .counterpoint import CounterpointProblem, CounterpointSolution, RuleViolation, Severity

__all__ = [
    "Pitch",
    "Scale",
    "Mode",
    "Key",
    "Duration",
    "Note",
    "VoiceLine",
    "VoiceRange",
    "SpeciesType",
    "CounterpointProblem",
    "CounterpointSolution",
    "RuleViolation",
    "Severity",
]
