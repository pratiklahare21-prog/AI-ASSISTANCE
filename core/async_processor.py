"""
Asynchronous Processing Utilities for MARK LII
Helpers for concurrent and parallel processing
"""

import asyncio
import concurrent.futures
import threading
from typing import Any, Callable, List, Optional, TypeVar, Coroutine
from functools import wraps

T = TypeVar('T')

# ============================================================================
# Thread Pool Processing
# ============================================================================

class ThreadPool:
    """
    Thread pool for concurrent processing
    """
    def __init__(self, max_workers: Optional[int] = None):
        """
        Initialize thread pool
        
        Args:
            max_workers: Maximum number of worker threads (default: CPU count)
        """
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    
    def submit(self, func: Callable, *args, **kwargs) -> concurrent.futures.Future:
        """
        Submit function to thread pool
        
        Args:
            func: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Future object
        """
        return self.executor.submit(func, *args, **kwargs)
    
    def map(self, func: Callable[[T], Any], items: List[T], 
            timeout: Optional[float] = None) -> List[Any]:
        """
        Map function over items in parallel
        
        Args:
            func: Function to apply
            items: Items to process
            timeout: Optional timeout in seconds
            
        Returns:
            List of results
        """
        return list(self.executor.map(func, items, timeout=timeout))
    
    def shutdown(self, wait: bool = True):
        """
        Shutdown thread pool
        
        Args:
            wait: Wait for pending tasks to complete
        """
        self.executor.shutdown(wait=wait)

# Global thread pool instance
_global_pool = ThreadPool()

def run_in_thread(func: Callable) -> Callable:
    """
    Decorator to run function in separate thread
    
    Example:
        @run_in_thread
        def long_running_task():
            time.sleep(10)
            return "Done"
        
        future = long_running_task()
        result = future.result()  # Blocks until complete
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return _global_pool.submit(func, *args, **kwargs)
    return wrapper

def parallel_map(func: Callable[[T], Any], items: List[T],
                max_workers: Optional[int] = None) -> List[Any]:
    """
    Map function over items in parallel using thread pool
    
    Args:
        func: Function to apply
        items: Items to process
        max_workers: Maximum number of workers
        
    Returns:
        List of results
        
    Example:
        def process_item(x):
            return x * 2
        
        results = parallel_map(process_item, [1,2,3,4,5])
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(func, items))

# ============================================================================
# Process Pool Processing
# ============================================================================

def parallel_process(func: Callable[[T], Any], items: List[T],
                    max_workers: Optional[int] = None) -> List[Any]:
    """
    Map function over items in parallel using process pool (CPU-intensive tasks)
    
    Args:
        func: Function to apply (must be picklable)
        items: Items to process
        max_workers: Maximum number of processes
        
    Returns:
        List of results
        
    Example:
        def cpu_intensive_task(x):
            return sum(range(x * 1000000))
        
        results = parallel_process(cpu_intensive_task, [1,2,3,4,5])
    """
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(func, items))

# ============================================================================
# Async/Await Utilities
# ============================================================================

def run_async(coro: Coroutine) -> Any:
    """
    Run async coroutine in sync context
    
    Args:
        coro: Coroutine to run
        
    Returns:
        Result of coroutine
        
    Example:
        async def async_function():
            await asyncio.sleep(1)
            return "Done"
        
        result = run_async(async_function())
    """
    try:
        loop = asyncio.get_running_loop()
        # If we're already in an event loop, create a new one in a thread
        future = concurrent.futures.Future()
        
        def run_in_new_loop():
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                result = new_loop.run_until_complete(coro)
                future.set_result(result)
            except Exception as e:
                future.set_exception(e)
            finally:
                new_loop.close()
        
        thread = threading.Thread(target=run_in_new_loop)
        thread.start()
        thread.join()
        return future.result()
    except RuntimeError:
        # No event loop running, we can use asyncio.run directly
        return asyncio.run(coro)

async def gather_with_limit(coros: List[Coroutine], limit: int = 10) -> List[Any]:
    """
    Run coroutines concurrently with concurrency limit
    
    Args:
        coros: List of coroutines
        limit: Maximum concurrent coroutines
        
    Returns:
        List of results
        
    Example:
        async def fetch(url):
            # fetch url
            pass
        
        urls = ["url1", "url2", "url3", ...]
        results = await gather_with_limit([fetch(url) for url in urls], limit=5)
    """
    semaphore = asyncio.Semaphore(limit)
    
    async def bounded_coro(coro):
        async with semaphore:
            return await coro
    
    return await asyncio.gather(*[bounded_coro(coro) for coro in coros])

async def timeout_after(coro: Coroutine, seconds: float,
                       default: Optional[Any] = None) -> Any:
    """
    Run coroutine with timeout
    
    Args:
        coro: Coroutine to run
        seconds: Timeout in seconds
        default: Default value if timeout
        
    Returns:
        Result or default value
        
    Example:
        async def slow_function():
            await asyncio.sleep(10)
            return "Done"
        
        result = await timeout_after(slow_function(), 5, default="Timeout")
    """
    try:
        return await asyncio.wait_for(coro, timeout=seconds)
    except asyncio.TimeoutError:
        return default

# ============================================================================
# Background Task Management
# ============================================================================

class BackgroundTask:
    """
    Manages a background task running in a separate thread
    """
    def __init__(self, func: Callable, *args, daemon: bool = True, **kwargs):
        """
        Initialize background task
        
        Args:
            func: Function to run in background
            *args: Positional arguments for function
            daemon: Whether thread should be daemon
            **kwargs: Keyword arguments for function
        """
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.thread = None
        self.daemon = daemon
        self._stop_event = threading.Event()
        self._result = None
        self._exception = None
    
    def start(self) -> 'BackgroundTask':
        """Start the background task"""
        if self.thread and self.thread.is_alive():
            raise RuntimeError("Task is already running")
        
        def wrapper():
            try:
                self._result = self.func(*self.args, **self.kwargs)
            except Exception as e:
                self._exception = e
        
        self.thread = threading.Thread(target=wrapper, daemon=self.daemon)
        self.thread.start()
        return self
    
    def stop(self):
        """Signal the task to stop"""
        self._stop_event.set()
    
    def is_running(self) -> bool:
        """Check if task is running"""
        return self.thread is not None and self.thread.is_alive()
    
    def join(self, timeout: Optional[float] = None) -> Any:
        """
        Wait for task to complete
        
        Args:
            timeout: Optional timeout in seconds
            
        Returns:
            Task result
            
        Raises:
            Exception if task raised an exception
        """
        if self.thread:
            self.thread.join(timeout)
        
        if self._exception:
            raise self._exception
        
        return self._result
    
    @property
    def should_stop(self) -> bool:
        """Check if task should stop"""
        return self._stop_event.is_set()

def run_in_background(func: Callable, *args, daemon: bool = True, **kwargs) -> BackgroundTask:
    """
    Run function in background thread
    
    Args:
        func: Function to run
        *args: Positional arguments
        daemon: Whether thread should be daemon
        **kwargs: Keyword arguments
        
    Returns:
        BackgroundTask instance
        
    Example:
        def long_task():
            for i in range(100):
                if task.should_stop:
                    break
                time.sleep(0.1)
            return "Done"
        
        task = run_in_background(long_task)
        # ... do other work ...
        result = task.join()  # Wait for completion
    """
    task = BackgroundTask(func, *args, daemon=daemon, **kwargs)
    return task.start()

# ============================================================================
# Debounce and Throttle
# ============================================================================

def debounce(wait: float):
    """
    Debounce function calls - only execute after wait time with no new calls
    
    Args:
        wait: Wait time in seconds
        
    Example:
        @debounce(0.5)
        def search(query):
            print(f"Searching for: {query}")
        
        # Typing quickly - only last call executes
        search("a")
        search("ap")
        search("app")  # Only this executes after 0.5s of no calls
    """
    def decorator(func: Callable) -> Callable:
        timer = None
        lock = threading.Lock()
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal timer
            
            def execute():
                func(*args, **kwargs)
            
            with lock:
                if timer:
                    timer.cancel()
                timer = threading.Timer(wait, execute)
                timer.start()
        
        return wrapper
    return decorator

def throttle(wait: float):
    """
    Throttle function calls - execute at most once per wait period
    
    Args:
        wait: Minimum time between calls in seconds
        
    Example:
        @throttle(1.0)
        def update_ui():
            print("UI updated")
        
        # Called rapidly - executes at most once per second
        for i in range(100):
            update_ui()
    """
    def decorator(func: Callable) -> Callable:
        last_called = [0.0]
        lock = threading.Lock()
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                now = threading.Timer.__class__.time() if hasattr(threading.Timer, 'time') else __import__('time').time()
                if now - last_called[0] >= wait:
                    last_called[0] = now
                    return func(*args, **kwargs)
        
        return wrapper
    return decorator

# ============================================================================
# Export
# ============================================================================

__all__ = [
    'ThreadPool',
    'run_in_thread',
    'parallel_map',
    'parallel_process',
    'run_async',
    'gather_with_limit',
    'timeout_after',
    'BackgroundTask',
    'run_in_background',
    'debounce',
    'throttle',
]
