# Species Counterpoint Generator - Backend

Python backend API for generating and evaluating species counterpoint music.

## Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv .venv
```

### 2. Activate Virtual Environment

**Windows (Git Bash):**
```bash
source .venv/Scripts/activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` as needed for your environment.

### 5. Run the Development Server

```bash
# Option 1: Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Option 2: Using Python
python -m app.main
```

### 6. Access the API

- **API Base**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── models/              # Pydantic data models
│   ├── services/            # Business logic (generators, validators)
│   └── api/                 # API route handlers
├── tests/                   # Unit and integration tests
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Development

### Running Tests

```bash
pytest
```

### Running Tests with Coverage

```bash
pytest --cov=app --cov-report=html
```

### Code Style

Follow PEP 8 guidelines. Use type hints for all functions.

## API Endpoints

### Current

- `GET /` - Root endpoint with API info
- `GET /health` - Health check

### Planned

- `POST /generate-cantus-firmus` - Generate a cantus firmus melody
- `POST /generate-counterpoint` - Generate counterpoint voices
- `POST /evaluate-counterpoint` - Evaluate counterpoint against rules
- `POST /evaluate-melody` - Evaluate a single melody

## Technologies

- **FastAPI** - Modern async web framework
- **Pydantic** - Data validation using Python type hints
- **Uvicorn** - ASGI server
- **pytest** - Testing framework
