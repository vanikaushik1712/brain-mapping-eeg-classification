#!/usr/bin/env python
"""
Data Exploration Notebook for Brain Mapping EEG Classification
Interactive analysis of EEG patterns and classification performance
"""

import matplotlib.pyplot as plt
import numpy as np
from eeg_processor import EEGProcessor
from signal_generator import EEGSignalGenerator
import seaborn as sns

def explore_frequency_bands():
    """Explore EEG frequency bands"""
    generator = EEGSignalGenerator()
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    bands = ['delta', 'theta', 'alpha', 'beta', 'gamma']
    for i, band in enumerate(bands):
        row = i // 3
        col = i % 3
        
        freq_range = generator.bands[band]
        signal = generator.generate_brain_wave(freq_range)
        
        axes[row, col].plot(generator.t[:1000], signal[:1000])
        axes[row, col].set_title(f'{band.title()} Wave ({freq_range[0]}-{freq_range[1]} Hz)')
        axes[row, col].set_xlabel('Time (s)')
        axes[row, col].set_ylabel('Amplitude')
    
    # Remove empty subplot
    axes[1, 2].remove()
    
    plt.tight_layout()
    plt.savefig('docs/images/frequency_bands_analysis.png', dpi=150)
    plt.show()

def analyze_classification_patterns():
    """Analyze classification patterns across different thresholds"""
    processor = EEGProcessor()
    
    # Test different thresholds
    thresholds = [200, 400, 600, 800, 1000]
    normal_classifications = []
    
    # Mock test for demonstration
    test_mse_values = [300, 450, 550, 750, 950]
    
    for threshold in thresholds:
        normal_count = sum(1 for mse in test_mse_values if mse < threshold)
        normal_classifications.append(normal_count)
    
    plt.figure(figsize=(10, 6))
    plt.plot(thresholds, normal_classifications, 'bo-', linewidth=2, markersize=8)
    plt.xlabel('Classification Threshold')
    plt.ylabel('Number of Normal Classifications')
    plt.title('Threshold Sensitivity Analysis')
    plt.grid(True, alpha=0.3)
    plt.savefig('docs/images/threshold_analysis.png', dpi=150)
    plt.show()

if __name__ == "__main__":
    print("Starting EEG Data Exploration...")
    explore_frequency_bands()
    analyze_classification_patterns()
    print("Exploration complete!")
