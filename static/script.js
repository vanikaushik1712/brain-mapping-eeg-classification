/*
 * Brain Mapping EEG Classification System - JavaScript
 * Frontend interactions and visualization
 * Using jQuery 1.10.2 (2013-era compatible)
 */

$(document).ready(function() {
    console.log('Brain Mapping EEG Classification System initialized');
    
    // Load system status on page load
    loadSystemStatus();
    
    // File upload handling
    $('#browse-btn').click(function() {
        $('#file-input').click();
    });
    
    $('#file-input').change(function() {
        if (this.files && this.files[0]) {
            uploadFile(this.files[0]);
        }
    });
    
    // Drag and drop functionality
    var uploadArea = $('#upload-area');
    
    uploadArea.on('dragover', function(e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).addClass('dragover');
    });
    
    uploadArea.on('dragleave', function(e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).removeClass('dragover');
    });
    
    uploadArea.on('drop', function(e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).removeClass('dragover');
        
        var files = e.originalEvent.dataTransfer.files;
        if (files.length > 0) {
            uploadFile(files[0]);
        }
    });
    
    // Test sample buttons
    $('.btn-sample').click(function() {
        var sampleName = $(this).data('sample');
        processSample(sampleName);
    });
    
    // Generate data button
    $('#generate-data-btn').click(function() {
        generateData();
    });
});

function loadSystemStatus() {
    $.get('/info')
        .done(function(data) {
            displaySystemStatus(data);
        })
        .fail(function(xhr) {
            $('#system-status').html('<p class="text-danger">Failed to load system status</p>');
        });
}

function displaySystemStatus(data) {
    var statusHtml = '';
    
    statusHtml += '<div class="status-item">';
    statusHtml += '<div class="status-label">Reference Patterns</div>';
    statusHtml += '<div class="status-value">' + data.reference_patterns_loaded + ' loaded</div>';
    statusHtml += '</div>';
    
    statusHtml += '<div class="status-item">';
    statusHtml += '<div class="status-label">Test Samples</div>';
    statusHtml += '<div class="status-value">' + data.test_samples_available + ' available</div>';
    statusHtml += '</div>';
    
    statusHtml += '<div class="status-item">';
    statusHtml += '<div class="status-label">Wavelet Type</div>';
    statusHtml += '<div class="status-value">' + data.wavelet_type + '</div>';
    statusHtml += '</div>';
    
    statusHtml += '<div class="status-item">';
    statusHtml += '<div class="status-label">Classification Threshold</div>';
    statusHtml += '<div class="status-value">' + data.classification_threshold + '</div>';
    statusHtml += '</div>';
    
    $('#system-status').html(statusHtml);
}

function uploadFile(file) {
    // Validate file type
    var allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/bmp'];
    if (allowedTypes.indexOf(file.type) === -1) {
        alert('Invalid file type. Please upload PNG, JPG, JPEG, or BMP files.');
        return;
    }
    
    // Validate file size (16MB max)
    var maxSize = 16 * 1024 * 1024; // 16MB
    if (file.size > maxSize) {
        alert('File too large. Maximum size is 16MB.');
        return;
    }
    
    var formData = new FormData();
    formData.append('file', file);
    
    showLoading();
    
    $.ajax({
        url: '/upload',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
            hideLoading();
            displayResults(data);
        },
        error: function(xhr) {
            hideLoading();
            var error = 'Upload failed';
            try {
                var response = JSON.parse(xhr.responseText);
                error = response.error || error;
            } catch(e) {}
            alert('Error: ' + error);
        }
    });
}

function processSample(sampleName) {
    showLoading();
    
    $.get('/test_sample/' + sampleName)
        .done(function(data) {
            hideLoading();
            displayResults(data);
        })
        .fail(function(xhr) {
            hideLoading();
            var error = 'Processing failed';
            try {
                var response = JSON.parse(xhr.responseText);
                error = response.error || error;
            } catch(e) {}
            alert('Error: ' + error);
        });
}

function displayResults(data) {
    if (data.error) {
        alert('Error: ' + data.error);
        return;
    }
    
    // Show results section
    $('#results-section').show().addClass('fade-in');
    
    // Update classification result
    var classificationElement = $('#classification-result');
    classificationElement.text(data.classification);
    classificationElement.removeClass('normal abnormal');
    classificationElement.addClass(data.classification.toLowerCase());
    
    // Update confidence
    $('#confidence-result').text(data.confidence);
    
    // Update MSE
    $('#mse-result').text(data.min_mse.toFixed(4));
    
    // Update matched frame
    $('#frame-result').text(data.matched_frame || 'None');
    
    // Display MSE chart
    displayMSEChart(data.all_mse_values, data.matched_frame, data.threshold);
    
    // Display image if available
    if (data.sample_filename) {
        displayProcessedImage('/images/' + data.sample_filename);
    }
    
    // Scroll to results
    $('html, body').animate({
        scrollTop: $('#results-section').offset().top - 100
    }, 1000);
}

function displayMSEChart(mseValues, matchedFrame, threshold) {
    var canvas = document.getElementById('mse-canvas');
    var ctx = canvas.getContext('2d');
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    var width = canvas.width;
    var height = canvas.height;
    var margin = 50;
    var chartWidth = width - 2 * margin;
    var chartHeight = height - 2 * margin;
    
    // Find max MSE for scaling
    var maxMSE = Math.max(...mseValues, threshold * 1.5);
    
    // Draw axes
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(margin, margin);
    ctx.lineTo(margin, height - margin);
    ctx.lineTo(width - margin, height - margin);
    ctx.stroke();
    
    // Draw threshold line
    var thresholdY = height - margin - (threshold / maxMSE) * chartHeight;
    ctx.strokeStyle = '#e74c3c';
    ctx.lineWidth = 2;
    ctx.setLineDash([5, 5]);
    ctx.beginPath();
    ctx.moveTo(margin, thresholdY);
    ctx.lineTo(width - margin, thresholdY);
    ctx.stroke();
    ctx.setLineDash([]);
    
    // Draw bars
    var barWidth = chartWidth / mseValues.length;
    
    for (var i = 0; i < mseValues.length; i++) {
        var barHeight = (mseValues[i] / maxMSE) * chartHeight;
        var x = margin + i * barWidth;
        var y = height - margin - barHeight;
        
        // Choose color based on whether this is the matched frame
        ctx.fillStyle = (i + 1 === matchedFrame) ? '#27ae60' : '#3498db';
        
        ctx.fillRect(x + 2, y, barWidth - 4, barHeight);
        
        // Draw frame number
        ctx.fillStyle = '#333';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText((i + 1).toString(), x + barWidth / 2, height - margin + 20);
        
        // Draw MSE value
        ctx.font = '10px Arial';
        ctx.fillText(mseValues[i].toFixed(2), x + barWidth / 2, y - 5);
    }
    
    // Draw labels
    ctx.fillStyle = '#333';
    ctx.font = '14px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('Reference Frame', width / 2, height - 10);
    
    ctx.save();
    ctx.translate(15, height / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText('MSE Value', 0, 0);
    ctx.restore();
    
    // Draw threshold label
    ctx.fillStyle = '#e74c3c';
    ctx.font = '12px Arial';
    ctx.textAlign = 'left';
    ctx.fillText('Threshold (' + threshold + ')', margin + 10, thresholdY - 5);
}

function displayProcessedImage(imagePath) {
    var img = $('#result-image');
    img.attr('src', imagePath);
    img.show();
}

function generateData() {
    showLoading();
    
    $.get('/generate_data')
        .done(function(data) {
            hideLoading();
            alert('Dataset generated successfully! ' + data.reference_count + ' reference patterns loaded.');
            location.reload(); // Reload to show new test samples
        })
        .fail(function(xhr) {
            hideLoading();
            var error = 'Data generation failed';
            try {
                var response = JSON.parse(xhr.responseText);
                error = response.error || error;
            } catch(e) {}
            alert('Error: ' + error);
        });
}

function showLoading() {
    $('#loading').show();
}

function hideLoading() {
    $('#loading').hide();
}

// Utility functions
function formatNumber(num, decimals) {
    return parseFloat(num).toFixed(decimals || 2);
}

function validateImageFile(file) {
    var allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/bmp'];
    var maxSize = 16 * 1024 * 1024; // 16MB
    
    if (allowedTypes.indexOf(file.type) === -1) {
        return { valid: false, error: 'Invalid file type. Please upload PNG, JPG, JPEG, or BMP files.' };
    }
    
    if (file.size > maxSize) {
        return { valid: false, error: 'File too large. Maximum size is 16MB.' };
    }
    
    return { valid: true };
}

// Handle window resize for canvas
$(window).resize(function() {
    // Redraw chart if results are visible
    if ($('#results-section').is(':visible')) {
        // Chart will be redrawn automatically due to CSS
    }
});

console.log('Brain Mapping EEG Classification System ready!');