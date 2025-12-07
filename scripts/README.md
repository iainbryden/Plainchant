# Scripts

Quick commands to manage the Species Counterpoint Generator.

## Usage

### Start Everything
```bash
./scripts/start.sh [browser]
```
- Starts backend server (http://localhost:8000)
- Starts frontend server (http://localhost:5173)
- Opens browser automatically
- Runs in background

**Browser options:**
```bash
./scripts/start.sh          # Default browser
./scripts/start.sh chrome   # Google Chrome
./scripts/start.sh firefox  # Firefox
./scripts/start.sh safari   # Safari
```

### Stop Everything
```bash
./scripts/stop.sh
```
- Stops both backend and frontend servers

### Restart Everything
```bash
./scripts/restart.sh
```
- Stops then starts both servers

### Open Browser
```bash
./scripts/open.sh
```
- Opens http://localhost:5173 in default browser

## Logs

Logs are saved to `logs/` directory:
- `logs/backend.log` - Backend server output
- `logs/frontend.log` - Frontend server output

View logs in real-time:
```bash
tail -f logs/backend.log
tail -f logs/frontend.log
```

## Process IDs

PIDs are stored in:
- `logs/backend.pid`
- `logs/frontend.pid`

## Manual Commands

If scripts don't work, use manual commands:

### Backend
```bash
cd backend
source .venv/bin/activate
python3 -m uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm run dev
```

## Troubleshooting

### Port already in use
If you get "port already in use" errors:
```bash
# Find and kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Find and kill process on port 5173 (frontend)
lsof -ti:5173 | xargs kill -9
```

### Scripts not executable
```bash
chmod +x scripts/*.sh
```

### Backend won't start
Check that virtual environment exists:
```bash
ls backend/.venv/
```

If missing, recreate:
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Frontend won't start
Check that node_modules exists:
```bash
ls frontend/node_modules/
```

If missing:
```bash
cd frontend
npm install
```
