from __future__ import annotations
from typing import Iterable, Tuple
from .base import ActuatorProtocol

class SimProtocol(ActuatorProtocol):
    def __init__(self, bus):
        super().__init__(bus)
        self._last = {}
    def enable(self):
        print("[SIM] enable motors")
    def disable(self):
        print("[SIM] disable motors")
    def set_positions(self, targets: Iterable[Tuple[int, float]]):
        self._last = {mid: pos for mid, pos in targets}
        print(f"[SIM] positions: {self._last}")
    def hold_position(self):
        # keep last
        if self._last:
            print("[SIM] hold ", self._last)
