#!/usr/bin/env python3

import os

def load_readme(directory):
    """
    Load the README.md file from the specified directory.

    Args:
        directory (str): The path to the directory where README.md is expected.

    Returns:
        str: The content of README.md if found, otherwise None.
    """
    readme_path = os.path.join(directory, 'README.md')
    if os.path.isfile(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as file:
            return file.read()
    return None

def get_rfc_summary(directory):
    """
    Extract the first line of the README.md file after the first heading,
    the following summary paragraph, and the last modified line.

    Args:
        directory (str): The path to the directory where README.md is expected.

    Returns:
        tuple: (first_line, next_line, last_modified) or None if not found.
    """
    readme_content = load_readme(directory)
    if not readme_content:
        return None

    lines = readme_content.splitlines()
    first_line = None
    next_line = []
    last_modified = None

    for idx, line in enumerate(lines):
        if line.startswith('# '):
            first_line = line[2:].strip()
            # Collect summary paragraph (lines after heading, skipping empty lines)
            for next_line_candidate in lines[idx + 1:]:
                if next_line_candidate.strip() == '':
                    if next_line:  # Stop at first empty line after collecting summary
                        break
                    continue
                if next_line_candidate.startswith('**'):
                    last_modified = next_line_candidate.strip()
                    break
                next_line.append(next_line_candidate.strip())
            # If last_modified not found in above loop, search further
            if last_modified is None:
                for next_line_candidate in lines[idx + 1:]:
                    if next_line_candidate.startswith('**'):
                        last_modified = next_line_candidate.strip()
                        break
            break

    if not (first_line and next_line and last_modified):
        return None
    return (first_line, ' '.join(next_line), last_modified)

def list_rfc_directories(rfcs_directory):
    """
    List all RFC directories in the given rfcs_directory.

    Args:
        rfcs_directory (str): Path to the rfcs directory.

    Returns:
        list: List of RFC directory names.
    """
    if not os.path.isdir(rfcs_directory):
        print(f"{rfcs_directory} is not a valid directory.")
        return []
    return [
        item for item in os.listdir(rfcs_directory)
        if os.path.isdir(os.path.join(rfcs_directory, item))
    ]

def collect_rfcs(rfcs_directory):
    """
    Collect RFC summaries from all RFC directories.

    Args:
        rfcs_directory (str): Path to the rfcs directory.

    Returns:
        list: List of RFC summary dicts.
    """
    rfcs = []
    rfc_dirs = list_rfc_directories(rfcs_directory)
    for rfc_dir in rfc_dirs:
        summary = get_rfc_summary(os.path.join(rfcs_directory, rfc_dir))
        if summary:
            first_line, next_line, last_modified = summary
            rfcs.append({
                "id": rfc_dir,
                "summary": first_line,
                "next_line": next_line,
                "last_modified": last_modified
            })
        else:
            print(f"RFC: {rfc_dir} - No summary found.")
    return rfcs

def print_rfc_table(rfcs, rfcs_directory):
    """
    Print the RFC summaries in a markdown table format.

    Args:
        rfcs (list): List of RFC summary dicts.
        rfcs_directory (str): Path to the rfcs directory.
    """
    print("| RFC ID | Summary | Next Line | Last Modified |")
    print("|--------|---------|-----------|---------------|")
    for rfc in rfcs:
        rfc_id = rfc["id"]
        summary = rfc["summary"]
        next_line = rfc["next_line"]
        last_modified = rfc["last_modified"]
        readme_link = f"[{rfc_id}]({os.path.join(rfc_id, 'README.md')})"
        print(f"| {readme_link} | {summary} | {next_line} | {last_modified} |")

def main():
    rfcs_directory = './rfcs'
    rfcs = collect_rfcs(rfcs_directory)
    # Sort rfcs by last_modified date (string sort, may need datetime for strictness)
    rfcs.sort(key=lambda x: x["last_modified"], reverse=True)
    print_rfc_table(rfcs, rfcs_directory)

if __name__ == "__main__":
    main()



