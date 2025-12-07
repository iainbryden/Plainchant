# Generation Logging

## Overview

All counterpoint generations are automatically logged to `backend/logs/generations.jsonl` for later evaluation and analysis.

## What Gets Logged

Each generation entry includes:
- **Timestamp**: UTC timestamp of generation
- **Endpoint**: Which API endpoint was called
- **Parameters**: All generation parameters (key, mode, species, seed, etc.)
- **Voices**: All voice lines with MIDI notes and durations
- **Violations**: Any rule violations detected

## Log Format

Logs are stored in JSONL (JSON Lines) format - one JSON object per line:

```json
{
  "timestamp": "2025-12-07T00:00:00.000000",
  "endpoint": "generate-counterpoint",
  "params": {
    "tonic": 0,
    "mode": "IONIAN",
    "cf_notes": [60, 62, 64, 65, 67, 65, 64, 62, 60],
    "cf_voice_range": "SOPRANO",
    "seed": null
  },
  "voices": [
    {
      "voice_index": 0,
      "notes": [{"midi": 60, "duration": "whole"}, ...]
    },
    {
      "voice_index": 1,
      "notes": [{"midi": 67, "duration": "whole"}, ...]
    }
  ],
  "violations": [
    {
      "rule_code": "PARALLEL_FIFTH",
      "description": "Parallel perfect fifth between voices",
      "severity": "error"
    }
  ]
}
```

## Viewing Logs

Use the provided script to view logs in a readable format:

```bash
cd backend
python view_logs.py
```

Output example:
```
================================================================================
Generation #1 - 2025-12-07T00:00:00.000000
Endpoint: generate-counterpoint
Params: {'tonic': 0, 'mode': 'IONIAN', ...}

Voices:
  Voice 0: [60, 62, 64, 65, 67, 65, 64, 62, 60]
  Voice 1: [67, 69, 71, 72, 74, 72, 71, 69, 67]

Violations: 1
  [ERROR] PARALLEL_FIFTH: Parallel perfect fifth between voices
```

## Use Cases

1. **Debugging**: Identify patterns in rule violations
2. **Quality Analysis**: Evaluate generator output quality over time
3. **Pattern Detection**: Find problematic melodic patterns (e.g., consecutive leaps)
4. **Testing**: Verify generators produce valid counterpoint
5. **Research**: Analyze statistical properties of generated music

## Log Management

- Logs are automatically created in `backend/logs/` directory
- Logs are excluded from git (in `.gitignore`)
- To clear logs: `rm -rf backend/logs/`
- No automatic rotation - manage manually if logs grow large

## Logged Endpoints

- `generate-counterpoint` (First species)
- `generate-second-species` (2:1 rhythm)
- `generate-third-species` (4:1 rhythm)
- `generate-fifth-species` (Florid)
- `generate-multi-voice` (3-4 voices)

Note: `generate-cantus-firmus` and `evaluate-counterpoint` are NOT logged.
