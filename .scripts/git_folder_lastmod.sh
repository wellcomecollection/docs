#!/bin/bash

# Script to determine the last Git modification date for any file within a specified folder.

# --- Configuration ---
# Use committer date (c) or author date (a). ISO 8601 format (I).
# %cI: committer date, ISO 8601 format (recommended for "when integrated")
# %aI: author date, ISO 8601 format (when originally written)
GIT_DATE_FORMAT="%cI"

# --- Functions ---
usage() {
    echo "Usage: $0 <folder_path>"
    echo "Description: Determines the date of the last Git commit that modified"
    echo "             any file within the specified folder."
    echo "The folder path should be a path to a directory, either relative to the"
    echo "current working directory or an absolute path."
    exit 1
}

# --- Argument Parsing ---
if [ -z "$1" ] || [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    usage
fi

FOLDER_PATH="$1"

# --- Validations ---
# 1. Check if the current directory is inside a Git repository's working tree.
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "Error: Not inside a Git repository."
    echo "Please run this script from within a Git repository that contains the target folder."
    exit 1
fi

# 2. Check if the provided path is actually a directory on the filesystem.
# This helps catch typos or if the user points to a file when expecting a folder.
if [ ! -d "$FOLDER_PATH" ]; then
    echo "Error: Path '$FOLDER_PATH' is not a directory or does not exist on the filesystem."
    exit 1
fi

# --- Main Logic ---
# Get the specified date of the last commit affecting the folder path.
# The '--' is crucial to separate paths from revisions if FOLDER_PATH could resemble a branch/tag name.
# We redirect stderr to /dev/null to suppress "does not have any commits yet" messages for new paths,
# and check the exit code and output.
LAST_MODIFIED_OUTPUT=$(git log -1 --format="$GIT_DATE_FORMAT" -- "$FOLDER_PATH" 2>/dev/null)
GIT_LOG_EXIT_CODE=$?

if [ $GIT_LOG_EXIT_CODE -ne 0 ]; then
    # This can happen for various git errors, not just "no history for path".
    # For example, if FOLDER_PATH has an invalid pathspec format (though '--' helps).
    # Or if the repository itself is in a bad state.
    echo "Error: 'git log' command failed for path '$FOLDER_PATH'."
    # You could re-run without 2>/dev/null to show the specific git error if needed for debugging:
    # echo "--- Git Error Output ---"
    # git log -1 --format="$GIT_DATE_FORMAT" -- "$FOLDER_PATH"
    # echo "------------------------"
    exit 1
fi

# Check if any commit history was found for the path
if [ -z "$LAST_MODIFIED_OUTPUT" ]; then
    # This typically means no commits in the current branch's history have affected this path.
    echo "Info: No Git commit history found that modified files within '$FOLDER_PATH'."
    echo "      This could mean:"
    echo "      1. The folder or files within it are not tracked by Git (e.g., new, untracked, or in .gitignore)."
    echo "      2. The folder and its contents have never been committed to the current branch's history."
    echo "      3. The path '$FOLDER_PATH' might be misspelled or does not correspond to any tracked content."

    # Provide a hint by checking if any files are actually tracked under that path
    TRACKED_FILES_COUNT=$(git ls-files -- "$FOLDER_PATH" 2>/dev/null | wc -l)
    if [ "$TRACKED_FILES_COUNT" -eq 0 ]; then
         echo "      Hint: No files seem to be currently tracked by Git under '$FOLDER_PATH'."
    fi

    # generate a last modified date in ISO 8601 format for consistency
    LAST_MODIFIED_OUTPUT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo "If you need a last modified date, using the current date: $LAST_MODIFIED_OUTPUT"
    echo ""
    echo "**Last modified:** $LAST_MODIFIED_OUTPUT"

    # Reporting "no modification found" is a valid outcome of the query, so exit 0.
    exit 0
else
    echo "**Last modified:** $LAST_MODIFIED_OUTPUT"

    # Optional: Uncomment to show more details about the commit
    # echo ""
    # echo "--- Commit Details ---"
    # git log -1 --pretty="format:Commit:  %h%nAuthor:  %an <%ae>%nDate:    %ad%nSubject: %s" --date="format-local:%Y-%m-%d %H:%M:%S %Z" -- "$FOLDER_PATH"
    # echo "----------------------"
fi

exit 0