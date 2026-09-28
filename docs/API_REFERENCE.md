# 📖 API Reference

Complete API reference for MARK LII modules and functions.

---

## Table of Contents

- [Core Modules](#core-modules)
- [Actions](#actions)
- [Memory System](#memory-system)
- [UI Components](#ui-components)
- [Error Handling](#error-handling)
- [Plugin System](#plugin-system)

---

## Core Modules

### audio_devices.py

Audio device management and selection.

#### Functions

**`configure(input_rate: int, output_rate: int) -> None`**
- Configure audio sample rates
- Called at startup to sync with main.py constants

**`list_devices(direction: str) -> list[dict]`**
- List available audio devices
- **Parameters:**
  - `direction`: "input" or "output"
- **Returns:** List of device dictionaries with name and index

**`get_device_by_name(name: str, direction: str) -> Optional[int]`**
- Get device index by name
- **Parameters:**
  - `name`: Device name
  - `direction`: "input" or "output"
- **Returns:** Device index or None

**`test_device(device_index: int, direction: str) -> bool`**
- Test if device works
- **Parameters:**
  - `device_index`: Device index
  - `direction`: "input" or "output"
- **Returns:** True if device works

---

### error_handler.py

Centralized error handling framework.

#### Classes

**`ErrorCategory(Enum)`**
- Enum of error categories: API, AUDIO, FILE, NETWORK, SYSTEM, UI, PLUGIN, MEMORY, VALIDATION, UNKNOWN

**`MarkLIIException(Exception)`**
- Base exception for MARK LII
- **Attributes:**
  - `category`: ErrorCategory
  - `recoverable`: bool
  - `user_message`: str
  - `timestamp`: datetime

**`APIException(MarkLIIException)`**
- API-related errors

**`AudioException(MarkLIIException)`**
- Audio input/output errors

**`FileException(MarkLIIException)`**
- File operation errors

**`NetworkException(MarkLIIException)`**
- Network/connection errors

**`ValidationException(MarkLIIException)`**
- Input validation errors

**`ErrorLogger`**
- Centralized error logging
- **Methods:**
  - `log_error(error, context=None)`: Log an error
  - `log_warning(message)`: Log a warning
  - `log_info(message)`: Log informational message
  - `log_debug(message)`: Log debug message

**`ErrorContext`**
- Context manager for error handling
- **Parameters:**
  - `context_name`: str
  - `category`: ErrorCategory
  - `suppress`: bool (default: False)
  - `default_return`: Any (default: None)

**`ErrorRecovery`**
- Error recovery strategies
- **Static Methods:**
  - `retry_with_fallback(primary_func, fallback_func, *args, **kwargs)`: Try primary, fall back on error
  - `safe_call(func, default=None, *args, **kwargs)`: Call function with default on error
  - `validate_and_fix(value, validator, fixer=None)`: Validate and attempt to fix value

#### Decorators

**`@handle_errors(category=ErrorCategory.UNKNOWN, default_return=None, user_friendly=True, reraise=False)`**
- Decorator for consistent error handling
- **Example:**
  ```python
  @handle_errors(category=ErrorCategory.FILE, default_return=None)
  def read_file(path):
      with open(path) as f:
          return f.read()
  ```

**`@retry_on_error(max_attempts=3, delay=1.0, exceptions=(Exception,), backoff=True)`**
- Retry function on specific exceptions
- **Example:**
  ```python
  @retry_on_error(max_attempts=3, delay=1.0, backoff=True)
  def fetch_api_data(url):
      return requests.get(url).json()
  ```

#### Helper Functions

**`get_user_message(error_key: str, default: str) -> str`**
- Get user-friendly error message
- **Parameters:**
  - `error_key`: Error message key
  - `default`: Default message if key not found

**`safe_import(module_name: str, package: Optional[str]) -> Optional[module]`**
- Safely import module with error handling

**`safe_get_attr(obj: Any, attr: str, default: Any) -> Any`**
- Safely get attribute with default

**`safe_dict_get(d: dict, key: str, default: Any) -> Any`**
- Safely get dictionary value

---

## Actions

### file_processor.py

Process uploaded files.

**`file_processor(file_path: str, params: dict, player=None) -> str`**
- Main file processing function
- **Parameters:**
  - `file_path`: Path to file
  - `params`: Dictionary with action and parameters
  - `player`: Optional UI player for feedback
- **Supported Actions:**
  - Images: describe, ocr, resize, compress, convert, info
  - PDFs: summarize, extract_text, to_word, info
  - Documents: summarize, fix, reformat, translate, word_count
  - CSV/Excel: analyze, stats, filter, sort, convert
  - Code: explain, review, fix, optimize, run, document
  - Audio: transcribe, trim, convert, info
  - Video: trim, extract_audio, compress, transcribe, info

---

### web_search.py

Web search functionality.

**`web_search(query: str, params: dict, player=None) -> str`**
- Perform web search
- **Parameters:**
  - `query`: Search query
  - `params`: Dictionary with mode and parameters
  - `player`: Optional UI player for feedback
- **Modes:**
  - `search`: Standard web search
  - `news`: Latest news headlines
  - `research`: Deep comprehensive answer
  - `price`: Product price lookup
  - `compare`: Side-by-side comparison

---

### computer_settings.py

Control computer settings.

**`computer_settings(action: str, params: dict, player=None) -> str`**
- Control computer settings
- **Parameters:**
  - `action`: Action name
  - `params`: Dictionary with parameters
  - `player`: Optional UI player for feedback
- **Actions:**
  - Volume: volume_up, volume_down, volume_set, mute
  - Brightness: brightness_up, brightness_down
  - Power: sleep_display, lock_screen, restart, shutdown
  - Window: close_app, minimize, maximize, full_screen

---

## Memory System

### memory_manager.py

Persistent memory management.

**`load_memory() -> dict`**
- Load memory from disk
- **Returns:** Memory dictionary

**`update_memory(category: str, key: str, value: str) -> None`**
- Update memory entry
- **Parameters:**
  - `category`: Memory category (identity, preferences, projects, etc.)
  - `key`: Memory key
  - `value`: Memory value

**`format_memory_for_prompt(memory: dict) -> str`**
- Format memory for AI prompt
- **Returns:** Formatted memory string

**`search_memory(query: str, memory: dict) -> list[dict]`**
- Search memory by query
- **Parameters:**
  - `query`: Search query
  - `memory`: Memory dictionary
- **Returns:** List of matching entries

**`save_session_summary(summary: str) -> None`**
- Save session summary
- **Parameters:**
  - `summary`: Summary text

**`pop_last_session() -> Optional[str]`**
- Get and remove last session summary
- **Returns:** Last session summary or None

---

## UI Components

### JarvisUI

Main UI class.

#### Properties

**`muted: bool`**
- Get/set microphone mute state

**`current_file: Optional[str]`**
- Get currently selected file path

**`assistant_name: str`**
- Get assistant name

#### Methods

**`set_audio_level(level: float) -> None`**
- Update waveform with audio level
- **Parameters:**
  - `level`: Audio level 0.0-1.0

**`set_state(state: str) -> None`**
- Update UI state
- **Parameters:**
  - `state`: "idle", "listening", "processing", "speaking"

**`write_log(text: str) -> None`**
- Write to activity log
- **Parameters:**
  - `text`: Log text

**`show_content(title: str, text: str) -> None`**
- Show content in scrollable panel
- **Parameters:**
  - `title`: Content title
  - `text`: Content text

**`show_confirm(title: str, detail: str) -> None`**
- Show confirmation banner
- **Parameters:**
  - `title`: Banner title
  - `detail`: Detail text

**`hide_confirm() -> None`**
- Hide confirmation banner

**`notify_phone_connected() -> None`**
- Show phone connected notification

**`show_camera_frame(img_bytes: bytes) -> None`**
- Display camera frame
- **Parameters:**
  - `img_bytes`: Image bytes

**`start_camera_stream() -> None`**
- Start camera preview stream

**`stop_camera_stream() -> None`**
- Stop camera preview stream

#### Events

**`on_text_command: Callable`**
- Called when text command is sent

**`on_remote_clicked: Callable`**
- Called when remote button is clicked

**`on_interrupt: Callable`**
- Called when interrupt button is clicked

**`on_voice_change: Callable[[str], None]`**
- Called when voice is changed

**`on_audio_device_change: Callable[[str, str], None]`**
- Called when audio device is changed

**`get_plugins: Callable[[], list[dict]]`**
- Called to get plugin list

---

## Error Handling

See [ERROR_HANDLING.md](ERROR_HANDLING.md) for complete error handling guide.

### Quick Reference

```python
from core.error_handler import (
    handle_errors, ErrorCategory, APIException,
    retry_on_error, ErrorContext, error_logger
)

# Error handling decorator
@handle_errors(category=ErrorCategory.FILE, default_return=None)
def risky_function():
    pass

# Retry decorator
@retry_on_error(max_attempts=3, delay=1.0)
def api_call():
    pass

# Error context manager
with ErrorContext("Operation", ErrorCategory.SYSTEM, suppress=True):
    risky_operation()

# Logging
error_logger.log_error(exception, context="Context info")
error_logger.log_warning("Warning message")
error_logger.log_info("Info message")
```

---

## Plugin System

### Plugin Structure

Plugins are Python files in `plugins/` directory.

#### Required Structure

```python
"""
Plugin Name: My Plugin
Description: What it does
Author: Your Name
Version: 1.0.0
"""

PLUGIN_INFO = {
    "name": "my_plugin",
    "description": "Description",
    "version": "1.0.0",
    "author": "Your Name",
    "enabled": True,
}

TOOL_DECLARATION = {
    "name": "my_action",
    "description": "Clear description for AI",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "param_name": {
                "type": "STRING",
                "description": "Parameter description"
            }
        },
        "required": ["param_name"]
    }
}

def execute(params: dict) -> str:
    """
    Main execution function
    
    Args:
        params: Parameters from AI
        
    Returns:
        Result string
    """
    result = do_something(params.get('param_name'))
    return f"Result: {result}"
```

#### Plugin Loader

**`discover_plugins(plugin_dir: Path) -> list[dict]`**
- Discover and load plugins
- **Parameters:**
  - `plugin_dir`: Plugins directory
- **Returns:** List of loaded plugins

---

## Configuration

### api_keys.json

Main configuration file in `config/api_keys.json`.

```json
{
  "gemini_api_key": "YOUR_API_KEY",
  "assistant_name": "JARVIS",
  "user_name": "Sir",
  "voice": "Puck",
  "color": "#00d4ff",
  "input_device": "Microphone Name",
  "output_device": "Speaker Name",
  "brief_enabled": true,
  "boot_sound": true
}
```

### Config Manager

**`get_config() -> dict`**
- Get full config dictionary

**`get_api_key() -> str`**
- Get Gemini API key

**`get_voice() -> str`**
- Get selected voice

**`get_input_device() -> Optional[str]`**
- Get input device name

**`get_output_device() -> Optional[str]`**
- Get output device name

**`get_brief_enabled() -> bool`**
- Check if morning briefing is enabled

---

## Constants

### Main Constants (main.py)

```python
LIVE_MODEL = "models/gemini-2.5-flash-native-audio-preview-12-2025"
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024
```

### UI Constants (ui.py)

```python
DEFAULT_WIDTH = 980
DEFAULT_HEIGHT = 700
MIN_WIDTH = 820
MIN_HEIGHT = 580
```

---

## Examples

### Complete Plugin Example

```python
"""
Example Weather Plugin
"""

PLUGIN_INFO = {
    "name": "weather_extended",
    "description": "Extended weather information",
    "version": "1.0.0",
    "author": "Example",
    "enabled": True,
}

TOOL_DECLARATION = {
    "name": "get_extended_weather",
    "description": "Get detailed weather including forecast",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "city": {
                "type": "STRING",
                "description": "City name"
            },
            "days": {
                "type": "INTEGER",
                "description": "Forecast days (1-7)"
            }
        },
        "required": ["city"]
    }
}

def execute(params: dict) -> str:
    from core.error_handler import handle_errors, NetworkException
    import requests
    
    @handle_errors(default_return="Weather unavailable")
    def fetch_weather():
        city = params.get('city')
        days = params.get('days', 3)
        
        # API call here
        response = requests.get(f"https://api.weather.com/{city}")
        
        if response.status_code != 200:
            raise NetworkException("Weather API failed")
        
        data = response.json()
        return f"Weather in {city}: {data['temp']}°C, {data['condition']}"
    
    return fetch_weather()
```

---

## Type Hints

Common type hints used throughout the codebase:

```python
from typing import Optional, Callable, Any, Dict, List, Tuple
from pathlib import Path

# Function signatures
def function(
    required_param: str,
    optional_param: Optional[int] = None,
    callback: Optional[Callable[[str], None]] = None
) -> str:
    pass

# Collections
config: Dict[str, Any] = {}
files: List[Path] = []
result: Tuple[bool, str] = (True, "Success")
```

---

**Last Updated**: September 22, 2026  
**Version**: Mark LII
