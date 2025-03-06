#!/usr/bin/env python
"""
Basic usage example for Brain Mapping EEG Classification System
"""

from eeg_processor import EEGProcessor
from signal_generator import EEGSignalGenerator

def main():
    print("Brain Mapping EEG Classification - Basic Usage Example")
    
    # 1. Generate synthetic data
    print("\n1. Generating synthetic EEG data...")
    generator = EEGSignalGenerator()
    generator.generate_dataset('example_data')
    
    # 2. Initialize processor
    print("\n2. Initializing EEG processor...")
    processor = EEGProcessor()
    processor.load_reference_database('example_data/reference_signals')
    
    # 3. Classify a test pattern
    print("\n3. Classifying test pattern...")
    result = processor.classify_eeg_pattern('example_data/test_samples/test_normal_1.png')
    
    print(f"Classification: {result['classification']}")
    print(f"Confidence: {result['confidence']}")
    print(f"MSE: {result['min_mse']:.2f}")

if __name__ == "__main__":
    main()
