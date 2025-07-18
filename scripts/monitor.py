#!/usr/bin/env python
"""System monitoring utilities for Brain Mapping EEG"""

import psutil
import time
import json
from datetime import datetime

def monitor_system_resources():
    """Monitor system resource usage"""
    monitoring_data = []
    
    print("Monitoring system resources... (Press Ctrl+C to stop)")
    try:
        while True:
            timestamp = datetime.now().isoformat()
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            data_point = {
                'timestamp': timestamp,
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_used_gb': memory.used / (1024**3),
                'disk_percent': disk.percent,
                'processes': len(psutil.pids())
            }
            
            monitoring_data.append(data_point)
            
            print(f"Time: {timestamp}")
            print(f"CPU: {cpu_percent}%")
            print(f"Memory: {memory.percent}% ({data_point['memory_used_gb']:.2f} GB)")
            print(f"Disk: {disk.percent}%")
            print("-" * 40)
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\nStopping monitoring...")
        
        # Save monitoring data
        with open('logs/system_monitoring.json', 'w') as f:
            json.dump(monitoring_data, f, indent=2)
        
        print(f"Monitoring data saved to logs/system_monitoring.json")

if __name__ == "__main__":
    monitor_system_resources()
