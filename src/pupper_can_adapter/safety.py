import time

class Watchdog:
    def __init__(self, timeout_s: float = 0.25):
        self.timeout_s = timeout_s
        self._last = time.time()
    def kick(self):
        self._last = time.time()
    def expired(self) -> bool:
        return (time.time() - self._last) > self.timeout_s
