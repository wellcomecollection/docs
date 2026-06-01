#!/usr/bin/env python3

import argparse
import os
import re
import sys
from datetime import datetime, timezone


# Canonical metadata line format enforced by validate_rfc.py.
# Example: "**Last modified:** 2026-06-01T12:00:00+00:00"
LAST_MODIFIED_PATTERN = re.compile(r"^\*\*Last modified:\*\*\s+(.+?)\s*$")


def parse_iso_datetime(value):
    """
    Parse an ISO-like datetime string into a timezone-aware datetime.

    Returns:
        datetime | None: Parsed datetime, or None if parsing fails.
    """
    raw = value.strip()

    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return None

    # Canonical values are timezone-aware; reject naive values.
    if parsed.tzinfo is None:
        return None

    return parsed.astimezone(timezone.utc)


def looks_like_block_boundary(text):
    """Return True if text likely starts a new markdown block.

    Used when extracting the Purpose paragraph to know when to stop collecting
    prose lines, e.g. if Purpose contains a subheading, code block, or list
    before (or instead of) the opening prose sentence.
    """
    stripped = text.strip()
    if not stripped:
        return False

    if stripped.startswith('#'):     # any heading
        return True
    if stripped.startswith('|'):     # table row
        return True
    if stripped.startswith('```'):   # fenced code block
        return True
    if stripped.startswith('>'):     # blockquote
        return True
    if stripped == '---':            # horizontal rule
        return True
    if stripped.startswith('- '):    # unordered list
        return True
    if stripped.startswith('* '):    # unordered list (asterisk style)
        return True
    if re.match(r'^\d+\.\s', stripped):  # ordered list
        return True

    return False


def looks_like_metadata_line(text):
    """Return True for RFC metadata label lines like **Status:** Draft.

    These follow the bold-label pattern used throughout our RFCs for status,
    priority, etc. We skip them when looking for the Purpose prose paragraph.
    """
    stripped = text.strip()
    if re.match(r'^\*\*[^*]+:\*\*\s+.+', stripped):
        return True
    return False


def extract_section_summary(lines, heading_index, section_names):
    """Extract the first prose paragraph under the first matching H2 section.

    Searches forward from heading_index for a heading named in section_names
    (e.g. 'Purpose'), then collects the first paragraph of plain prose beneath
    it. Stops as soon as a blank line is encountered after prose has started,
    or when a non-prose element (heading, code block, list, metadata line) is
    hit.

    Returns:
        str | None: The paragraph as a single string, or None if not found.
    """
    # Find the target section heading (e.g. ## Purpose)
    section_header_index = None
    names_pattern = '|'.join(re.escape(name) for name in section_names)
    section_pattern = re.compile(rf'^##\s+(?:{names_pattern})\s*$', re.IGNORECASE)

    for idx in range(heading_index + 1, len(lines)):
        if section_pattern.match(lines[idx]):
            section_header_index = idx
            break

    if section_header_index is None:
        return None

    summary_lines = []
    in_summary = False  # True once we've found the first prose line

    for idx in range(section_header_index + 1, len(lines)):
        candidate = lines[idx]
        stripped = candidate.strip()

        # A blank line ends the paragraph once we've started collecting.
        if not stripped:
            if in_summary:
                break
            continue

        # Skip any stray Last modified line that appears in the section.
        if LAST_MODIFIED_PATTERN.match(candidate):
            continue

        # Skip (or stop at) **Bold:** metadata label lines.
        if looks_like_metadata_line(candidate):
            if in_summary:
                break
            continue

        # Skip block-level elements (headings, lists, code) before prose starts;
        # stop if we encounter them after prose has already started.
        if looks_like_block_boundary(candidate):
            if in_summary:
                break
            continue

        in_summary = True
        summary_lines.append(stripped)

    if not summary_lines:
        return None

    # Re-join wrapped lines into a single space-separated string.
    return ' '.join(summary_lines)


def load_readme(directory):
    """Return the text of README.md in directory, or None if it doesn't exist."""
    readme_path = os.path.join(directory, 'README.md')
    if os.path.isfile(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as file:
            return file.read()
    return None


def get_rfc_summary(directory):
    """Read one RFC directory and return its data for the listing table.

    Extracts:
    - The H1 title (used as the table Summary column)
    - The first paragraph under ## Purpose (used as the description)
    - The Last modified timestamp (used for sorting and display)

    Returns:
        tuple: (summary_dict, warnings) where summary_dict is None if the
        README couldn't be read or had no H1 title.
    """
    warnings = []
    readme_content = load_readme(directory)
    if not readme_content:
        warnings.append('README.md not found')
        return (None, warnings)

    lines = readme_content.splitlines()

    # Find the H1 title line (e.g. "# RFC 056: Prismic ETL pipeline").
    first_heading = None
    heading_index = None
    for idx, line in enumerate(lines):
        if line.startswith('# '):
            first_heading = line[2:].strip()
            heading_index = idx
            break

    if not first_heading or heading_index is None:
        warnings.append('missing top-level title (# ...)')
        return (None, warnings)

    # Find the Last modified timestamp anywhere after the H1.
    last_modified_value = None
    last_modified_dt = None
    for candidate in lines[heading_index + 1:]:
        match = LAST_MODIFIED_PATTERN.match(candidate)
        if not match:
            continue

        parsed = parse_iso_datetime(match.group(1))
        if parsed is None:
            warnings.append(f"invalid Last modified value: {match.group(1)!r}")
            continue

        last_modified_value = match.group(1).strip()
        last_modified_dt = parsed
        break

    if last_modified_value is None or last_modified_dt is None:
        warnings.append('missing or invalid Last modified metadata')

    # Extract the first prose paragraph under ## Purpose for the table.
    purpose_summary = extract_section_summary(lines, heading_index, ['Purpose'])
    if not purpose_summary:
        warnings.append('missing Purpose summary paragraph')

    summary = {
        'id': os.path.basename(directory),
        'summary': first_heading,
        'next_line': purpose_summary or '',
        'last_modified_value': last_modified_value,
        'last_modified_dt': last_modified_dt,
    }

    return (summary, warnings)

def list_rfc_directories(rfcs_directory):
    """Return a sorted list of subdirectory names within rfcs_directory."""
    if not os.path.isdir(rfcs_directory):
        print(f"{rfcs_directory} is not a valid directory.")
        return []
    return sorted([
        item for item in os.listdir(rfcs_directory)
        if os.path.isdir(os.path.join(rfcs_directory, item))
    ])


def collect_rfcs(rfcs_directory):
    """Collect summary data for every RFC directory, returning (rfcs, warnings)."""
    rfcs = []
    warnings = []
    for rfc_dir in list_rfc_directories(rfcs_directory):
        directory_path = os.path.join(rfcs_directory, rfc_dir)
        summary, rfc_warnings = get_rfc_summary(directory_path)

        for warning in rfc_warnings:
            warnings.append(f"RFC: {rfc_dir} - {warning}")

        if summary is not None:
            rfcs.append(summary)

    return (rfcs, warnings)


def escape_cell(value):
    """Escape markdown table cell content."""
    compact = ' '.join(value.split())
    return compact.replace('|', r'\|')


def build_rfc_table_lines(rfcs):
    """Build the markdown table rows for the RFC listing in rfcs/README.md.

    Each row links the RFC ID to its README, shows the H1 title, the first
    paragraph of the Purpose section, and the Last modified timestamp.
    """
    lines = [
        '| RFC ID | Summary | Next Line | Last Modified |',
        '|--------|---------|-----------|---------------|',
    ]

    for rfc in rfcs:
        rfc_id = escape_cell(rfc['id'])
        summary = escape_cell(rfc['summary'])
        next_line = escape_cell(rfc['next_line'])
        last_modified = escape_cell(
            f"**Last modified:** {rfc['last_modified_value'] or 'MISSING'}"
        )
        readme_link = f"[{rfc_id}]({os.path.join(rfc['id'], 'README.md')})"
        lines.append(
            f"| {readme_link} | {summary} | {next_line} | {last_modified} |"
        )

    return lines


def update_rfc_readme_table(readme_path, table_lines):
    """
    Replace the RFC listing table in rfcs/README.md.

    Returns:
        bool: True if update was written, False otherwise.
    """
    if not os.path.isfile(readme_path):
        return False

    with open(readme_path, 'r', encoding='utf-8') as file:
        lines = file.read().splitlines()

    listing_index = None
    for idx, line in enumerate(lines):
        if line.strip() == '## RFC Listing':
            listing_index = idx
            break

    if listing_index is None:
        return False

    table_start = None
    for idx in range(listing_index + 1, len(lines)):
        if lines[idx].startswith('| RFC ID |'):
            table_start = idx
            break

    if table_start is None:
        return False

    table_end = table_start
    while table_end < len(lines) and lines[table_end].startswith('|'):
        table_end += 1

    updated_lines = lines[:table_start] + table_lines + lines[table_end:]
    with open(readme_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(updated_lines) + '\n')

    return True


def is_rfc_readme_table_in_sync(readme_path, table_lines):
    """
    Check whether the RFC listing table in rfcs/README.md is already in sync.

    Returns:
        bool: True if table content matches generated table_lines, False otherwise.
    """
    if not os.path.isfile(readme_path):
        return False

    with open(readme_path, 'r', encoding='utf-8') as file:
        lines = file.read().splitlines()

    listing_index = None
    for idx, line in enumerate(lines):
        if line.strip() == '## RFC Listing':
            listing_index = idx
            break

    if listing_index is None:
        return False

    table_start = None
    for idx in range(listing_index + 1, len(lines)):
        if lines[idx].startswith('| RFC ID |'):
            table_start = idx
            break

    if table_start is None:
        return False

    table_end = table_start
    while table_end < len(lines) and lines[table_end].startswith('|'):
        table_end += 1

    existing_table_lines = lines[table_start:table_end]
    return existing_table_lines == table_lines


def parse_args():
    parser = argparse.ArgumentParser(description='Generate RFC summary markdown table.')
    parser.add_argument(
        '--rfcs-directory',
        default='./rfcs',
        help='Path to the RFC directory (default: ./rfcs)',
    )
    parser.add_argument(
        '--readme-path',
        default='./rfcs/README.md',
        help='Path to RFC README for --write-readme mode',
    )
    parser.add_argument(
        '--write-readme',
        action='store_true',
        help='Update the RFC table directly in the README file',
    )
    parser.add_argument(
        '--check-readme',
        action='store_true',
        help='Fail if RFC README table is not in sync with generated content',
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Exit with non-zero status if any warnings are detected',
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Collect data from every RFC directory under rfcs/.
    rfcs, warnings = collect_rfcs(args.rfcs_directory)
    errors = []

    # Only include RFCs that have a parseable Last modified date; sort them
    # most-recently-modified first, with RFC ID as a tiebreaker.
    valid_rfcs = [rfc for rfc in rfcs if rfc['last_modified_dt'] is not None]
    valid_rfcs.sort(key=lambda x: (-x['last_modified_dt'].timestamp(), x['id']))

    table_lines = build_rfc_table_lines(valid_rfcs)

    if args.write_readme:
        # Regenerate the table in rfcs/README.md in place.
        updated = update_rfc_readme_table(args.readme_path, table_lines)
        if updated:
            print(f"✓ Updated RFC table in {args.readme_path} ({len(valid_rfcs)} RFCs)")
        else:
            errors.append(f"Failed to update README table at {args.readme_path}")
    elif args.check_readme:
        # Used by CI: fail if the committed table doesn't match what would be generated.
        in_sync = is_rfc_readme_table_in_sync(args.readme_path, table_lines)
        if not in_sync:
            errors.append(
                "RFC README table is out of sync: run '.scripts/create_table_summary.py --write-readme'"
            )
    else:
        # Default: just print the table to stdout.
        print('\n'.join(table_lines))

    for warning in warnings:
        print(warning, file=sys.stderr)
    for error in errors:
        print(error, file=sys.stderr)

    if errors:
        return 1
    if args.strict and warnings:
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())



