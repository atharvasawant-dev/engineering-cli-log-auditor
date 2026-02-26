"""CLI entry point."""

import argparse
import json
import logging
from pathlib import Path

from src.services.analyzer import analyze_log

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog='log-auditor', description='Audit logs and produce anomaly reports.')
    sub = p.add_subparsers(dest='cmd', required=True)
    a = sub.add_parser('analyze', help='Analyze a log file')
    a.add_argument('--path', required=True, help='Path to log file')
    a.add_argument('--window', type=int, default=200, help='Sliding window size')
    a.add_argument('--threshold', type=float, default=0.15, help='Error-rate threshold for spike detection')
    a.add_argument('--out', default='-', help='Output path for JSON report, or - for stdout')
    return p

def main() -> int:
    args = _build_parser().parse_args()
    report = analyze_log(Path(args.path), window=args.window, threshold=args.threshold)
    payload = report.to_dict()
    if args.out == '-':
        print(json.dumps(payload, indent=2))
    else:
        Path(args.out).write_text(json.dumps(payload, indent=2), encoding='utf-8')
        logger.info('Report written to %s', args.out)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
