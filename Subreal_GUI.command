#!/bin/bash

# Set terminal title
echo -ne "\033]0;Subreal Engine Console GUI\007"

# Clear screen and show banner
clear
echo ""
echo "========================================"
echo "   Subreal Engine Console GUI"
echo "========================================"
echo "Starting application..."
echo ""

# Change to the script directory
cd "$(dirname "$0")"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "ERROR: Python is not installed or not in PATH"
    echo "Please install Python 3.7 or higher"
    echo "Visit: https://www.python.org/downloads/"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Determine which Python command to use
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
    echo "ERROR: Python 3.7 or higher is required"
    echo "Current version: $($PYTHON_CMD --version)"
    echo "Please update Python"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if the main script exists
if [ ! -f "subreal_gui.py" ]; then
    echo "ERROR: subreal_gui.py not found in current directory"
    echo "Make sure you're running this from the correct folder"
    echo "Current directory: $(pwd)"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Run the Python GUI
$PYTHON_CMD subreal_gui.py

# Check exit status
EXIT_STATUS=$?
if [ $EXIT_STATUS -ne 0 ]; then
    echo ""
    echo "Application exited with an error (code: $EXIT_STATUS)."
    read -p "Press Enter to exit..."
else
    echo ""
    echo "Application closed normally."
    sleep 2
fi