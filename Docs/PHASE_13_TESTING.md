# Phase 13 Testing Guide - Multi-Voice Support

**How to test the new multi-voice functionality**

---

## Prerequisites

### 1. Start Both Servers

```bash
./scripts/start.sh
```

This opens http://localhost:5173 automatically.

**Or manually:**
```bash
# Terminal 1 - Backend
cd backend
source .venv/bin/activate
python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

---

## What Should Work

### ✅ 2-Voice Mode (Original Functionality)
- Generate CF
- Generate 2-voice counterpoint
- Display on 2 staves
- Play both voices
- Show violations

### ✅ 3-Voice Mode (NEW)
- Generate CF
- Generate 3-voice counterpoint
- Display on 3 staves
- Play all 3 voices simultaneously
- Automatic voice range assignment

### ✅ 4-Voice Mode (NEW)
- Generate CF
- Generate 4-voice counterpoint (SATB)
- Display on 4 staves
- Play all 4 voices simultaneously
- Automatic clef assignment

---

## Step-by-Step Testing

### Test 1: 2-Voice Mode (Baseline)

1. **Open** http://localhost:5173
2. **Select:**
   - Tonic: C
   - Mode: Ionian
   - CF Voice: Alto
   - **Number of Voices: 2** ← Default
   - Length: 8
3. **Click** "Generate CF"
4. **Expected:** 
   - CF notes appear (e.g., C4, D4, E4...)
   - Musical notation shows 1 staff
5. **Click** "Generate Counterpoint"
6. **Expected:**
   - Counterpoint notes appear
   - Musical notation shows 2 staves
   - Violations list appears (if any)
7. **Click** "Play"
8. **Expected:**
   - Hear both voices playing together
   - Tempo slider works (40-200 BPM)

**Status:** ✅ Should work (existing functionality)

---

### Test 2: 3-Voice Mode

1. **Refresh** page or click "Generate CF" again
2. **Select:**
   - Tonic: C
   - Mode: Ionian
   - CF Voice: Alto
   - **Number of Voices: 3** ← NEW
   - Length: 8
   - Seed: 42 (optional, for reproducibility)
3. **Click** "Generate CF"
4. **Expected:**
   - CF notes appear
5. **Click** "Generate Counterpoint"
6. **Expected:**
   - **3 voice lines appear** (Voice 1, Voice 2, Voice 3)
   - **Musical notation shows 3 staves**
   - Each staff has proper clef (treble/bass)
   - All staves aligned vertically
7. **Click** "Play"
8. **Expected:**
   - **Hear all 3 voices playing together**
   - Rich harmony
   - No violations list (multi-voice evaluation not yet implemented)

**Status:** ✅ Should work (NEW feature)

---

### Test 3: 4-Voice Mode (SATB)

1. **Refresh** page
2. **Select:**
   - Tonic: C
   - Mode: Ionian
   - CF Voice: Tenor (works best for 4-voice)
   - **Number of Voices: 4** ← NEW
   - Length: 8
   - Seed: 100 (recommended for 4-voice)
3. **Click** "Generate CF"
4. **Expected:**
   - CF notes appear in tenor range
5. **Click** "Generate Counterpoint"
   - **Note:** May take 1-2 seconds (more complex)
6. **Expected:**
   - **4 voice lines appear** (Voice 1-4)
   - **Musical notation shows 4 staves** (SATB layout)
   - Soprano: Treble clef (top)
   - Alto: Treble clef
   - Tenor: Treble or Bass clef
   - Bass: Bass clef (bottom)
7. **Click** "Play"
8. **Expected:**
   - **Hear full 4-part harmony**
   - Rich, complete sound
   - All voices balanced

**Status:** ✅ Should work (NEW feature)

---

### Test 4: Different Keys and Modes

Try generating 3-voice counterpoint in:

**Test 4a: G Major**
- Tonic: G (7)
- Mode: Ionian
- Voices: 3
- **Expected:** Key signature shows 1 sharp (F#)

**Test 4b: D Dorian**
- Tonic: D (2)
- Mode: Dorian
- Voices: 3
- **Expected:** Key signature shows 1 flat (Bb)

**Test 4c: A Aeolian (Natural Minor)**
- Tonic: A (9)
- Mode: Aeolian
- Voices: 4
- **Expected:** No sharps/flats in key signature

**Status:** ✅ Should work

---

### Test 5: Reproducibility

1. **Generate** 3-voice with seed 42
2. **Note** the MIDI values
3. **Refresh** page
4. **Generate** 3-voice with seed 42 again
5. **Expected:** Exact same notes

**Status:** ✅ Should work

---

### Test 6: Switching Between Voice Counts

1. **Generate** CF (any settings)
2. **Select** 2 voices → Generate Counterpoint
3. **Expected:** 2 staves, violations shown
4. **Select** 3 voices → Generate Counterpoint again
5. **Expected:** 3 staves, no violations (not evaluated)
6. **Select** 4 voices → Generate Counterpoint again
7. **Expected:** 4 staves

**Status:** ✅ Should work

---

## What You Should See

### Visual Elements

**Voice Count Selector:**
```
Number of Voices:
○ 2 voices  ○ 3 voices  ○ 4 voices
```

**2-Voice Display:**
```
Musical Notation
[Two staves with notes]

Cantus Firmus
C4 D4 E4 F4 G4 A4 B4 C5
MIDI: [60, 62, 64, 65, 67, 69, 71, 72]

Counterpoint
G4 A4 B4 C5 D5 E5 F5 G5
MIDI: [67, 69, 71, 72, 74, 76, 77, 79]

Rule Violations (if any)
```

**3-Voice Display:**
```
Musical Notation
[Three staves with notes]

Voice 1
C4 D4 E4 F4 G4 A4 B4 C5
MIDI: [60, 62, 64, 65, 67, 69, 71, 72]

Voice 2
E4 F4 G4 A4 B4 C5 D5 E5
MIDI: [64, 65, 67, 69, 71, 72, 74, 76]

Voice 3
G3 A3 C4 C4 D4 E4 G4 G4
MIDI: [55, 57, 60, 60, 62, 64, 67, 67]
```

**4-Voice Display:**
```
Musical Notation
[Four staves with notes - SATB layout]

Voice 1 (Soprano)
Voice 2 (Alto)
Voice 3 (Tenor/CF)
Voice 4 (Bass)
```

---

## Audio Expectations

### 2 Voices
- Clear two-part harmony
- Can distinguish both lines

### 3 Voices
- Richer harmony
- Fuller sound
- Three distinct lines

### 4 Voices
- Full SATB harmony
- Complete, rich sound
- Four distinct lines
- Sounds like a choir

---

## Known Limitations

### What Doesn't Work Yet

❌ **Multi-voice violation detection**
- 3-4 voice counterpoint doesn't show violations
- Only 2-voice shows violations

❌ **Per-voice mute toggles**
- Can't mute individual voices
- All voices play together

❌ **Volume control**
- No volume slider yet

❌ **Voice labels**
- Doesn't show "Soprano", "Alto", etc.
- Just shows "Voice 1", "Voice 2"

### Generation Failures

**If generation fails:**
- Try different seed
- Try shorter CF (6-8 notes)
- 4-voice is harder, may need multiple attempts
- Check console for errors

---

## Troubleshooting

### Issue: "Failed to generate counterpoint"

**For 4-voice:**
- This is normal, 4-voice is complex
- Try seed: 100, 200, or 300
- Try different CF voice (Tenor works best)
- Try shorter length (6-8 notes)

**Solution:** Click "Generate Counterpoint" again

### Issue: No sound when playing

**Solution:**
1. Check system volume
2. Click Play again (browser may block first attempt)
3. Check browser console for errors
4. Try refreshing page

### Issue: Notation looks wrong

**Solution:**
1. Check that CF was generated first
2. Refresh page (Cmd+Shift+R)
3. Check browser console for VexFlow errors

### Issue: Voice count selector disabled

**Solution:**
- Wait for generation to complete
- Selector is disabled during loading

---

## Backend API Testing

### Test API Directly

```bash
# Generate 3-voice
curl -X POST http://localhost:8000/api/generate-multi-voice \
  -H "Content-Type: application/json" \
  -d '{
    "tonic": 0,
    "mode": "ionian",
    "cf_notes": [60, 62, 64, 65, 67, 69, 71, 72],
    "cf_voice_range": "alto",
    "num_voices": 3,
    "seed": 42
  }'
```

**Expected Response:**
```json
{
  "voices": [
    {
      "voice_index": 0,
      "voice_range": "alto",
      "notes": [{"midi": 60, "duration": "whole"}, ...]
    },
    {
      "voice_index": 1,
      "voice_range": "soprano",
      "notes": [...]
    },
    {
      "voice_index": 2,
      "voice_range": "tenor",
      "notes": [...]
    }
  ],
  "num_voices": 3
}
```

### API Documentation

Visit: http://localhost:8000/docs

Look for: `POST /api/generate-multi-voice`

---

## Success Criteria

### ✅ Phase 13 is working if:

1. Voice count selector appears and works
2. Can generate 2, 3, and 4 voice counterpoint
3. Notation displays correct number of staves
4. All voices play simultaneously
5. Different clefs assigned automatically
6. No console errors
7. Build completes without TypeScript errors

---

## Next Steps After Testing

If everything works:
- ✅ Phase 13 Complete!
- Ready for Phase 14 (Second Species)
- Or add polish features (mute toggles, volume)

If issues found:
- Check browser console
- Check backend logs
- Report specific error messages

---

**Last Updated:** December 2024
