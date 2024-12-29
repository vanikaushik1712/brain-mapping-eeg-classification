#!/bin/bash
# Setup script for Brain Mapping EEG Classification System

echo "Setting up Brain Mapping EEG Classification System..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Generate synthetic data
echo "Generating synthetic EEG data..."
python signal_generator.py

echo "Setup complete! Run 'python app.py' to start the application."
