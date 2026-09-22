"""
UI Configuration for MARK LII
Centralized settings for UI appearance, behavior, and accessibility
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class UIConfig:
    """UI configuration settings"""
    
    # Window Settings
    default_width: int = 980
    default_height: int = 700
    min_width: int = 820
    min_height: int = 580
    
    # Panel Widths
    left_panel_width: int = 148
    right_panel_width: int = 340
    
    # Animation Settings
    animation_duration_fast: int = 150      # Quick transitions (ms)
    animation_duration_normal: int = 250    # Standard transitions (ms)
    animation_duration_slow: int = 400      # Smooth transitions (ms)
    enable_animations: bool = True
    enable_boot_animation: bool = True
    
    # Audio Settings
    waveform_bars: int = 32                 # Number of waveform bars
    waveform_update_rate: int = 30          # FPS for waveform
    audio_level_smoothing: float = 0.3      # Audio level smoothing factor
    
    # Performance Settings
    enable_gpu_monitoring: bool = True
    metrics_update_interval: int = 1000     # System metrics update (ms)
    log_max_lines: int = 100                # Maximum log lines to keep
    enable_vsync: bool = True
    
    # Accessibility Settings
    high_contrast_mode: bool = False
    large_text_mode: bool = False
    reduce_motion: bool = False
    screen_reader_support: bool = False
    keyboard_navigation_hints: bool = True
    
    # Color Settings
    default_accent_color: str = "#00d4ff"
    
    # Font Settings
    default_font_family: str = "Segoe UI"   # Windows default
    default_font_size: int = 12
    monospace_font_family: str = "Courier New"
    
    # File Processing
    max_file_size_mb: int = 100             # Maximum file size for processing
    supported_image_formats: tuple = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
    supported_doc_formats: tuple = ('.pdf', '.docx', '.txt', '.md', '.rtf')
    supported_audio_formats: tuple = ('.mp3', '.wav', '.m4a', '.flac', '.ogg')
    supported_video_formats: tuple = ('.mp4', '.avi', '.mov', '.mkv', '.webm')
    
    # Remote Dashboard
    qr_code_size: int = 200                 # QR code size in pixels
    remote_key_length: int = 32             # Remote access key length
    
    # Memory
    memory_display_limit: int = 100         # Max memories to display at once
    memory_search_enabled: bool = True
    
    # Developer Options
    debug_mode: bool = False
    show_fps: bool = False
    log_ui_events: bool = False


# Global UI configuration instance
ui_config = UIConfig()


# ============================================================================
# Theme Presets
# ============================================================================

THEME_PRESETS = {
    "classic": {
        "name": "Classic Arc Reactor",
        "accent": "#00d4ff",
        "description": "The original cyan glow"
    },
    "gold": {
        "name": "Iron Man Gold",
        "accent": "#ffcc00",
        "description": "Stark Industries gold"
    },
    "red": {
        "name": "Hostile Red",
        "accent": "#ff3355",
        "description": "Alert mode crimson"
    },
    "green": {
        "name": "Matrix Green",
        "accent": "#00ff88",
        "description": "Digital green glow"
    },
    "purple": {
        "name": "Royal Purple",
        "accent": "#9d4edd",
        "description": "Regal purple tone"
    },
    "orange": {
        "name": "Sunset Orange",
        "accent": "#ff6b00",
        "description": "Warm orange hue"
    },
    "blue": {
        "name": "Deep Blue",
        "accent": "#0066ff",
        "description": "Ocean blue"
    },
    "pink": {
        "name": "Neon Pink",
        "accent": "#ff006e",
        "description": "Vibrant pink"
    }
}


# ============================================================================
# Responsive Layout Configurations
# ============================================================================

LAYOUT_CONFIGS = {
    "compact": {
        "width_range": (820, 979),
        "font_scale": 0.9,
        "padding_scale": 0.8,
        "hide_labels": True,
        "single_column": True
    },
    "normal": {
        "width_range": (980, 1199),
        "font_scale": 1.0,
        "padding_scale": 1.0,
        "hide_labels": False,
        "single_column": False
    },
    "comfortable": {
        "width_range": (1200, 1599),
        "font_scale": 1.05,
        "padding_scale": 1.1,
        "hide_labels": False,
        "single_column": False
    },
    "spacious": {
        "width_range": (1600, 9999),
        "font_scale": 1.1,
        "padding_scale": 1.2,
        "hide_labels": False,
        "single_column": False
    }
}


# ============================================================================
# Keyboard Shortcut Configuration
# ============================================================================

DEFAULT_SHORTCUTS = {
    "mute_toggle": "Ctrl+M",
    "customize": "Ctrl+,",
    "audio_devices": "Ctrl+A",
    "memory_panel": "Ctrl+K",
    "plugin_manager": "Ctrl+P",
    "remote_dashboard": "Ctrl+R",
    "toggle_drawer": "Ctrl+D",
    "quit": "Ctrl+Q",
    "fullscreen": "F11",
    "help": "F1",
    "interrupt": "Esc",
    "send_command": "Return",
}


# ============================================================================
# Accessibility Presets
# ============================================================================

ACCESSIBILITY_PRESETS = {
    "default": {
        "name": "Default",
        "high_contrast": False,
        "large_text": False,
        "reduce_motion": False,
    },
    "high_contrast": {
        "name": "High Contrast",
        "high_contrast": True,
        "large_text": False,
        "reduce_motion": False,
    },
    "low_vision": {
        "name": "Low Vision",
        "high_contrast": True,
        "large_text": True,
        "reduce_motion": False,
    },
    "motion_sensitive": {
        "name": "Motion Sensitive",
        "high_contrast": False,
        "large_text": False,
        "reduce_motion": True,
    },
    "maximum_accessibility": {
        "name": "Maximum Accessibility",
        "high_contrast": True,
        "large_text": True,
        "reduce_motion": True,
    }
}


# ============================================================================
# Helper Functions
# ============================================================================

def get_layout_config(window_width: int) -> dict:
    """Get layout configuration based on window width"""
    for config_name, config in LAYOUT_CONFIGS.items():
        min_w, max_w = config["width_range"]
        if min_w <= window_width <= max_w:
            return config
    return LAYOUT_CONFIGS["normal"]


def apply_accessibility_preset(preset_name: str) -> None:
    """Apply an accessibility preset to the UI config"""
    if preset_name not in ACCESSIBILITY_PRESETS:
        return
    
    preset = ACCESSIBILITY_PRESETS[preset_name]
    ui_config.high_contrast_mode = preset["high_contrast"]
    ui_config.large_text_mode = preset["large_text"]
    ui_config.reduce_motion = preset["reduce_motion"]


def get_theme_preset(preset_name: str) -> Optional[str]:
    """Get accent color for a theme preset"""
    if preset_name in THEME_PRESETS:
        return THEME_PRESETS[preset_name]["accent"]
    return None


def validate_config() -> list[str]:
    """Validate UI configuration and return list of issues"""
    issues = []
    
    if ui_config.min_width > ui_config.default_width:
        issues.append("Minimum width cannot exceed default width")
    
    if ui_config.min_height > ui_config.default_height:
        issues.append("Minimum height cannot exceed default height")
    
    if ui_config.animation_duration_fast > ui_config.animation_duration_normal:
        issues.append("Fast animation duration should be less than normal")
    
    if ui_config.max_file_size_mb < 1:
        issues.append("Maximum file size must be at least 1 MB")
    
    return issues


# ============================================================================
# Export Configuration
# ============================================================================

def export_config_dict() -> dict:
    """Export UI configuration as dictionary"""
    return {
        "window": {
            "default_width": ui_config.default_width,
            "default_height": ui_config.default_height,
            "min_width": ui_config.min_width,
            "min_height": ui_config.min_height,
        },
        "animations": {
            "enabled": ui_config.enable_animations,
            "boot_animation": ui_config.enable_boot_animation,
            "duration_fast": ui_config.animation_duration_fast,
            "duration_normal": ui_config.animation_duration_normal,
            "duration_slow": ui_config.animation_duration_slow,
        },
        "accessibility": {
            "high_contrast": ui_config.high_contrast_mode,
            "large_text": ui_config.large_text_mode,
            "reduce_motion": ui_config.reduce_motion,
            "keyboard_hints": ui_config.keyboard_navigation_hints,
        },
        "performance": {
            "gpu_monitoring": ui_config.enable_gpu_monitoring,
            "metrics_interval": ui_config.metrics_update_interval,
            "vsync": ui_config.enable_vsync,
        }
    }
