#!/usr/bin/env python
"""
Unit tests for EEG Processor module
Brain Mapping EEG Classification System
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch
import os

# Import the module to test
from eeg_processor import EEGProcessor


class TestEEGProcessor:
    """Test cases for EEGProcessor class"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.processor = EEGProcessor()
        self.test_image_data = np.random.rand(256, 256)
    
    def test_initialization(self):
        """Test EEGProcessor initialization"""
        assert self.processor.wavelet == 'db1'
        assert self.processor.levels == 3
        assert len(self.processor.reference_patterns) == 0
        assert len(self.processor.reference_transforms) == 0
    
    def test_custom_initialization(self):
        """Test EEGProcessor with custom parameters"""
        processor = EEGProcessor(wavelet='db4', levels=4, threshold=800)
        assert processor.wavelet == 'db4'
        assert processor.levels == 4
    
    def test_apply_2d_dwt(self):
        """Test 2D DWT application"""
        result = self.processor.apply_2d_dwt(self.test_image_data)
        assert result is not None
        assert isinstance(result, np.ndarray)
        assert result.shape[0] > 0
        assert result.shape[1] > 0
    
    def test_calculate_mse(self):
        """Test MSE calculation"""
        img1 = np.ones((100, 100))
        img2 = np.zeros((100, 100))
        mse = self.processor.calculate_mse(img1, img2)
        assert mse == 1.0
        
        # Test identical images
        mse_identical = self.processor.calculate_mse(img1, img1)
        assert mse_identical == 0.0
    
    def test_calculate_mse_different_shapes(self):
        """Test MSE calculation with different image shapes"""
        img1 = np.ones((100, 100))
        img2 = np.zeros((50, 50))
        mse = self.processor.calculate_mse(img1, img2)
        assert isinstance(mse, float)
        assert mse >= 0
    
    @patch('os.path.exists')
    @patch('os.listdir')
    def test_load_reference_database_empty(self, mock_listdir, mock_exists):
        """Test loading reference database from empty directory"""
        mock_exists.return_value = True
        mock_listdir.return_value = []
        
        self.processor.load_reference_database('fake_dir')
        assert len(self.processor.reference_patterns) == 0
        assert len(self.processor.reference_transforms) == 0
    
    def test_dwt_with_invalid_input(self):
        """Test DWT with invalid input"""
        result = self.processor.apply_2d_dwt(None)
        assert result is None
    
    def test_load_image_nonexistent(self):
        """Test loading non-existent image"""
        result = self.processor.load_image('nonexistent_file.png')
        assert result is None


class TestEEGProcessorIntegration:
    """Integration tests for EEGProcessor"""
    
    def setup_method(self):
        """Setup integration test fixtures"""
        self.processor = EEGProcessor()
    
    def test_full_classification_pipeline(self):
        """Test complete classification pipeline with mock data"""
        # Create mock reference data
        mock_ref_transforms = [np.random.rand(128, 128) for _ in range(3)]
        self.processor.reference_transforms = mock_ref_transforms
        
        # Mock the image loading and DWT application
        with patch.object(self.processor, 'load_image') as mock_load:
            with patch.object(self.processor, 'apply_2d_dwt') as mock_dwt:
                mock_load.return_value = np.random.rand(256, 256)
                mock_dwt.return_value = np.random.rand(128, 128)
                
                result = self.processor.classify_eeg_pattern('test_image.png')
                
                assert 'classification' in result
                assert 'confidence' in result
                assert 'min_mse' in result
                assert result['classification'] in ['Normal', 'Abnormal']


if __name__ == '__main__':
    pytest.main([__file__])