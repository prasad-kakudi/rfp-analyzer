import os
import subprocess
import sys

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def create_directories():
    """Create necessary directories"""
    dirs = ['uploads', 'static/css', 'static/js', 'static/images', 'templates']
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created directory: {dir_path}")

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write("""SECRET_KEY=change-this-secret-key-in-production
FLASK_ENV=development
FLASK_DEBUG=True
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
""")
        print("Created .env file")

def main():
    print("Setting up RFP Analyzer...")
    
    try:
        create_directories()
        create_env_file()
        install_dependencies()
        
        print("\nSetup complete!")
        print("To run the application:")
        print("1. Activate your virtual environment")
        print("2. Run: python app.py")
        print("3. Open http://localhost:5000")
        
    except Exception as e:
        print(f"Error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
