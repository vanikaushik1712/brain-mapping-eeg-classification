#!/bin/bash
# Test runner script for Brain Mapping EEG Classification System

echo "Running Brain Mapping EEG Classification System Tests..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run different types of tests
echo "Running unit tests..."
pytest tests/test_eeg_processor.py tests/test_signal_generator.py -v

echo "Running integration tests..."
pytest tests/test_app.py -v

echo "Running performance benchmarks..."
python benchmark/speed_test.py

echo "Code quality checks..."
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
black . --check

echo "All tests completed!"
