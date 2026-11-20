# File Integrity Monitor (SHA-256)

Creates a baseline JSON manifest of SHA-256 file hashes for a directory and verifies later whether files were added, modified, or deleted.

## Usage
```bash
python3 fim.py init ./watched_dir --manifest manifest.json
python3 fim.py verify ./watched_dir --manifest manifest.json
```
