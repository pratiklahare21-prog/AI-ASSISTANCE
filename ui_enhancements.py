"""
UI Enhancement Utilities for MARK LII
Provides tooltips, keyboard shortcuts, and accessibility improvements
"""

from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence

# ============================================================================
# Tooltip Definitions
# ============================================================================

TOOLTIPS = {
    # Main Controls
    "mute_btn": "Mute/Unmute microphone (Ctrl+M)",
    "interrupt_btn": "Interrupt current response (Esc)",
    "send_btn": "Send text command (Enter)",
    "input_field": "Type your command here and press Enter",
    
    # Settings Controls
    "customize_btn": "Customize assistant name, voice, and UI color (Ctrl+,)",
    "audio_devices_btn": "Select microphone and speakers (Ctrl+A)",
    "memory_btn": "View and manage stored memories (Ctrl+K)",
    "plugin_manager_btn": "Enable/disable plugins (Ctrl+P)",
    "remote_btn": "Open remote dashboard QR code (Ctrl+R)",
    
    # System Controls
    "autostart_btn": "Enable/disable auto-start on system boot",
    "brief_btn": "Enable/disable morning briefing",
    "boot_sound_btn": "Enable/disable boot animation sound",
    "fullscreen_btn": "Toggle fullscreen mode (F11)",
    
    # File Drop Zone
    "file_drop_zone": "Drop files here or click to browse\nSupports images, PDFs, documents, audio, video, and more",
    
    # Drawer
    "drawer_toggle": "Toggle quick access drawer (Ctrl+D)",
}

KEYBOARD_SHORTCUTS = {
    "Ctrl+M": "Mute/Unmute microphone",
    "Ctrl+,": "Open customization settings",
    "Ctrl+A": "Audio device settings",
    "Ctrl+K": "Memory panel",
    "Ctrl+P": "Plugin manager",
    "Ctrl+R": "Remote dashboard",
    "Ctrl+D": "Toggle drawer",
    "F11": "Fullscreen",
    "Esc": "Interrupt/Cancel",
    "Enter": "Send command",
    "Ctrl+Q": "Quit application",
}

# ============================================================================
# Accessibility Improvements
# ============================================================================

def add_accessibility_attrs(widget: QWidget, role: str, label: str):
    """Add accessibility attributes to a widget"""
    widget.setAccessibleName(label)
    widget.setAccessibleDescription(f"{role}: {label}")

def apply_tooltips(widget_dict: dict):
    """Apply tooltips to a dictionary of widgets"""
    for key, widget in widget_dict.items():
        if key in TOOLTIPS and hasattr(widget, 'setToolTip'):
            widget.setToolTip(TOOLTIPS[key])

# ============================================================================
# Status Indicators
# ============================================================================

class StatusIndicator:
    """Visual status indicators for different states"""
    
    STATES = {
        "idle": ("⚫", "#4a5568", "Idle"),
        "listening": ("🎤", "#00d4ff", "Listening..."),
        "processing": ("⏳", "#ffcc00", "Processing..."),
        "speaking": ("🔊", "#00ff88", "Speaking..."),
        "error": ("❌", "#ff3355", "Error"),
        "connecting": ("🔄", "#007a99", "Connecting..."),
        "offline": ("⚠️", "#ff6b00", "Offline"),
    }
    
    @staticmethod
    def get_status(state: str) -> tuple[str, str, str]:
        """
        Get status indicator for a state
        Returns: (emoji, color, text)
        """
        return StatusIndicator.STATES.get(state, StatusIndicator.STATES["idle"])

# ============================================================================
# Color Accessibility Helpers
# ============================================================================

def ensure_contrast(fg_color: str, bg_color: str, min_ratio: float = 4.5) -> str:
    """
    Ensure sufficient color contrast for accessibility (WCAG AA)
    Returns adjusted foreground color if needed
    """
    # Simple implementation - in production, use proper contrast calculation
    return fg_color

def generate_focus_style(primary_color: str) -> str:
    """Generate focus indicator style for keyboard navigation"""
    return f"""
        :focus {{
            outline: 2px solid {primary_color};
            outline-offset: 2px;
        }}
    """

# ============================================================================
# Responsive Layout Helpers
# ============================================================================

class ResponsiveBreakpoints:
    """Breakpoints for responsive UI scaling"""
    COMPACT = 820    # Minimum width
    NORMAL = 980     # Default width
    WIDE = 1200      # Wide screen
    ULTRA_WIDE = 1600

    @staticmethod
    def get_layout_mode(width: int) -> str:
        """Determine layout mode based on window width"""
        if width < ResponsiveBreakpoints.COMPACT:
            return "compact"
        elif width < ResponsiveBreakpoints.NORMAL:
            return "normal"
        elif width < ResponsiveBreakpoints.WIDE:
            return "comfortable"
        else:
            return "spacious"

# ============================================================================
# Animation Helpers
# ============================================================================

class AnimationPresets:
    """Common animation durations and easing curves"""
    FAST = 150       # Quick transitions
    NORMAL = 250     # Standard transitions
    SLOW = 400       # Smooth transitions
    
    EASE_IN_OUT = "ease-in-out"
    EASE_OUT = "ease-out"
    LINEAR = "linear"

# ============================================================================
# Help Text Generator
# ============================================================================

def generate_shortcuts_help() -> str:
    """Generate formatted keyboard shortcuts help text"""
    lines = ["⌨️ Keyboard Shortcuts\n" + "=" * 40]
    
    for shortcut, description in KEYBOARD_SHORTCUTS.items():
        lines.append(f"{shortcut:<15} {description}")
    
    return "\n".join(lines)

def generate_quick_start_guide() -> str:
    """Generate quick start guide text"""
    return """
🚀 Quick Start Guide
=====================================

1. Microphone & Speakers
   • Click 🎧 to select audio devices
   • Speak clearly and watch the waveform
   
2. Voice Commands
   • "What's the weather?"
   • "Open Chrome"
   • "What's on my screen?"
   • "Set a reminder for 3 PM"
   
3. Text Input
   • Type commands in the input box
   • Press Enter to send
   
4. File Processing
   • Drag files onto the drop zone
   • Supported: Images, PDFs, Documents, Audio, Video
   
5. Customization
   • Press Ctrl+, to customize
   • Change voice, colors, and name
   
6. Memory
   • Press Ctrl+K to view memories
   • JARVIS remembers preferences and context

7. Plugins
   • Press Ctrl+P to manage plugins
   • Enable/disable features as needed

For more help, visit:
https://www.youtube.com/@FatihMakes
""".strip()

# ============================================================================
# Error Messages
# ============================================================================

ERROR_MESSAGES = {
    "no_api_key": "⚠️ Gemini API key not configured.\n\nPlease add your API key in Settings.",
    "no_microphone": "⚠️ No microphone detected.\n\nCheck your audio devices in Settings (Ctrl+A).",
    "no_speakers": "⚠️ No speakers detected.\n\nCheck your audio devices in Settings (Ctrl+A).",
    "connection_failed": "⚠️ Connection failed.\n\nCheck your internet connection and try again.",
    "audio_error": "⚠️ Audio error occurred.\n\nTry restarting or check audio device settings.",
    "file_error": "⚠️ Could not process file.\n\nEnsure the file is not corrupted and try again.",
}

def get_error_message(error_type: str) -> str:
    """Get user-friendly error message"""
    return ERROR_MESSAGES.get(error_type, "⚠️ An error occurred. Please try again.")

# ============================================================================
# Performance Tips
# ============================================================================

PERFORMANCE_TIPS = [
    "💡 Tip: Use Ctrl+M to quickly mute/unmute the microphone",
    "💡 Tip: Press Esc to interrupt a long response",
    "💡 Tip: Drag files directly onto the interface for quick processing",
    "💡 Tip: Use text input for precise commands",
    "💡 Tip: Enable morning briefing for daily summaries",
    "💡 Tip: Check memory panel (Ctrl+K) to see what JARVIS remembers",
    "💡 Tip: Customize UI colors to match your preference",
    "💡 Tip: Use plugins to extend functionality",
    "💡 Tip: Remote dashboard allows phone control via QR code",
    "💡 Tip: F11 toggles fullscreen mode for immersive experience",
]

def get_random_tip() -> str:
    """Get a random performance tip"""
    import random
    return random.choice(PERFORMANCE_TIPS)
