#!/usr/bin/env python
"""Health check utility for Brain Mapping EEG Classification System"""

import requests
import sys
import json
import time

def check_health(base_url="http://localhost:9999"):
    """Perform comprehensive health check"""
    checks = {
        "web_server": False,
        "api_endpoints": False,
        "data_availability": False
    }
    
    try:
        # Test web server
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            checks["web_server"] = True
            print("✓ Web server is responding")
        
        # Test API endpoints
        info_response = requests.get(f"{base_url}/info", timeout=10)
        if info_response.status_code == 200:
            checks["api_endpoints"] = True
            data = info_response.json()
            if data.get("reference_patterns_loaded", 0) > 0:
                checks["data_availability"] = True
                print("✓ API endpoints working")
                print("✓ Reference data loaded")
            else:
                print("⚠ API working but no reference data")
    
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server")
    except requests.exceptions.Timeout:
        print("✗ Server timeout")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    # Overall health
    all_healthy = all(checks.values())
    status = "HEALTHY" if all_healthy else "UNHEALTHY"
    
    health_report = {
        "status": status,
        "timestamp": time.time(),
        "checks": checks
    }
    
    print(f"\nOverall Status: {status}")
    return health_report

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Health check for Brain Mapping EEG")
    parser.add_argument("--url", default="http://localhost:9999", help="Base URL to check")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    
    args = parser.parse_args()
    
    report = check_health(args.url)
    
    if args.json:
        print(json.dumps(report, indent=2))
    
    sys.exit(0 if report["status"] == "HEALTHY" else 1)
