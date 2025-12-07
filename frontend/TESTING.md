# Frontend Testing Guide

## Manual Testing

### Prerequisites
1. Backend running at `http://localhost:8000`
2. Frontend running at `http://localhost:5173`

```bash
# Terminal 1 - Backend
cd backend
source .venv/bin/activate
python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Test Scenarios

#### 1. Generate Cantus Firmus
- [ ] Select tonic (e.g., C)
- [ ] Select mode (e.g., Ionian)
- [ ] Select CF voice range (e.g., Alto)
- [ ] Set length (e.g., 8)
- [ ] Click "Generate CF"
- [ ] Verify CF notes appear in readable format (e.g., C4, D4, E4...)
- [ ] Verify MIDI values shown below

#### 2. Generate Counterpoint
- [ ] After CF generated, click "Generate Counterpoint"
- [ ] Verify counterpoint notes appear
- [ ] Verify violations list shows (either success or violations)
- [ ] Check violations are categorized (errors/warnings)

#### 3. Error Handling
- [ ] Stop backend server
- [ ] Try to generate CF
- [ ] Verify error message appears
- [ ] Restart backend
- [ ] Verify generation works again

#### 4. Loading States
- [ ] Click "Generate CF"
- [ ] Verify button shows "Generating..." and is disabled
- [ ] Verify button returns to normal after completion

#### 5. Seed Reproducibility
- [ ] Generate CF with seed 42
- [ ] Note the CF notes
- [ ] Generate CF again with seed 42
- [ ] Verify same CF notes generated

## Browser Testing

Test in:
- [ ] Chrome
- [ ] Firefox
- [ ] Safari

## Responsive Testing

Test at screen widths:
- [ ] Desktop (1200px+)
- [ ] Tablet (768px)
- [ ] Mobile (375px)

## Network Tab Verification

Open browser DevTools → Network tab:
- [ ] Verify POST to `/api/generate-cantus-firmus`
- [ ] Verify POST to `/api/generate-counterpoint`
- [ ] Verify POST to `/api/evaluate-counterpoint`
- [ ] Check request/response payloads match expected format

## Console Verification

Open browser DevTools → Console:
- [ ] No errors during normal operation
- [ ] No warnings about React keys or hooks
- [ ] API errors logged when backend unavailable

## Automated Testing (Future)

To be implemented with Vitest:
- Component unit tests
- API service tests
- Integration tests
