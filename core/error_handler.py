"""
Centralized Error Handling for MARK LII
Provides consistent error handling, logging, and user feedback across the application
"""

import sys
import traceback
import logging
from pathlib import Path
from typing import Optional, Callable, Any
from functools import wraps
from datetime import datetime
from enum import Enum

# ============================================================================
# Error Categories
# ============================================================================

class ErrorCategory(Enum):
    """Categories of errors for better handling"""
    API = "api"                     # API-related errors
    AUDIO = "audio"                 # Audio input/output errors
    FILE = "file"                   # File operation errors
    NETWORK = "network"             # Network/connection errors
    SYSTEM = "system"               # System control errors
    UI = "ui"                       # UI-related errors
    PLUGIN = "plugin"               # Plugin loading/execution errors
    MEMORY = "memory"               # Memory/storage errors
    VALIDATION = "validation"       # Input validation errors
    UNKNOWN = "unknown"             # Uncategorized errors

# ============================================================================
# Custom Exceptions
# ============================================================================

class MarkLIIException(Exception):
    """Base exception for MARK LII"""
    def __init__(self, message: str, category: ErrorCategory = ErrorCategory.UNKNOWN,
                 recoverable: bool = True, user_message: Optional[str] = None):
        super().__init__(message)
        self.category = category
        self.recoverable = recoverable
        self.user_message = user_message or message
        self.timestamp = datetime.now()

class APIException(MarkLIIException):
    """API-related errors"""
    def __init__(self, message: str, user_message: Optional[str] = None):
        super().__init__(message, ErrorCategory.API, True, user_message)

class AudioException(MarkLIIException):
    """Audio input/output errors"""
    def __init__(self, message: str, user_message: Optional[str] = None):
        super().__init__(message, ErrorCategory.AUDIO, True, user_message)

class FileException(MarkLIIException):
    """File operation errors"""
    def __init__(self, message: str, user_message: Optional[str] = None):
        super().__init__(message, ErrorCategory.FILE, True, user_message)

class NetworkException(MarkLIIException):
    """Network/connection errors"""
    def __init__(self, message: str, user_message: Optional[str] = None):
        super().__init__(message, ErrorCategory.NETWORK, True, user_message)

class ValidationException(MarkLIIException):
    """Input validation errors"""
    def __init__(self, message: str, user_message: Optional[str] = None):
        super().__init__(message, ErrorCategory.VALIDATION, True, user_message)

# ============================================================================
# Error Logger
# ============================================================================

class ErrorLogger:
    """Centralized error logging"""
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self):
        """Set up logging configuration"""
        self._logger = logging.getLogger('MarkLII')
        self._logger.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_format)
        
        # File handler (if logs directory exists)
        try:
            log_dir = Path(__file__).parent.parent / "logs"
            log_dir.mkdir(exist_ok=True)
            
            log_file = log_dir / f"marklii_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_format = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_format)
            self._logger.addHandler(file_handler)
        except Exception:
            pass  # Silent fail if can't create log file
        
        self._logger.addHandler(console_handler)
    
    def log_error(self, error: Exception, context: Optional[str] = None):
        """Log an error with full context"""
        if isinstance(error, MarkLIIException):
            message = f"[{error.category.value.upper()}] {error}"
            if context:
                message += f" | Context: {context}"
            self._logger.error(message)
        else:
            message = f"Unexpected error: {type(error).__name__}: {error}"
            if context:
                message += f" | Context: {context}"
            self._logger.error(message)
            self._logger.debug(traceback.format_exc())
    
    def log_warning(self, message: str):
        """Log a warning"""
        self._logger.warning(message)
    
    def log_info(self, message: str):
        """Log informational message"""
        self._logger.info(message)
    
    def log_debug(self, message: str):
        """Log debug message"""
        self._logger.debug(message)

# Global logger instance
error_logger = ErrorLogger()

# ============================================================================
# Error Handler Decorator
# ============================================================================

def handle_errors(category: ErrorCategory = ErrorCategory.UNKNOWN,
                  default_return: Any = None,
                  user_friendly: bool = True,
                  reraise: bool = False):
    """
    Decorator for consistent error handling
    
    Args:
        category: Error category for better tracking
        default_return: Value to return on error
        user_friendly: Show user-friendly messages
        reraise: Re-raise exception after logging
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except MarkLIIException as e:
                error_logger.log_error(e, f"Function: {func.__name__}")
                if reraise:
                    raise
                return default_return
            except Exception as e:
                # Wrap in MarkLIIException
                wrapped_error = MarkLIIException(
                    str(e),
                    category,
                    user_message=f"An error occurred in {func.__name__}"
                )
                error_logger.log_error(wrapped_error, f"Function: {func.__name__}")
                if reraise:
                    raise wrapped_error from e
                return default_return
        return wrapper
    return decorator

# ============================================================================
# Retry Decorator
# ============================================================================

def retry_on_error(max_attempts: int = 3,
                   delay: float = 1.0,
                   exceptions: tuple = (Exception,),
                   backoff: bool = True):
    """
    Retry a function on specific exceptions
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries (seconds)
        exceptions: Tuple of exceptions to catch
        backoff: Use exponential backoff for delays
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            current_delay = delay
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        raise
                    
                    error_logger.log_warning(
                        f"Attempt {attempt + 1}/{max_attempts} failed for "
                        f"{func.__name__}: {e}. Retrying in {current_delay}s..."
                    )
                    time.sleep(current_delay)
                    
                    if backoff:
                        current_delay *= 2
        return wrapper
    return decorator

# ============================================================================
# Context Manager for Error Handling
# ============================================================================

class ErrorContext:
    """Context manager for handling errors in a block"""
    
    def __init__(self, context_name: str,
                 category: ErrorCategory = ErrorCategory.UNKNOWN,
                 suppress: bool = False,
                 default_return: Any = None):
        self.context_name = context_name
        self.category = category
        self.suppress = suppress
        self.default_return = default_return
        self.error = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.error = exc_val
            error_logger.log_error(exc_val, self.context_name)
            
            if self.suppress:
                return True  # Suppress the exception
        return False

# ============================================================================
# User-Friendly Error Messages
# ============================================================================

ERROR_MESSAGES = {
    # API Errors
    "api_key_invalid": "⚠️ Your API key appears to be invalid. Please check your configuration.",
    "api_quota_exceeded": "⚠️ API quota exceeded. Please wait a few moments and try again.",
    "api_timeout": "⚠️ Request timed out. Please check your internet connection.",
    "api_unavailable": "⚠️ Service temporarily unavailable. Please try again later.",
    
    # Audio Errors
    "no_microphone": "⚠️ No microphone detected. Please connect a microphone and select it in settings.",
    "no_speakers": "⚠️ No speakers detected. Please connect speakers/headphones and select them in settings.",
    "audio_device_error": "⚠️ Audio device error. Try selecting a different device in settings.",
    "audio_permission_denied": "⚠️ Microphone access denied. Please grant permission in system settings.",
    
    # File Errors
    "file_not_found": "⚠️ File not found. Please check the file path.",
    "file_too_large": "⚠️ File is too large. Maximum size is 100 MB.",
    "file_read_error": "⚠️ Could not read file. File may be corrupted or in use.",
    "file_write_error": "⚠️ Could not write file. Check disk space and permissions.",
    
    # Network Errors
    "network_unavailable": "⚠️ No internet connection. Please check your network.",
    "connection_timeout": "⚠️ Connection timed out. Please try again.",
    "connection_refused": "⚠️ Connection refused. Service may be down.",
    
    # System Errors
    "permission_denied": "⚠️ Permission denied. Try running with elevated privileges.",
    "resource_unavailable": "⚠️ System resource unavailable. Please try again.",
    
    # Validation Errors
    "invalid_input": "⚠️ Invalid input. Please check your input and try again.",
    "missing_required_field": "⚠️ Required field is missing.",
}

def get_user_message(error_key: str, default: str = "An error occurred") -> str:
    """Get user-friendly error message"""
    return ERROR_MESSAGES.get(error_key, default)

# ============================================================================
# Error Recovery Strategies
# ============================================================================

class ErrorRecovery:
    """Strategies for recovering from errors"""
    
    @staticmethod
    def retry_with_fallback(primary_func: Callable,
                           fallback_func: Callable,
                           *args, **kwargs):
        """Try primary function, fall back to alternative on error"""
        try:
            return primary_func(*args, **kwargs)
        except Exception as e:
            error_logger.log_warning(
                f"Primary function failed: {e}. Trying fallback..."
            )
            return fallback_func(*args, **kwargs)
    
    @staticmethod
    def safe_call(func: Callable, default: Any = None, *args, **kwargs):
        """Call function and return default on error"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_logger.log_error(e, f"Safe call to {func.__name__}")
            return default
    
    @staticmethod
    def validate_and_fix(value: Any, validator: Callable,
                         fixer: Optional[Callable] = None) -> Any:
        """Validate value and attempt to fix if invalid"""
        if validator(value):
            return value
        
        if fixer:
            try:
                fixed_value = fixer(value)
                if validator(fixed_value):
                    error_logger.log_info(f"Auto-fixed invalid value: {value} → {fixed_value}")
                    return fixed_value
            except Exception:
                pass
        
        raise ValidationException(f"Invalid value: {value}")

# ============================================================================
# Helper Functions
# ============================================================================

def safe_import(module_name: str, package: Optional[str] = None):
    """Safely import a module with error handling"""
    try:
        if package:
            return __import__(module_name, fromlist=[package])
        return __import__(module_name)
    except ImportError as e:
        error_logger.log_error(
            e,
            f"Failed to import {module_name}"
        )
        return None

def safe_get_attr(obj: Any, attr: str, default: Any = None):
    """Safely get attribute with default"""
    try:
        return getattr(obj, attr, default)
    except Exception:
        return default

def safe_dict_get(d: dict, key: str, default: Any = None):
    """Safely get dictionary value with error handling"""
    try:
        return d.get(key, default)
    except (AttributeError, TypeError):
        return default

# ============================================================================
# Export
# ============================================================================

__all__ = [
    'ErrorCategory',
    'MarkLIIException',
    'APIException',
    'AudioException',
    'FileException',
    'NetworkException',
    'ValidationException',
    'ErrorLogger',
    'error_logger',
    'handle_errors',
    'retry_on_error',
    'ErrorContext',
    'get_user_message',
    'ErrorRecovery',
    'safe_import',
    'safe_get_attr',
    'safe_dict_get',
]
