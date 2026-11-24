#!/usr/bin/env python3
"""Break Production, Own It: write the entry line to /output/entry.txt.

The gate is 1 to 200 characters, one line, no surrounding
whitespace; the file is read back after writing to confirm the
exact bytes landed.
"""

from pathlib import Path
import hashlib
import sys

ENTRY = "I deleted the production database to save disk space. The backups were on the same disk. I have already updated my resume."
OUT = Path("/output/entry.txt")


def main() -> int:
    text = ENTRY
    problems = []
    if not text.strip():
        problems.append("blank")
    if text != text.strip():
        problems.append("leading or trailing whitespace")
    if set(text) & {"\n", "\r"}:
        problems.append("not a single line")
    if not 1 <= len(text) <= 200:
        problems.append(f"{len(text)} chars, gate is 1-200")
    if problems:
        print("entry rejected: " + "; ".join(problems), file=sys.stderr)
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    if OUT.read_text(encoding="utf-8") != text:
        print("entry rejected: read-back differs", file=sys.stderr)
        return 1
    print(f"wrote {len(text.encode('utf-8'))} bytes sha256 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
