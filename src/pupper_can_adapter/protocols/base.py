from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterable, Tuple
from ..can.driver import CanBus

class ActuatorProtocol(ABC):
    def __init__(self, bus: CanBus):
        self.bus = bus

    @abstractmethod
    def enable(self):
        ...

    @abstractmethod
    def disable(self):
        ...

    @abstractmethod
    def set_positions(self, targets: Iterable[Tuple[int, float]]):
        """targets: iterable of (motor_id, position_rad)."""
        ...

    def hold_position(self):
        """Default behavior: do nothing (sim) or re-send last position (real)."""
        pass
