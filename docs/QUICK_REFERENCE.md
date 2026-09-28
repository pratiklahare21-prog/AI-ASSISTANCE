# ⚡ Quick Reference Guide

Quick reference for common MARK LII operations.

---

## 🎯 Essential Commands

### Voice Commands

| Command | Action |
|---------|--------|
| "What's the weather in [city]?" | Get weather report |
| "Open [app name]" | Launch application |
| "What's on my screen?" | Analyze screen content |
| "Set a reminder for [time]" | Create reminder |
| "Play [song] on YouTube" | Play YouTube video |
| "Search for [query]" | Web search |
| "Show my system status" | Display CPU, RAM, temp |
| "Turn up the volume" | Increase system volume |
| "Take a screenshot" | Capture screen |
| "Remember that [fact]" | Store in memory |

### Text Commands

Type in the input box and press Enter:
- Same as voice commands
- Better for long or precise commands
- Special characters supported

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+M` | Mute/Unmute microphone |
| `Ctrl+,` | Open customization settings |
| `Ctrl+A` | Audio device settings |
| `Ctrl+K` | Memory panel |
| `Ctrl+P` | Plugin manager |
| `Ctrl+R` | Remote dashboard QR code |
| `Ctrl+D` | Toggle quick drawer |
| `Ctrl+Q` | Quit application |
| `F1` | Show help overlay |
| `F11` | Toggle fullscreen |
| `Esc` | Interrupt/Cancel |
| `Enter` | Send text command |

---

## 🎨 Customization

### Change Voice

1. Press `Ctrl+,` or click ⚙
2. Select voice: Charon, Puck, Kore, Fenrir, Aoede
3. Click "Save & Apply"

### Change Theme Color

1. Press `Ctrl+,` or click ⚙
2. Drag hue wheel or enter hex code
3. Preview updates in real-time
4. Click "Save & Apply"

### Select Audio Devices

1. Press `Ctrl+A` or click 🎧
2. Choose microphone from dropdown
3. Choose speakers from dropdown
4. Click "Apply"

---

## 📁 File Processing

### Upload Files

- **Drag & Drop**: Drag file onto interface
- **Browse**: Click drop zone to browse files

### Supported File Types

| Type | Formats | Actions |
|------|---------|---------|
| **Images** | PNG, JPG, GIF, WebP | Describe, OCR, Resize, Compress, Convert |
| **Documents** | PDF, DOCX, TXT, MD | Summarize, Extract text, Translate |
| **Audio** | MP3, WAV, M4A, FLAC | Transcribe, Trim, Convert |
| **Video** | MP4, AVI, MOV, MKV | Trim, Extract audio, Transcribe |
| **Code** | PY, JS, TS, Java, C++ | Explain, Review, Fix, Optimize |
| **Data** | CSV, Excel, JSON | Analyze, Stats, Filter, Sort |

### Example Commands

- "Summarize this PDF"
- "What's in this image?"
- "Transcribe this audio file"
- "Explain this code"
- "Convert this image to PNG"

---

## 🧠 Memory Management

### View Memories

1. Press `Ctrl+K` or click 🧠
2. Browse stored facts
3. Click ✕ to delete any memory

### Add Memories

Say: "Remember that [fact]"
- "Remember that my birthday is June 15"
- "Remember that I prefer Python"
- "Remember that my sister's name is Sarah"

### Search Memories

JARVIS automatically searches memory when relevant.

---

## 🔌 Plugin Management

### Enable/Disable Plugins

1. Press `Ctrl+P` or click plugin icon
2. Toggle switches for each plugin
3. Plugins take effect immediately

### Create Custom Plugin

1. Copy `plugins/_template.py`
2. Edit PLUGIN_INFO and TOOL_DECLARATION
3. Implement `execute(params)` function
4. Place in `plugins/` folder
5. Restart MARK LII

---

## 🌐 Remote Access

### Connect from Phone

1. Press `Ctrl+R` or click 📱
2. Scan QR code with phone camera
3. Open the URL
4. Control MARK LII from phone

### Remote Commands

- Type commands in web interface
- Same functionality as desktop
- Secure connection with access key

---

## 🎯 System Control

### Volume Control

- "Turn up the volume" / "Volume up"
- "Turn down the volume" / "Volume down"
- "Mute" / "Unmute"
- "Set volume to 50%"

### Brightness

- "Increase brightness"
- "Decrease brightness"
- "Set brightness to 80%"

### Power Management

- "Lock my screen"
- "Restart the computer" (requires confirmation)
- "Shutdown" (requires confirmation)
- "Sleep display"

### Window Management

- "Close this window"
- "Minimize"
- "Maximize"
- "Full screen"
- "Switch window"

---

## 🌍 Web & Browser

### Open Websites

- "Open YouTube"
- "Open Google in Chrome"
- "Search for AI news on DuckDuckGo"

### Browser Control

- "Close all tabs"
- "Go back"
- "Refresh page"
- "Take screenshot of this page"
- "Scroll down"

---

## 🔍 Search Modes

### Standard Search

- "Search for Python tutorials"

### News Search

- "What's the news about AI?"

### Research Mode

- "Research quantum computing"

### Price Lookup

- "What's the price of iPhone 15?"

### Compare

- "Compare iPhone 15 and Samsung S24"

---

## ⚙️ Settings

### Configuration File

Location: `config/api_keys.json`

```json
{
  "gemini_api_key": "YOUR_KEY",
  "assistant_name": "JARVIS",
  "user_name": "Sir",
  "voice": "Puck",
  "color": "#00d4ff",
  "input_device": "Microphone",
  "output_device": "Speakers",
  "brief_enabled": true,
  "boot_sound": true
}
```

### Enable Features

- **Morning Briefing**: Toggle in ⚙ settings
- **Boot Sound**: Toggle in ⚙ settings
- **Auto-Start**: Toggle in ⚙ settings

---

## 🐛 Troubleshooting

### JARVIS Can't Hear Me

1. Check microphone is connected
2. Press `Ctrl+A` to select correct microphone
3. Watch waveform - should react to voice
4. Check system microphone permissions

### No Audio Output

1. Check speakers are connected
2. Press `Ctrl+A` to select correct speakers
3. Check system volume is not muted

### API Key Error

1. Open `config/api_keys.json`
2. Add valid Gemini API key
3. Get key from: https://aistudio.google.com/apikey

### Connection Issues

1. Check internet connection
2. Verify API key is valid
3. Wait a moment and retry
4. Session auto-resumes on reconnect

---

## 📊 System Requirements

### Minimum

- **OS**: Windows 10, macOS 10.15, Linux (Ubuntu 20.04)
- **Python**: 3.11 or 3.12
- **RAM**: 4 GB
- **Storage**: 500 MB

### Recommended

- **RAM**: 8 GB
- **Internet**: Stable broadband connection
- **Microphone**: Quality microphone
- **Speakers**: Good speakers or headphones

---

## 📚 More Help

- **F1**: Built-in help overlay
- **Documentation**: `docs/` folder
- **Troubleshooting**: `docs/TROUBLESHOOTING.md`
- **API Reference**: `docs/API_REFERENCE.md`
- **YouTube**: [@FatihMakes](https://www.youtube.com/@FatihMakes)

---

**Quick Tip**: Hold down a button to see its tooltip with keyboard shortcut!

---

**Last Updated**: September 22, 2026
