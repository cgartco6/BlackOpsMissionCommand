#!/usr/bin/env python3
"""
Black Ops Mission Command - Dashboard Launcher
"""
import sys
import os
import platform

def setup_dashboard():
    """Configure environment for dashboard"""
    # Add dashboard directory to Python path
    dashboard_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'dashboard'))
    if dashboard_dir not in sys.path:
        sys.path.insert(0, dashboard_dir)
    
    # Platform-specific configurations
    system = platform.system()
    if system == "Windows":
        # Windows-specific optimizations
        pass

def main():
    try:
        from dashboard import Dashboard
        dashboard = Dashboard()
        dashboard.run()
    except Exception as e:
        print(f"Dashboard error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_dashboard()
    main()
