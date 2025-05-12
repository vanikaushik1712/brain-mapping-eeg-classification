#!/usr/bin/env python
"""Performance benchmarking for EEG classification"""

import time
import numpy as np
from eeg_processor import EEGProcessor

def benchmark_classification():
    processor = EEGProcessor()
    
    # Mock reference data
    processor.reference_transforms = [np.random.rand(128, 128) for _ in range(5)]
    
    # Benchmark classification speed
    times = []
    for i in range(10):
        start = time.time()
        test_data = np.random.rand(256, 256)
        transform = processor.apply_2d_dwt(test_data)
        end = time.time()
        times.append(end - start)
    
    print(f"Average processing time: {np.mean(times):.3f}s")
    print(f"Min time: {np.min(times):.3f}s")
    print(f"Max time: {np.max(times):.3f}s")

if __name__ == "__main__":
    benchmark_classification()
