from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Tuple
import numpy as np

@dataclass
class JointLimits:
    min: float
    max: float

@dataclass
class Joint:
    motor_id: int  # CAN ID or node ID
    sign: int      # +1 or -1 to flip direction
    zero: float    # radians offset applied before sign
    limits: JointLimits

class JointMapper:
    """Maps 12 Pupper joints → per-motor targets with offsets/sign/limits.

    Joint order expected: [FR.hip, FR.thigh, FR.knee, FL.hip, FL.thigh, FL.knee,
                           RR.hip, RR.thigh, RR.knee, RL.hip, RL.thigh, RL.knee]
    """
    def __init__(self, joints_cfg: List[Dict]):
        assert len(joints_cfg) == 12, "Expect 12 joints in config"
        self.joints: List[Joint] = [
            Joint(
                motor_id=jc["id"],
                sign=int(jc.get("sign", 1)),
                zero=float(jc.get("zero", 0.0)),
                limits=JointLimits(min=float(jc.get("min", -3.14)), max=float(jc.get("max", 3.14))),
            )
            for jc in joints_cfg
        ]

    def joint_to_motor_targets(self, q_rad: np.ndarray) -> List[Tuple[int, float]]:
        assert q_rad.shape == (12,)
        targets = []
        for i, q in enumerate(q_rad):
            j = self.joints[i]
            cmd = j.sign * (q - j.zero)
            cmd = float(np.clip(cmd, j.limits.min, j.limits.max))
            targets.append((j.motor_id, cmd))
        return targets
