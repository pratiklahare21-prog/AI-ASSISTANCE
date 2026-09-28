# 🛡️ Error Handling Guide

This guide explains the error handling framework in MARK LII and how to use it effectively.

---

## 📋 Overview

MARK LII uses a centralized error handling system that provides:
- **Consistent error logging** across all modules
- **User-friendly error messages** for better UX
- **Error recovery strategies** for resilience
- **Automatic retry** for transient failures
- **Categorized errors** for better debugging

---

## 🔧 Error Categories

All errors are categorized for better tracking:

| Category | Description | Examples |
|----------|-------------|----------|
| `API` | API-related errors | Invalid API key, quota exceeded |
| `AUDIO` | Audio input/output errors | No microphone, device busy |
| `FILE` | File operation errors | File not found, permission denied |
| `NETWORK` | Network/connection errors | Timeout, connection refused |
| `SYSTEM` | System control errors | Permission denied, resource unavailable |
| `UI` | UI-related errors | Widget creation failed |
| `PLUGIN` | Plugin loading/execution | Import error, plugin crash |
| `MEMORY` | Memory/storage errors | Disk full, out of memory |
| `VALIDATION` | Input validation errors | Invalid format, missing field |

---

## 📚 Usage Examples

### Basic Error Handling with Decorator

```python
from core.error_handler import handle_errors, ErrorCategory

@handle_errors(
    category=ErrorCategory.FILE,
    default_return=None,
    user_friendly=True
)
def read_config_file(path: str):
    """Read configuration file with error handling"""
    with open(path, 'r') as f:
        return json.load(f)
```

### Custom Exceptions

```python
from core.error_handler import APIException, FileException

def load_api_key():
    """Load API key with proper error handling"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        if 'api_key' not in config:
            raise APIException(
                "API key not found in config",
                user_message="Please add your API key in settings"
            )
        
        return config['api_key']
    
    except FileNotFoundError:
        raise FileException(
            f"Config file not found: {config_path}",
            user_message="Configuration file is missing. Please run setup."
        )
```

### Retry with Exponential Backoff

```python
from core.error_handler import retry_on_error, NetworkException
import requests

@retry_on_error(
    max_attempts=3,
    delay=1.0,
    exceptions=(requests.Timeout, requests.ConnectionError),
    backoff=True
)
def fetch_data_from_api(url: str):
    """Fetch data with automatic retry on network errors"""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()
```

### Error Context Manager

```python
from core.error_handler import ErrorContext, ErrorCategory

def process_file(file_path: str):
    """Process file with error context"""
    with ErrorContext(
        context_name=f"Processing {file_path}",
        category=ErrorCategory.FILE,
        suppress=True
    ) as ctx:
        # Code that might fail
        data = load_file(file_path)
        result = process_data(data)
        save_result(result)
    
    if ctx.error:
        print(f"Failed to process file: {ctx.error}")
        return None
    
    return result
```

### Error Recovery with Fallback

```python
from core.error_handler import ErrorRecovery

def get_system_info():
    """Get system info with fallback"""
    return ErrorRecovery.retry_with_fallback(
        primary_func=get_detailed_system_info,
        fallback_func=get_basic_system_info
    )

def get_detailed_system_info():
    """Detailed info (may require admin privileges)"""
    # Complex system queries
    pass

def get_basic_system_info():
    """Basic info (always works)"""
    # Simple system queries
    pass
```

### Safe Function Calls

```python
from core.error_handler import ErrorRecovery

# Safe call with default value
result = ErrorRecovery.safe_call(
    risky_function,
    default="fallback_value",
    arg1="value1",
    arg2="value2"
)

# Safe attribute access
value = safe_get_attr(obj, 'attribute_name', default=0)

# Safe dictionary access
value = safe_dict_get(config, 'key', default={})
```

### Input Validation with Auto-Fix

```python
from core.error_handler import ErrorRecovery, ValidationException

def process_audio_sample_rate(rate):
    """Validate and fix audio sample rate"""
    
    def validate(r):
        return r in [8000, 16000, 22050, 44100, 48000]
    
    def fix(r):
        # Round to nearest valid rate
        valid_rates = [8000, 16000, 22050, 44100, 48000]
        return min(valid_rates, key=lambda x: abs(x - r))
    
    return ErrorRecovery.validate_and_fix(
        value=rate,
        validator=validate,
        fixer=fix
    )

# Usage
rate = process_audio_sample_rate(16100)  # Auto-fixed to 16000
```

### Logging Errors

```python
from core.error_handler import error_logger

# Log different severity levels
error_logger.log_info("Starting operation...")
error_logger.log_warning("Configuration file not found, using defaults")
error_logger.log_error(exception, context="Loading plugins")
error_logger.log_debug("Variable state: x=10, y=20")
```

---

## 🎯 Best Practices

### 1. Use Specific Exception Types

```python
# ❌ Bad - Generic exception
raise Exception("API call failed")

# ✅ Good - Specific exception with context
raise APIException(
    "API call failed: Quota exceeded",
    user_message="You've reached your API limit. Please try again in an hour."
)
```

### 2. Provide User-Friendly Messages

```python
# ❌ Bad - Technical jargon
raise FileException("ENOENT: no such file or directory")

# ✅ Good - Clear explanation
raise FileException(
    f"File not found: {file_path}",
    user_message="The file you're looking for doesn't exist. Please check the path."
)
```

### 3. Log Context Information

```python
# ❌ Bad - No context
try:
    result = process_data(data)
except Exception as e:
    print(f"Error: {e}")

# ✅ Good - Rich context
try:
    result = process_data(data)
except Exception as e:
    error_logger.log_error(
        e,
        context=f"Processing data for user {user_id}, batch {batch_id}"
    )
```

### 4. Don't Swallow Errors Silently

```python
# ❌ Bad - Silent failure
try:
    save_settings(settings)
except:
    pass  # Oops, settings weren't saved and nobody knows!

# ✅ Good - Log and handle
try:
    save_settings(settings)
except Exception as e:
    error_logger.log_error(e, "Failed to save settings")
    # Optionally retry or use defaults
    use_default_settings()
```

### 5. Use Appropriate Recovery Strategies

```python
# ❌ Bad - Fail completely on first error
def load_plugins(plugin_dir):
    plugins = []
    for file in plugin_dir.glob("*.py"):
        plugins.append(load_plugin(file))  # One failure kills all
    return plugins

# ✅ Good - Continue on individual failures
def load_plugins(plugin_dir):
    plugins = []
    for file in plugin_dir.glob("*.py"):
        with ErrorContext(f"Loading {file.name}", suppress=True) as ctx:
            plugin = load_plugin(file)
            if plugin:
                plugins.append(plugin)
    return plugins
```

---

## 🔍 Error Recovery Patterns

### Pattern 1: Fallback Chain

Try multiple strategies in order:

```python
def get_weather(city):
    """Try multiple weather services"""
    services = [
        lambda: get_weather_from_service_a(city),
        lambda: get_weather_from_service_b(city),
        lambda: get_cached_weather(city),
    ]
    
    for service in services:
        try:
            return service()
        except Exception as e:
            error_logger.log_warning(f"Service failed: {e}")
            continue
    
    raise NetworkException("All weather services failed")
```

### Pattern 2: Graceful Degradation

Provide reduced functionality instead of failing:

```python
def get_system_status():
    """Get system status with graceful degradation"""
    status = {
        'cpu': ErrorRecovery.safe_call(get_cpu_usage, default=0),
        'memory': ErrorRecovery.safe_call(get_memory_usage, default=0),
        'gpu': ErrorRecovery.safe_call(get_gpu_usage, default=None),  # Optional
        'temp': ErrorRecovery.safe_call(get_temperature, default=None),  # Optional
    }
    return status
```

### Pattern 3: Circuit Breaker

Stop trying after repeated failures:

```python
class CircuitBreaker:
    def __init__(self, max_failures=5, timeout=60):
        self.max_failures = max_failures
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = 0
    
    def call(self, func, *args, **kwargs):
        if self.failures >= self.max_failures:
            if time.time() - self.last_failure_time < self.timeout:
                raise NetworkException("Circuit breaker open - service unavailable")
            else:
                self.failures = 0  # Reset after timeout
        
        try:
            result = func(*args, **kwargs)
            self.failures = 0  # Reset on success
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            raise
```

---

## 📊 Error Logging

### Log Locations

- **Console**: INFO and above
- **File**: `logs/marklii_YYYYMMDD.log` - All levels

### Log Levels

| Level | When to Use |
|-------|-------------|
| `DEBUG` | Detailed diagnostic information |
| `INFO` | Confirmation that things are working |
| `WARNING` | Something unexpected but not breaking |
| `ERROR` | Serious problem, functionality impaired |
| `CRITICAL` | System about to crash |

### Example Log Entries

```
2026-09-22 15:30:45 - MarkLII - INFO - Starting voice session
2026-09-22 15:30:46 - MarkLII - WARNING - API key not found, using default
2026-09-22 15:30:50 - MarkLII - ERROR - [AUDIO] No microphone detected | Context: Audio device setup
2026-09-22 15:30:51 - MarkLII - DEBUG - Available devices: ['Device 1', 'Device 2']
```

---

## 🧪 Testing Error Handling

### Test Error Scenarios

```python
import pytest
from core.error_handler import APIException, handle_errors

def test_api_exception_message():
    """Test API exception carries user message"""
    error = APIException(
        "Technical error message",
        user_message="User-friendly message"
    )
    assert error.user_message == "User-friendly message"
    assert error.category == ErrorCategory.API

@handle_errors(category=ErrorCategory.FILE, default_return=None)
def read_file_with_handling(path):
    with open(path, 'r') as f:
        return f.read()

def test_error_handler_decorator():
    """Test error handler returns default on error"""
    result = read_file_with_handling("/nonexistent/file.txt")
    assert result is None  # Should return default instead of raising
```

---

## 🔧 Migrating Existing Code

### Before (Basic try/except)

```python
def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error: {e}")
        return {}
```

### After (With error handling framework)

```python
from core.error_handler import handle_errors, FileException, ErrorCategory

@handle_errors(
    category=ErrorCategory.FILE,
    default_return={},
    user_friendly=True
)
def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileException(
            "Config file not found: config.json",
            user_message="Configuration file is missing. Please run setup."
        )
    except json.JSONDecodeError as e:
        raise FileException(
            f"Invalid JSON in config file: {e}",
            user_message="Configuration file is corrupted. Please restore or recreate it."
        )
```

---

## 📚 Additional Resources

- [BUGFIXES.md](BUGFIXES.md) - Known bugs and fixes
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Code guidelines

---

**Last Updated**: September 22, 2026  
**Version**: Mark LII
