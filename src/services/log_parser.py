"""Log parsing utilities."""

import json
from typing import Iterable, Iterator, Tuple

def iter_lines(path) -> Iterator[str]:
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if line:
                yield line

def classify_line(line: str) -> Tuple[bool, str]:
    # JSON logs: treat level=error as error
    if line.startswith('{') and line.endswith('}'):
        try:
            obj = json.loads(line)
            level = str(obj.get('level', '')).lower()
            msg = str(obj.get('message', line))
            return (level in {'error', 'fatal', 'critical'}, msg)
        except Exception:
            pass
    lowered = line.lower()
    is_err = any(tok in lowered for tok in [' error ', 'exception', 'traceback', 'fatal']) or lowered.startswith('error')
    return is_err, line
