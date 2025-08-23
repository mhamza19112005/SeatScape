#!/usr/bin/env python3
"""
SeatScape Setup Script
Automated setup for the Django event booking system
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {description} failed")
        print(f"Command: {command}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")

def setup_project():
    """Main setup function"""
    print("🚀 Setting up SeatScape Event Booking System")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Create virtual environment
    venv_command = "python -m venv venv"
    if not run_command(venv_command, "Creating virtual environment"):
        return False
    
    # Determine activation command based on OS
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    # Install dependencies
    install_cmd = f"{pip_cmd} install -r requirements.txt"
    if not run_command(install_cmd, "Installing dependencies"):
        return False
    
    # Run migrations
    migrate_cmd = f"{python_cmd} manage.py migrate"
    if not run_command(migrate_cmd, "Applying database migrations"):
        return False
    
    # Create sample data (optional)
    if os.path.exists("create_sample_data.py"):
        sample_cmd = f"{python_cmd} create_sample_data.py"
        run_command(sample_cmd, "Creating sample data (optional)")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print(f"1. Activate virtual environment: {activate_cmd}")
    print(f"2. Run development server: {python_cmd} manage.py runserver")
    print("3. Open http://127.0.0.1:8000/ in your browser")
    print("\n🔧 Optional:")
    print(f"- Create superuser: {python_cmd} manage.py createsuperuser")
    print("- Access admin panel: http://127.0.0.1:8000/admin/")
    
    return True

if __name__ == "__main__":
    setup_project()
