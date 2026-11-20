#!/usr/bin/env python3
"""Simple SHA-256 File Integrity Monitor (FIM)."""

import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def scan_directory(root: Path, manifest_path: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for file_path in sorted(root.rglob("*")):
        if file_path.is_file() and file_path.resolve() != manifest_path.resolve():
            rel = str(file_path.relative_to(root))
            hashes[rel] = sha256_file(file_path)
    return hashes


def main() -> None:
    parser = argparse.ArgumentParser(description="SHA-256 File Integrity Monitor")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Create baseline hash manifest")
    p_init.add_argument("directory", type=Path)
    p_init.add_argument("--manifest", type=Path, default=Path("manifest.json"))

    p_ver = sub.add_parser("verify", help="Verify directory against baseline manifest")
    p_ver.add_argument("directory", type=Path)
    p_ver.add_argument("--manifest", type=Path, default=Path("manifest.json"))

    args = parser.parse_args()
    target = args.directory.resolve()

    if args.command == "init":
        data = scan_directory(target, args.manifest)
        args.manifest.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"Baseline created with {len(data)} files -> {args.manifest}")

    elif args.command == "verify":
        if not args.manifest.exists():
            print(f"Manifest not found: {args.manifest}")
            raise SystemExit(1)
        baseline: dict[str, str] = json.loads(args.manifest.read_text(encoding="utf-8"))
        current = scan_directory(target, args.manifest)

        added = sorted(set(current) - set(baseline))
        removed = sorted(set(baseline) - set(current))
        modified = sorted(k for k in set(current) & set(baseline) if current[k] != baseline[k])

        print(f"Added ({len(added)}):       {added}")
        print(f"Removed ({len(removed)}):     {removed}")
        print(f"Modified ({len(modified)}):    {modified}")


if __name__ == "__main__":
    main()
