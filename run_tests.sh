#!/bin/bash

# Activate virtual environment (if you had one)
# source venv/bin/activate

# Run tests
pytest test_app.py

# Check result
if [ $? -eq 0 ]; then
  echo "All tests passed ✅"
  exit 0
else
  echo "Tests failed ❌"
  exit 1
fi
