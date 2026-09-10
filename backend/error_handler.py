"""
Comprehensive error handling and recovery utilities
"""

import logging
import asyncio
import time
from functools import wraps
from typing import Callable, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class RateLimitError(Exception):
    """Raised when API rate limit is exceeded"""
    pass

class APIError(Exception):
    """Raised when API call fails"""
    pass

class ErrorHandler:
    """Handle errors with retry logic and fallback"""
    
    def __init__(self, max_retries: int = 3, timeout: int = 30):
        self.max_retries = max_retries
        self.timeout = timeout
        self.failed_calls = []
    
    def retry_with_backoff(self, func: Callable, *args, **kwargs) -> Any:
        """
        Retry function with exponential backoff
        
        Retry strategy:
        - 1st retry: 1 second
        - 2nd retry: 2 seconds
        - 3rd retry: 4 seconds
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Attempt {attempt + 1}/{self.max_retries}: {func.__name__}")
                result = func(*args, **kwargs)
                return result
            
            except RateLimitError as e:
                wait_time = 2 ** attempt  # Exponential backoff
                logger.warning(
                    f"Rate limit hit. Waiting {wait_time}s before retry..."
                )
                time.sleep(wait_time)
                last_exception = e
            
            except APIError as e:
                wait_time = 2 ** attempt
                logger.warning(
                    f"API error: {e}. Waiting {wait_time}s before retry..."
                )
                time.sleep(wait_time)
                last_exception = e
            
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                last_exception = e
                break
        
        # All retries exhausted
        logger.error(f"Failed after {self.max_retries} attempts")
        self.failed_calls.append({
            "function": func.__name__,
            "timestamp": datetime.now(),
            "error": str(last_exception)
        })
        raise last_exception
    
    async def async_retry_with_backoff(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """Async version of retry_with_backoff"""
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Attempt {attempt + 1}/{self.max_retries}: {func.__name__}")
                result = await func(*args, **kwargs)
                return result
            
            except (RateLimitError, APIError) as e:
                wait_time = 2 ** attempt
                logger.warning(
                    f"Error: {e}. Waiting {wait_time}s before retry..."
                )
                await asyncio.sleep(wait_time)
                last_exception = e
            
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                last_exception = e
                break
        
        logger.error(f"Failed after {self.max_retries} attempts")
        self.failed_calls.append({
            "function": func.__name__,
            "timestamp": datetime.now(),
            "error": str(last_exception)
        })
        raise last_exception
    
    def get_failed_calls(self, last_n: int = 10):
        """Get last N failed calls"""
        return self.failed_calls[-last_n:]
    
    def clear_failed_calls(self):
        """Clear failed calls history"""
        self.failed_calls = []

class CircuitBreaker:
    """Circuit breaker pattern for preventing cascading failures"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'closed'  # closed, open, half_open
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Call function with circuit breaker protection"""
        
        # Check if circuit should be reset
        if self.state == 'open':
            if datetime.now() - self.last_failure_time > timedelta(seconds=self.timeout):
                logger.info("Circuit breaker: Attempting to recover...")
                self.state = 'half_open'
            else:
                raise Exception("Circuit breaker is OPEN - Service temporarily unavailable")
        
        try:
            result = func(*args, **kwargs)
            
            # Success - reset breaker
            if self.state == 'half_open':
                logger.info("Circuit breaker: Recovered successfully")
            
            self.failure_count = 0
            self.state = 'closed'
            return result
        
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()
            
            if self.failure_count >= self.failure_threshold:
                self.state = 'open'
                logger.error(
                    f"Circuit breaker: OPEN after {self.failure_count} failures"
                )
            
            raise e

class HealthMonitor:
    """Monitor system health and detect issues"""
    
    def __init__(self):
        self.metrics = {
            'requests_total': 0,
            'requests_failed': 0,
            'avg_response_time': 0,
            'last_check': datetime.now()
        }
    
    def record_request(self, success: bool, response_time: float):
        """Record request metrics"""
        self.metrics['requests_total'] += 1
        if not success:
            self.metrics['requests_failed'] += 1
        
        # Update average response time
        total = self.metrics['requests_total']
        avg = self.metrics['avg_response_time']
        self.metrics['avg_response_time'] = (
            (avg * (total - 1) + response_time) / total
        )
        self.metrics['last_check'] = datetime.now()
    
    def get_health_status(self) -> str:
        """Get overall health status"""
        total = self.metrics['requests_total']
        if total == 0:
            return "unknown"
        
        failed_rate = self.metrics['requests_failed'] / total
        
        if failed_rate < 0.05:  # Less than 5% failure
            return "healthy"
        elif failed_rate < 0.20:  # Less than 20% failure
            return "degraded"
        else:
            return "unhealthy"
    
    def get_metrics(self):
        """Get all metrics"""
        return self.metrics

# Global instances
error_handler = ErrorHandler()
circuit_breaker = CircuitBreaker()
health_monitor = HealthMonitor()

def handle_errors(func: Callable) -> Callable:
    """Decorator for automatic error handling"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            start_time = time.time()
            result = error_handler.retry_with_backoff(func, *args, **kwargs)
            response_time = time.time() - start_time
            health_monitor.record_request(True, response_time)
            return result
        except Exception as e:
            health_monitor.record_request(False, 0)
            logger.error(f"Handler error in {func.__name__}: {e}")
            raise
    return wrapper

def handle_errors_async(func: Callable) -> Callable:
    """Decorator for automatic async error handling"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            start_time = time.time()
            result = await error_handler.async_retry_with_backoff(func, *args, **kwargs)
            response_time = time.time() - start_time
            health_monitor.record_request(True, response_time)
            return result
        except Exception as e:
            health_monitor.record_request(False, 0)
            logger.error(f"Async handler error in {func.__name__}: {e}")
            raise
    return wrapper
