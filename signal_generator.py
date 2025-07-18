#!/usr/bin/env python
"""
EEG Signal Generator for Brain Mapping Project
Generates synthetic EEG signals and converts them to spectrogram images
Based on 2013 Brain Mapping using MATLAB Technology project
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy import signal
import os
from PIL import Image

class EEGSignalGenerator:
    def __init__(self, fs=256, duration=10):
        """
        Initialize EEG Signal Generator
        
        Args:
            fs: Sampling frequency (Hz) - typical EEG sampling rate
            duration: Signal duration in seconds
        """
        self.fs = fs
        self.duration = duration
        self.t = np.linspace(0, duration, fs * duration)
        
        # EEG frequency bands (Hz)
        self.bands = {
            'delta': (0.5, 4),
            'theta': (4, 8),
            'alpha': (8, 12),
            'beta': (12, 30),
            'gamma': (30, 50)
        }
    
    def generate_brain_wave(self, freq_range, amplitude=1.0, noise_level=0.1):
        """
        Generate a single brain wave component
        
        Args:
            freq_range: Tuple of (low_freq, high_freq)
            amplitude: Wave amplitude
            noise_level: Noise level to add
        """
        # Random frequency within the range
        freq = np.random.uniform(freq_range[0], freq_range[1])
        
        # Generate sine wave with some phase variation
        phase = np.random.uniform(0, 2 * np.pi)
        wave = amplitude * np.sin(2 * np.pi * freq * self.t + phase)
        
        # Add some amplitude modulation for realism
        modulation_freq = np.random.uniform(0.1, 0.5)
        modulation = 0.3 * np.sin(2 * np.pi * modulation_freq * self.t)
        wave = wave * (1 + modulation)
        
        # Add noise
        noise = noise_level * np.random.randn(len(self.t))
        return wave + noise
    
    def generate_normal_eeg(self):
        """
        Generate a normal EEG signal with typical frequency distribution
        """
        eeg_signal = np.zeros(len(self.t))
        
        # Normal EEG characteristics:
        # - Moderate alpha waves (relaxed state)
        # - Some beta waves (active thinking)
        # - Low delta waves (should be minimal in awake state)
        # - Some theta waves
        
        eeg_signal += self.generate_brain_wave(self.bands['alpha'], amplitude=2.0, noise_level=0.2)
        eeg_signal += self.generate_brain_wave(self.bands['beta'], amplitude=1.5, noise_level=0.15)
        eeg_signal += self.generate_brain_wave(self.bands['theta'], amplitude=1.0, noise_level=0.1)
        eeg_signal += self.generate_brain_wave(self.bands['delta'], amplitude=0.5, noise_level=0.05)
        
        return eeg_signal
    
    def generate_abnormal_eeg(self, abnormality_type='high_delta'):
        """
        Generate an abnormal EEG signal with specific abnormalities
        
        Args:
            abnormality_type: Type of abnormality
                - 'high_delta': Excessive delta waves (sleep disorder, brain damage)
                - 'missing_alpha': Missing or reduced alpha waves
                - 'high_beta': Excessive beta waves (anxiety, medication effects)
        """
        eeg_signal = np.zeros(len(self.t))
        
        if abnormality_type == 'high_delta':
            # Excessive delta waves - often indicates brain damage or deep sleep
            eeg_signal += self.generate_brain_wave(self.bands['delta'], amplitude=4.0, noise_level=0.3)
            eeg_signal += self.generate_brain_wave(self.bands['theta'], amplitude=2.0, noise_level=0.2)
            eeg_signal += self.generate_brain_wave(self.bands['alpha'], amplitude=0.5, noise_level=0.1)
            eeg_signal += self.generate_brain_wave(self.bands['beta'], amplitude=0.8, noise_level=0.1)
            
        elif abnormality_type == 'missing_alpha':
            # Missing alpha waves - can indicate various neurological conditions
            eeg_signal += self.generate_brain_wave(self.bands['beta'], amplitude=2.5, noise_level=0.2)
            eeg_signal += self.generate_brain_wave(self.bands['theta'], amplitude=1.8, noise_level=0.15)
            eeg_signal += self.generate_brain_wave(self.bands['delta'], amplitude=1.0, noise_level=0.1)
            # Minimal alpha
            eeg_signal += self.generate_brain_wave(self.bands['alpha'], amplitude=0.2, noise_level=0.05)
            
        elif abnormality_type == 'high_beta':
            # Excessive beta waves - anxiety, stimulants, or certain medications
            eeg_signal += self.generate_brain_wave(self.bands['beta'], amplitude=4.0, noise_level=0.3)
            eeg_signal += self.generate_brain_wave(self.bands['alpha'], amplitude=1.0, noise_level=0.1)
            eeg_signal += self.generate_brain_wave(self.bands['theta'], amplitude=0.8, noise_level=0.1)
            eeg_signal += self.generate_brain_wave(self.bands['delta'], amplitude=0.3, noise_level=0.05)
        
        return eeg_signal
    
    def signal_to_spectrogram(self, eeg_signal, save_path=None):
        """
        Convert EEG signal to spectrogram image
        
        Args:
            eeg_signal: 1D EEG signal
            save_path: Path to save the spectrogram image
        
        Returns:
            2D spectrogram data
        """
        # Compute spectrogram
        nperseg = 128  # Window size
        noverlap = 64  # Overlap
        
        f, t, Sxx = signal.spectrogram(eeg_signal, 
                                     fs=self.fs, 
                                     window='hann',
                                     nperseg=nperseg, 
                                     noverlap=noverlap)
        
        # Limit frequency range to typical EEG range (0-50 Hz)
        freq_mask = f <= 50
        f = f[freq_mask]
        Sxx = Sxx[freq_mask, :]
        
        # Convert to dB scale
        Sxx_db = 10 * np.log10(Sxx + 1e-10)
        
        # Create the plot
        plt.figure(figsize=(8, 6))
        plt.pcolormesh(t, f, Sxx_db, shading='gouraud', cmap='gray')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.title('EEG Spectrogram')
        plt.colorbar(label='Power/Frequency (dB/Hz)')
        
        if save_path:
            plt.savefig(save_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            # Convert to grayscale and resize to 256x256 as per original project
            img = Image.open(save_path)
            img = img.convert('L')  # Convert to grayscale
            img = img.resize((256, 256))  # Resize to 256x256
            img.save(save_path)
        else:
            plt.show()
        
        return Sxx_db
    
    def generate_dataset(self, output_dir):
        """
        Generate a complete dataset of normal and abnormal EEG patterns
        """
        # Ensure output directories exist
        normal_dir = os.path.join(output_dir, 'reference_signals')
        test_dir = os.path.join(output_dir, 'test_samples')
        
        os.makedirs(normal_dir, exist_ok=True)
        os.makedirs(test_dir, exist_ok=True)
        
        print("Generating reference (normal) EEG patterns...")
        # Generate 5 normal reference patterns (as per original project)
        for i in range(5):
            eeg_signal = self.generate_normal_eeg()
            save_path = os.path.join(normal_dir, f'eeg{i+1}n.png')
            self.signal_to_spectrogram(eeg_signal, save_path)
            print(f"Generated normal pattern {i+1}")
        
        print("\nGenerating test samples...")
        # Generate 3 normal test samples
        for i in range(3):
            eeg_signal = self.generate_normal_eeg()
            save_path = os.path.join(test_dir, f'test_normal_{i+1}.png')
            self.signal_to_spectrogram(eeg_signal, save_path)
            print(f"Generated normal test sample {i+1}")
        
        # Generate 3 abnormal test samples
        abnormalities = ['high_delta', 'missing_alpha', 'high_beta']
        for i, abnormality in enumerate(abnormalities):
            eeg_signal = self.generate_abnormal_eeg(abnormality)
            save_path = os.path.join(test_dir, f'test_abnormal_{abnormality}.png')
            self.signal_to_spectrogram(eeg_signal, save_path)
            print(f"Generated abnormal test sample: {abnormality}")
        
        print(f"\nDataset generation complete!")
        print(f"Reference patterns saved to: {normal_dir}")
        print(f"Test samples saved to: {test_dir}")


if __name__ == "__main__":
    # Generate the dataset
    generator = EEGSignalGenerator()
    generator.generate_dataset('data')