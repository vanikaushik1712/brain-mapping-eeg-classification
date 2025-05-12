#!/usr/bin/env python
"""Unit tests for Signal Generator module"""

import pytest
import numpy as np
from signal_generator import EEGSignalGenerator

class TestEEGSignalGenerator:
    def setup_method(self):
        self.generator = EEGSignalGenerator()
    
    def test_initialization(self):
        assert self.generator.fs == 256
        assert self.generator.duration == 10
        assert len(self.generator.t) == 256 * 10
    
    def test_generate_brain_wave(self):
        wave = self.generator.generate_brain_wave((8, 12), amplitude=1.0)
        assert len(wave) == len(self.generator.t)
        assert isinstance(wave, np.ndarray)
    
    def test_generate_normal_eeg(self):
        signal = self.generator.generate_normal_eeg()
        assert len(signal) == len(self.generator.t)
        assert isinstance(signal, np.ndarray)

if __name__ == '__main__':
    pytest.main([__file__])
