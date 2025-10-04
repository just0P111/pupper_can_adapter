from dataclasses import dataclass
from typing import Optional

@dataclass
class MotorState:
    id: int
    position: float
    velocity: float
    torque: float
    temperature: Optional[float] = None
