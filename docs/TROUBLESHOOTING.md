# 🐛 Troubleshooting Guide

Common issues and their solutions for MARK LII.

---

## Audio Issues

### ❌ "JARVIS can't hear me"

**Symptoms:** The waveform doesn't respond to your voice, or the assistant doesn't respond to commands.

**Solutions:**

1. **Check Microphone Selection**
   - Open **⚙ → 🎧 AUDIO DEVICES**
   - Select the correct microphone from the dropdown
   - Speak and watch the waveform - it should react

2. **Check System Microphone Permission**
   - **Windows:** Settings → Privacy → Microphone → Allow apps
   - **macOS:** System Preferences → Security & Privacy → Microphone
   - **Linux:** Check PulseAudio mixer: `pavucontrol`

3. **Test Microphone Outside MARK LII**
   - Record audio using system voice recorder
   - If it doesn't work elsewhere, it's a hardware/driver issue

4. **Check Microphone Level**
   - Ensure microphone isn't muted in system settings
   - Increase input volume if too quiet

### ❌ "No Audio Output / Can't Hear JARVIS"

**Solutions:**

1. **Check Speaker Selection**
   - Open **⚙ → 🎧 AUDIO DEVICES**
   - Select the correct output device

2. **Check System Volume**
   - Ensure volume isn't muted
   - Increase system volume

3. **Test Speakers**
   - Play music or video to confirm speakers work
   - Try different audio output device

4. **Restart Audio Session**
   - Close MARK LII
   - Restart and let it reconnect

---

## Installation Issues

### ❌ "ModuleNotFoundError: No module named 'X'"

**Cause:** Missing Python package dependency.

**Solution:**
```bash
pip install <module_name>
```

**Common Missing Modules:**
- `pip install PyQt6`
- `pip install sounddevice`
- `pip install google-genai`
- `pip install playwright`

### ❌ "pip: command not found"

**Solution:** Use Python module syntax:
```bash
python -m pip install -r requirements.txt
```

### ❌ "Permission denied" during installation (Linux/macOS)

**Solution:** Install in user directory:
```bash
pip install --user -r requirements.txt
```

### ❌ Playwright browsers not installed

**Symptoms:** Browser automation fails with "Browser not found"

**Solution:**
```bash
playwright install
```

---

## API & Connection Issues

### ❌ "Invalid API Key" or "API Error"

**Solutions:**

1. **Verify API Key**
   - Open `config/api_keys.json`
   - Ensure the key is correct (no extra spaces)
   - Get a new key from [Google AI Studio](https://aistudio.google.com/apikey)

2. **Check API Key Format**
   ```json
   {
     "gemini_api_key": "AIzaSy..."
   }
   ```

3. **API Quota Exceeded**
   - Free tier has rate limits
   - Wait a few minutes and try again
   - Check usage at [Google AI Studio](https://aistudio.google.com/)

### ❌ "Connection Failed" or "Network Error"

**Solutions:**

1. **Check Internet Connection**
   - Open a web browser and test connectivity
   - Ping Google: `ping google.com`

2. **Firewall/Antivirus Blocking**
   - Add Python to firewall exceptions
   - Temporarily disable antivirus to test

3. **Proxy Issues**
   - If behind corporate proxy, configure it:
   ```bash
   export HTTPS_PROXY=http://proxy:port
   ```

4. **API Service Status**
   - Check [Google Cloud Status](https://status.cloud.google.com/)

### ❌ Session keeps disconnecting

**Solutions:**

1. **Unstable Internet**
   - Use wired connection instead of WiFi
   - Check router stability

2. **Session Timeout**
   - This is normal for long idle periods
   - Session will auto-resume with conversation intact

---

## UI Issues

### ❌ UI Window Not Appearing

**Solutions:**

1. **Check if Process is Running**
   ```bash
   # Windows
   tasklist | findstr python
   
   # macOS/Linux
   ps aux | grep python
   ```

2. **Display/Monitor Issues**
   - Try connecting/disconnecting external monitors
   - Check if window is off-screen

3. **PyQt6 Installation**
   ```bash
   pip install --upgrade PyQt6
   ```

### ❌ UI Freezes or Becomes Unresponsive

**Solutions:**

1. **Close and Restart**
   - Kill the process: `Ctrl+C` in terminal
   - Restart: `python main.py`

2. **Check CPU Usage**
   - High CPU might indicate a stuck task
   - Check Task Manager / Activity Monitor

3. **Clear Cache**
   ```bash
   python cleanup.py
   ```

---

## Voice/Speech Issues

### ❌ Assistant Doesn't Understand My Accent

**Solutions:**

1. **Speak Clearly and Slowly**
   - Enunciate words
   - Avoid background noise

2. **Use Text Input**
   - Type your command in the UI input box

3. **Check Language Detection**
   - MARK LII auto-detects language on first use
   - Restart if language seems wrong

### ❌ Assistant Keeps Responding to Background Noise

**Solutions:**

1. **Reduce Background Noise**
   - Close windows
   - Mute TV/music
   - Use push-to-talk mode (if available)

2. **Adjust Microphone Sensitivity**
   - Lower input volume in system settings

---

## System Control Issues

### ❌ "Access Denied" when controlling system

**Cause:** Insufficient permissions for system operations.

**Solutions:**

1. **Run as Administrator (Windows)**
   ```bash
   # Right-click terminal → "Run as Administrator"
   python main.py
   ```

2. **Grant Accessibility Permissions (macOS)**
   - System Preferences → Security & Privacy → Accessibility
   - Add Terminal or Python

3. **Check User Permissions (Linux)**
   - Ensure user is in necessary groups:
   ```bash
   sudo usermod -aG input,video $USER
   ```

### ❌ Keyboard/Mouse Control Not Working

**Solutions:**

1. **Install pyautogui Dependencies**
   ```bash
   pip install pyautogui pillow
   ```

2. **macOS Accessibility**
   - Grant accessibility permissions (see above)

3. **Linux Display Server**
   - Ensure X11 or Wayland is running
   - Set DISPLAY variable: `export DISPLAY=:0`

---

## Memory & Performance Issues

### ❌ High CPU Usage

**Solutions:**

1. **Disable Visual Effects**
   - Turn off boot sound
   - Reduce UI animation

2. **Close Unnecessary Plugins**
   - Open plugin manager
   - Disable unused plugins

3. **Reduce Audio Quality**
   - Lower sample rate in settings

### ❌ Memory Usage Growing Over Time

**Solutions:**

1. **Restart Periodically**
   - Long-running sessions accumulate memory
   - Restart daily for best performance

2. **Clear Old Memories**
   - Open **🧠 MEMORY** panel
   - Delete old entries

---

## Platform-Specific Issues

### Windows

#### ❌ "DLL load failed" error

**Solution:** Install Visual C++ Redistributable:
- Download from [Microsoft](https://aka.ms/vs/17/release/vc_redist.x64.exe)

#### ❌ Terminal shows weird characters

**Solution:** Set UTF-8 encoding:
```bash
chcp 65001
```

### macOS

#### ❌ "Python not found" despite installation

**Solution:** Use full path or create alias:
```bash
alias python=python3
```

#### ❌ SSL Certificate Error

**Solution:** Install certificates:
```bash
/Applications/Python\ 3.11/Install\ Certificates.command
```

### Linux

#### ❌ Audio subsystem error

**Solution:** Install PortAudio:
```bash
# Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-pyaudio

# Fedora
sudo dnf install portaudio-devel python3-pyaudio

# Arch
sudo pacman -S portaudio python-pyaudio
```

---

## Still Having Issues?

### Check Logs

Look for error messages in:
- Terminal output where you ran `python main.py`
- Any `.log` files in the project directory

### Get Help

1. **Search Existing Issues:** [GitHub Issues](https://github.com/FatihMakes/Mark-LII/issues)
2. **Open New Issue:** Include:
   - OS and version
   - Python version: `python --version`
   - Full error message
   - Steps to reproduce
3. **Watch Tutorial Videos:** [YouTube Channel](https://www.youtube.com/@FatihMakes)

---

## Diagnostic Commands

Run these to gather system information for bug reports:

```bash
# Python version
python --version

# Installed packages
pip list

# System info
python -c "import platform; print(platform.platform())"

# Check audio devices
python -c "import sounddevice as sd; print(sd.query_devices())"
```

---

**Last Updated:** September 2026
