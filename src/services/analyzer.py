"""Log analysis with spike detection."""

import logging
from datetime import datetime
from pathlib import Path
from typing import List

from src.models.report import Report, Spike
from src.services.log_parser import iter_lines, classify_line

logger = logging.getLogger(__name__)

def analyze_log(path: Path, window: int = 200, threshold: float = 0.15) -> Report:
    if window < 20:
        raise ValueError('window must be >= 20')
    if threshold <= 0 or threshold >= 1:
        raise ValueError('threshold must be between 0 and 1')

    total = 0
    error_flags: List[int] = []

    for line in iter_lines(path):
        is_err, _ = classify_line(line)
        error_flags.append(1 if is_err else 0)
        total += 1

    err = sum(error_flags)
    overall_rate = (err / total) if total else 0.0

    spikes: List[Spike] = []
    if total >= window:
        current = sum(error_flags[:window])
        for i in range(window, total + 1):
            rate = current / window
            if rate >= threshold:
                spikes.append(Spike(index=i - 1, error_rate=rate, window=window))
            if i < total:
                current += error_flags[i] - error_flags[i - window]

    logger.info('Analyzed %s lines, error_rate=%.3f spikes=%s', total, overall_rate, len(spikes))
    return Report(
        path=str(path),
        total_lines=total,
        error_lines=err,
        error_rate=overall_rate,
        spikes=spikes,
        generated_at=datetime.utcnow().isoformat(),
    )
