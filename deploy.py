#!/usr/bin/env python3
"""
PythonAnywhere Deployment Script
Run this script to deploy updates to PythonAnywhere
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def deploy_to_pythonanywhere():
    """Deploy the application to PythonAnywhere"""
    print("🚀 Starting PythonAnywhere deployment...")
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Error: app.py not found. Make sure you're in the project directory.")
        return False
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("❌ Error: requirements.txt not found.")
        return False
    
    print("📋 Deployment checklist:")
    print("1. Upload files to PythonAnywhere")
    print("2. Install dependencies")
    print("3. Reload web application")
    print("4. Check logs for errors")
    
    print("\n📝 Manual steps to complete:")
    print("1. Go to PythonAnywhere Files tab")
    print("2. Upload all project files")
    print("3. Open Bash console")
    print("4. Run: pip3.10 install --user -r requirements.txt")
    print("5. Go to Web tab and click 'Reload'")
    print("6. Check Error log for any issues")
    
    return True

if __name__ == "__main__":
    deploy_to_pythonanywhere()
