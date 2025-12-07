# Project Structure

```
Plainchant/
├── backend/                    # Backend API (Python/FastAPI)
│   ├── app/
│   │   ├── api/               # REST API routes
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── models/            # Pydantic data models
│   │   │   ├── __init__.py
│   │   │   ├── pitch.py
│   │   │   ├── scale.py
│   │   │   ├── note.py
│   │   │   ├── voice.py
│   │   │   └── counterpoint.py
│   │   ├── services/          # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── intervals.py
│   │   │   ├── motion.py
│   │   │   ├── melodic_rules.py
│   │   │   ├── harmonic_rules.py
│   │   │   ├── species_rules.py
│   │   │   ├── cf_generator.py
│   │   │   └── first_species_generator.py
│   │   ├── __init__.py
│   │   └── main.py            # FastAPI application
│   ├── tests/                 # Unit tests (84 tests)
│   │   ├── test_api.py
│   │   ├── test_cf_generator.py
│   │   ├── test_first_species_generator.py
│   │   ├── test_harmonic_rules.py
│   │   ├── test_intervals.py
│   │   ├── test_melodic_rules.py
│   │   ├── test_models.py
│   │   └── test_species_rules.py
│   ├── .env.example           # Environment variables template
│   ├── .gitignore
│   ├── README.md              # Backend-specific readme
│   └── requirements.txt       # Python dependencies
│
├── Docs/                      # Documentation
│   ├── BACKEND_COMPLETE.md    # Backend completion summary
│   ├── DEPLOYMENT.md          # Deployment guide
│   ├── development-checklist.md  # Main progress tracker
│   ├── NEXT_STEPS.md          # What to build next
│   ├── PROGRESS.md            # Detailed progress log
│   ├── species-counterpoint-rules.md  # Music theory rules
│   ├── species-counterpoint-recommended-approach.md
│   └── species-counterpoint-generator-app-tasks.md
│
├── scripts/                   # Utility scripts
│   └── test_api_live.py       # Live API testing script
│
├── .gitignore                 # Root gitignore
├── .python-version            # Python version (3.12)
├── PROJECT_STRUCTURE.md       # This file
└── README.md                  # Main project readme

Future directories (not yet created):
├── frontend/                  # React frontend (Phase 9+)
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── types/
│   │   └── utils/
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
```

## Directory Purposes

### `/backend`
Complete Python/FastAPI backend with:
- REST API endpoints
- Counterpoint generation algorithms
- Rule validation
- 84 passing tests

### `/Docs`
All project documentation:
- Development checklist (main progress tracker)
- Progress logs
- Deployment guides
- Music theory references

### `/scripts`
Utility scripts for:
- Testing the live API
- Development helpers
- Data generation

### `/frontend` (future)
React + TypeScript frontend for:
- User interface
- Music notation display
- Audio playback

## Key Files

- `README.md` - Main project overview
- `Docs/development-checklist.md` - **Main progress tracker**
- `Docs/BACKEND_COMPLETE.md` - Backend summary
- `Docs/DEPLOYMENT.md` - How to run/deploy
- `Docs/NEXT_STEPS.md` - What to build next
- `backend/app/main.py` - FastAPI application entry point
- `backend/requirements.txt` - Python dependencies
- `.python-version` - Python 3.12 requirement

## Running the Project

### Backend
```bash
cd backend
source .venv/bin/activate
python -m uvicorn app.main:app --reload
```

### Tests
```bash
cd backend
source .venv/bin/activate
python -m pytest tests/ -v
```

### Live API Test
```bash
python scripts/test_api_live.py
```

## Documentation Flow

1. Start with `README.md` for overview
2. Check `Docs/development-checklist.md` for progress
3. See `Docs/BACKEND_COMPLETE.md` for what's done
4. Read `Docs/NEXT_STEPS.md` for what's next
5. Use `Docs/DEPLOYMENT.md` to run/deploy

## Clean Structure Benefits

✅ Clear separation of concerns
✅ Easy to navigate
✅ Scalable for frontend addition
✅ Professional organization
✅ Documentation centralized
✅ Scripts isolated
