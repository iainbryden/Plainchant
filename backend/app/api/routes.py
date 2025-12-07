"""API routes for counterpoint generation."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.models import Key, Mode, VoiceRange, SpeciesType, CounterpointProblem
from app.services import generate_cantus_firmus, generate_first_species, evaluate_first_species
from app.services.multi_voice_generator import generate_multi_voice_first_species
from app.services.generation_logger import logger

router = APIRouter()


class GenerateCFRequest(BaseModel):
    tonic: int = Field(ge=0, le=11, description="Tonic pitch class (0-11, C=0)")
    mode: Mode
    length: int = Field(ge=6, le=16, description="Number of notes")
    voice_range: VoiceRange
    seed: int | None = None


class GenerateCFResponse(BaseModel):
    notes: list[dict]
    voice_range: str


class GenerateCounterpointRequest(BaseModel):
    tonic: int = Field(ge=0, le=11)
    mode: Mode
    cf_notes: list[int] = Field(description="CF as MIDI numbers")
    cf_voice_range: VoiceRange
    seed: int | None = None


class GenerateCounterpointResponse(BaseModel):
    cf_notes: list[dict]
    cp_notes: list[dict]
    violations: list[dict]


class EvaluateCounterpointRequest(BaseModel):
    tonic: int = Field(ge=0, le=11)
    mode: Mode
    cf_notes: list[int]
    cp_notes: list[int]


class EvaluateCounterpointResponse(BaseModel):
    violations: list[dict]
    is_valid: bool


class GenerateMultiVoiceRequest(BaseModel):
    tonic: int = Field(ge=0, le=11)
    mode: Mode
    cf_notes: list[int] = Field(description="CF as MIDI numbers")
    cf_voice_range: VoiceRange
    num_voices: int = Field(ge=3, le=4, description="Total voices including CF (3 or 4)")
    seed: int | None = None


class GenerateMultiVoiceResponse(BaseModel):
    voices: list[dict] = Field(description="List of voices with notes and range")
    num_voices: int


class GenerateSecondSpeciesRequest(BaseModel):
    tonic: int = Field(ge=0, le=11)
    mode: Mode
    cf_notes: list[int] = Field(description="CF as MIDI numbers")
    cf_voice_range: VoiceRange
    seed: int | None = None


class GenerateSecondSpeciesResponse(BaseModel):
    cf_notes: list[dict]
    cp_notes: list[dict]
    violations: list[dict]


class GenerateThirdSpeciesRequest(BaseModel):
    tonic: int = Field(ge=0, le=11)
    mode: Mode
    cf_notes: list[int] = Field(description="CF as MIDI numbers")
    cf_voice_range: VoiceRange
    seed: int | None = None


class GenerateThirdSpeciesResponse(BaseModel):
    cf_notes: list[dict]
    cp_notes: list[dict]
    violations: list[dict]


class GenerateFifthSpeciesRequest(BaseModel):
    tonic: int = Field(ge=0, le=11)
    mode: Mode
    cf_notes: list[int] = Field(description="CF as MIDI numbers")
    cf_voice_range: VoiceRange
    seed: int | None = None


class GenerateFifthSpeciesResponse(BaseModel):
    cf_notes: list[dict]
    cp_notes: list[dict]
    violations: list[dict]


@router.post("/generate-cantus-firmus", response_model=GenerateCFResponse)
async def generate_cf_endpoint(request: GenerateCFRequest):
    """Generate a cantus firmus."""
    key = Key(tonic=request.tonic, mode=request.mode)
    
    cf = generate_cantus_firmus(
        key=key,
        length=request.length,
        voice_range=request.voice_range,
        seed=request.seed
    )
    
    if not cf:
        raise HTTPException(status_code=500, detail="Failed to generate cantus firmus")
    
    return GenerateCFResponse(
        notes=[{"midi": n.pitch.midi, "duration": n.duration.value} for n in cf.notes],
        voice_range=cf.voice_range.value
    )


@router.post("/generate-counterpoint", response_model=GenerateCounterpointResponse)
async def generate_counterpoint_endpoint(request: GenerateCounterpointRequest):
    """Generate first species counterpoint."""
    from app.models import Pitch, Note, Duration, VoiceLine
    
    key = Key(tonic=request.tonic, mode=request.mode)
    
    # Reconstruct CF
    cf_notes = [Note(pitch=Pitch.from_midi(m), duration=Duration.WHOLE) for m in request.cf_notes]
    cf = VoiceLine(notes=cf_notes, voice_index=0, voice_range=request.cf_voice_range)
    
    problem = CounterpointProblem(
        key=key,
        cantus_firmus=cf,
        num_voices=2,
        species_per_voice=[SpeciesType.FIRST]
    )
    
    solution = generate_first_species(problem, seed=request.seed)
    
    if not solution:
        raise HTTPException(status_code=500, detail="Failed to generate counterpoint")
    
    violations = evaluate_first_species(cf, solution.voice_lines[1])
    solution.diagnostics = violations
    
    try:
        logger.log_generation(solution, request.model_dump(), "generate-counterpoint")
    except Exception as e:
        print(f"Logging error: {e}")
    
    return GenerateCounterpointResponse(
        cf_notes=[{"midi": n.pitch.midi, "duration": n.duration.value} for n in solution.voice_lines[0].notes],
        cp_notes=[{"midi": n.pitch.midi, "duration": n.duration.value} for n in solution.voice_lines[1].notes],
        violations=[{
            "rule_code": v.rule_code,
            "description": v.description,
            "severity": v.severity.value
        } for v in violations]
    )


@router.post("/evaluate-counterpoint", response_model=EvaluateCounterpointResponse)
async def evaluate_counterpoint_endpoint(request: EvaluateCounterpointRequest):
    """Evaluate a counterpoint against a cantus firmus."""
    from app.models import Pitch, Note, Duration, VoiceLine
    
    # Reconstruct CF and CP
    cf_notes = [Note(pitch=Pitch.from_midi(m), duration=Duration.WHOLE) for m in request.cf_notes]
    cp_notes = [Note(pitch=Pitch.from_midi(m), duration=Duration.WHOLE) for m in request.cp_notes]
    
    cf = VoiceLine(notes=cf_notes, voice_index=0, voice_range=VoiceRange.SOPRANO)
    cp = VoiceLine(notes=cp_notes, voice_index=1, voice_range=VoiceRange.SOPRANO)
    
    violations = evaluate_first_species(cf, cp)
    
    return EvaluateCounterpointResponse(
        violations=[{
            "rule_code": v.rule_code,
            "description": v.description,
            "severity": v.severity.value
        } for v in violations],
        is_valid=len(violations) == 0
    )


@router.post("/generate-second-species", response_model=GenerateSecondSpeciesResponse)
async def generate_second_species_endpoint(request: GenerateSecondSpeciesRequest):
    """Generate second species counterpoint (2:1 rhythm)."""
    from app.models import Pitch, Note, Duration, VoiceLine
    from app.services.second_species_generator import generate_second_species
    from app.services.second_species_rules import evaluate_second_species
    
    key = Key(tonic=request.tonic, mode=request.mode)
    
    # Reconstruct CF
    cf_notes = [Note(pitch=Pitch.from_midi(m), duration=Duration.WHOLE) for m in request.cf_notes]
    cf = VoiceLine(notes=cf_notes, voice_index=0, voice_range=request.cf_voice_range)
    
    problem = CounterpointProblem(
        key=key,
        cantus_firmus=cf,
        num_voices=2,
        species_per_voice=[SpeciesType.SECOND]
    )
    
    solution = generate_second_species(problem, seed=request.seed)
    
    if not solution:
        raise HTTPException(status_code=500, detail="Failed to generate second species counterpoint")
    
    violations = evaluate_second_species(cf, solution.voice_lines[1])
    solution.diagnostics = violations
    
    try:
        logger.log_generation(solution, request.model_dump(), "generate-second-species")
    except Exception as e:
        print(f"Logging error: {e}")
    
    return GenerateSecondSpeciesResponse(
        cf_notes=[{"midi": n.pitch.midi, "duration": n.duration.value} for n in solution.voice_lines[0].notes],
        cp_notes=[{"midi": n.pitch.midi, "duration": n.duration.value} for n in solution.voice_lines[1].notes],
        violations=[{
            "rule_code": v.rule_code,
            "description": v.description,
            "severity": v.severity.value
        } for v in violations]
    )


@router.post("/generate-third-species", response_model=GenerateThirdSpeciesResponse)
async def generate_third_species_endpoint(request: GenerateThirdSpeciesRequest):
    """Generate third species counterpoint (4:1 rhythm)."""
    from app.models import Pitch, Note, Duration, VoiceLine
    from app.services.third_species_generator import generate_third_species
    from app.services.third_species_rules import evaluate_third_species
    
    key = Key(tonic=request.tonic, mode=request.mode)
    
    # Reconstruct CF
    cf_notes = [Note(pitch=Pitch.from_midi(m), duration=Duration.WHOLE) for m in request.cf_notes]
    cf = VoiceLine(notes=cf_notes, voice_index=0, voice_range=request.cf_voice_range)
    
    problem = CounterpointProblem(
        key=key,
        cantus_firmus=cf,
        num_voices=2,
        species_per_voice=[SpeciesType.THIRD]
    )
    
    solution = generate_third_species(problem, seed=request.seed)
    
    if not solution:
        raise HTTPException(status_code=500, detail="Failed to generate third species counterpoint")
    
    violations = evaluate_third_species(cf, solution.voice_lines[1])
    solution.diagnostics = violations
    
    try:
        logger.log_generation(solution, request.model_dump(), "generate-third-species")
    except Exception as e:
        print(f"Logging error: {e}")
    
    return GenerateThirdSpeciesResponse(
        cf_notes=[{"midi": n.pitch.midi, "duration": n.duration.value} for n in solution.voice_lines[0].notes],
        cp_notes=[{"midi": n.pitch.midi, "duration": n.duration.value} for n in solution.voice_lines[1].notes],
        violations=[{
            "rule_code": v.rule_code,
            "description": v.description,
            "severity": v.severity.value
        } for v in violations]
    )


@router.post("/generate-fifth-species", response_model=GenerateFifthSpeciesResponse)
async def generate_fifth_species_endpoint(request: GenerateFifthSpeciesRequest):
    """Generate fifth species counterpoint (florid with mixed rhythms)."""
    from app.models import Pitch, Note, Duration, VoiceLine
    from app.services.fifth_species_generator import generate_fifth_species
    from app.services.fifth_species_rules import evaluate_fifth_species
    
    key = Key(tonic=request.tonic, mode=request.mode)
    
    # Reconstruct CF
    cf_notes = [Note(pitch=Pitch.from_midi(m), duration=Duration.WHOLE) for m in request.cf_notes]
    cf = VoiceLine(notes=cf_notes, voice_index=0, voice_range=request.cf_voice_range)
    
    problem = CounterpointProblem(
        key=key,
        cantus_firmus=cf,
        num_voices=2,
        species_per_voice=[SpeciesType.FIFTH]
    )
    
    solution = generate_fifth_species(problem, seed=request.seed)
    
    if not solution:
        raise HTTPException(status_code=500, detail="Failed to generate fifth species counterpoint")
    
    violations = evaluate_fifth_species(cf, solution.voice_lines[1])
    solution.diagnostics = violations
    
    try:
        logger.log_generation(solution, request.model_dump(), "generate-fifth-species")
    except Exception as e:
        print(f"Logging error: {e}")
    
    return GenerateFifthSpeciesResponse(
        cf_notes=[{"midi": n.pitch.midi, "duration": n.duration.value} for n in solution.voice_lines[0].notes],
        cp_notes=[{"midi": n.pitch.midi, "duration": n.duration.value} for n in solution.voice_lines[1].notes],
        violations=[{
            "rule_code": v.rule_code,
            "description": v.description,
            "severity": v.severity.value
        } for v in violations]
    )


@router.post("/generate-multi-voice", response_model=GenerateMultiVoiceResponse)
async def generate_multi_voice_endpoint(request: GenerateMultiVoiceRequest):
    """Generate 3-4 voice first species counterpoint."""
    from app.models import Pitch, Note, Duration, VoiceLine
    
    key = Key(tonic=request.tonic, mode=request.mode)
    
    # Reconstruct CF
    cf_notes = [Note(pitch=Pitch.from_midi(m), duration=Duration.WHOLE) for m in request.cf_notes]
    cf = VoiceLine(notes=cf_notes, voice_index=0, voice_range=request.cf_voice_range)
    
    problem = CounterpointProblem(
        key=key,
        cantus_firmus=cf,
        num_voices=request.num_voices,
        species_per_voice=[SpeciesType.FIRST] * (request.num_voices - 1)
    )
    
    solution = generate_multi_voice_first_species(
        problem,
        num_voices=request.num_voices,
        seed=request.seed
    )
    
    if not solution:
        raise HTTPException(status_code=500, detail="Failed to generate multi-voice counterpoint")
    
    # Ensure diagnostics field exists for logging
    if not hasattr(solution, 'diagnostics') or solution.diagnostics is None:
        solution.diagnostics = []
    
    try:
        logger.log_generation(solution, request.model_dump(), "generate-multi-voice")
    except Exception as e:
        print(f"Logging error: {e}")
    
    return GenerateMultiVoiceResponse(
        voices=[{
            "voice_index": v.voice_index,
            "voice_range": v.voice_range.value,
            "notes": [{"midi": n.pitch.midi, "duration": n.duration.value} for n in v.notes]
        } for v in solution.voice_lines],
        num_voices=len(solution.voice_lines)
    )
