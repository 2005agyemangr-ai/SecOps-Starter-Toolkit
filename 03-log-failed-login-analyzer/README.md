# Failed Login Log Analyzer

A defensive log-parsing utility that scans authentication or web access logs for repeated failed login attempts, summarizes top source IPs, and outputs a JSON report.

## Sample Test
```bash
python3 log_analyzer.py sample_auth.log --threshold 3 --json report.json
```
