#!/usr/bin/env python
"""Unit tests for Flask application"""

import pytest
import json
from app import app

class TestFlaskApp:
    def setup_method(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_page(self):
        response = self.app.get('/')
        assert response.status_code == 200
    
    def test_info_endpoint(self):
        response = self.app.get('/info')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'wavelet_type' in data

if __name__ == '__main__':
    pytest.main([__file__])
