#!/usr/bin/env python3
"""Audit HTTP response headers for common security hardening directives."""

import argparse
import sys
import urllib.error
import urllib.request

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
]


def audit_url(url: str, timeout: float = 10.0) -> int:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "HeaderSecurityAuditor/1.0 (+Educational)"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            headers = {k.lower(): v for k, v in resp.headers.items()}
            status = resp.status
    except urllib.error.HTTPError as exc:
        headers = {k.lower(): v for k, v in exc.headers.items()} if exc.headers else {}
        status = exc.code
        print(f"Warning: HTTP {status} received from {url}")
    except Exception as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        return 1

    print(f"Target: {url} (Status: {status})\n")
    present_count = 0
    for header in SECURITY_HEADERS:
        val = headers.get(header.lower())
        if val:
            present_count += 1
            print(f"[PRESENT] {header}: {val}")
        else:
            print(f"[MISSING] {header}")

    server_banner = headers.get("server")
    powered_by = headers.get("x-powered-by")
    if server_banner or powered_by:
        print("\nInformation Disclosure Headers:")
        if server_banner:
            print(f"  Server: {server_banner}")
        if powered_by:
            print(f"  X-Powered-By: {powered_by}")

    print(f"\nScore: {present_count}/{len(SECURITY_HEADERS)} checked headers present.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="HTTP Security Header Auditor")
    parser.add_argument("url", help="Target URL starting with http:// or https://")
    parser.add_argument("--timeout", type=float, default=10.0, help="Request timeout in seconds")
    args = parser.parse_args()
    sys.exit(audit_url(args.url, args.timeout))


if __name__ == "__main__":
    main()
