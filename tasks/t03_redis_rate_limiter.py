from typing import Optional
# Task 3: Sliding Window Rate Limiter
import time

class SlidingWindowRateLimiter:
    def __init__(self, limit: int, window_seconds: float):
        self.limit = limit
        self.window_seconds = window_seconds
        self.requests = []

    def allow_request(self, current_time: Optional[float] = None) -> bool:
        now = current_time if current_time is not None else time.time()
        # Evict timestamps outside current sliding window
        self.requests = [t for t in self.requests if t > now - self.window_seconds]
        if len(self.requests) < self.limit:
            self.requests.append(now)
            return True
        return False
