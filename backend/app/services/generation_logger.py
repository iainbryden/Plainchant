"""Generation logging service for counterpoint evaluation."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from app.models.counterpoint import CounterpointSolution


class GenerationLogger:
    """Logs generated counterpoint to file for later evaluation."""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = self.log_dir / "generations.jsonl"
    
    def log_generation(
        self,
        solution: CounterpointSolution,
        params: dict[str, Any],
        endpoint: str
    ) -> None:
        """Log a generated counterpoint solution."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "endpoint": endpoint,
            "params": params,
            "voices": [
                {
                    "voice_index": voice.voice_index,
                    "voice_range": voice.voice_range.value,
                    "notes": [{"midi": note.pitch.midi, "duration": note.duration.value} for note in voice.notes]
                }
                for voice in solution.voice_lines
            ],
            "violations": [
                {
                    "rule_code": v.rule_code,
                    "description": v.description,
                    "severity": v.severity.value
                }
                for v in solution.diagnostics
            ]
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")


# Global logger instance
logger = GenerationLogger()
