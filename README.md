# Species Counterpoint Generator

A rule-based system for generating and evaluating species counterpoint compositions following classical Fuxian principles.

## Overview

This application generates and validates multi-voice counterpoint compositions (2-4 voices) across all five species, with comprehensive rule checking for melodic and harmonic constraints.

## Tech Stack

- **Backend**: Python 3.12 + FastAPI + Pydantic
- **Testing**: pytest
- **Frontend**: React + Vite + TypeScript (planned)
- **Notation**: VexFlow (planned)
- **Audio**: Tone.js (planned)

## Current Status

✅ **Phase 1**: Foundation & Core Data Models (11/11 complete)  
✅ **Phase 2**: Musical Theory Engine (7/7 complete)  
✅ **Phase 3**: Melodic Rules Engine (9/9 complete)  
✅ **Phase 4**: Harmonic Rules Engine (5/5 complete)  
✅ **Phase 5**: Species-Specific Rules (6/6 complete)  
✅ **Phase 6**: Cantus Firmus Generator (6/6 complete)  
✅ **Phase 7**: First Species Counterpoint Generator (9/9 complete)  
✅ **Phase 8**: REST API - First Species Only (7/7 complete)

**Test Coverage**: 84 tests, all passing

## Quick Start

### Prerequisites

- Python 3.12+
- pip

### Installation

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Unix/macOS
pip install -r requirements.txt
```

### Run Backend

```bash
cd backend
python -m uvicorn app.main:app --reload
```

API available at: `http://localhost:8000`  
Docs available at: `http://localhost:8000/docs`

### Run Tests

```bash
cd backend
source .venv/bin/activate
python -m pytest tests/ -v
```

With coverage:
```bash
python -m pytest tests/ --cov=app --cov-report=term-missing
```

## Project Structure

```
backend/
├── app/
│   ├── models/          # Pydantic data models
│   │   ├── pitch.py     # Pitch representation
│   │   ├── scale.py     # Scales, modes, keys
│   │   ├── note.py      # Notes and durations
│   │   ├── voice.py     # Voice lines and ranges
│   │   └── counterpoint.py  # Problems and solutions
│   ├── services/        # Business logic
│   │   ├── intervals.py      # Interval calculations
│   │   ├── motion.py         # Motion detection
│   │   ├── melodic_rules.py  # Per-voice constraints
│   │   └── harmonic_rules.py # Voice interactions
│   └── main.py          # FastAPI application
└── tests/               # Unit tests (84 tests)
```

## Features Implemented

### Core Models
- Pitch (MIDI, pitch class, octave, spelling)
- Scales & Modes (Ionian, Dorian, Phrygian, Lydian, Mixolydian, Aeolian, Locrian)
- Notes & Durations (whole, half, quarter, eighth, sixteenth)
- Voice Lines & Ranges (SOPRANO, ALTO, TENOR, BASS)
- Species Types (FIRST through FIFTH)

### Musical Theory
- Interval calculation (semitones)
- Consonance/dissonance classification
- Perfect consonances (P1, P5, P8)
- Imperfect consonances (M3, m3, M6, m6)
- Special handling: P4 above bass is dissonant
- Motion detection (parallel, similar, contrary, oblique)

### Melodic Rules
- Range constraints per voice
- Leap size limits (max octave)
- Leap compensation (large leap → opposite step)
- Step preference (≥60% stepwise motion)
- Repeated note limits
- Single melodic climax
- No augmented intervals
- No melodic tritones
- Start/end on tonic

### Harmonic Rules
- No parallel perfect fifths or octaves
- No hidden (direct) perfects in outer voices
- No voice crossing
- Voice overlap detection
- Reasonable spacing between voices

### First Species Rules
- All intervals must be consonant
- Start with perfect consonance (P1, P5, P8)
- End with unison or octave
- Penultimate cadence (6-8 or 3-1)
- Complete validator for first species counterpoint

## API Endpoints

### Health Check
```http
GET /health
```

### Generate Cantus Firmus
```http
POST /api/generate-cantus-firmus
```

Request body:
```json
{
  "tonic": 0,
  "mode": "ionian",
  "length": 8,
  "voice_range": "soprano",
  "seed": 42
}
```

### Generate Counterpoint
```http
POST /api/generate-counterpoint
```

Request body:
```json
{
  "tonic": 0,
  "mode": "ionian",
  "cf_notes": [60, 62, 64, 65, 67, 69, 71, 72],
  "cf_voice_range": "alto",
  "seed": 42
}
```

### Evaluate Counterpoint
```http
POST /api/evaluate-counterpoint
```

Request body:
```json
{
  "tonic": 0,
  "mode": "ionian",
  "cf_notes": [60, 62, 64, 65, 67, 69, 71, 72],
  "cp_notes": [67, 69, 71, 72, 74, 76, 77, 79]
}
```

## Development

See [development-checklist.md](Docs/development-checklist.md) for detailed implementation roadmap.

See [PROGRESS.md](PROGRESS.md) for current progress tracking.

## Documentation

- [Development Checklist](Docs/development-checklist.md) - Implementation roadmap
- [Species Counterpoint Rules](Docs/species-counterpoint-rules.md) - Complete rule reference
- [Recommended Approach](Docs/species-counterpoint-recommended-approach.md) - Architecture guidance
- [Task List](Docs/species-counterpoint-generator-app-tasks.md) - Detailed task breakdown

## Testing

All implemented features have comprehensive unit test coverage:

- **Models**: 13 tests
- **Intervals & Motion**: 11 tests
- **Melodic Rules**: 17 tests
- **Harmonic Rules**: 11 tests
- **Species Rules**: 15 tests
- **CF Generator**: 6 tests
- **First Species Generator**: 5 tests
- **API Endpoints**: 6 tests

**Total**: 84 tests passing on Python 3.12

Run specific test suites:
```bash
cd backend
source .venv/bin/activate
pytest tests/test_models.py -v
pytest tests/test_intervals.py -v
pytest tests/test_melodic_rules.py -v
pytest tests/test_harmonic_rules.py -v
pytest tests/test_species_rules.py -v
```

## Next Steps

1. Build React frontend
3. Create REST API endpoints
4. Build React frontend
5. Add notation display (VexFlow)
6. Add audio playback (Tone.js)

## License

MIT
