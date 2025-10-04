"""
RMD (MyActuator) protocol skeleton.

⚠️ Complete this driver using your motor's official CAN protocol doc.
Start with very low torque/current limits and test with the robot lifted.
"""
from __future__ import annotations
from typing import Iterable, Tuple
import struct
from .base import ActuatorProtocol

class RMDProtocol(ActuatorProtocol):
    def __init__(self, bus, *, base_id: int = 0x140):
        super().__init__(bus)
        self.base_id = base_id
        self._last = {}

    def _arb(self, motor_id: int) -> int:
        return self.base_id + int(motor_id)

    def enable(self):
        # Typically: exit motor stop; clear faults. IMPLEMENT PER DOC.
        pass

    def disable(self):
        # Typically: motor stop / torque off
        pass

    def set_positions(self, targets: Iterable[Tuple[int, float]]):
        # IMPLEMENT: Example for multi-turn position command if supported by your model.
        # angle_rad → angle_ticks conversion must use your encoder scale / gear ratio.
        # Placeholder sends nothing to avoid unsafe behavior.
        self._last = {mid: pos for mid, pos in targets}
        return

    def hold_position(self):
        # Optionally re-send last positions
        if not self._last:
            return
        self.set_positions(list(self._last.items()))
