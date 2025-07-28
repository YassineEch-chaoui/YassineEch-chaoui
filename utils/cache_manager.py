"""
Cache management utilities for improved performance
"""
import streamlit as st
import time
import hashlib
from typing import Any, Optional, Callable, Dict
from functools import wraps
from config.constants import CACHE_TTL

class CacheManager:
    """Manages application caching with TTL support"""
    
    def __init__(self):
        self.initialize_cache()
    
    def initialize_cache(self):
        """Initialize cache in session state"""
        if 'app_cache' not in st.session_state:
            st.session_state.app_cache = {}
        
        if 'cache_timestamps' not in st.session_state:
            st.session_state.cache_timestamps = {}
    
    def get_cache_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate a unique cache key"""
        # Create a string representation of arguments
        key_parts = [prefix]
        
        for arg in args:
            key_parts.append(str(arg))
        
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}:{v}")
        
        key_string = "|".join(key_parts)
        
        # Hash the key to ensure consistent length
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def is_cache_valid(self, cache_key: str, ttl: int = CACHE_TTL) -> bool:
        """Check if cached data is still valid"""
        if cache_key not in st.session_state.cache_timestamps:
            return False
        
        cache_time = st.session_state.cache_timestamps[cache_key]
        current_time = time.time()
        
        return (current_time - cache_time) < ttl
    
    def get_cached_data(self, cache_key: str, ttl: int = CACHE_TTL) -> Optional[Any]:
        """Retrieve cached data if valid"""
        if not self.is_cache_valid(cache_key, ttl):
            return None
        
        return st.session_state.app_cache.get(cache_key)
    
    def set_cached_data(self, cache_key: str, data: Any):
        """Store data in cache with timestamp"""
        st.session_state.app_cache[cache_key] = data
        st.session_state.cache_timestamps[cache_key] = time.time()
    
    def invalidate_cache(self, cache_key: str):
        """Remove specific item from cache"""
        if cache_key in st.session_state.app_cache:
            del st.session_state.app_cache[cache_key]
        
        if cache_key in st.session_state.cache_timestamps:
            del st.session_state.cache_timestamps[cache_key]
    
    def clear_expired_cache(self, ttl: int = CACHE_TTL):
        """Clear all expired cache entries"""
        current_time = time.time()
        expired_keys = []
        
        for cache_key, cache_time in st.session_state.cache_timestamps.items():
            if (current_time - cache_time) >= ttl:
                expired_keys.append(cache_key)
        
        for key in expired_keys:
            self.invalidate_cache(key)
    
    def clear_all_cache(self):
        """Clear all cached data"""
        st.session_state.app_cache = {}
        st.session_state.cache_timestamps = {}
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_items = len(st.session_state.app_cache)
        current_time = time.time()
        
        valid_items = 0
        expired_items = 0
        
        for cache_key, cache_time in st.session_state.cache_timestamps.items():
            if (current_time - cache_time) < CACHE_TTL:
                valid_items += 1
            else:
                expired_items += 1
        
        return {
            'total_items': total_items,
            'valid_items': valid_items,
            'expired_items': expired_items,
            'cache_hit_ratio': valid_items / max(total_items, 1)
        }

def cached_function(ttl: int = CACHE_TTL, key_prefix: str = None):
    """
    Decorator for caching function results
    
    Args:
        ttl: Time to live in seconds
        key_prefix: Custom prefix for cache key
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_manager = CacheManager()
            
            # Generate cache key
            prefix = key_prefix or func.__name__
            cache_key = cache_manager.get_cache_key(prefix, *args, **kwargs)
            
            # Try to get cached result
            cached_result = cache_manager.get_cached_data(cache_key, ttl)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            try:
                result = func(*args, **kwargs)
                cache_manager.set_cached_data(cache_key, result)
                return result
            except Exception as e:
                # Don't cache errors
                raise e
        
        return wrapper
    return decorator

class PerformanceMonitor:
    """Monitor and track application performance"""
    
    def __init__(self):
        self.initialize_metrics()
    
    def initialize_metrics(self):
        """Initialize performance metrics in session state"""
        if 'perf_metrics' not in st.session_state:
            st.session_state.perf_metrics = {
                'page_loads': 0,
                'api_calls': 0,
                'cache_hits': 0,
                'cache_misses': 0,
                'total_load_time': 0,
                'function_times': {}
            }
    
    def track_page_load(self):
        """Track page load event"""
        st.session_state.perf_metrics['page_loads'] += 1
    
    def track_api_call(self):
        """Track API call event"""
        st.session_state.perf_metrics['api_calls'] += 1
    
    def track_cache_hit(self):
        """Track cache hit event"""
        st.session_state.perf_metrics['cache_hits'] += 1
    
    def track_cache_miss(self):
        """Track cache miss event"""
        st.session_state.perf_metrics['cache_misses'] += 1
    
    def track_function_time(self, function_name: str, execution_time: float):
        """Track function execution time"""
        if function_name not in st.session_state.perf_metrics['function_times']:
            st.session_state.perf_metrics['function_times'][function_name] = []
        
        st.session_state.perf_metrics['function_times'][function_name].append(execution_time)
        
        # Keep only last 100 measurements
        if len(st.session_state.perf_metrics['function_times'][function_name]) > 100:
            st.session_state.perf_metrics['function_times'][function_name] = \
                st.session_state.perf_metrics['function_times'][function_name][-100:]
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        metrics = st.session_state.perf_metrics
        
        # Calculate cache hit ratio
        total_cache_requests = metrics['cache_hits'] + metrics['cache_misses']
        cache_hit_ratio = metrics['cache_hits'] / max(total_cache_requests, 1)
        
        # Calculate average function times
        avg_function_times = {}
        for func_name, times in metrics['function_times'].items():
            if times:
                avg_function_times[func_name] = sum(times) / len(times)
        
        return {
            'page_loads': metrics['page_loads'],
            'api_calls': metrics['api_calls'],
            'cache_hit_ratio': cache_hit_ratio,
            'avg_function_times': avg_function_times
        }

def timed_function(monitor: PerformanceMonitor = None):
    """
    Decorator for timing function execution
    
    Args:
        monitor: PerformanceMonitor instance
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.time()
                execution_time = end_time - start_time
                
                if monitor:
                    monitor.track_function_time(func.__name__, execution_time)
        
        return wrapper
    return decorator

# Global instances
cache_manager = CacheManager()
performance_monitor = PerformanceMonitor()