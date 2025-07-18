#!/usr/bin/env python
"""Data validation utilities for EEG datasets"""

import os
from PIL import Image
import numpy as np

def validate_eeg_dataset(data_dir):
    """Validate EEG dataset integrity"""
    print(f"Validating dataset in {data_dir}...")
    
    ref_dir = os.path.join(data_dir, 'reference_signals')
    test_dir = os.path.join(data_dir, 'test_samples')
    
    issues = []
    
    # Check reference signals
    if os.path.exists(ref_dir):
        ref_files = [f for f in os.listdir(ref_dir) if f.endswith('.png')]
        if len(ref_files) < 5:
            issues.append(f"Only {len(ref_files)} reference patterns found, expected 5")
        
        for filename in ref_files:
            filepath = os.path.join(ref_dir, filename)
            try:
                img = Image.open(filepath)
                if img.size != (256, 256):
                    issues.append(f"{filename}: Invalid size {img.size}, expected (256, 256)")
            except Exception as e:
                issues.append(f"{filename}: Cannot open image - {e}")
    else:
        issues.append("Reference signals directory not found")
    
    # Check test samples
    if os.path.exists(test_dir):
        test_files = [f for f in os.listdir(test_dir) if f.endswith('.png')]
        if len(test_files) == 0:
            issues.append("No test samples found")
    else:
        issues.append("Test samples directory not found")
    
    if issues:
        print("Validation failed:")
        for issue in issues:
            print(f"- {issue}")
        return False
    else:
        print("Dataset validation passed!")
        return True

if __name__ == "__main__":
    validate_eeg_dataset('data')
