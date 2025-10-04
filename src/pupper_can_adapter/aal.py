from __future__ import annotations
import threading, time
from dataclasses import dataclass
from typing import List, Optional
import numpy as np
import yaml

from .mapper import JointMapper, JointLimits
from .safety import Watchdog
from .can.driver import CanBus
from .protocols.base import ActuatorProtocol
from .protocols.sim import SimProtocol
# You may later import your concrete protocol here, e.g. RMDProtocol
# from .protocols.rmd import RMDProtocol

@dataclass
class AALConfig:
    hz: int
    channel: str  # e.g., "can0" (SocketCAN)
    bitrate: int  # e.g., 1000000
    protocol: str # "sim" or "rmd" or your custom
    joints: list  # 12 items, each with: id, sign, zero, min, max

class AAL:
    """Actuation Abstraction Layer: accepts 12 joint angles (rad) and drives motors."""
    def __init__(self, config_path: str, hz: int | None = None):
        with open(config_path, "r") as f:
            cfg = yaml.safe_load(f)
        if hz is not None:
            cfg["hz"] = hz
        self.cfg = AALConfig(**cfg)

        self.mapper = JointMapper(self.cfg.joints)
        self.watchdog = Watchdog(timeout_s=0.25)
        self.bus: Optional[CanBus] = None
        self.proto: Optional[ActuatorProtocol] = None

        self._thread: Optional[threading.Thread] = None
        self._stop = threading.Event()
        self._q_latest = np.zeros(12, dtype=float)
        self._last_update = time.time()

    def _make_protocol(self, bus: CanBus) -> ActuatorProtocol:
        name = self.cfg.protocol.lower()
        if name == "sim":
            return SimProtocol(bus)
        # elif name == "rmd":
        #     return RMDProtocol(bus)
        raise ValueError(f"Unknown protocol '{name}'. Implement a driver in protocols/ and select it in config.")

    def start(self):
        if self._thread is not None:
            return
        self.bus = CanBus(channel=self.cfg.channel, bitrate=self.cfg.bitrate)
        self.proto = self._make_protocol(self.bus)
        self.proto.enable()
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=1.0)
            self._thread = None
        if self.proto:
            try:
                self.proto.disable()
            except Exception:
                pass
        if self.bus:
            self.bus.close()

    def set_joint_angles(self, q_rad: List[float] | np.ndarray):
        q = np.asarray(q_rad, dtype=float)
        assert q.shape == (12,), f"Expected 12 joint angles, got shape {q.shape}"
        self._q_latest = q
        self._last_update = time.time()
        self.watchdog.kick()

    def _loop(self):
        dt = 1.0 / float(self.cfg.hz)
        next_t = time.time()
        while not self._stop.is_set():
            now = time.time()
            if now - self._last_update > self.watchdog.timeout_s:
                # Hold position or gracefully relax per protocol policy
                if self.proto:
                    self.proto.hold_position()
            else:
                targets = self.mapper.joint_to_motor_targets(self._q_latest)
                if self.proto:
                    self.proto.set_positions(targets)  # list of (motor_id, position_rad)
            next_t += dt
            sleep = max(0.0, next_t - time.time())
            time.sleep(sleep)
