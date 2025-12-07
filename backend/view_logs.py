#!/usr/bin/env python3
"""View generation logs in a readable format."""

import json
from pathlib import Path


def view_logs(log_file: str = "logs/generations.jsonl"):
    """Display generation logs."""
    log_path = Path(log_file)
    
    if not log_path.exists():
        print(f"No log file found at {log_file}")
        return
    
    with open(log_path) as f:
        for i, line in enumerate(f, 1):
            entry = json.loads(line)
            print(f"\n{'='*80}")
            print(f"Generation #{i} - {entry['timestamp']}")
            print(f"Endpoint: {entry['endpoint']}")
            print(f"Params: {entry['params']}")
            print(f"\nVoices:")
            for voice in entry['voices']:
                notes = [n['midi'] for n in voice['notes']]
                print(f"  Voice {voice['voice_index']}: {notes}")
            print(f"\nViolations: {len(entry['violations'])}")
            for v in entry['violations']:
                print(f"  [{v['severity']}] {v['rule_code']}: {v['description']}")


if __name__ == "__main__":
    view_logs()
