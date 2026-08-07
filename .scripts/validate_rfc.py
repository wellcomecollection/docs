#!/usr/bin/env python3

import argparse
import pathlib
import re
import sys

# Paths we consider RFC README files (e.g. rfcs/070-foo/README.md).
RFC_README_PATTERN = re.compile(r"^rfcs/([^/]+)/README\.md$")
# Expected H1 format: "# RFC 070: Title".
TITLE_PATTERN = re.compile(r"^# RFC\s+(\d{3}):\s+.+$")
# Canonical metadata line format we enforce.
LAST_MODIFIED_LINE_PATTERN = re.compile(r"^\*\*Last modified:\*\*\s+(.+?)\s*$")
# More permissive matcher used only to produce a helpful formatting error.
GENERIC_LAST_MODIFIED_PATTERN = re.compile(
    r"^\s*(?:[-*]\s+)?(?:\*\*)?\s*Last modified\s*:\s*(?:\*\*)?\s*(.+?)\s*$",
    re.IGNORECASE,
)

# Canonical RFC timestamp format: explicit UTC offset with seconds.
ISO_8601_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+00:00$")


def get_first_h1(lines):
    """Return the first H1 line in the file, or None if missing."""
    for line in lines:
        if line.startswith("# "):
            return line
    return None


def has_purpose_section(lines):
    """Return True when a "## Purpose" section exists (case-insensitive)."""
    for line in lines:
        if re.match(r"^##\s+Purpose\s*$", line, flags=re.IGNORECASE):
            return True
    return False


def get_last_modified_value(lines):
    """Extract Last modified value and whether the line is canonically formatted.

    Returns:
        tuple[str | None, bool | None]:
            (timestamp, True)   -> canonical line found
            (timestamp, False)  -> non-canonical but recognisable line found
            (None, None)        -> no Last modified line found
    """
    for line in lines:
        canonical = LAST_MODIFIED_LINE_PATTERN.match(line)
        if canonical:
            return canonical.group(1).strip(), True

        generic = GENERIC_LAST_MODIFIED_PATTERN.match(line)
        if generic:
            return generic.group(1).strip(), False

    return None, None


def validate_rfc_readme(path):
    """Validate a single RFC README file and return a list of error messages."""
    errors = []
    relative_path = path.as_posix()
    match = RFC_README_PATTERN.match(relative_path)
    if not match:
        # Ignore non-RFC paths when called with mixed input.
        return errors

    rfc_dir = match.group(1)

    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"{relative_path}: cannot read file ({exc})")
        return errors

    lines = content.splitlines()

    # 1) Validate H1 title shape and RFC number consistency with directory name.
    title = get_first_h1(lines)
    if title is None:
        errors.append(f"{relative_path}: missing H1 title")
    else:
        title_match = TITLE_PATTERN.match(title)
        if not title_match:
            errors.append(
                f"{relative_path}: title must match 'RFC {{number}}: {{title}}' (e.g. '# RFC 070: Concepts API changes')"
            )
        else:
            title_number = title_match.group(1)
            if not rfc_dir.startswith(f"{title_number}-"):
                errors.append(
                    f"{relative_path}: title RFC number ({title_number}) does not match directory name ({rfc_dir})"
                )

    # 2) Validate Last modified line format and canonical UTC timestamp value.
    last_modified, is_canonical_line = get_last_modified_value(lines)
    if last_modified is None:
        errors.append(f"{relative_path}: missing 'Last modified' metadata line")
    elif not is_canonical_line:
        errors.append(
            f"{relative_path}: Last modified line must be exactly '**Last modified:** YYYY-MM-DDTHH:MM:SS+00:00'"
        )
    elif not ISO_8601_PATTERN.match(last_modified):
        errors.append(
            f"{relative_path}: Last modified must be ISO8601 UTC with +00:00 offset (got: {last_modified})"
        )

    # 3) Enforce required Purpose section.
    if not has_purpose_section(lines):
        errors.append(f"{relative_path}: missing '## Purpose' section")

    return errors


def normalize_paths(paths):
    """Normalize CLI paths to cwd-relative paths where possible."""
    normalized = []
    for raw in paths:
        path = pathlib.Path(raw)
        if path.is_absolute():
            try:
                path = path.relative_to(pathlib.Path.cwd())
            except ValueError:
                # Keep as-is if it isn't under cwd.
                pass
        normalized.append(path)
    return normalized


def main():
    """CLI entry point: validate selected RFCs or all RFC README files."""
    parser = argparse.ArgumentParser(
        description="Validate required sections in RFC README files."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Paths to files to validate. If omitted, all rfcs/*/README.md files are validated.",
    )
    args = parser.parse_args()

    if args.paths:
        candidates = normalize_paths(args.paths)
    else:
        candidates = sorted(pathlib.Path("rfcs").glob("*/README.md"))

    all_errors = []
    checked = 0

    for candidate in candidates:
        candidate_posix = candidate.as_posix()
        # Keep behavior predictable when users pass extra files/paths.
        if not RFC_README_PATTERN.match(candidate_posix):
            continue

        checked += 1
        errors = validate_rfc_readme(candidate)
        all_errors.extend(errors)

    if all_errors:
        print("RFC validation failed:", file=sys.stderr)
        for error in all_errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"RFC validation passed for {checked} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
