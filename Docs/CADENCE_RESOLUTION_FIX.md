# Cadence Resolution Improvements

## Issue

Counterpoint generators were violating cadential resolution rules:
- Parallel motion at cadence
- Same notes before resolution
- Not resolving properly with 3rd or 6th to octave/unison

## Solution

### Changes Made

#### 1. First Species Generator (`first_species_generator.py`)

**Penultimate Preference System**:
- Added preference for 3rds and 6ths (intervals 3, 4, 8, 9 semitones) at penultimate position
- Candidates are split into `preferred` (3rds/6ths) and `candidates` (other consonances)
- Each group is shuffled separately to maintain randomization
- Preferred candidates are tried first, fallback to others if needed

**Flexible Final Note**:
- Relaxed stepwise requirement for final note
- Prefers stepwise motion (≤2 semitones) but allows small leaps (≤5 semitones) if needed
- Handles cases where CF has repeated final notes

**Increased Attempts**:
- Raised `max_attempts` from 1000 to 5000 to handle more constrained scenarios

#### 2. Second Species Generator (`second_species_generator.py`)

**Same improvements applied**:
- Penultimate strong beat prefers 3rds/6ths
- Flexible final note with stepwise preference
- Maintains 2:1 rhythm constraints

### Technical Details

**Preference Implementation**:
```python
# Prefer 3rd or 6th for penultimate
if is_penultimate:
    penult_mod = vert_interval % 12
    if penult_mod in [3, 4, 8, 9]:
        preferred.append(midi)
    else:
        candidates.append(midi)
else:
    candidates.append(midi)

# Shuffle each group separately, then combine
if preferred:
    random.shuffle(preferred)
random.shuffle(candidates)
return preferred + candidates if preferred else candidates
```

**Final Note Flexibility**:
```python
step_dist = abs(midi - prev_note.pitch.midi)
if step_dist <= 2:
    preferred.append(midi)  # Stepwise
elif step_dist <= 5:
    candidates.append(midi)  # Small leap fallback
```

## Results

- All 100 backend tests passing
- Generators now strongly prefer proper cadential resolutions
- Maintains randomization within preference groups
- Handles edge cases (repeated CF notes, constrained ranges)
- Penultimate violations reduced from frequent to rare

## Cadential Rules Enforced

1. **Penultimate Interval**: Prefers M3, m3, M6, or m6 (3rd or 6th)
2. **Final Interval**: Must be P1 or P8 (unison or octave)
3. **Stepwise Approach**: Strongly prefers stepwise motion to final note
4. **No Parallel Perfects**: Existing parallel perfect detection still active

## Testing

Run tests to verify:
```bash
cd backend
source .venv/bin/activate
python -m pytest tests/ -v
```

All 100 tests should pass, including:
- `test_generate_valid_counterpoint` - No violations
- `test_generate_different_keys` - Works in all keys
- `test_generate_different_modes` - Works in all modes
- `test_generate_different_lengths` - Works with various CF lengths
