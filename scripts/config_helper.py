#!/usr/bin/env python
"""Configuration helper utilities"""

import json
import os
from typing import Dict, Any

class ConfigManager:
    """Manage application configuration"""
    
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.default_config = {
            'eeg_processor': {
                'wavelet_type': 'db1',
                'levels': 3,
                'threshold': 600
            },
            'signal_generator': {
                'sampling_frequency': 256,
                'duration': 10,
                'noise_level': 0.1
            },
            'flask_app': {
                'port': 9999,
                'debug': True,
                'max_file_size': 16777216
            }
        }
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return self.default_config
    
    def save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get_setting(self, section: str, key: str) -> Any:
        """Get specific setting value"""
        config = self.load_config()
        return config.get(section, {}).get(key)
    
    def update_setting(self, section: str, key: str, value: Any) -> None:
        """Update specific setting"""
        config = self.load_config()
        if section not in config:
            config[section] = {}
        config[section][key] = value
        self.save_config(config)

if __name__ == "__main__":
    manager = ConfigManager()
    config = manager.load_config()
    print("Current configuration:")
    print(json.dumps(config, indent=2))
