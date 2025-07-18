#!/usr/bin/env python
"""Data analysis tools for EEG classification performance"""

import matplotlib.pyplot as plt
import numpy as np
from eeg_processor import EEGProcessor
import os

def analyze_classification_performance():
    """Analyze performance across test samples"""
    processor = EEGProcessor()
    processor.load_reference_database('data/reference_signals')
    
    results = []
    test_dir = 'data/test_samples'
    
    if not os.path.exists(test_dir):
        print("No test samples found. Run signal_generator.py first.")
        return
    
    for filename in os.listdir(test_dir):
        if filename.endswith('.png'):
            filepath = os.path.join(test_dir, filename)
            result = processor.classify_eeg_pattern(filepath)
            results.append({
                'filename': filename,
                'classification': result['classification'],
                'mse': result['min_mse'],
                'confidence': float(result['confidence'].strip('%'))
            })
    
    # Generate analysis plots
    plt.figure(figsize=(12, 8))
    
    # MSE distribution
    plt.subplot(2, 2, 1)
    mse_values = [r['mse'] for r in results]
    plt.hist(mse_values, bins=10, alpha=0.7)
    plt.xlabel('MSE Value')
    plt.ylabel('Frequency')
    plt.title('MSE Distribution')
    
    # Classification results
    plt.subplot(2, 2, 2)
    classifications = [r['classification'] for r in results]
    unique, counts = np.unique(classifications, return_counts=True)
    plt.pie(counts, labels=unique, autopct='%1.1f%%')
    plt.title('Classification Results')
    
    plt.tight_layout()
    plt.savefig('docs/images/performance_analysis.png', dpi=150)
    print("Performance analysis saved to docs/images/performance_analysis.png")

if __name__ == "__main__":
    analyze_classification_performance()
