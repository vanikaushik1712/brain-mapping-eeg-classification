#!/usr/bin/env python
"""
Brain Mapping EEG Classification Web Application
Flask web server for EEG pattern classification using 2D DWT
Based on 2013 Brain Mapping using MATLAB Technology project
"""

import os
import json
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from eeg_processor import EEGProcessor
from signal_generator import EEGSignalGenerator
import tempfile
import shutil

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}
REFERENCE_DIR = 'data/reference_signals'
TEST_SAMPLES_DIR = 'data/test_samples'

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize EEG processor
processor = EEGProcessor()

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page"""
    # Get list of test samples for demo
    test_samples = []
    if os.path.exists(TEST_SAMPLES_DIR):
        for filename in os.listdir(TEST_SAMPLES_DIR):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                test_samples.append(filename)
    test_samples.sort()
    
    return render_template('index.html', test_samples=test_samples)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and EEG classification"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            # Save uploaded file
            filename = secure_filename(file.filename)
            temp_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(temp_path)
            
            # Load reference database if not already loaded
            if not processor.reference_transforms:
                processor.load_reference_database(REFERENCE_DIR)
            
            # Classify the uploaded image
            results = processor.classify_eeg_pattern(temp_path)
            
            # Add image path for frontend display
            results['uploaded_filename'] = filename
            
            # Clean up uploaded file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            return jsonify(results)
        else:
            return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, JPEG, or BMP files.'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 500

@app.route('/test_sample/<filename>')
def test_sample(filename):
    """Process a test sample from the demo data"""
    try:
        sample_path = os.path.join(TEST_SAMPLES_DIR, filename)
        
        if not os.path.exists(sample_path):
            return jsonify({'error': 'Test sample not found'}), 404
        
        # Load reference database if not already loaded
        if not processor.reference_transforms:
            processor.load_reference_database(REFERENCE_DIR)
        
        # Classify the test sample
        results = processor.classify_eeg_pattern(sample_path)
        results['sample_filename'] = filename
        results['is_demo_sample'] = True
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 500

@app.route('/generate_data')
def generate_data():
    """Generate synthetic EEG data"""
    try:
        generator = EEGSignalGenerator()
        generator.generate_dataset('data')
        
        # Reload reference database
        processor.load_reference_database(REFERENCE_DIR)
        
        return jsonify({
            'message': 'Dataset generated successfully',
            'reference_count': len(processor.reference_transforms)
        })
        
    except Exception as e:
        return jsonify({'error': f'Data generation error: {str(e)}'}), 500

@app.route('/visualize/<path:filename>')
def visualize_decomposition(filename):
    """Generate wavelet decomposition visualization"""
    try:
        # Determine if it's a test sample or uploaded file
        if filename.startswith('test_'):
            image_path = os.path.join(TEST_SAMPLES_DIR, filename)
        else:
            image_path = os.path.join(UPLOAD_FOLDER, filename)
        
        if not os.path.exists(image_path):
            return jsonify({'error': 'Image file not found'}), 404
        
        # Generate visualization
        viz_path = os.path.join(UPLOAD_FOLDER, f'viz_{filename}')
        processor.visualize_wavelet_decomposition(image_path, viz_path)
        
        return send_from_directory(UPLOAD_FOLDER, f'viz_{filename}')
        
    except Exception as e:
        return jsonify({'error': f'Visualization error: {str(e)}'}), 500

@app.route('/images/<path:filename>')
def serve_image(filename):
    """Serve images from various directories"""
    # Try different directories
    directories = [TEST_SAMPLES_DIR, REFERENCE_DIR, UPLOAD_FOLDER]
    
    for directory in directories:
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path):
            return send_from_directory(directory, filename)
    
    return jsonify({'error': 'Image not found'}), 404

@app.route('/info')
def info():
    """Get system information"""
    try:
        # Count reference patterns
        ref_count = len(processor.reference_transforms) if processor.reference_transforms else 0
        
        # Count test samples
        test_count = 0
        if os.path.exists(TEST_SAMPLES_DIR):
            test_count = len([f for f in os.listdir(TEST_SAMPLES_DIR) 
                            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))])
        
        return jsonify({
            'reference_patterns_loaded': ref_count,
            'test_samples_available': test_count,
            'wavelet_type': processor.wavelet,
            'decomposition_levels': processor.levels,
            'classification_threshold': 600
        })
        
    except Exception as e:
        return jsonify({'error': f'Info error: {str(e)}'}), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Initialize the system
    print("Brain Mapping EEG Classification System")
    print("======================================")
    
    # Check if reference data exists
    if not os.path.exists(REFERENCE_DIR) or len(os.listdir(REFERENCE_DIR)) == 0:
        print("No reference data found. Generating synthetic EEG dataset...")
        try:
            generator = EEGSignalGenerator()
            generator.generate_dataset('data')
            print("Dataset generated successfully!")
        except Exception as e:
            print(f"Error generating dataset: {e}")
    
    # Load reference database
    print("Loading reference database...")
    try:
        processor.load_reference_database(REFERENCE_DIR)
        print(f"Loaded {len(processor.reference_transforms)} reference patterns")
    except Exception as e:
        print(f"Error loading reference database: {e}")
    
    print("\nStarting web server...")
    print("Access the application at: http://localhost:3000")
    print("Press Ctrl+C to stop the server")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=3000)