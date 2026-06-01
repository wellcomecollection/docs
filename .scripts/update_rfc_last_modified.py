#!/usr/bin/env python3

import argparse
import pathlib
import re
import sys
from datetime import datetime, timezone

LAST_MODIFIED_PATTERN = re.compile(
    r"^\s*(?:[-*]\s+)?(?:\*\*)?\s*Last modified\s*:\s*(?:\*\*)?\s*(.+?)\s*$",
    re.IGNORECASE,
)


def update_last_modified(path):
    """
    Update the Last modified timestamp in an RFC README to current UTC time.
    
    Returns:
        bool: True if the file was modified, False otherwise.
    """
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return False
    
    lines = content.splitlines(keepends=True)
    # Use +00:00 suffix (explicit UTC offset) rather than Z shorthand,
    # as it is more widely supported by date parsers including Python's own.
    iso_now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    
    modified = False
    for idx, line in enumerate(lines):
        m = LAST_MODIFIED_PATTERN.match(line)
        if m:
            newline = "\n" if line.endswith("\n") else ""
            new_line = f"**Last modified:** {iso_now}{newline}"
            if new_line != line:
                lines[idx] = new_line
                modified = True
            break
    
    if modified:
        path.write_text("".join(lines), encoding="utf-8")
    
    return modified


def main():
    parser = argparse.ArgumentParser(
        description="Update Last modified timestamp in RFC README files."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Paths to RFC README files to update.",
    )
    args = parser.parse_args()
    
    if not args.paths:
        return 0
    
    for raw_path in args.paths:
        path = pathlib.Path(raw_path)
        if path.name == "README.md" and "rfcs" in path.parts:
            if update_last_modified(path):
                print(f"Updated: {path}")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
