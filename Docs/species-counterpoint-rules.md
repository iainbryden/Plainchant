You were almost certainly studying **species counterpoint** (sometimes called *strict 16th-century/modal counterpoint in the style of Palestrina*).

The guide below is a fairly strict, app-friendly rule set for **species counterpoint up to 4 voices** in Markdown.

---

# Species Counterpoint: Full Rule Set (Up to 4 Voices)

## 1. Global Concepts

### 1.1. Basic Objects (for your app)

* **Pitch**:

  * Represent as `(scaleDegree, octave)` or absolute pitch (`MIDI`, etc.).
* **Mode / Scale**:

  * Usually modal (Dorian, Phrygian, etc.) or modern major/minor for convenience.
  * For an app, you can generalize to any 7-note diatonic set.
* **Voice**:

  * Each voice is a **sequence of pitches** over equal subdivisions of time.
  * Voices have named ranges and “clefs” but you can treat ranges abstractly.

Example data model (conceptual):

```text
CantusFirmus = [Pitch]             // whole notes only
SpeciesType  = FIRST | SECOND | THIRD | FOURTH | FIFTH
Voice        = { pitches: [Pitch], species: SpeciesType }
Composition  = { cf: CantusFirmus, voices: [Voice], mode, meter }
```

### 1.2. Voice Ranges (approximate, for SATB)

Use these to constrain generation:

* **Soprano**: C4 – G5
* **Alto**: G3 – D5
* **Tenor**: C3 – G4
* **Bass**: E2 – C4

Rules:

* Keep each voice mostly in its *central* range; avoid extremes except for expressive high points.
* Avoid long stays at the extremes.

### 1.3. Vertical Intervals

Define intervals as distance between voices (in scale steps or semitones).

* **Perfect consonances**:

  * Unison (P1)
  * Perfect fifth (P5)
  * Octave (P8)
  * In 3+ voices, also compounds (P12, P15 etc.).
* **Imperfect consonances**:

  * Major/minor 3rd
  * Major/minor 6th
  * (Their compounds: 10ths, 13ths)
* **Dissonances**:

  * 2nds, 7ths, augmented/diminished intervals
  * 4ths **above the bass** are treated as dissonant.

Your helper predicates:

```text
isPerfectConsonance(interval)
isImperfectConsonance(interval)
isConsonance(interval) = perfect OR imperfect
isDissonance(interval) = NOT consonance
```

### 1.4. Motion Types (Between Two Voices)

Between any adjacent notes in two voices (V1, V2):

* **Parallel motion**: both move in the same direction by the same interval.
* **Similar motion**: both move in the same direction, but different intervals.
* **Contrary motion**: one goes up, one goes down.
* **Oblique motion**: one stays, the other moves.

Important global rules:

* **No parallel perfect consonances** (P5, P8, sometimes P1) between **any pair of voices**.
* Avoid **direct (hidden) perfects** between outer voices:

  * If S and B move in similar motion to a perfect consonance, and **soprano leaps**, that’s usually forbidden.
* Prefer **contrary and oblique motion**; use **similar** sparingly.

Pseudocode check for parallel perfects (pairwise):

```text
if isPerfectConsonance(prevInterval) and isPerfectConsonance(currInterval)
   and motionType(prevPitch1, currPitch1, prevPitch2, currPitch2) == PARALLEL
       => reject
```

### 1.5. General Melodic Rules (Any Voice, Any Species)

Per voice:

1. **Conjunct motion** (by step) should dominate.

   * Rough heuristic: ≥ 60–70% steps.
2. **Leaps**:

   * Allow 3rd and 4th freely (not too many).
   * 5ths, 6ths, 7ths, octaves sparingly.
3. **Leap compensation**:

   * After a large leap (≥ a 5th), move by **step in the opposite direction**.
4. **No augmented intervals** (aug 2nd, aug 4th, etc.) unless you intentionally support chromaticism (classically you don’t).
5. **Avoid repeated notes** too much (no long strings of the same note).
6. **Single melodic high point (climax)**:

   * One highest note per voice; if repeated, it should be close together.
7. **No melodic tritones** (e.g., F–B in C major) unless you’re in a specific modal context and explicitly allow them.
8. **No voice crossing**:

   * Voice i should not move above voice i+1.
9. **Avoid voice overlap**:

   * V1_new should not be lower than V2_old, etc., in strict style.

---

## 2. Cantus Firmus (CF) Rules

A **cantus firmus** is a single line of whole notes, used as the reference.

### 2.1. Length & Shape

* Length: roughly 8–16 notes.
* Clear, stepwise melodic line with:

  * One main climax.
  * Mostly stepwise.
  * Few leaps; leaps must be compensated.

### 2.2. Start and End

* **Start**: Usually on the **final** (tonic of mode).
* **End**: On the **final**.
* Penultimate note: usually **2nd or 7th** above/below final (depending on mode) resolving by step.

### 2.3. CF Melodic Constraints

* No large leaps without stepwise compensation.
* No successive leaps in the same direction.
* No melodic tritones.
* Avoid outlining dissonant intervals (e.g., sequences that strongly imply tritone/dim5).
* Avoid overly static or overly angular lines.

Your app can generate CF first using these constraints, then generate counterpoint above/below.

---

## 3. First Species (Note-Against-Note)

One note in the counterpoint for every CF note.

### 3.1. Vertical Consonances Only

For **every sonority** (each CF note + each active voice note):

* Interval with CF (if 2 voices) or with the **bass** (if 3–4 voices) must be **consonant**.
* No dissonances at all in first species.

### 3.2. Start & End

For **2 voices**:

* If CF is in **lower voice**:

  * **Start**: unison, P5, or P8.
  * **End**: unison or octave.
* If CF is in **upper voice**:

  * **Start**: unison or P8.
  * **End**: unison or P8.

For **3–4 voices**:

* At beginning and end:

  * Include the **final** in the bass.
  * Typically a full triad built from final (or modal equivalent).
  * Outer voices: unison or octave at the end.

### 3.3. Penultimate Sonority

* Typically: **6–8** or **3–1** between top and bass (e.g., leading to a final).
* For 2 voices:

  * If CF above: counterpoint below usually moves 2–1 or 7–8.
  * If CF below: similar stepwise approach.

### 3.4. Motion Rules (2 voices, apply pairwise for more voices)

* No parallel 5ths or 8ves.
* No direct (hidden) 5ths or 8ves between bass and soprano with a leap in the soprano.
* Prefer contrary or oblique motion.
* Avoid too many similar motions into imperfect consonances as well; vary texture.

### 3.5. Multi-Voice Constraints (3–4 Voices)

At each beat:

* All intervals with **bass** are consonant.
* Between **upper voices**, prefer consonances; a **4th between two upper voices** is usually OK if overall harmony is consonant (but keep it sparse).
* No parallel perfects between **any pair of voices** (not just with CF).

Algorithmic idea:

```text
for each beat i:
    candidateChord = [candidatePitchVoice1, candidatePitchVoice2, ..., cf[i]]
    if any intervalWithBass is dissonant => reject
    if any pair (v_a, v_b) forms forbidden parallel perfect with previous beat => reject
    if violates range / voice crossing / melodic constraints => reject
```

---

## 4. Second Species (Two Notes Against One)

Counterpoint has **two notes** for each CF note (half-note motion vs whole-note CF).

### 4.1. Beat Structure

* **Strong beats** (downbeat): **must be consonant**.
* **Weak beats**:

  * May be consonant, or
  * Dissonant **only as passing or neighboring tones** by step.

### 4.2. Dissonance Rules

On weak beats:

* Dissonance must be:

  * Approached by step
  * Left by step, in the **same direction** (passing tone) or opposite (neighbor).
* No leaps into or out of dissonances.
* No accented dissonances in 2nd species (strong beat dissonance forbidden).

### 4.3. Start & End

Common patterns:

* Begin with a half-note rest + consonance on 2nd half note, or
* Begin with consonance on first half note.
* End:

  * Last minim pair typically: consonance + stepwise motion to final.
  * Penultimate strong beat consonance that leads cadentially, similar to 1st species.

### 4.4. Multi-Voice Handling

Each non-CF voice may be in a different species in more advanced work; for a simple generator, give all non-CF voices the same species.

* Ensure that any **vertical dissonances** (between upper voices) occur only where:

  * At least one voice’s note is a passing/neighbor relative to its **own previous/next notes**.
  * And the **bass + each upper voice** combination respects strong-beat consonance rules.

---

## 5. Third Species (Four Notes Against One)

Counterpoint has **four notes** for each CF note (quarter-note motion vs whole-note CF).

### 5.1. Beat Structure

With CF in whole notes, counterpoint in quarters within each bar:

* Beats: 1, 2, 3, 4 (strongest: 1; secondary: 3).
* **Strong beats (1 and sometimes 3)**:

  * Must be **consonant** with CF.
* **Weak beats (2, 4)**:

  * May be dissonant only as passing/neighbor tones.

### 5.2. Dissonance Types Allowed

* **Passing tones**: stepwise motion across the dissonant note.
* **Neighbor tones**: step away from consonance and back to that same consonance.
* **Double passing** allowed (stepwise chain across multiple beats) as long as:

  * Each dissonance is approached/left by step.

Forbidden:

* Leaps into or out of dissonance.
* Dissonances on **beat 1**; treat beat 3 as strong enough to prefer consonance.

### 5.3. Melodic Shape

* Long scalar runs are fine, but avoid **monotonous scalar chains** across many measures.
* Same leap rules as before.

---

## 6. Fourth Species (Suspensions / Syncopatio)

Counterpoint notes are **tied over the bar line**, creating **accented dissonances**.

### 6.1. Basic Pattern (Preparation – Suspension – Resolution)

For each suspension:

1. **Preparation**: consonance on weak beat or previous bar.
2. **Suspension**: note is tied over to next strong beat, now forming **dissonance** with CF.
3. **Resolution**: dissonance resolves down by **step** on following weak beat.

Example (CF in lower voice):

* CF: whole notes: C – C – C – …
* Counterpoint:

  * Beat (bar 1): G (consonant 5th)
  * Bar line: tie G over to bar 2 beat 1 (now 4th = dissonant 4–3 suspension)
  * Beat 2: F (resolution down by step to 3rd)

### 6.2. Types of Suspensions (Above the Bass)

Common ones:

* 4–3 (most common)
* 7–6
* 9–8
* 2–3 (in 3rd above, etc.)

Rules:

* Dissonant suspension **must resolve down by step**.
* Preparation and resolution should be consonant.
* Avoid chains that break melodic rules (e.g., too high tension or awkward leaps).

### 6.3. Multi-Voice Suspensions

* Only allow a few **simultaneous dissonant suspensions**, or you’ll over-densify.
* At any moment:

  * **Bass + each upper voice**: if dissonant, it must be a legitimate suspension.
  * Suspended notes must have proper preparation in previous bar and stepwise resolution.

Algorithmically:

```text
If on strong beat:
    if isDissonant(intervalWithBass):
        check:
            prevBeatSameVoice == samePitch (preparation consonant)
            nextBeatSameVoice == pitch - step (resolution down)
        else reject
```

---

## 7. Fifth Species (Florid Counterpoint)

Combines all previous species:

* Note-against-note
* 2:1 motion
* 4:1 motion
* Suspensions (4th species)
* Occasional ornamental figures (cambiata, etc.)

### 7.1. General Rules

* Overall: each bar’s **strong beat** must be consonant with CF.
* Dissonances:

  * Only as passing/neighbor tones on weak beats or suspensions on strong beats.
* Mixture of note values:

  * Quarter, half, whole notes (depending on your underlying time grid).
* Maintain melodic coherence:

  * Same rules as earlier: mostly stepwise, few leaps, compensation, single climax.

### 7.2. Additional Ornament: Cambiata (Optional)

* 4-note figure: step – leap of 3rd – step – step that resolves the dissonance.
* The dissonance is one of the inner notes and must be approached & left appropriately.
* This is more advanced; you can add later as a special pattern.

---

## 8. Extending to 3 & 4 Voices

All previous rules still apply **pairwise between any two voices**.

### 8.1. Vertical Sonorities

At each beat:

* With the **bass** as reference:

  * Intervals must be consonant (depending on species).
* Upper voices:

  * Prefer consonances between them.
  * Occasional 4ths **between upper voices** can be tolerated if overall sonority is consonant and no tritones/unprepared dissonances arise.

You can approximate species counterpoint sonorities as **triads and their inversions** (major/minor), but classical Fuxian counterpoint doesn’t think in terms of “chords,” only consonant stacks.

### 8.2. Global Constraints for 3–4 Voices

For every time step:

1. No parallel 5ths or 8ves between any pair of voices.
2. Avoid hidden 5ths/8ves between **outer voices**.
3. Avoid voice crossing / overlap.
4. Respect each voice’s melodic rules independently.

Pseudo-constraint per time slice `t`:

```text
for each pair (voiceA, voiceB):
    checkParallelPerfects(previous[t-1], current[t])
    checkHiddenPerfects(bass, soprano)   // if you identify outer voices
for each voice v:
    checkMelodicStepAndLeap(v[t-1], v[t], v[t+1])
    checkRange(v[t])
```

---

## 9. Cadence Rules

Cadences tie together local and global constraints.

### 9.1. Typical 2-Voice Cadences (in modern major/minor terms)

If CF is in **lower voice**:

* Penultimate:

  * CF: ♭7 or 2 above final (depending on mode).
  * Counterpoint: 2 or 7 above CF, forming a **6–8** motion to the final.
* Final:

  * Both voices end on tonic (unison or octave).

If CF is in **upper voice**:

* Similar logic but mirrored.

### 9.2. 3–4 Voices

* Bass: usually approaches the final by **5–1** or **2–1** (in step or 5th).
* Upper voices:

  * One voice may form leading tone → tonic motion.
  * Others form 3rd/6th above the bass then resolve to 3rd/octave on final.

Algorithmically:

* Reserve last 2–3 measures to **force** a cadential pattern with pre-defined interval relationships.

---

## 10. Implementation Strategy for an App

### 10.1. Core Functions

You’ll likely need:

```text
interval(pitchA, pitchB) -> Interval
isConsonance(interval)
isPerfectConsonance(interval)
isDissonance(interval)
motionType(prevA, currA, prevB, currB) -> {PARALLEL, SIMILAR, CONTRARY, OBLIQUE}
checkMelodicConstraints(voiceLine)
checkVerticalConstraints(chord)
checkSpeciesConstraints(species, localContext)
```

### 10.2. Generation Algorithm (Backtracking / CSP)

High-level approach:

1. **Generate Cantus Firmus**:

   * Choose length, mode, and apply CF rules until you get a valid line.
2. For each **additional voice**:

   * Decide species (1–5).
   * For each time step:

     * Generate a list of candidate pitches within range.
     * Filter by:

       * Local melodic constraints (stepwise, leap rules).
       * Vertical consonance rules (with CF or bass).
       * Species‐specific dissonance rules.
       * Parallel/hidden perfect checks with all existing voices.
     * If no candidates: backtrack.
3. At the end:

   * Check global constraints: single climax, cadence rules, range usage, etc.

Pseudo-outline:

```text
function generateCounterpoint(cf, numVoices, speciesPerVoice):
    composition = initComposition(cf, numVoices, speciesPerVoice)
    if backtrackFill(composition, timeIndex=0):
        return composition
    else:
        fail

function backtrackFill(comp, timeIndex):
    if timeIndex == totalTimeSteps:
        return cadenceCheck(comp)
    for each voice v:
        if v is CF: continue
        candidates[v] = possiblePitches(comp, v, timeIndex)
    for each combination of candidates (cartesian product):
        if allConstraintsSatisfied(comp, combination, timeIndex):
            applyCombination(comp, combination, timeIndex)
            if backtrackFill(comp, timeIndex+1):
                return true
            undoCombination(comp, timeIndex)
    return false
```

You can optimize by filling **one voice at a time** rather than all at once.

---

If you’d like, next I can:

* Turn this into concrete **rule tables** (e.g., JSON schemas) for each species, or
* Sketch actual code stubs in the language of your choice (PHP, TS, etc.) for things like `isConsonance`, `checkParallelPerfects`, and a simple backtracking generator.
