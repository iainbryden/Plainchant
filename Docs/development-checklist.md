# Species Counterpoint Generator - Development Checklist

## Tech Stack & Architecture

### Recommended Technologies
- **Backend**: Python with FastAPI (async, modern, excellent type hints)
- **Frontend**: React with Vite (fast development, modern tooling)
- **Notation**: VexFlow (mature music notation library)
- **Audio**: Tone.js (Web Audio wrapper, excellent scheduling)
- **State Management**: React Context or Zustand (lightweight)
- **API Communication**: Axios or Fetch API
- **Testing**: pytest (backend), Vitest/React Testing Library (frontend)
- **Type Safety**: Pydantic (backend), TypeScript (frontend)

---

## Phase 1: Foundation & Core Data Models ✅ COMPLETE

### Backend Setup
- [x] **1.1.1** Create project structure (`backend/`, `frontend/`, `docs/`)
- [x] **1.1.2** Set up Python virtual environment (`.venv`)
- [x] **1.1.3** Install core dependencies (`fastapi`, `uvicorn`, `pydantic`)
- [x] **1.1.4** Create `backend/app/main.py` with basic FastAPI app
- [x] **1.1.5** Implement `/health` endpoint
- [x] **1.1.6** Configure CORS for local development

**Test Criteria**: ✅ Run `uvicorn app.main:app --reload` and verify `/health` returns 200

### Core Data Models
- [x] **1.2.1** Define `Pitch` class (MIDI number, pitch class, octave, spelling)
- [x] **1.2.2** Define `Scale` and `Mode` enums (Ionian, Dorian, Phrygian, etc.)
- [x] **1.2.3** Define `Key` model (tonic + mode)
- [x] **1.2.4** Define `Duration` enum (whole, half, quarter notes)
- [x] **1.2.5** Define `Note` model (pitch, duration, optional accent/tie)
- [x] **1.2.6** Define `VoiceLine` model (notes list, voice index, range metadata)
- [x] **1.2.7** Define `SpeciesType` enum (FIRST, SECOND, THIRD, FOURTH, FIFTH)
- [x] **1.2.8** Define `VoiceRange` enum/model (SOPRANO, ALTO, TENOR, BASS with pitch ranges)
- [x] **1.2.9** Define `CounterpointProblem` model (key, cantus_firmus, num_voices, species_per_voice)
- [x] **1.2.10** Define `CounterpointSolution` model (voice_lines, diagnostics)
- [x] **1.2.11** Define `RuleViolation` model (rule_code, description, voice_indices, note_indices, severity)

**Test Criteria**: ✅ Unit tests for model instantiation and validation with valid/invalid data

---

## Phase 2: Musical Theory Engine ✅ COMPLETE

### Interval & Consonance System
- [x] **2.1.1** Implement `calculate_interval(pitch1, pitch2)` (semitone distance)
- [x] **2.1.2** Implement `interval_to_scale_degree(interval, key)` mapping
- [x] **2.1.3** Implement `is_perfect_consonance(interval)` (P1, P5, P8)
- [x] **2.1.4** Implement `is_imperfect_consonance(interval)` (M3, m3, M6, m6)
- [x] **2.1.5** Implement `is_consonant(interval)` (perfect OR imperfect)
- [x] **2.1.6** Implement `is_dissonant(interval)`
- [x] **2.1.7** Handle special case: 4th above bass is dissonant

**Test Criteria**: ✅ Unit tests covering all interval types and edge cases (octave wraparound, enharmonics)

### Motion Detection
- [x] **2.2.1** Implement `motion_type(prev_p1, curr_p1, prev_p2, curr_p2)`
- [x] **2.2.2** Detect PARALLEL motion (same direction, same interval)
- [x] **2.2.3** Detect SIMILAR motion (same direction, different interval)
- [x] **2.2.4** Detect CONTRARY motion (opposite directions)
- [x] **2.2.5** Detect OBLIQUE motion (one voice static)

**Test Criteria**: ✅ Unit tests for all motion types with various pitch combinations

---

## Phase 3: Melodic Rules Engine ✅ COMPLETE

### Per-Voice Melodic Constraints
- [x] **3.1.1** Implement `check_range(voice_line, voice_range)` constraint
- [x] **3.1.2** Implement `check_leap_size(voice_line)` (max octave, prefer ≤5th)
- [x] **3.1.3** Implement `check_leap_compensation(voice_line)` (large leap → opposite step)
- [x] **3.1.4** Implement `check_step_preference(voice_line)` (≥60-70% stepwise)
- [x] **3.1.5** Implement `check_repeated_notes(voice_line)` (avoid long repetitions)
- [x] **3.1.6** Implement `check_melodic_climax(voice_line)` (single highest point)
- [x] **3.1.7** Implement `check_no_augmented_intervals(voice_line)` (no aug 2nd, etc.)
- [x] **3.1.8** Implement `check_no_melodic_tritones(voice_line)`
- [x] **3.1.9** Implement `check_start_end_degrees(voice_line, key)` (stable tonic)

**Test Criteria**: ✅ Create test melodies with known violations, verify detection accuracy

---

## Phase 4: Harmonic Rules Engine (2-Voice) ✅ COMPLETE

### Voice Interaction Constraints
- [x] **4.1.1** Implement `check_parallel_perfects(voice1, voice2)` (P5, P8)
- [x] **4.1.2** Implement `check_hidden_perfects(bass, soprano)` (similar motion + leap)
- [x] **4.1.3** Implement `check_voice_crossing(voices)`
- [x] **4.1.4** Implement `check_voice_overlap(voices)`
- [x] **4.1.5** Implement `check_spacing(voices)` (reasonable intervals between adjacent voices)

**Test Criteria**: ✅ Create 2-voice examples with each violation type, verify detection

---

## Phase 5: Species-Specific Rules (First Species Only) ✓ Testable

### First Species Implementation
- [ ] **5.1.1** Implement `check_first_species_consonances(cantus, counterpoint)` (all consonant)
- [ ] **5.1.2** Implement `check_first_species_start(cantus, counterpoint)` (P1, P5, P8)
- [ ] **5.1.3** Implement `check_first_species_end(cantus, counterpoint)` (P1 or P8)
- [ ] **5.1.4** Implement `check_first_species_penultimate(cantus, counterpoint)` (6-8 or 3-1)
- [ ] **5.1.5** Create `FirstSpeciesValidator` class combining all checks
- [ ] **5.1.6** Implement `evaluate_first_species(problem)` → list of violations

**Test Criteria**: Test with valid and invalid first species examples from Fux

---

## Phase 6: Cantus Firmus Generator ✓ Testable

### CF Generation
- [ ] **6.1.1** Implement `generate_cf_candidates(key, length, voice_range)`
- [ ] **6.1.2** Apply CF-specific melodic rules (mostly stepwise, single climax)
- [ ] **6.1.3** Implement `score_cf_quality(cf)` (prefer smooth contours)
- [ ] **6.1.4** Implement backtracking for CF generation
- [ ] **6.1.5** Add randomization (seed-based for reproducibility)
- [ ] **6.1.6** Handle timeout/max attempts (fail gracefully)

**Test Criteria**: Generate 50 CFs in various keys/modes, verify all pass CF rules

---

## Phase 7: First Species Counterpoint Generator ✓ Testable

### 2-Voice Generator (First Species)
- [ ] **7.1.1** Implement `generate_candidates(current_state, cf_note, species)`
- [ ] **7.1.2** Filter candidates by range constraints
- [ ] **7.1.3** Filter by melodic rules (step/leap from previous)
- [ ] **7.1.4** Filter by vertical consonance with CF
- [ ] **7.1.5** Filter by parallel/hidden perfect checks
- [ ] **7.1.6** Implement backtracking search algorithm
- [ ] **7.1.7** Add randomization to candidate order
- [ ] **7.1.8** Implement cadence forcing (last 2 measures)
- [ ] **7.1.9** Create `generate_first_species(problem)` main function

**Test Criteria**: Generate 20 first species examples, manually verify quality and rule compliance

---

## Phase 8: REST API - First Species Only ✓ Testable

### API Endpoints (Minimal Viable)
- [ ] **8.1.1** Implement Pydantic request/response models for all endpoints
- [ ] **8.1.2** Endpoint: `POST /generate-cantus-firmus` (key, length, voice_range)
- [ ] **8.1.3** Endpoint: `POST /generate-counterpoint` (first species only)
- [ ] **8.1.4** Endpoint: `POST /evaluate-counterpoint` (return violations)
- [ ] **8.1.5** Add error handling and validation
- [ ] **8.1.6** Add request logging
- [ ] **8.1.7** Create API documentation (auto-generated by FastAPI)

**Test Criteria**: Use Postman/curl to test all endpoints, verify JSON schemas

---

## Phase 9: Frontend Foundation ✓ Testable

### React App Setup
- [ ] **9.1.1** Scaffold React app with Vite + TypeScript
- [ ] **9.1.2** Configure API base URL (environment variables)
- [ ] **9.1.3** Set up project structure (`components/`, `services/`, `types/`, `utils/`)
- [ ] **9.1.4** Install dependencies (axios, tone.js, vexflow)
- [ ] **9.1.5** Create TypeScript interfaces matching backend models
- [ ] **9.1.6** Set up basic routing (if needed)

**Test Criteria**: Run `npm run dev`, verify app loads without errors

### API Service Layer
- [ ] **9.2.1** Create `apiClient.ts` (axios configuration)
- [ ] **9.2.2** Implement `generateCantusFirmus(params)`
- [ ] **9.2.3** Implement `generateCounterpoint(params)`
- [ ] **9.2.4** Implement `evaluateCounterpoint(params)`
- [ ] **9.2.5** Add error handling and loading states

**Test Criteria**: Mock API calls in dev, verify data flow

---

## Phase 10: Basic UI (First Species) ✓ Testable

### Control Panel Components
- [ ] **10.1.1** Create `KeySelector` component (key + mode dropdowns)
- [ ] **10.1.2** Create `VoiceRangeSelector` (SATB radio buttons)
- [ ] **10.1.3** Create `CantusFirmusControls` (generate button, length input)
- [ ] **10.1.4** Create `CounterpointControls` (generate button, species selector)
- [ ] **10.1.5** Wire up state management (Context or Zustand)
- [ ] **10.1.6** Connect controls to API calls

**Test Criteria**: Click buttons, verify API calls in network tab

### Display Components (Simple)
- [ ] **10.2.1** Create `NoteList` component (simple text display of notes)
- [ ] **10.2.2** Create `ViolationsList` component (display rule violations)
- [ ] **10.2.3** Add loading spinners
- [ ] **10.2.4** Add error messages display

**Test Criteria**: Generate counterpoint, see notes and violations displayed

---

## Phase 11: Music Notation Rendering ✓ Testable

### VexFlow Integration
- [ ] **11.1.1** Create `ScoreRenderer` component wrapper for VexFlow
- [ ] **11.1.2** Convert internal note format to VexFlow format
- [ ] **11.1.3** Render single staff (treble clef)
- [ ] **11.1.4** Render two staves (treble + bass or two treble)
- [ ] **11.1.5** Handle clef selection based on voice range
- [ ] **11.1.6** Add bar lines and time signature
- [ ] **11.1.7** Add key signature rendering
- [ ] **11.1.8** Handle note accidentals properly
- [ ] **11.1.9** Add responsive sizing

**Test Criteria**: Render generated counterpoint, verify notes are positioned correctly

### Notation Enhancement
- [ ] **11.2.1** Highlight notes with violations (red color)
- [ ] **11.2.2** Add click handlers for note selection
- [ ] **11.2.3** Display measure numbers
- [ ] **11.2.4** Add zoom controls

**Test Criteria**: Generate counterpoint with violations, verify highlighting

---

## Phase 12: Audio Playback (Basic) ✓ Testable

### Tone.js Integration
- [ ] **12.1.1** Initialize Tone.js synth (simple instrument)
- [ ] **12.1.2** Convert pitch numbers to note names (e.g., 60 → C4)
- [ ] **12.1.3** Create `PlaybackEngine` class
- [ ] **12.1.4** Implement `scheduleNotes(voices, tempo)`
- [ ] **12.1.5** Create `PlaybackControls` component (play/pause/stop buttons)
- [ ] **12.1.6** Implement play functionality
- [ ] **12.1.7** Implement pause/resume functionality
- [ ] **12.1.8** Implement stop functionality
- [ ] **12.1.9** Add visual playback cursor on notation

**Test Criteria**: Play generated counterpoint, verify timing and pitch accuracy

### Playback Features
- [ ] **12.2.1** Create `TempoSlider` component (40-200 BPM)
- [ ] **12.2.2** Update playback speed in real-time (stop/restart)
- [ ] **12.2.3** Create per-voice mute toggles
- [ ] **12.2.4** Update synth to respect mute states
- [ ] **12.2.5** Add volume control

**Test Criteria**: Test all playback controls, verify behavior

---

## Phase 13: Multi-Voice Support (3-4 Voices) ✓ Testable

### Backend Multi-Voice Rules
- [ ] **13.1.1** Extend `check_parallel_perfects()` for N voices (pairwise)
- [ ] **13.1.2** Extend `check_voice_crossing()` for N voices
- [ ] **13.1.3** Extend `check_spacing()` for adjacent voice pairs
- [ ] **13.1.4** Implement `check_vertical_sonority(chord)` (all vs bass)
- [ ] **13.1.5** Update first species validator for multi-voice

**Test Criteria**: Create 3 and 4 voice examples, test rule detection

### Multi-Voice Generator
- [ ] **13.2.1** Update candidate generation for multiple voices
- [ ] **13.2.2** Optimize voice generation order (closest to CF first)
- [ ] **13.2.3** Update backtracking for N voices
- [ ] **13.2.4** Test 3-voice generation
- [ ] **13.2.5** Test 4-voice generation

**Test Criteria**: Generate multiple 3 and 4 voice examples successfully

### Frontend Multi-Voice
- [ ] **13.3.1** Update UI to show 2-4 voice selector
- [ ] **13.3.2** Update notation renderer for 4 staves
- [ ] **13.3.3** Handle SATB clef assignment automatically
- [ ] **13.3.4** Update playback for 4 voices
- [ ] **13.3.5** Add individual volume per voice

**Test Criteria**: Generate and render 4-voice counterpoint with playback

---

## Phase 14: Second Species Implementation ✓ Testable

### Second Species Rules
- [ ] **14.1.1** Implement beat subdivision logic (2 notes per CF note)
- [ ] **14.1.2** Implement `check_strong_beat_consonance(voice, cf, beat_index)`
- [ ] **14.1.3** Implement `check_weak_beat_dissonance(voice, cf, beat_index)`
- [ ] **14.1.4** Implement passing tone detection (stepwise approach/leave)
- [ ] **14.1.5** Implement neighbor tone detection
- [ ] **14.1.6** Create `SecondSpeciesValidator` class

**Test Criteria**: Test with valid second species examples, verify rules

### Second Species Generator
- [ ] **14.2.1** Implement 2-note candidate generation per CF note
- [ ] **14.2.2** Apply strong beat consonance constraints
- [ ] **14.2.3** Apply weak beat passing tone patterns
- [ ] **14.2.4** Update backtracking for 2:1 rhythm
- [ ] **14.2.5** Add second species option to API

**Test Criteria**: Generate 10 second species examples, verify quality

---

## Phase 15: Third Species Implementation ✓ Testable

### Third Species Rules
- [ ] **15.1.1** Implement beat subdivision logic (4 notes per CF note)
- [ ] **15.1.2** Implement beat hierarchy (beats 1,3 strong; 2,4 weak)
- [ ] **15.1.3** Extend passing/neighbor tone detection for 4:1
- [ ] **15.1.4** Implement double passing tone validation
- [ ] **15.1.5** Create `ThirdSpeciesValidator` class

**Test Criteria**: Test with valid third species examples

### Third Species Generator
- [ ] **15.2.1** Implement 4-note candidate generation per CF note
- [ ] **15.2.2** Apply beat hierarchy constraints
- [ ] **15.2.3** Generate scalar runs (controlled)
- [ ] **15.2.4** Update backtracking for 4:1 rhythm
- [ ] **15.2.5** Add third species option to API

**Test Criteria**: Generate third species examples, verify rhythmic variety

---

## Phase 16: Fourth Species Implementation ✓ Testable

### Fourth Species Rules (Suspensions)
- [ ] **16.1.1** Implement suspension pattern detection (prep-sus-res)
- [ ] **16.1.2** Implement `check_suspension_preparation(voice, index)`
- [ ] **16.1.3** Implement `check_suspension_dissonance(voice, cf, index)`
- [ ] **16.1.4** Implement `check_suspension_resolution(voice, index)` (stepwise down)
- [ ] **16.1.5** Implement suspension types (4-3, 7-6, 9-8, 2-3)
- [ ] **16.1.6** Create `FourthSpeciesValidator` class

**Test Criteria**: Test suspension chains, verify prep-sus-res patterns

### Fourth Species Generator
- [ ] **16.2.1** Implement tied note generation
- [ ] **16.2.2** Generate valid suspension patterns
- [ ] **16.2.3** Apply preparation consonance constraint
- [ ] **16.2.4** Apply resolution stepwise-down constraint
- [ ] **16.2.5** Add fourth species option to API

**Test Criteria**: Generate suspensions, verify all follow pattern

---

## Phase 17: Fifth Species Implementation ✓ Testable

### Fifth Species Rules (Florid)
- [ ] **17.1.1** Combine all previous species rules
- [ ] **17.1.2** Implement mixed rhythm validation
- [ ] **17.1.3** Implement optional cambiata pattern detection
- [ ] **17.1.4** Ensure strong beat consonance in mixed contexts
- [ ] **17.1.5** Create `FifthSpeciesValidator` class

**Test Criteria**: Test complex florid examples

### Fifth Species Generator
- [ ] **17.2.1** Implement mixed rhythm generation (whole/half/quarter)
- [ ] **17.2.2** Randomly select from species patterns per measure
- [ ] **17.2.3** Maintain melodic coherence across rhythm changes
- [ ] **17.2.4** Add fifth species option to API

**Test Criteria**: Generate florid counterpoint, verify variety and correctness

---

## Phase 18: User Melody Input ✓ Testable

### Melody Editor
- [ ] **18.1.1** Design melody input UI (piano roll or note grid)
- [ ] **18.1.2** Implement `MelodyEditor` component
- [ ] **18.1.3** Add pitch selection (visual keyboard or dropdowns)
- [ ] **18.1.4** Add duration selection
- [ ] **18.1.5** Implement add/remove/edit note operations
- [ ] **18.1.6** Display edited melody in notation
- [ ] **18.1.7** Add "Use Custom CF" vs "Generate Random" toggle

**Test Criteria**: Create custom melodies, verify they appear in notation

### Melody Evaluation
- [ ] **18.2.1** Endpoint: `POST /evaluate-melody` (standalone melody)
- [ ] **18.2.2** Apply melodic rules to user input
- [ ] **18.2.3** Return detailed violations with positions
- [ ] **18.2.4** Create `MelodyEvaluationPanel` component
- [ ] **18.2.5** Highlight violations in editor
- [ ] **18.2.6** Add "Evaluate My Melody" button

**Test Criteria**: Enter bad melodies, verify violations are detected and displayed

---

## Phase 19: Advanced UI/UX Polish ✓ Testable

### UI Enhancements
- [ ] **19.1.1** Add loading states with progress indicators
- [ ] **19.1.2** Add toast notifications for success/error
- [ ] **19.1.3** Improve responsive layout (mobile-friendly)
- [ ] **19.1.4** Add dark mode support
- [ ] **19.1.5** Add keyboard shortcuts (play: spacebar, etc.)
- [ ] **19.1.6** Add "Save/Load" composition feature (localStorage)
- [ ] **19.1.7** Add "Export MIDI" functionality
- [ ] **19.1.8** Add "Export PDF" functionality (notation)
- [ ] **19.1.9** Add tutorial/help overlay for first-time users

**Test Criteria**: User testing for usability and accessibility

### Rule Violation UI
- [ ] **19.2.1** Create filterable violations list (by type, severity)
- [ ] **19.2.2** Click violation → highlight in notation
- [ ] **19.2.3** Show rule explanations on hover
- [ ] **19.2.4** Add "Show Only Errors" vs "Show Warnings" filter
- [ ] **19.2.5** Add violation statistics dashboard

**Test Criteria**: Generate counterpoint with violations, test all UI interactions

---

## Phase 20: Testing & Quality Assurance ✓ Testable

### Backend Testing
- [ ] **20.1.1** Write unit tests for all interval functions (>90% coverage)
- [ ] **20.1.2** Write unit tests for melodic rules
- [ ] **20.1.3** Write unit tests for harmonic rules
- [ ] **20.1.4** Write unit tests for each species validator
- [ ] **20.1.5** Write integration tests for generators
- [ ] **20.1.6** Write API endpoint tests
- [ ] **20.1.7** Add test fixtures (known good/bad examples)
- [ ] **20.1.8** Set up pytest configuration and coverage reports

**Test Criteria**: Achieve >85% code coverage, all tests pass

### Frontend Testing
- [ ] **20.2.1** Write component tests for controls
- [ ] **20.2.2** Write component tests for displays
- [ ] **20.2.3** Write integration tests for API service
- [ ] **20.2.4** Add E2E tests for critical user flows (Playwright)
- [ ] **20.2.5** Test browser compatibility (Chrome, Firefox, Safari)
- [ ] **20.2.6** Test responsive design on various screen sizes

**Test Criteria**: All tests pass, no console errors in supported browsers

### Performance Testing
- [ ] **20.3.1** Test generator performance (time to generate)
- [ ] **20.3.2** Optimize backtracking (add timeout, smart pruning)
- [ ] **20.3.3** Test UI rendering performance (large scores)
- [ ] **20.3.4** Optimize audio scheduling (no clicks/pops)
- [ ] **20.3.5** Profile and optimize hotspots

**Test Criteria**: Generate 4-voice counterpoint in <5 seconds

---

## Phase 21: Documentation & Deployment ✓ Testable

### Documentation
- [ ] **21.1.1** Write README.md (project overview, setup instructions)
- [ ] **21.1.2** Document API endpoints (OpenAPI/Swagger)
- [ ] **21.1.3** Write backend code comments and docstrings
- [ ] **21.1.4** Write frontend component documentation
- [ ] **21.1.5** Create user guide (how to use the app)
- [ ] **21.1.6** Document species counterpoint rules in app (help section)
- [ ] **21.1.7** Add code architecture diagram

**Test Criteria**: New developer can set up and understand project from docs

### Deployment Preparation
- [ ] **21.2.1** Create `requirements.txt` (backend dependencies)
- [ ] **21.2.2** Create Docker configuration (optional)
- [ ] **21.2.3** Set up environment variables management
- [ ] **21.2.4** Configure production build (frontend)
- [ ] **21.2.5** Set up CI/CD pipeline (GitHub Actions)
- [ ] **21.2.6** Configure production CORS settings
- [ ] **21.2.7** Add security headers
- [ ] **21.2.8** Set up error monitoring (Sentry or similar)

**Test Criteria**: Successful deployment to staging environment

### Deployment
- [ ] **21.3.1** Deploy backend to cloud service (Heroku, AWS, DigitalOcean)
- [ ] **21.3.2** Deploy frontend to hosting (Vercel, Netlify, AWS S3)
- [ ] **21.3.3** Set up custom domain (optional)
- [ ] **21.3.4** Configure SSL/HTTPS
- [ ] **21.3.5** Set up monitoring and logging
- [ ] **21.3.6** Perform smoke tests on production

**Test Criteria**: App is live and fully functional in production

---

## Phase 22: Extended Features (Optional Enhancements)

### Musical Features
- [ ] **22.1.1** Add more modes (Lydian, Mixolydian, Aeolian, Locrian)
- [ ] **22.1.2** Add chromatic support (accidentals)
- [ ] **22.1.3** Add mixed species (different species per voice)
- [ ] **22.1.4** Add configurable style preferences (strict vs free)
- [ ] **22.1.5** Add alternate tuning systems (just intonation)

### Generation Features
- [ ] **22.2.1** Add "regenerate single voice" option
- [ ] **22.2.2** Add "suggest fixes" for violations
- [ ] **22.2.3** Add genetic algorithm generator (alternative to backtracking)
- [ ] **22.2.4** Add machine learning model (trained on corpus)
- [ ] **22.2.5** Add style transfer (imitate specific composers)

### UI Features
- [ ] **22.3.1** Add multiple instrument sounds (piano, strings, organ)
- [ ] **22.3.2** Add reverb/effects controls
- [ ] **22.3.3** Add loop playback with region selection
- [ ] **22.3.4** Add practice mode (hide counterpoint, try to write it)
- [ ] **22.3.5** Add learning mode (step-by-step generation with explanations)
- [ ] **22.3.6** Add composition history/gallery
- [ ] **22.3.7** Add sharing functionality (URL with composition data)

### Educational Features
- [ ] **22.4.1** Add interactive tutorial (guided composition)
- [ ] **22.4.2** Add quizzes (identify violations)
- [ ] **22.4.3** Add exercises (complete partial counterpoints)
- [ ] **22.4.4** Add historical examples database (Fux, Palestrina)
- [ ] **22.4.5** Add rule explanations with audio examples

---

## Success Metrics

### Phase Completion Criteria
- Each phase must pass its "Test Criteria" before proceeding
- All unit tests passing with >85% coverage
- No critical bugs in issue tracker
- Code reviewed and documented

### Final Deliverable
- Working web application accessible via URL
- Backend API with full documentation
- Frontend UI with intuitive controls
- Ability to generate valid counterpoint in all 5 species
- Ability to evaluate user-entered melodies
- Notation display with violation highlighting
- Audio playback with tempo and mute controls
- Comprehensive test suite
- Complete documentation

---

## Development Timeline Estimate

**Minimum Viable Product (MVP)**: Phases 1-12 (~6-8 weeks part-time)
- First species only, 2 voices, basic UI, playback

**Full Core Features**: Phases 1-18 (~12-16 weeks part-time)
- All species, multi-voice, user input, complete functionality

**Production Ready**: Phases 1-21 (~16-20 weeks part-time)
- Polished UI, full testing, deployment

**Extended Features**: Phase 22 (ongoing)
- Enhancements based on user feedback

---

## Notes on Best Practices

### Code Quality
- Write modular, testable code from the start
- Use type hints (Python) and TypeScript (frontend)
- Follow consistent naming conventions
- Keep functions small and single-purpose
- Document complex algorithms

### Version Control
- Commit after each completed task
- Use meaningful commit messages
- Create branches for major features
- Tag releases

### Testing Strategy
- Write tests alongside features (TDD when possible)
- Test edge cases and boundary conditions
- Use fixtures for known good/bad examples
- Automate testing in CI/CD

### Performance Considerations
- Profile before optimizing
- Set reasonable timeouts for generation
- Use caching where appropriate
- Optimize notation rendering for large scores

### Security
- Validate all user input
- Set rate limits on API endpoints
- Use HTTPS in production
- Keep dependencies updated

---

**Last Updated**: December 6, 2025
**Total Tasks**: 300+
**Estimated Total Time**: 16-20 weeks (part-time) for production-ready app
