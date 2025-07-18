#!/usr/bin/env python
"""
EEG Processor for Brain Mapping Project
Implements 2D Discrete Wavelet Transform for EEG classification
Based on 2013 Brain Mapping using MATLAB Technology project
"""

import numpy as np
import pywt
from PIL import Image
import os
import matplotlib.pyplot as plt

class EEGProcessor:
    def __init__(self, wavelet='db1', levels=3):
        """
        Initialize EEG Processor
        
        Args:
            wavelet: Wavelet type (default: 'db1' as per original project)
            levels: Number of decomposition levels (default: 3)
        """
        self.wavelet = wavelet
        self.levels = levels
        self.reference_patterns = []
        self.reference_transforms = []
        
    def load_image(self, image_path):
        """
        Load and preprocess image
        
        Args:
            image_path: Path to the image file
            
        Returns:
            numpy array of the processed image
        """
        try:
            # Load image and convert to grayscale if needed
            img = Image.open(image_path)
            img = img.convert('L')  # Convert to grayscale
            img = img.resize((256, 256))  # Resize to 256x256 as per original
            
            # Convert to numpy array
            img_array = np.array(img, dtype=np.float64)
            
            return img_array
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None
    
    def apply_2d_dwt(self, image):
        """
        Apply 2D Discrete Wavelet Transform
        Implements the same algorithm as the original MATLAB code
        
        Args:
            image: 2D numpy array representing the image
            
        Returns:
            Reconstructed wavelet coefficients as 2D array
        """
        try:
            # Apply 3-level 2D DWT decomposition (as per original project)
            current_image = image.copy()
            
            # Level 1 decomposition
            coeffs1 = pywt.dwt2(current_image, self.wavelet)
            cA1, (cH1, cV1, cD1) = coeffs1
            
            # Level 2 decomposition on approximation coefficients
            coeffs2 = pywt.dwt2(cA1, self.wavelet)
            cA2, (cH2, cV2, cD2) = coeffs2
            
            # Level 3 decomposition on approximation coefficients
            coeffs3 = pywt.dwt2(cA2, self.wavelet)
            cA3, (cH3, cV3, cD3) = coeffs3
            
            # Reconstruct the wavelet representation as per original MATLAB code:
            # caa = [cA3 cH3; cV3 cD3]
            # ca = [caa cH2; cV2 cD2]  
            # w1 = [ca cH1; cV1 cD1]
            
            # Level 3 reconstruction
            caa = np.block([[cA3, cH3], [cV3, cD3]])
            
            # Level 2 reconstruction  
            ca = np.block([[caa, cH2], [cV2, cD2]])
            
            # Level 1 reconstruction (final wavelet representation)
            w1 = np.block([[ca, cH1], [cV1, cD1]])
            
            return w1
            
        except Exception as e:
            print(f"Error in 2D DWT: {e}")
            return None
    
    def calculate_mse(self, img1, img2):
        """
        Calculate Mean Square Error between two images
        
        Args:
            img1, img2: 2D numpy arrays
            
        Returns:
            MSE value
        """
        if img1.shape != img2.shape:
            # Resize to match if shapes are different
            min_h = min(img1.shape[0], img2.shape[0])
            min_w = min(img1.shape[1], img2.shape[1])
            img1 = img1[:min_h, :min_w]
            img2 = img2[:min_h, :min_w]
        
        # Calculate MSE as per original project
        mse = np.mean((img1 - img2) ** 2)
        return mse
    
    def load_reference_database(self, reference_dir):
        """
        Load reference (normal) EEG patterns from directory
        
        Args:
            reference_dir: Directory containing reference pattern images
        """
        self.reference_patterns = []
        self.reference_transforms = []
        
        # Load reference images (expecting 5 as per original project)
        reference_files = [f for f in os.listdir(reference_dir) if f.endswith('.png') or f.endswith('.bmp')]
        reference_files.sort()  # Ensure consistent ordering
        
        print(f"Loading {len(reference_files)} reference patterns...")
        
        for i, filename in enumerate(reference_files):
            file_path = os.path.join(reference_dir, filename)
            img = self.load_image(file_path)
            
            if img is not None:
                # Apply DWT to reference image
                wavelet_transform = self.apply_2d_dwt(img)
                
                if wavelet_transform is not None:
                    self.reference_patterns.append(img)
                    self.reference_transforms.append(wavelet_transform)
                    print(f"Loaded reference pattern {i+1}: {filename}")
                else:
                    print(f"Failed to process reference pattern: {filename}")
            else:
                print(f"Failed to load reference pattern: {filename}")
        
        print(f"Successfully loaded {len(self.reference_transforms)} reference patterns\n")
    
    def classify_eeg_pattern(self, test_image_path, threshold=600):
        """
        Classify EEG pattern as normal or abnormal
        Implements the core algorithm from the original project
        
        Args:
            test_image_path: Path to test image
            threshold: MSE threshold for classification (default: 0.5 as per original)
            
        Returns:
            Dictionary containing classification results
        """
        # Load test image
        test_img = self.load_image(test_image_path)
        if test_img is None:
            return {"error": "Failed to load test image"}
        
        # Apply DWT to test image
        test_transform = self.apply_2d_dwt(test_img)
        if test_transform is None:
            return {"error": "Failed to apply DWT to test image"}
        
        # Calculate MSE with each reference pattern
        mse_values = []
        for i, ref_transform in enumerate(self.reference_transforms):
            mse = self.calculate_mse(test_transform, ref_transform)
            mse_values.append(mse)
        
        # Find minimum MSE
        min_mse = min(mse_values)
        matched_frame = mse_values.index(min_mse) + 1  # 1-indexed as per original
        
        # Classification decision
        if min_mse < threshold:
            classification = "Normal"
            confidence = (threshold - min_mse) / threshold * 100
        else:
            classification = "Abnormal"
            confidence = min(min_mse / threshold * 100, 100)
        
        # Prepare results
        results = {
            "classification": classification,
            "confidence": f"{confidence:.2f}%",
            "min_mse": min_mse,
            "matched_frame": matched_frame if classification == "Normal" else None,
            "all_mse_values": mse_values,
            "threshold": threshold,
            "test_image": test_image_path,
            "wavelet_coefficients": {
                "test_transform_shape": test_transform.shape,
                "reference_count": len(self.reference_transforms)
            }
        }
        
        return results
    
    def visualize_wavelet_decomposition(self, image_path, save_path=None):
        """
        Visualize the wavelet decomposition process
        
        Args:
            image_path: Path to input image
            save_path: Path to save visualization (optional)
        """
        # Load image
        img = self.load_image(image_path)
        if img is None:
            return
        
        # Apply DWT
        coeffs1 = pywt.dwt2(img, self.wavelet)
        cA1, (cH1, cV1, cD1) = coeffs1
        
        coeffs2 = pywt.dwt2(cA1, self.wavelet)
        cA2, (cH2, cV2, cD2) = coeffs2
        
        coeffs3 = pywt.dwt2(cA2, self.wavelet)
        cA3, (cH3, cV3, cD3) = coeffs3
        
        # Create visualization
        fig, axes = plt.subplots(2, 4, figsize=(16, 8))
        
        # Original image
        axes[0, 0].imshow(img, cmap='gray')
        axes[0, 0].set_title('Original EEG Spectrogram')
        axes[0, 0].axis('off')
        
        # Level 1 coefficients
        axes[0, 1].imshow(cA1, cmap='gray')
        axes[0, 1].set_title('Level 1 - Approximation (cA1)')
        axes[0, 1].axis('off')
        
        axes[0, 2].imshow(cH1, cmap='gray')
        axes[0, 2].set_title('Level 1 - Horizontal (cH1)')
        axes[0, 2].axis('off')
        
        axes[0, 3].imshow(cV1, cmap='gray')
        axes[0, 3].set_title('Level 1 - Vertical (cV1)')
        axes[0, 3].axis('off')
        
        # Level 2 and 3 coefficients
        axes[1, 0].imshow(cD1, cmap='gray')
        axes[1, 0].set_title('Level 1 - Diagonal (cD1)')
        axes[1, 0].axis('off')
        
        axes[1, 1].imshow(cA2, cmap='gray')
        axes[1, 1].set_title('Level 2 - Approximation (cA2)')
        axes[1, 1].axis('off')
        
        axes[1, 2].imshow(cA3, cmap='gray')
        axes[1, 2].set_title('Level 3 - Approximation (cA3)')
        axes[1, 2].axis('off')
        
        # Final wavelet representation
        final_transform = self.apply_2d_dwt(img)
        axes[1, 3].imshow(final_transform, cmap='gray')
        axes[1, 3].set_title('3-Level Wavelet Transform')
        axes[1, 3].axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            plt.close()
        else:
            plt.show()


if __name__ == "__main__":
    # Example usage
    processor = EEGProcessor()
    
    # Load reference database
    processor.load_reference_database('data/reference_signals')
    
    # Test with a sample (this will be created later)
    # results = processor.classify_eeg_pattern('data/test_samples/test_normal_1.png')
    # print("Classification Results:")
    # print(f"Classification: {results['classification']}")
    # print(f"Confidence: {results['confidence']}")
    # if results.get('matched_frame'):
    #     print(f"Matched Reference Frame: {results['matched_frame']}")