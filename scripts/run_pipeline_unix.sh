#!/usr/bin/env bash
set -u

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR" || exit 1

echo "============================================================"
echo "PHOTO-CAT - Pipeline"
echo "============================================================"
echo "Project folder: $PROJECT_DIR"
echo "Configuration:  $PROJECT_DIR/config.yaml"
echo

PYTHON_EXE="./.venv/bin/python"
if [ ! -x "$PYTHON_EXE" ]; then
    echo "ERROR: the local virtual environment was not found."
    echo "Run sh START_UNIX.sh first so PHOTO-CAT can create .venv and install libraries."
    echo
    printf "Press Enter to close this window..."
    read -r _
    exit 1
fi

"$PYTHON_EXE" "src/config_and_run.py"
STATUS=$?

echo
if [ "$STATUS" -eq 0 ]; then
    echo "============================================================"
    echo "PHOTO-CAT finished successfully."
    echo "Check the configured output folder for the results."
    echo "============================================================"
else
    echo "============================================================"
    echo "PHOTO-CAT stopped because of an error."
    echo "Read the message above, fix the configuration, then try again."
    echo "============================================================"
fi

echo
printf "Press Enter to close this window..."
read -r _
exit "$STATUS"
