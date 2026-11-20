#!/usr/bin/env python3
"""Analyze log lines for failed authentication attempts and suspicious IP frequency."""

import argparse
import json
import re
from collections import Counter
from pathlib import Path

IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
FAIL_KEYWORDS = ("failed password", "authentication failure", "invalid user", "401", "login failed")


def analyze_log(log_path: Path, threshold: int) -> dict:
    ip_counts: Counter[str] = Counter()
    total_failed_lines = 0

    with log_path.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            lower = line.lower()
            if any(k in lower for k in FAIL_KEYWORDS):
                total_failed_lines += 1
                ips = IPV4_RE.findall(line)
                for ip in ips:
                    ip_counts[ip] += 1

    flagged = {ip: count for ip, count in ip_counts.items() if count >= threshold}
    return {
        "file": str(log_path),
        "total_failed_events": total_failed_lines,
        "threshold": threshold,
        "top_ips": dict(ip_counts.most_common(10)),
        "flagged_ips": flagged,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Failed Login Log Analyzer")
    parser.add_argument("logfile", type=Path, help="Path to log file")
    parser.add_argument("--threshold", type=int, default=5, help="Flag IPs with >= N failures")
    parser.add_argument("--json", dest="json_out", type=Path, default=None, help="Optional JSON output path")
    args = parser.parse_args()

    summary = analyze_log(args.logfile, args.threshold)
    print(f"Log file:            {summary['file']}")
    print(f"Failed events found: {summary['total_failed_events']}")
    print("Top source IPs:")
    for ip, cnt in summary["top_ips"].items():
        mark = " [FLAGGED]" if ip in summary["flagged_ips"] else ""
        print(f"  {ip:<16} {cnt}{mark}")

    if args.json_out:
        args.json_out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"\nSaved JSON summary to {args.json_out}")


if __name__ == "__main__":
    main()
