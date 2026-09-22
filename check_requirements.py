#!/usr/bin/env python3
"""
Requirements Checker for MARK LII
Verifies all dependencies are installed and compatible
"""

import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor in (11, 12):
        print("   ✓ Python version is compatible")
        return True
    else:
        print("   ✗ Python 3.11 or 3.12 required")
        return False

def check_package(package_name, import_name=None):
    """Check if a package is installed and importable"""
    if import_name is None:
        import_name = package_name.replace("-", "_")
    
    try:
        __import__(import_name)
        print(f"   ✓ {package_name}")
        return True
    except ImportError:
        print(f"   ✗ {package_name} - NOT INSTALLED")
        return False

def check_packages():
    """Check all required packages"""
    print("\n📦 Checking Python packages...")
    
    packages = {
        "PyQt6": "PyQt6",
        "sounddevice": "sounddevice",
        "google-genai": "google.genai",
        "google-generativeai": "google.generativeai",
        "pillow": "PIL",
        "requests": "requests",
        "beautifulsoup4": "bs4",
        "ddgs": "ddgs",
        "playwright": "playwright",
        "pyautogui": "pyautogui",
        "pyperclip": "pyperclip",
        "pygetwindow": "pygetwindow",
        "opencv-python": "cv2",
        "numpy": "numpy",
        "mss": "mss",
        "psutil": "psutil",
        "send2trash": "send2trash",
        "youtube-transcript-api": "youtube_transcript_api",
        "python-pptx": "pptx",
        "fastapi": "fastapi",
        "uvicorn": "uvicorn",
        "cryptography": "cryptography",
        "qrcode": "qrcode",
    }
    
    missing = []
    for package, import_name in packages.items():
        if not check_package(package, import_name):
            missing.append(package)
    
    # Platform-specific packages
    if sys.platform == "win32":
        print("\n   Windows-specific packages:")
        win_packages = {
            "comtypes": "comtypes",
            "pycaw": "pycaw",
            "win10toast": "win10toast",
            "pywinauto": "pywinauto",
            "pywin32": "win32api",
        }
        for package, import_name in win_packages.items():
            if not check_package(package, import_name):
                missing.append(package)
    
    return missing

def check_config_file():
    """Check if API key config exists"""
    print("\n🔑 Checking configuration...")
    config_path = Path(__file__).parent / "config" / "api_keys.json"
    
    if config_path.exists():
        print(f"   ✓ Config file exists: {config_path}")
        
        try:
            import json
            with open(config_path, 'r') as f:
                config = json.load(f)
                if "gemini_api_key" in config and config["gemini_api_key"]:
                    print("   ✓ Gemini API key is configured")
                    return True
                else:
                    print("   ⚠ Gemini API key not found in config")
                    return False
        except Exception as e:
            print(f"   ✗ Error reading config: {e}")
            return False
    else:
        print(f"   ✗ Config file not found: {config_path}")
        print(f"   → Copy config/api_keys.json.example to config/api_keys.json")
        return False

def check_playwright_browsers():
    """Check if Playwright browsers are installed"""
    print("\n🌐 Checking Playwright browsers...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "--dry-run"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if "chromium" in result.stdout.lower():
            print("   ⚠ Playwright browsers not installed")
            print("   → Run: playwright install")
            return False
        else:
            print("   ✓ Playwright browsers installed")
            return True
    except Exception as e:
        print(f"   ⚠ Could not check Playwright: {e}")
        return False

def check_audio_devices():
    """Check if audio devices are available"""
    print("\n🎧 Checking audio devices...")
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        
        input_devices = [d for d in devices if d['max_input_channels'] > 0]
        output_devices = [d for d in devices if d['max_output_channels'] > 0]
        
        if input_devices:
            print(f"   ✓ Found {len(input_devices)} input device(s)")
        else:
            print("   ✗ No microphone found")
            
        if output_devices:
            print(f"   ✓ Found {len(output_devices)} output device(s)")
        else:
            print("   ✗ No speakers found")
            
        return bool(input_devices and output_devices)
    except Exception as e:
        print(f"   ✗ Error checking audio: {e}")
        return False

def main():
    """Run all checks"""
    print("=" * 70)
    print("🔍 MARK LII - Requirements Checker")
    print("=" * 70)
    
    checks = {
        "Python Version": check_python_version(),
        "API Configuration": check_config_file(),
        "Audio Devices": check_audio_devices(),
    }
    
    missing_packages = check_packages()
    checks["Python Packages"] = len(missing_packages) == 0
    
    playwright_ok = check_playwright_browsers()
    checks["Playwright Browsers"] = playwright_ok
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Summary")
    print("=" * 70)
    
    for check_name, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"{status} {check_name}")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages ({len(missing_packages)}):")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install missing packages with:")
        print("   pip install -r requirements.txt")
    
    if not checks["API Configuration"]:
        print("\n💡 Configure API key:")
        print("   1. Copy config/api_keys.json.example to config/api_keys.json")
        print("   2. Add your Gemini API key")
        print("   3. Get key from: https://aistudio.google.com/apikey")
    
    if not playwright_ok:
        print("\n💡 Install Playwright browsers:")
        print("   playwright install")
    
    if all(checks.values()) and not missing_packages:
        print("\n✨ All checks passed! You're ready to run MARK LII.")
        print("   python main.py")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
