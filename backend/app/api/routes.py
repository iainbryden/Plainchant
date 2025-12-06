"""API routes for counterpoint generation."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.models import Key, Mode, VoiceRange, SpeciesType, CounterpointProblem
from app.services import generate_cantus_firmus, generate_first_species, evaluate_first_species

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
