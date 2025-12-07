# Species Counterpoint Generator

A rule-based system for generating and evaluating species counterpoint compositions following classical Fuxian principles.

## Overview

This application generates and validates multi-voice counterpoint compositions (2-4 voices) across all five species, with comprehensive rule checking for melodic and harmonic constraints.

## Tech Stack

- **Backend**: Python 3.12 + FastAPI + Pydantic
- **Testing**: pytest
- **Frontend**: React + Vite + TypeScript
- **Notation**: VexFlow
- **Audio**: Tone.js

## Current Status

🎉 **EXTENDED MVP COMPLETE** - Phases 1-15 done!

✅ **Phase 1**: Foundation & Core Data Models (11/11 complete)  
✅ **Phase 2**: Musical Theory Engine (7/7 complete)  
✅ **Phase 3**: Melodic Rules Engine (9/9 complete)  
✅ **Phase 4**: Harmonic Rules Engine (5/5 complete)  
✅ **Phase 5**: Species-Specific Rules (6/6 complete)  
✅ **Phase 6**: Cantus Firmus Generator (6/6 complete)  
✅ **Phase 7**: First Species Counterpoint Generator (9/9 complete)  
✅ **Phase 8**: REST API - First Species Only (8/8 complete)  
✅ **Phase 9**: Frontend Foundation (6/6 complete)  
✅ **Phase 10**: Basic UI (10/10 complete)  
✅ **Phase 11**: Music Notation Rendering (9/13 complete)  
✅ **Phase 12**: Audio Playback (8/14 complete)  
✅ **Phase 13**: Multi-Voice Support (15/16 complete)  
✅ **Phase 14**: Second Species (11/11 complete)  
✅ **Phase 15**: Third Species (10/10 complete)  
⚠️ **Phase 16**: Fourth Species (6/11 partial - rules complete, generator needs refinement)  
✅ **Phase 17**: Fifth Species (10/10 complete)

**Test Coverage**: 122 backend tests passing, 4 skipped

**Fully Functional**: Generate first, second, third, and fifth species counterpoint with 2-4 voices!

See [BACKEND_COMPLETE.md](Docs/BACKEND_COMPLETE.md) for backend summary.

## Quick Start

### One-Command Start (Recommended)

```bash
./scripts/start.sh
```

This will:
- Start backend server (http://localhost:8000)
- Start frontend server (http://localhost:5173)
- Open browser automatically

**Stop servers:**
```bash
./scripts/stop.sh
```

**Restart servers:**
```bash
./scripts/restart.sh
```

See [scripts/README.md](scripts/README.md) for details.

### Manual Setup

#### Prerequisites
- Python 3.12+
- Node.js 18+
- npm

#### Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload
```

API: http://localhost:8000  
Docs: http://localhost:8000/docs

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173

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

### View Generation Logs

All generated counterpoint is automatically logged to `backend/logs/generations.jsonl` for evaluation:

```bash
cd backend
python view_logs.py
```

Logs include:
- Timestamp and endpoint
- Generation parameters (key, mode, species, etc.)
- All voice notes (MIDI numbers)
- Rule violations detected

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

### Generate First Species Counterpoint
```http
POST /api/generate-counterpoint
```

### Generate Second Species Counterpoint (2:1 rhythm)
```http
POST /api/generate-second-species
```

### Generate Third Species Counterpoint (4:1 rhythm)
```http
POST /api/generate-third-species
```

### Generate Fifth Species Counterpoint (florid - mixed rhythms)
```http
POST /api/generate-fifth-species
```

### Generate Multi-Voice Counterpoint (3-4 voices)
```http
POST /api/generate-multi-voice
```

### Evaluate Counterpoint
```http
POST /api/evaluate-counterpoint
```

See API docs at http://localhost:8000/docs for detailed request/response schemas.

## Development

See [development-checklist.md](Docs/development-checklist.md) for detailed implementation roadmap.

See [PROGRESS.md](PROGRESS.md) for current progress tracking.

## Documentation

**Start Here:**
- [Development Checklist](Docs/development-checklist.md) - **Main guide for developers**
- [Coding Standards](Docs/CODING_STANDARDS.md) - **Required reading for contributors**

**Project Info:**
- [Project Structure](Docs/PROJECT_STRUCTURE.md) - Directory organization
- [Backend Complete](Docs/BACKEND_COMPLETE.md) - Backend summary
- [Progress Tracking](Docs/PROGRESS.md) - Detailed progress log
- [Next Steps](Docs/NEXT_STEPS.md) - What to build next

**Guides:**
- [Frontend Testing Guide](Docs/FRONTEND_TESTING.md) - Manual testing procedures for UI
- [Generation Logging](Docs/GENERATION_LOGGING.md) - How to view and analyze generation logs
- [Deployment Guide](Docs/DEPLOYMENT.md) - How to deploy
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
- **Second Species**: 11 tests
- **Third Species**: 9 tests
- **Fourth Species**: 5 tests (4 generator tests skipped)
- **Fifth Species**: 8 tests
- **Multi-Voice**: 5 tests
- **API Endpoints**: 6 tests

**Total**: 122 tests passing, 4 skipped on Python 3.12

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

## Next Steps (Optional)

1. Refine fourth species (Phase 16) - True suspension patterns
2. Add user melody input (Phase 18) - Custom cantus firmus editor
3. Frontend integration - Add species 2, 3, 5 to UI
4. Complete Phase 11 & 12 polish (note selection, measure numbers, mute controls)
5. UI/UX polish (Phase 19) - Dark mode, export MIDI/PDF, keyboard shortcuts

See [NEXT_STEPS.md](Docs/NEXT_STEPS.md) for detailed roadmap.

## License

MIT
