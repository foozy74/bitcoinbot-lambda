import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 9):
        print("Error: Python 3.9 or higher is required")
        sys.exit(1)

def generate_requirements():
    """Generate requirements.txt file"""
    requirements = [
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'python-dotenv',
        'boto3',
        'ccxt',
        'sqlalchemy',
        'psycopg2-binary'
    ]

    print("Generating requirements.txt...")
    with open('requirements.txt', 'w') as f:
        for package in requirements:
            f.write(f"{package}\n")
    print("Generated requirements.txt")

def install_dependencies():
    """Install required packages"""
    packages = [
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'python-dotenv',
        'boto3',
        'ccxt',
        'sqlalchemy',
        'psycopg2-binary'
    ]

    print("Installing required packages...")
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError:
            print(f"Error installing {package}")
            sys.exit(1)

def setup_environment():
    """Set up local development environment"""
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write("""# Local Development Settings
DEBUG=True
PORT=5000
""")
        print("Created .env file with default settings")

if __name__ == "__main__":
    print("Setting up Bitcoin Trading Bot development environment...")
    check_python_version()
    generate_requirements()
    install_dependencies()
    setup_environment()
    print("\nSetup complete! You can now run the trading bot with:")
    print("streamlit run trading_bot.py")