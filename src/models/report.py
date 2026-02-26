"""Typed report model."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

@dataclass(frozen=True)
class Spike:
    index: int
    error_rate: float
    window: int

    def to_dict(self) -> Dict[str, Any]:
        return {'index': self.index, 'error_rate': self.error_rate, 'window': self.window}

@dataclass(frozen=True)
class Report:
    path: str
    total_lines: int
    error_lines: int
    error_rate: float
    spikes: List[Spike]
    generated_at: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            'path': self.path,
            'total_lines': self.total_lines,
            'error_lines': self.error_lines,
            'error_rate': self.error_rate,
            'spikes': [s.to_dict() for s in self.spikes],
            'generated_at': self.generated_at,
        }
