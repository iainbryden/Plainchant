# Deployment Guide

## Quick Start

### Local Development

1. **Setup Environment**
```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate  # Unix/macOS
pip install -r requirements.txt
```

2. **Run Server**
```bash
python -m uvicorn app.main:app --reload
```

3. **Access API**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

### Run Tests
```bash
cd backend
source .venv/bin/activate
python -m pytest tests/ -v
```

## Production Deployment

### Requirements
- Python 3.12+
- 512MB RAM minimum
- Linux/macOS/Windows

### Environment Variables

Create `.env` file:
```env
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:5173,https://yourdomain.com
```

### Docker (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t counterpoint-api .
docker run -p 8000:8000 counterpoint-api
```

### Cloud Deployment Options

#### Heroku
```bash
# Procfile
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### AWS Lambda (with Mangum)
```python
from mangum import Mangum
from app.main import app

handler = Mangum(app)
```

#### DigitalOcean App Platform
- Connect GitHub repo
- Set build command: `pip install -r requirements.txt`
- Set run command: `uvicorn app.main:app --host 0.0.0.0 --port 8080`

## API Usage Examples

### Generate Cantus Firmus
```bash
curl -X POST http://localhost:8000/api/generate-cantus-firmus \
  -H "Content-Type: application/json" \
  -d '{
    "tonic": 0,
    "mode": "ionian",
    "length": 8,
    "voice_range": "soprano",
    "seed": 42
  }'
```

### Generate Counterpoint
```bash
curl -X POST http://localhost:8000/api/generate-counterpoint \
  -H "Content-Type: application/json" \
  -d '{
    "tonic": 0,
    "mode": "ionian",
    "cf_notes": [60, 62, 64, 65, 67, 69, 71, 72],
    "cf_voice_range": "alto",
    "seed": 42
  }'
```

### Evaluate Counterpoint
```bash
curl -X POST http://localhost:8000/api/evaluate-counterpoint \
  -H "Content-Type: application/json" \
  -d '{
    "tonic": 0,
    "mode": "ionian",
    "cf_notes": [60, 62, 64, 65, 67, 69, 71, 72],
    "cp_notes": [67, 69, 71, 72, 74, 76, 77, 79]
  }'
```

## Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### Logs
Server logs include:
- Request method and path
- Response status code
- Request duration

Example log:
```
INFO: POST /api/generate-counterpoint - 200 - 0.045s
```

## Performance

- CF generation: ~50-200ms
- Counterpoint generation: ~50-500ms
- Evaluation: ~5-20ms

## Security

- CORS configured for specified origins
- Input validation via Pydantic
- No authentication required (add if needed)
- Rate limiting recommended for production

## Troubleshooting

### Port Already in Use
```bash
# Find process
lsof -i :8000
# Kill process
kill -9 <PID>
```

### Module Not Found
```bash
# Ensure virtual environment is activated
source .venv/bin/activate
# Reinstall dependencies
pip install -r requirements.txt
```

### Tests Failing
```bash
# Run with verbose output
python -m pytest tests/ -v -s
```
