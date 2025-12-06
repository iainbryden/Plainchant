Here’s a concrete, end-to-end task list to build your **species counterpoint generator** with:

* **Python API backend (in a venv)**
* **React frontend UI**
* **2–4 voices, random or user-entered melody**
* **Rule-based generation + evaluation**
* **Notation display + audio playback**
* **Tempo + per-voice mute**

I’ll assume “classical Fux-style species counterpoint in 2–4 voices” and diatonic pitch only (no microtones).

---

## 1. Plan the architecture & data model

**1.1. Decide on overall architecture**

* Frontend: React app (Vite or CRA) talking to a REST API.
* Backend: Python (FastAPI is a great fit, Flask also fine).
* Communication format: JSON (for melodies, rules, errors, etc.).
* Audio & notation handled in the browser.

**1.2. Core musical abstractions**

Define these as Python classes / types:

* `Pitch` (e.g., MIDI number or pitch class + octave, plus spelling info).
* `Scale` and `Mode` (Ionian, Dorian, etc.).
* `Key` (tonic + mode).
* `Duration` (whole, half, quarter, etc. – you can restrict to simple values).
* `Note` (`pitch`, `duration`, maybe `accent` / `tie` later).
* `VoiceLine` = ordered list of `Note`s with metadata:

  * voice index
  * range (e.g., soprano/alto/tenor/bass)
* `SpeciesType` enum: FIRST, SECOND, THIRD, FOURTH, FIFTH (florid).
* `CounterpointProblem`:

  * `key`
  * `cantus_firmus` (required)
  * `num_voices`
  * `species_per_voice` (could be same or mixed)
* `CounterpointSolution`:

  * list of `VoiceLine`s
  * diagnostics (warnings, rule violations, etc.)

---

## 2. Set up the Python backend & venv

**2.1. Create the project**

* Create a folder `species_counterpoint_app`.
* Create `backend/` and `frontend/` subfolders.

**2.2. Create and activate a virtual environment**

* `python -m venv .venv`
* Activate it (`source .venv/bin/activate` or `.\.venv\Scripts\activate` on Windows).

**2.3. Install backend dependencies**

At minimum:

* Web framework: `fastapi`, `uvicorn[standard]`
* Data modeling / validation: `pydantic`
* For audio generation later (optional): `mido` or direct MIDI writing, or just return pitch/duration and let frontend handle sound.

Example:

```bash
pip install fastapi uvicorn pydantic
```

(You can add testing libs later: `pytest`, etc.)

**2.4. Create basic FastAPI structure**

* `backend/app/main.py`
* Define a simple health check endpoint (`/health`) to verify everything works.
* Run with `uvicorn app.main:app --reload`.

---

## 3. Implement the counterpoint rule engine

This is the heart of the system. You’ll want a *clean, testable* layer independent of FastAPI.

### 3.1. Represent intervals & consonance/dissonance

* Implement interval calculations:

  * `interval_size = abs(pitch2 - pitch1)` in semitones.
  * Map to scale degrees / generic intervals (2nd, 3rd, 4th, 5th, 6th, 7th, 8ve).
* Implement categorization:

  * Perfect consonances: unison, 5th, octave.
  * Imperfect consonances: 3rds, 6ths.
  * Dissonances: 2nds, 7ths, augmented/diminished intervals, etc.
* Add helpers:

  * `is_consonant(interval)`
  * `is_perfect_consonance(interval)`
  * `is_dissonant(interval)`

### 3.2. Species-independent melodic rules (per voice)

Implement reusable melodic checks:

* **Range**: each voice stays within a defined range (e.g., soprano C4–G5).
* **Leaps**:

  * Max leap: usually ≤ octave; prefer ≤ 5th.
  * Large leaps followed by stepwise motion in opposite direction.
* **Step preference**: mostly stepwise motion, leaps used sparingly.
* **No augmented seconds** in diatonic context (unless style allows).
* **No repeated notes** (or restrict them).
* **Melodic high point**: one clear climax (optional for v1).
* **Begin & end** on stable degrees (tonic, sometimes dominant).

Design as functions:

```python
def check_melodic_leaps(voice_line) -> list[RuleViolation]:
    ...

def check_range(voice_line, min_pitch, max_pitch) -> list[RuleViolation]:
    ...
```

### 3.3. Species-independent harmonic rules (between voices)

* No **parallel perfect 5ths or octaves**.
* No **hidden (direct) fifths/octaves**: outer voices move in similar motion to a perfect consonance with leap in the upper voice.
* No **voice crossing** (e.g., alto goes above soprano).
* Avoid excessive **voice overlap** (a voice goes into another’s previous range).
* Maintain reasonable spacing between adjacent voices.

Again, implement as functions:

```python
def check_parallels(voices) -> list[RuleViolation]:
    ...

def check_voice_crossings(voices) -> list[RuleViolation]:
    ...
```

### 3.4. Species-specific harmonic / rhythmic rules

For each species, implement rules that apply to *relationships to the cantus firmus at each beat*.

#### First species (note-against-note)

* Every note in counterpoint is a **consonance** against cantus.
* Start & end in perfect consonance.
* Penultimate bar: approach final by step (usually leading tone to tonic).
* No dissonances at all.

Rules:

```python
def check_first_species(voices, cantus_index) -> list[RuleViolation]:
    ...
```

#### Second species (two notes against one)

* Two half-notes per cantus note (in 4/2 context).
* **Strong beat (downbeat)**: must be consonant.
* **Weak beat (upbeat)**: may be consonant or dissonant.
* Dissonances only **as passing tones** between consonances, stepwise motion.
* Still avoid parallels between strong beats and also across beats where applicable.

#### Third species (four notes against one)

* Four quarter-notes per cantus note.
* Dissonance allowed only as passing tones or neighbor tones, in stepwise motion.
* Beat hierarchy: 1 and 3 often treated more strictly (more likely consonant).

#### Fourth species (syncopation / suspensions)

* Tied notes across the bar (or half notes tied).
* Dissonances most often occur as **suspensions**:

  * Preparation (consonance), suspension (dissonance on strong beat), resolution (stepwise down).
* Implement detection of valid suspensions vs “bad” dissonances.

#### Fifth species (florid)

* Combination of previous species:

  * Mix of whole, half, quarter notes.
  * Dissonance use must conform to passing, neighbor, suspension patterns.
* Use all melodic and harmonic rules, with extra attention to rhythmic shaping.

Each species function can use the generic melodic & harmonic checkers and add its own.

### 3.5. Multi-voice interaction (3–4 voices)

Extend 2-voice rules to N voices:

* For each pair of voices, run:

  * parallel checks
  * crossing / overlap checks
* Keep track of vertical sonorities:

  * At each time slice, label chord quality (rough, but enough to ensure consonant verticals when required).
* Additional constraints:

  * Avoid having more than two perfect intervals at once (e.g., no double octaves across 3+ voices when possible).
  * Keep each voice independently singable (apply melodic rules per voice).

---

## 4. Build the generation engine

You want a **rule-constrained search** generator that can:

* Generate a cantus firmus (optional; or user provides).
* Generate counterpoint lines for 1–3 additional voices.
* Handle randomization (so compositions are not identical).

### 4.1. Choose generation approach

* Backtracking search:

  * Build voices note-by-note.
  * At each step:

    * Generate candidate notes (in key, appropriate range, plausible step/leap).
    * Apply local melodic rules.
    * Apply local harmonic rules with cantus and previously built voices.
  * If no candidate works, backtrack.
* Add randomness:

  * Shuffle candidate notes at each step for variation.
  * Optionally use scoring (soft constraints) rather than all hard-fail.

### 4.2. Implement candidate generation

For each voice and each cantus note:

* Get all pitches in an acceptable range.
* Filter by:

  * allowed interval to cantus for the species at that beat.
  * allowed motion from previous note (step/leap).
* For species >1, generate subdivisions (two or four notes) with patterns like:

  * stepwise passing
  * small leaps with stepwise recovery
  * suspension patterns in 4th species.

### 4.3. Implement search orchestration

* `generate_counterpoint(problem: CounterpointProblem) -> CounterpointSolution`

  * Handle species per voice.
  * Build voices in order (e.g., from cantus, then closest voice, etc.).
  * Provide a “max attempts / depth” to avoid infinite loops.

---

## 5. Implement melody evaluation (user-entered)

You also want to evaluate a user melody against the rules.

**5.1. Define an evaluation function**

* `evaluate_melody(melody: VoiceLine, key, role: 'cantus'|'counterpoint', species=None) -> EvaluationResult`

  * Check melodic rules.
  * If role is `counterpoint`, also check intervals vs cantus.
  * `EvaluationResult` includes:

    * `score` (0–100)
    * `errors`: list of violations with:

      * rule name
      * description
      * index/time of mistake
      * severity

**5.2. Integrate with API**

* Endpoint: `POST /evaluate-melody`

  * Input:

    * melody notes
    * key
    * role
    * species (if counterpoint)
  * Output:

    * `EvaluationResult` JSON.

---

## 6. Design the REST API

Define endpoints to support all required workflows.

### 6.1. Endpoints

1. `GET /health`

   * Simple status check.

2. `POST /generate-melody`

   * Generate cantus firmus (or generic melody).
   * Body:

     * `key`
     * `length` (number of measures or notes)
     * `voice_range` (e.g., soprano).
   * Response:

     * `melody` as list of `{pitch, duration}`.

3. `POST /generate-counterpoint`

   * Generate full species counterpoint.
   * Body:

     * `key`
     * `cantus_firmus` (array of notes)
     * `num_voices` (2–4)
     * `species_per_voice` (array of species strings)
   * Response:

     * `voices` (array of VoiceLines)
     * diagnostic info

4. `POST /evaluate-melody`

   * As above.

5. (Optional) `POST /export-midi` or just return a structured representation that the frontend can map to Tone.js or Web Audio events.

### 6.2. JSON schemas

Use Pydantic models:

* `NoteModel` (`pitch`, `duration`, `start_time` or `index`).
* `VoiceLineModel` (list of `NoteModel`).
* `GenerateCounterpointRequest`, `GenerateCounterpointResponse`, etc.

---

## 7. Build the React frontend

### 7.1. Scaffold the app

* Use `npm create vite@latest` or `npx create-react-app`.
* Configure proxy or env var for API base URL.

### 7.2. Choose libraries for notation & audio

* **Notation**: something like VexFlow (JS library for rendering music notation to canvas/SVG).
* **Audio**:

  * Tone.js for scheduling notes and playing a simple synth.
  * Or Web Audio API manually (Tone.js is easier).

(Your frontend can convert pitch numbers to scientific pitch notation + durations that these libs expect.)

### 7.3. Core UI layout

Create main components:

* `CounterpointControls`

  * Key selector (key + mode).
  * Number of voices (2–4).
  * Species selector per voice.
  * Tempo slider / input.
* `MelodyInput`

  * Toggle: “Random melody” vs “User-entered melody”.
  * For user-entered:

    * Maybe a simple piano roll or staff editor, or a grid of steps/pitches.
* `ScoreView`

  * Uses notation library to render staff with 2–4 staves.
  * Multi-voice support (each staff or voices on shared staves).
* `PlaybackControls`

  * Play / Pause / Stop.
  * Tempo slider.
  * Per-voice mute toggles (check boxes, etc.).

### 7.4. API integration

Implement service functions:

* `apiGenerateMelody(params)`
* `apiGenerateCounterpoint(params)`
* `apiEvaluateMelody(melody, params)`

Wire them to UI events:

* “Randomize Melody” button:

  * Calls `/generate-melody`, stores result as cantus.
* “Generate Counterpoint” button:

  * Sends cantus + parameters to `/generate-counterpoint`.
  * Stores result as array of voices, updates the score view.
* “Evaluate Melody” button:

  * Sends current user melody (and maybe CF) to `/evaluate-melody`.
  * Shows rule violations in a panel (maybe highlight offending notes in red).

### 7.5. Playback logic

Implement a playback engine in React:

* Convert all voices into a timeline:

  * For each note, compute absolute start time and duration in beats.
* Use tempo (BPM) to compute seconds (`sec = beats * 60 / BPM`).
* For each note, schedule playback using Tone.js:

  * Respect per-voice mute flags (don’t schedule notes from muted voices).
* Provide controls:

  * Start/Stop changes a `isPlaying` state and handles unscheduling/rescheduling.
  * Tempo changes will adjust future scheduling; simplest is to stop and replay with new tempo.

---

## 8. Rule visualization & feedback

You want to make the system educational and debuggable.

**8.1. Represent rule violations**

* Each `RuleViolation` has:

  * `rule_code` (e.g., `PARALLEL_PERFECT_FIFTH`)
  * `description`
  * `voice_indices` affected
  * note indices or time positions
  * severity (`warning`, `error`)

**8.2. Frontend display**

* Create a `RuleViolationsPanel` that lists errors per voice, with:

  * Filter by voice.
  * Clicking an error highlights the relevant notes in notation view.

**8.3. Generation logging (optional)**

* For debugging: API can optionally return a “trace” of decisions.
* Not required for first version, but helpful if the generator gets stuck.

---

## 9. Environment, packaging & dev tooling

**9.1. Development scripts**

* Backend:

  * `python -m uvicorn app.main:app --reload`
* Frontend:

  * `npm run dev` (or equivalent).

**9.2. Cross-origin / proxy**

* Configure CORS in FastAPI to allow requests from your React dev server.
* Or set up a dev proxy in Vite/CRA to forward `/api` requests.

**9.3. Testing**

Back-end tests:

* Unit tests for:

  * interval calculations
  * melodic rules
  * harmonic rules
  * species-specific logic
* Integration tests for:

  * `generate_counterpoint` for simple configurations (e.g., 2 voices, first species).

Front-end tests (optional initially):

* Snapshot / component tests for critical UI pieces.
* Manual testing for playback & interactions at first.

---

## 10. Incremental implementation plan

To make this practical, here’s a good step-by-step roadmap:

1. **Set up backend skeleton** (venv, FastAPI, basic models).
2. **Implement pitch, interval, key, and simple melodic rules.**
3. **Implement 2-voice, first species only**:

   * Rule checks
   * Simple backtracking generator
   * Basic `POST /generate-counterpoint`.
4. **Set up React app**:

   * Call `/generate-counterpoint`.
   * Display notes simply (even as text at first).
5. **Add notation rendering & basic playback.**
6. **Add other species (2nd, 3rd, 4th, 5th)** with rule sets.
7. **Add multi-voice (3–4 voices) support** to rule engine and generator.
8. **Add user-entered melody editor + `/evaluate-melody`** endpoint.
9. **Add UI polish**:

   * Tempo control.
   * Per-voice mute.
   * Rule violation highlighting.
10. **Refine rule set** and expand key/mode support, additional stylistic nuances.

