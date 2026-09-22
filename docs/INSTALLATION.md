# 📦 Installation Guide

Complete installation instructions for MARK LII AI Assistant.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11 or 3.12** ([Download here](https://www.python.org/downloads/))
- **pip** (Python package manager, included with Python)
- **Git** (for cloning the repository)
- **Working microphone and speakers**
- **Internet connection** (required for AI features)

## System Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+) |
| **RAM** | 4 GB minimum, 8 GB recommended |
| **Storage** | 500 MB for project + 2 GB for dependencies |
| **Python** | 3.11 or 3.12 (3.13 not yet supported) |

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/FatihMakes/Mark-LII.git
cd Mark-LII
```

---

## Step 2: Create Virtual Environment (Recommended)

### Windows
```bash
python -m venv venv
.\venv\Scripts\activate
```

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Common Installation Issues

#### Issue: `pip` command not found
**Solution:** Use `python -m pip` instead:
```bash
python -m pip install -r requirements.txt
```

#### Issue: Permission denied on Linux/macOS
**Solution:** Use `--user` flag:
```bash
pip install --user -r requirements.txt
```

#### Issue: Slow download speed
**Solution:** Use a faster PyPI mirror:
```bash
pip install -r requirements.txt -i https://pypi.org/simple
```

---

## Step 4: Install Playwright Browsers

Playwright is used for browser automation features:

```bash
playwright install
```

This will download Chromium, Firefox, and WebKit browsers (~300 MB).

### Install Only Chromium (Smaller Download)
```bash
playwright install chromium
```

---

## Step 5: Configure API Keys

### Get Your Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

### Add API Key to Configuration

1. Navigate to the `config` folder
2. Copy `api_keys.json.example` to `api_keys.json`:
   ```bash
   # Windows
   copy config\api_keys.json.example config\api_keys.json
   
   # macOS/Linux
   cp config/api_keys.json.example config/api_keys.json
   ```
3. Edit `config/api_keys.json` and add your API key:
   ```json
   {
     "gemini_api_key": "YOUR_API_KEY_HERE"
   }
   ```

---

## Step 6: Run First-Time Setup

```bash
python setup.py
```

This interactive setup will guide you through:
- Microphone selection
- Speaker selection
- Assistant name (default: JARVIS)
- Your name (how the assistant addresses you)
- Voice selection (Charon, Puck, Kore, Fenrir, Aoede)
- UI theme color

---

## Step 7: Launch MARK LII

```bash
python main.py
```

If everything is configured correctly, you should see:
- The MARK LII UI window
- A boot animation (if enabled)
- "Listening..." status

---

## Platform-Specific Notes

### Windows

**Windows Defender:** You may need to allow Python through the firewall for network features.

**Audio Devices:** Use the UI settings (⚙ → 🎧 AUDIO DEVICES) to select the correct microphone if it's not working.

### macOS

**Microphone Permission:** macOS will prompt for microphone access on first run. Click "Allow".

**Python Version:** macOS comes with Python 2.7. Ensure you install Python 3.11+ separately:
```bash
brew install python@3.11
```

### Linux

**Additional Dependencies:** Some features may require system packages:
```bash
# Ubuntu/Debian
sudo apt-get install python3-pyaudio portaudio19-dev

# Fedora
sudo dnf install python3-pyaudio portaudio-devel

# Arch
sudo pacman -S python-pyaudio portaudio
```

**Audio Setup:** Ensure PulseAudio or PipeWire is running:
```bash
pulseaudio --check
```

---

## Verifying Installation

### Test Audio Input
1. Launch MARK LII
2. Watch the waveform in the UI
3. Speak normally - you should see the waveform react

### Test Voice Output
Say: "What is 2 plus 2?"
You should hear the assistant respond.

### Test System Control
Say: "What's my system status?"
The assistant should report CPU, RAM, and temperature.

---

## Optional: Auto-Start on Boot

### Windows
Run MARK LII once, then from the UI select:
**⚙ → Enable Auto-Start**

### macOS
Create a LaunchAgent (instructions coming soon)

### Linux
Create a systemd service (instructions coming soon)

---

## Updating MARK LII

To update to the latest version:

```bash
# Navigate to project directory
cd Mark-LII

# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Update Playwright browsers
playwright install
```

---

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.

---

## Next Steps

- Read [USAGE.md](USAGE.md) for voice command examples
- Explore the [Plugin System](PLUGINS.md) to extend functionality
- Configure [Memory Settings](CONFIGURATION.md) for personalization

---

**Need Help?** Open an issue on GitHub or check the video tutorials on [YouTube](https://www.youtube.com/@FatihMakes).
