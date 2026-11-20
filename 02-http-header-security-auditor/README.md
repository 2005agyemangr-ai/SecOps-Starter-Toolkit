# HTTP Security Header Auditor

A small Python script that fetches a target URL's HTTP response headers and checks for common defensive headers (`Strict-Transport-Security`, `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`).

## Disclaimer
Only run against URLs and systems you own or have explicit authorization to test.

## Usage
```bash
python3 header_audit.py https://example.com
```
