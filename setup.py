#!/usr/bin/env python3
"""
MARK LII Setup Script
Installs dependencies and performs initial configuration
"""

import subprocess
import sys
import platform
import json
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def install_requirements():
    """Install Python dependencies"""
    print_header("📦 Installing Python Dependencies")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found!")
        return False
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            check=True
        )
        print("✅ Python dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def install_playwright():
    """Install Playwright browsers"""
    print_header("🌐 Installing Playwright Browsers")
    
    try:
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            check=True
        )
        print("✅ Playwright browsers installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Playwright installation failed: {e}")
        print("   You can install manually later with: playwright install")
        return False

def setup_config():
    """Set up configuration files"""
    print_header("⚙️  Setting Up Configuration")
    
    config_dir = Path(__file__).parent / "config"
    example_file = config_dir / "api_keys.json.example"
    config_file = config_dir / "api_keys.json"
    
    # Check if config already exists
    if config_file.exists():
        print("✅ Configuration file already exists")
        return True
    
    # Create from example if it exists
    if example_file.exists():
        try:
            with open(example_file, 'r') as f:
                config = json.load(f)
            
            # Write new config
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"✅ Created configuration file: {config_file}")
            print("\n⚠️  IMPORTANT: You need to add your Gemini API key!")
            print("   1. Get your key from: https://aistudio.google.com/apikey")
            print(f"   2. Edit: {config_file}")
            print('   3. Replace "YOUR_API_KEY_HERE" with your actual key')
            return True
        except Exception as e:
            print(f"❌ Failed to create config: {e}")
            return False
    else:
        print(f"⚠️  Example config not found: {example_file}")
        return False

def check_pywin32():
    """Check pywin32 installation on Windows"""
    if platform.system() != "Windows":
        return True
    
    print_header("🪟 Checking Windows Components")
    
    try:
        import win32com.client  # noqa: F401
        print("✅ pywin32 installed correctly")
        return True
    except ImportError:
        postinstall = Path(sys.executable).parent / "Scripts" / "pywin32_postinstall.py"
        print("\n⚠️  pywin32 did not install correctly")
        print("    Desktop shortcut creation may not work properly.")
        print("\n    Try fixing it manually with:")
        print(f'    "{sys.executable}" -m pip install --force-reinstall pywin32')
        print(f'    "{sys.executable}" "{postinstall}" -install')
        return False

def verify_installation():
    """Run verification checks"""
    print_header("🔍 Verifying Installation")
    
    check_script = Path(__file__).parent / "check_requirements.py"
    
    if check_script.exists():
        print("Running verification checks...\n")
        try:
            subprocess.run([sys.executable, str(check_script)])
        except Exception as e:
            print(f"⚠️  Verification failed: {e}")
    else:
        print("⚠️  Verification script not found, skipping checks")

def main():
    """Main setup process"""
    print("\n" + "🚀" * 35)
    print("  MARK LII - AI Personal Assistant Setup")
    print("🚀" * 35)
    
    # Check Python version
    version = sys.version_info
    print(f"\n🐍 Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if not (version.major == 3 and version.minor in (11, 12)):
        print("❌ Python 3.11 or 3.12 required!")
        print(f"   Current version: {version.major}.{version.minor}")
        sys.exit(1)
    
    print("✅ Python version compatible")
    
    # Installation steps
    steps = [
        ("Install Python dependencies", install_requirements),
        ("Install Playwright browsers", install_playwright),
        ("Set up configuration", setup_config),
        ("Check Windows components", check_pywin32),
    ]
    
    success = True
    for step_name, step_func in steps:
        try:
            result = step_func()
            if not result:
                success = False
        except Exception as e:
            print(f"❌ Error during '{step_name}': {e}")
            success = False
    
    # Verify installation
    verify_installation()
    
    # Final message
    print_header("📋 Setup Complete!")
    
    if success:
        print("\n✅ MARK LII is ready to use!")
        print("\n📖 Next steps:")
        print("   1. Make sure you've added your Gemini API key to config/api_keys.json")
        print("   2. Run the assistant: python main.py")
        print("\n📺 For help, watch the tutorial: https://www.youtube.com/@FatihMakes")
    else:
        print("\n⚠️  Setup completed with some issues.")
        print("   Please review the errors above and fix them manually.")
        print("\n📖 For troubleshooting, see: docs/TROUBLESHOOTING.md")
    
    print("\n" + "=" * 70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Setup failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


