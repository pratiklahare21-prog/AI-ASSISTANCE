"""
Processing Utilities for MARK LII
Optimized data processing, caching, and performance utilities
"""

import hashlib
import time
import json
from typing import Any, Callable, Optional, Dict, List
from functools import wraps, lru_cache
from pathlib import Path
from datetime import datetime, timedelta
import threading

# ============================================================================
# Caching System
# ============================================================================

class Cache:
    """
    Simple in-memory cache with TTL (Time To Live) support
    """
    def __init__(self, default_ttl: int = 300):
        """
        Initialize cache
        
        Args:
            default_ttl: Default time-to-live in seconds (default: 5 minutes)
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._default_ttl = default_ttl
        self._lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if expired/not found
        """
        with self._lock:
            if key not in self._cache:
                return None
            
            entry = self._cache[key]
            
            # Check if expired
            if entry['expires_at'] < time.time():
                del self._cache[key]
                return None
            
            entry['hits'] += 1
            entry['last_accessed'] = time.time()
            return entry['value']
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (uses default if None)
        """
        with self._lock:
            ttl = ttl if ttl is not None else self._default_ttl
            self._cache[key] = {
                'value': value,
                'created_at': time.time(),
                'expires_at': time.time() + ttl,
                'last_accessed': time.time(),
                'hits': 0,
            }
    
    def delete(self, key: str) -> bool:
        """
        Delete value from cache
        
        Args:
            key: Cache key
            
        Returns:
            True if deleted, False if not found
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def clear(self) -> None:
        """Clear entire cache"""
        with self._lock:
            self._cache.clear()
    
    def cleanup_expired(self) -> int:
        """
        Remove expired entries
        
        Returns:
            Number of entries removed
        """
        with self._lock:
            now = time.time()
            expired_keys = [
                k for k, v in self._cache.items()
                if v['expires_at'] < now
            ]
            for key in expired_keys:
                del self._cache[key]
            return len(expired_keys)
    
    def stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Dictionary with cache stats
        """
        with self._lock:
            total_entries = len(self._cache)
            total_hits = sum(e['hits'] for e in self._cache.values())
            
            return {
                'total_entries': total_entries,
                'total_hits': total_hits,
                'memory_usage_estimate': sum(
                    len(str(v['value'])) for v in self._cache.values()
                ),
            }

# Global cache instance
_global_cache = Cache()

def cache_result(ttl: int = 300, key_prefix: str = ""):
    """
    Decorator to cache function results
    
    Args:
        ttl: Time-to-live in seconds
        key_prefix: Prefix for cache key
        
    Example:
        @cache_result(ttl=600, key_prefix="weather")
        def get_weather(city):
            return fetch_weather_api(city)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            key_parts = [key_prefix, func.__name__] if key_prefix else [func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = ":".join(key_parts)
            
            # Try to get from cache
            cached_value = _global_cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Compute and cache result
            result = func(*args, **kwargs)
            _global_cache.set(cache_key, result, ttl)
            return result
        
        return wrapper
    return decorator

# ============================================================================
# Data Processing Utilities
# ============================================================================

def chunk_list(data: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split list into chunks of specified size
    
    Args:
        data: List to chunk
        chunk_size: Size of each chunk
        
    Returns:
        List of chunks
        
    Example:
        >>> chunk_list([1,2,3,4,5], 2)
        [[1,2], [3,4], [5]]
    """
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

def flatten_list(nested_list: List[List[Any]]) -> List[Any]:
    """
    Flatten a nested list
    
    Args:
        nested_list: Nested list to flatten
        
    Returns:
        Flattened list
        
    Example:
        >>> flatten_list([[1,2], [3,4], [5]])
        [1,2,3,4,5]
    """
    return [item for sublist in nested_list for item in sublist]

def deduplicate(items: List[Any], key: Optional[Callable] = None) -> List[Any]:
    """
    Remove duplicates from list while preserving order
    
    Args:
        items: List with potential duplicates
        key: Optional function to extract comparison key
        
    Returns:
        List without duplicates
        
    Example:
        >>> deduplicate([1,2,2,3,1,4])
        [1,2,3,4]
    """
    seen = set()
    result = []
    
    for item in items:
        item_key = key(item) if key else item
        
        # Handle unhashable types
        try:
            if item_key not in seen:
                seen.add(item_key)
                result.append(item)
        except TypeError:
            # For unhashable types, do linear search
            if item_key not in [key(r) if key else r for r in result]:
                result.append(item)
    
    return result

def batch_process(items: List[Any], 
                 processor: Callable[[Any], Any],
                 batch_size: int = 10,
                 show_progress: bool = False) -> List[Any]:
    """
    Process items in batches
    
    Args:
        items: Items to process
        processor: Function to process each item
        batch_size: Number of items per batch
        show_progress: Print progress updates
        
    Returns:
        List of processed items
    """
    results = []
    total = len(items)
    
    for i, chunk in enumerate(chunk_list(items, batch_size)):
        chunk_results = [processor(item) for item in chunk]
        results.extend(chunk_results)
        
        if show_progress:
            progress = ((i + 1) * batch_size) / total * 100
            print(f"Progress: {min(progress, 100):.1f}% ({i+1}/{total//batch_size+1} batches)")
    
    return results

# ============================================================================
# Text Processing
# ============================================================================

def truncate_text(text: str, max_length: int = 100, 
                  suffix: str = "...") -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """
    Sanitize filename for filesystem compatibility
    
    Args:
        filename: Original filename
        max_length: Maximum filename length
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing dots and spaces
    filename = filename.strip('. ')
    
    # Truncate if too long
    if len(filename) > max_length:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        max_name_length = max_length - len(ext) - 1
        filename = name[:max_name_length] + ('.' + ext if ext else '')
    
    return filename or 'unnamed'

def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract keywords from text (simple implementation)
    
    Args:
        text: Text to extract keywords from
        max_keywords: Maximum number of keywords
        
    Returns:
        List of keywords
    """
    # Simple word frequency approach
    words = text.lower().split()
    
    # Common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
                  'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'}
    
    # Filter and count
    word_freq = {}
    for word in words:
        # Remove punctuation
        word = ''.join(c for c in word if c.isalnum())
        if word and word not in stop_words and len(word) > 2:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, _ in sorted_words[:max_keywords]]

# ============================================================================
# File Processing Utilities
# ============================================================================

def compute_file_hash(file_path: Path, algorithm: str = 'sha256') -> str:
    """
    Compute hash of file
    
    Args:
        file_path: Path to file
        algorithm: Hash algorithm (md5, sha1, sha256)
        
    Returns:
        Hex digest of file hash
    """
    hash_func = hashlib.new(algorithm)
    
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()

def get_file_size_mb(file_path: Path) -> float:
    """
    Get file size in megabytes
    
    Args:
        file_path: Path to file
        
    Returns:
        File size in MB
    """
    return file_path.stat().st_size / (1024 * 1024)

def is_file_recent(file_path: Path, max_age_hours: int = 24) -> bool:
    """
    Check if file was modified recently
    
    Args:
        file_path: Path to file
        max_age_hours: Maximum age in hours
        
    Returns:
        True if file is recent
    """
    if not file_path.exists():
        return False
    
    modified_time = datetime.fromtimestamp(file_path.stat().st_mtime)
    age = datetime.now() - modified_time
    return age < timedelta(hours=max_age_hours)

# ============================================================================
# Performance Monitoring
# ============================================================================

class Timer:
    """Context manager for timing code blocks"""
    
    def __init__(self, name: str = "Operation", verbose: bool = True):
        self.name = name
        self.verbose = verbose
        self.start_time = None
        self.elapsed_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, *args):
        self.elapsed_time = time.time() - self.start_time
        if self.verbose:
            print(f"⏱️  {self.name} took {self.elapsed_time:.3f}s")
    
    def __str__(self):
        if self.elapsed_time is not None:
            return f"{self.elapsed_time:.3f}s"
        return "Not completed"

def timeit(func: Callable) -> Callable:
    """
    Decorator to time function execution
    
    Example:
        @timeit
        def slow_function():
            time.sleep(1)
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"⏱️  {func.__name__} took {elapsed:.3f}s")
        return result
    return wrapper

# ============================================================================
# Data Validation
# ============================================================================

def validate_url(url: str) -> bool:
    """
    Validate URL format
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid URL format
    """
    import re
    pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(pattern.match(url))

def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email to validate
        
    Returns:
        True if valid email format
    """
    import re
    pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(pattern.match(email))

def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Clamp value between min and max
    
    Args:
        value: Value to clamp
        min_value: Minimum value
        max_value: Maximum value
        
    Returns:
        Clamped value
    """
    return max(min_value, min(value, max_value))

# ============================================================================
# Export
# ============================================================================

__all__ = [
    'Cache',
    'cache_result',
    'chunk_list',
    'flatten_list',
    'deduplicate',
    'batch_process',
    'truncate_text',
    'sanitize_filename',
    'extract_keywords',
    'compute_file_hash',
    'get_file_size_mb',
    'is_file_recent',
    'Timer',
    'timeit',
    'validate_url',
    'validate_email',
    'clamp',
]
