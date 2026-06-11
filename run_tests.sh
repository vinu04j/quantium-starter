#!/bin/bash

# Activate virtual environment
source venv/Scripts/activate

# Execute test suite
python -m pytest

# Return correct exit code
if [ $? -eq 0 ]; then
    echo "All tests passed."
    exit 0
else
    echo "Tests failed."
    exit 1
fi
