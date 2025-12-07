# Coding Standards & Best Practices

## Project Overview

This document defines coding standards for the Species Counterpoint Generator to ensure consistency, maintainability, and quality across all development phases.

---

## General Principles

1. **Consistency**: Follow established patterns in the codebase
2. **Simplicity**: Write minimal, clear code that solves the problem
3. **Testability**: Design code to be easily testable
4. **Documentation**: Document complex logic and public APIs
5. **Type Safety**: Use type hints (Python) and TypeScript (frontend)

---

## Backend Standards (Python)

### Code Organization

```
backend/
├── app/
│   ├── models/          # Pydantic data models
│   ├── services/        # Business logic
│   ├── api/             # API routes
│   └── main.py          # FastAPI app
└── tests/               # Unit tests (mirrors app/ structure)
```

### Python Style

- **Version**: Python 3.12+
- **Type Hints**: Use native syntax (`list[int]`, `dict[str, Any]`)
- **Formatting**: Follow PEP 8
- **Line Length**: 100 characters max
- **Imports**: Group stdlib, third-party, local (separated by blank lines)

```python
# Good
def calculate_interval(pitch1: int, pitch2: int) -> int:
    """Calculate semitone interval between two pitches."""
    return abs(pitch2 - pitch1) % 12

# Bad - no type hints, no docstring
def calculate_interval(pitch1, pitch2):
    return abs(pitch2 - pitch1) % 12
```

### Pydantic Models

- Use `BaseModel` for all data structures
- Define clear field types and constraints
- Add docstrings for complex models
- Use `Field()` for validation and metadata

```python
from pydantic import BaseModel, Field

class Note(BaseModel):
    """Represents a musical note with pitch and duration."""
    pitch: int = Field(ge=0, le=127, description="MIDI pitch number")
    duration: Duration
```

### Service Layer

- Keep functions pure when possible
- Single responsibility per function
- Return explicit types (not `Any`)
- Raise specific exceptions with clear messages

```python
def check_range(voice_line: VoiceLine, voice_range: VoiceRange) -> list[RuleViolation]:
    """Check if all notes fall within the specified voice range."""
    violations = []
    for i, note in enumerate(voice_line.notes):
        if not (voice_range.min_pitch <= note.pitch <= voice_range.max_pitch):
            violations.append(RuleViolation(
                rule_code="RANGE_VIOLATION",
                description=f"Note {note.pitch} outside range",
                voice_indices=[voice_line.voice_index],
                note_indices=[i],
                severity="error"
            ))
    return violations
```

### Testing

- **Framework**: pytest
- **Coverage**: Aim for >85%
- **Location**: `tests/` directory mirroring `app/` structure
- **Naming**: `test_<module>.py`, `test_<function_name>()`
- **Structure**: Arrange-Act-Assert pattern

```python
def test_calculate_interval_perfect_fifth():
    # Arrange
    pitch1 = 60  # C4
    pitch2 = 67  # G4
    
    # Act
    result = calculate_interval(pitch1, pitch2)
    
    # Assert
    assert result == 7
```

### API Endpoints

- Use Pydantic models for request/response
- Include clear docstrings
- Handle errors with appropriate HTTP status codes
- Log requests for debugging

```python
@router.post("/api/generate-cantus-firmus", response_model=GenerateCantusFirmusResponse)
async def generate_cantus_firmus_endpoint(request: GenerateCantusFirmusRequest):
    """Generate a cantus firmus melody."""
    try:
        cf_notes = generate_cantus_firmus(...)
        return GenerateCantusFirmusResponse(cf_notes=cf_notes, ...)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## Frontend Standards (TypeScript/React)

### Code Organization

```
frontend/
├── src/
│   ├── components/      # React components
│   ├── services/        # API client, utilities
│   ├── types/           # TypeScript interfaces
│   ├── utils/           # Helper functions
│   └── App.tsx          # Main component
└── tests/               # Component tests
```

### TypeScript Style

- **Strict Mode**: Enable strict type checking
- **Interfaces**: Define all data structures
- **No `any`**: Avoid `any` type, use `unknown` if needed
- **Naming**: PascalCase for components/types, camelCase for functions/variables

```typescript
// Good
interface GenerateCounterpointRequest {
  tonic: number;
  mode: Mode;
  cf_notes: number[];
}

// Bad - using any
interface GenerateCounterpointRequest {
  tonic: any;
  mode: any;
  cf_notes: any;
}
```

### React Components

- **Functional Components**: Use hooks, not classes
- **Props**: Define explicit interface for props
- **State**: Use `useState` for local state
- **Effects**: Use `useEffect` with proper dependencies
- **Naming**: PascalCase for component files and names

```typescript
// Good
interface KeySelectorProps {
  value: number;
  onChange: (value: number) => void;
}

export const KeySelector: React.FC<KeySelectorProps> = ({ value, onChange }) => {
  return (
    <select value={value} onChange={(e) => onChange(Number(e.target.value))}>
      {/* options */}
    </select>
  );
};

// Bad - no props interface, inline logic
export const KeySelector = (props: any) => {
  return <select>{/* ... */}</select>;
};
```

### API Service Layer

- Centralize all API calls in `services/apiClient.ts`
- Use async/await (not `.then()`)
- Type all requests and responses
- Handle errors consistently

```typescript
export const generateCounterpoint = async (
  params: GenerateCounterpointRequest
): Promise<GenerateCounterpointResponse> => {
  const response = await apiClient.post<GenerateCounterpointResponse>(
    '/api/generate-counterpoint',
    params
  );
  return response.data;
};
```

### State Management

- **Simple State**: Use `useState` for component-local state
- **Shared State**: Use Context API or Zustand for app-wide state
- **Avoid**: Redux (overkill for this project)

### Styling

- **CSS Modules** or **Plain CSS**: Keep it simple
- **No Inline Styles**: Use CSS classes
- **Responsive**: Mobile-first approach
- **Naming**: BEM or semantic class names

```css
/* Good */
.key-selector {
  padding: 0.5rem;
  border: 1px solid #e5e7eb;
}

.key-selector__label {
  font-weight: 500;
}

/* Bad - inline styles in JSX */
<div style={{ padding: '0.5rem', border: '1px solid #e5e7eb' }}>
```

### Testing

- **Framework**: Vitest + React Testing Library
- **Coverage**: Aim for >80% on critical components
- **Test User Behavior**: Not implementation details

```typescript
test('KeySelector calls onChange when value changes', () => {
  const handleChange = vi.fn();
  render(<KeySelector value={0} onChange={handleChange} />);
  
  const select = screen.getByRole('combobox');
  fireEvent.change(select, { target: { value: '2' } });
  
  expect(handleChange).toHaveBeenCalledWith(2);
});
```

---

## Git Workflow

### Commits

- **Frequency**: Commit after each completed task
- **Messages**: Clear, descriptive (present tense)
- **Format**: `<type>: <description>`

```bash
# Good
git commit -m "feat: add cantus firmus generator"
git commit -m "fix: resolve parallel fifths detection bug"
git commit -m "test: add melodic rules test coverage"

# Bad
git commit -m "stuff"
git commit -m "fixed it"
```

### Commit Types

- `feat`: New feature
- `fix`: Bug fix
- `test`: Add/update tests
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `style`: Formatting changes
- `chore`: Build/config changes

### Branches

- `main`: Production-ready code
- `feature/<name>`: New features
- `fix/<name>`: Bug fixes

---

## Documentation Standards

### Code Comments

- **When**: Complex algorithms, non-obvious logic
- **Not**: Obvious code (let code be self-documenting)
- **Style**: Clear, concise explanations

```python
# Good - explains WHY
# P4 above bass is dissonant in counterpoint, but consonant elsewhere
if interval == 5 and is_bass_voice:
    return False

# Bad - explains WHAT (obvious from code)
# Check if interval equals 5
if interval == 5:
```

### Docstrings (Python)

- All public functions and classes
- Format: Google style or NumPy style
- Include parameters, return types, examples for complex functions

```python
def generate_cantus_firmus(
    key: Key,
    length: int,
    voice_range: VoiceRange,
    seed: int | None = None
) -> list[int]:
    """
    Generate a valid cantus firmus melody.
    
    Args:
        key: Musical key (tonic + mode)
        length: Number of notes (typically 8-16)
        voice_range: Target voice range (SATB)
        seed: Random seed for reproducibility
        
    Returns:
        List of MIDI pitch numbers
        
    Raises:
        ValueError: If unable to generate valid CF within max attempts
    """
```

### README Files

- Each major directory should have a README
- Include: purpose, structure, usage examples
- Keep updated as code evolves

---

## Performance Guidelines

### Backend

- Avoid N+1 queries (not applicable yet, but plan ahead)
- Use generators for large sequences
- Set timeouts on generation algorithms
- Profile before optimizing

### Frontend

- Lazy load heavy components (VexFlow, Tone.js)
- Debounce user input
- Memoize expensive computations
- Optimize re-renders with `React.memo` when needed

---

## Security Best Practices

### Backend

- Validate all input with Pydantic
- Set rate limits on API endpoints
- Use HTTPS in production
- Never log sensitive data
- Keep dependencies updated

### Frontend

- Sanitize user input before display
- Use environment variables for config
- Never commit `.env` files
- Validate API responses

---

## Error Handling

### Backend

```python
# Good - specific exception with context
if length < 4:
    raise ValueError(f"CF length must be ≥4, got {length}")

# Bad - generic exception
if length < 4:
    raise Exception("Invalid length")
```

### Frontend

```typescript
// Good - user-friendly error messages
try {
  await generateCounterpoint(params);
} catch (error) {
  if (axios.isAxiosError(error)) {
    setError('Failed to generate counterpoint. Please try again.');
  } else {
    setError('An unexpected error occurred.');
  }
}

// Bad - exposing technical details to user
catch (error) {
  alert(error.message);
}
```

---

## Checklist for New Features

Before marking a task complete:

- [ ] Code follows style guidelines
- [ ] Type hints/types added
- [ ] Unit tests written and passing
- [ ] Documentation updated (if needed)
- [ ] No console errors/warnings
- [ ] Tested manually
- [ ] Committed with clear message
- [ ] Development checklist updated

---

## Tools & Configuration

### Backend

- **Linter**: Ruff or Flake8
- **Formatter**: Black (optional)
- **Type Checker**: mypy (optional)
- **Test Runner**: pytest

### Frontend

- **Linter**: ESLint
- **Formatter**: Prettier (optional)
- **Type Checker**: TypeScript compiler
- **Test Runner**: Vitest

---

## Questions?

When in doubt:
1. Check existing code for patterns
2. Refer to this document
3. Prioritize simplicity and clarity
4. Ask for clarification before implementing

---

**Last Updated**: December 2024
