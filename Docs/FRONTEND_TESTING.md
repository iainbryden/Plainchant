# Frontend Testing Guide - Phases 9-11

## Prerequisites

### 1. Start Backend Server
```bash
cd backend
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Use python (after venv activation) or python3
python -m uvicorn app.main:app --reload
# OR if python not found:
python3 -m uvicorn app.main:app --reload
```

Verify backend at: http://localhost:8000/docs

### 2. Start Frontend Dev Server
```bash
cd frontend
npm run dev
```

Frontend runs at: http://localhost:5173

---

## Phase 9: Frontend Foundation - Testing

### Test 9.1: Basic App Load
1. Open http://localhost:5173
2. **Expected**: Page loads without errors
3. **Expected**: "Species Counterpoint Generator" title visible
4. **Expected**: API Status shows "ok" (green)

### Test 9.2: API Connection
1. Open browser DevTools → Console
2. **Expected**: No errors in console
3. **Expected**: Network tab shows successful GET to `/health`

### Test 9.3: Environment Configuration
1. Check `.env` file exists in `frontend/` directory
2. **Expected**: Contains `VITE_API_BASE_URL=http://localhost:8000`

---

## Phase 10: Basic UI - Testing

### Test 10.1: Key Selector
1. Locate "Tonic" dropdown
2. Select different tonics (C, D, E, F, G, A, B)
3. **Expected**: Dropdown updates correctly
4. Locate "Mode" dropdown
5. Select different modes (Ionian, Dorian, Aeolian, etc.)
6. **Expected**: Dropdown updates correctly

### Test 10.2: Voice Range Selector
1. Locate "CF Voice" radio buttons
2. Click each option: Soprano, Alto, Tenor, Bass
3. **Expected**: Radio button selection changes
4. **Expected**: Only one can be selected at a time

### Test 10.3: Generate Cantus Firmus
1. Set: Tonic = C, Mode = Ionian, CF Voice = Alto, Length = 8
2. Click "Generate CF" button
3. **Expected**: Button shows "Generating..." briefly
4. **Expected**: CF notes appear below (e.g., "C4 D4 E4 F4 G4 A4 B4 C5")
5. **Expected**: MIDI values shown (e.g., "MIDI: [60, 62, 64, 65, 67, 69, 71, 72]")
6. Open DevTools → Network tab
7. **Expected**: POST request to `/api/generate-cantus-firmus`
8. **Expected**: Response status 200

### Test 10.4: Generate Counterpoint
1. After CF generated, locate "Generate Counterpoint" button
2. **Expected**: Button is enabled (not grayed out)
3. Click "Generate Counterpoint"
4. **Expected**: Button shows "Generating..." briefly
5. **Expected**: Counterpoint notes appear
6. **Expected**: Violations list appears (either "✓ No Violations" or list of violations)
7. Open DevTools → Network tab
8. **Expected**: POST to `/api/generate-counterpoint`
9. **Expected**: POST to `/api/evaluate-counterpoint`

### Test 10.5: Violations Display
1. Generate multiple counterpoints until you get violations
2. **Expected**: Violations section shows count (e.g., "Rule Violations (2)")
3. **Expected**: Each violation shows:
   - Rule code (e.g., "PARALLEL_FIFTHS")
   - Description
   - Note indices
4. **Expected**: Errors shown in red background
5. **Expected**: Warnings shown in yellow background

### Test 10.6: Loading States
1. Click "Generate CF" button
2. **Expected**: Button disabled during generation
3. **Expected**: Button text changes to "Generating..."
4. **Expected**: Cannot click button again until complete

### Test 10.7: Error Handling
1. Stop backend server (Ctrl+C in backend terminal)
2. Try to generate CF
3. **Expected**: Error message appears: "Failed to generate Cantus Firmus. Please try again."
4. **Expected**: Error message has red background
5. Restart backend server
6. Try again
7. **Expected**: Works normally

### Test 10.8: Seed Reproducibility
1. Set seed to 42 in CF controls
2. Generate CF, note the notes
3. Generate CF again with seed 42
4. **Expected**: Exact same CF notes generated
5. Clear seed field
6. Generate CF multiple times
7. **Expected**: Different CF each time

---

## Phase 11: Music Notation - Testing

### Test 11.1: Single Staff Rendering (CF Only)
1. Generate a Cantus Firmus
2. **Expected**: Musical notation appears above note list
3. **Expected**: Single staff with treble or bass clef
4. **Expected**: Time signature "4/4" visible
5. **Expected**: Key signature visible (e.g., no sharps/flats for C major)
6. **Expected**: Notes positioned on correct lines/spaces
7. **Expected**: Number of notes matches CF length

### Test 11.2: Two Staves Rendering (CF + CP)
1. Generate Counterpoint
2. **Expected**: Two staves appear
3. **Expected**: Top staff = Counterpoint
4. **Expected**: Bottom staff = Cantus Firmus
5. **Expected**: Both staves aligned vertically
6. **Expected**: Both have clefs, key signature, time signature

### Test 11.3: Clef Selection
1. Generate CF with Alto voice (middle range)
2. **Expected**: Treble clef used
3. Generate CF with Bass voice (low range)
4. **Expected**: Bass clef used
5. Generate CF with Soprano voice (high range)
6. **Expected**: Treble clef used

### Test 11.4: Key Signatures
1. Set Tonic = C, Mode = Ionian
2. Generate CF
3. **Expected**: No sharps or flats in key signature
4. Set Tonic = G, Mode = Ionian
5. Generate CF
6. **Expected**: One sharp (F#) in key signature
7. Set Tonic = F, Mode = Ionian
8. Generate CF
9. **Expected**: One flat (Bb) in key signature

### Test 11.5: Accidentals
1. Generate CF in a key with sharps (e.g., D major)
2. **Expected**: Sharp symbols appear before affected notes
3. **Expected**: Accidentals render correctly (not overlapping)

### Test 11.6: Violation Highlighting
1. Generate counterpoint until violations occur
2. **Expected**: Notes with violations highlighted in RED
3. **Expected**: Red notes correspond to note indices in violations list
4. Generate valid counterpoint (no violations)
5. **Expected**: All notes in black (no red highlighting)

### Test 11.7: Responsive Sizing
1. Resize browser window to narrow width
2. **Expected**: Notation container scrolls horizontally
3. **Expected**: Notation doesn't overflow or break layout
4. Resize to wide width
5. **Expected**: Notation scales appropriately

### Test 11.8: Long Melodies
1. Set CF length to 16
2. Generate CF and CP
3. **Expected**: Notation renders all 16 notes
4. **Expected**: Horizontal scroll appears if needed
5. **Expected**: No notes cut off or missing

---

## Visual Verification Checklist

### Layout
- [ ] Header centered with title and subtitle
- [ ] Controls panel has light gray background
- [ ] Results panel below controls
- [ ] Proper spacing between sections
- [ ] No overlapping elements

### Controls
- [ ] All labels aligned and readable
- [ ] Dropdowns and inputs properly sized
- [ ] Radio buttons aligned horizontally
- [ ] Buttons have hover effects
- [ ] Disabled buttons appear grayed out

### Notation
- [ ] Staff lines straight and even
- [ ] Notes properly positioned on staff
- [ ] Clefs render correctly
- [ ] Time signatures clear
- [ ] Key signatures positioned correctly
- [ ] No overlapping symbols

### Colors
- [ ] Success messages: green background
- [ ] Error messages: red background
- [ ] Warnings: yellow background
- [ ] Violation highlights: red notes
- [ ] Buttons: blue with darker blue on hover

---

## Browser Compatibility Testing

Test in each browser:

### Chrome
- [ ] All features work
- [ ] Notation renders correctly
- [ ] No console errors

### Firefox
- [ ] All features work
- [ ] Notation renders correctly
- [ ] No console errors

### Safari (macOS)
- [ ] All features work
- [ ] Notation renders correctly
- [ ] No console errors

---

## Performance Testing

### Test 11.9: Generation Speed
1. Generate CF (length 8)
2. **Expected**: Completes in < 2 seconds
3. Generate CP
4. **Expected**: Completes in < 3 seconds

### Test 11.10: Notation Rendering Speed
1. Generate CP with 16 notes
2. **Expected**: Notation renders in < 1 second
3. **Expected**: No lag or freezing

---

## Common Issues & Solutions

### Issue: API Status shows "disconnected"
**Solution**: Ensure backend server is running at http://localhost:8000

### Issue: "Failed to generate" error
**Solution**: Check backend console for errors, verify backend is running

### Issue: Notation not appearing
**Solution**: Check browser console for VexFlow errors, refresh page

### Issue: Notes positioned incorrectly
**Solution**: Verify MIDI values are in valid range (0-127)

### Issue: Horizontal scroll not working
**Solution**: Check CSS for `.score-renderer` has `overflow-x: auto`

---

## Automated Testing (Future)

To be implemented:
- Component unit tests with Vitest
- API service mocking tests
- E2E tests with Playwright
- Visual regression tests

---

## Test Results Template

```
Date: ___________
Tester: ___________
Browser: ___________

Phase 9 Tests: __ / 3 passed
Phase 10 Tests: __ / 8 passed
Phase 11 Tests: __ / 10 passed

Issues Found:
1. 
2. 
3. 

Notes:

```

---

**Last Updated**: December 2024
