from __future__ import annotations
import can

class CanBus:
    """Thin wrapper over python-can (SocketCAN by default)."""
    def __init__(self, channel: str = "can0", bitrate: int = 1000000):
        # For SocketCAN, bitrate is set when you bring up the interface (ip link set can0 up type can bitrate 1000000)
        self.bus = can.interface.Bus(bustype="socketcan", channel=channel)

    def send(self, arb_id: int, data: bytes, is_extended_id: bool = False):
        msg = can.Message(arbitration_id=arb_id, data=data, is_extended_id=is_extended_id)
        self.bus.send(msg)

    def recv(self, timeout: float = 0.0):
        return self.bus.recv(timeout)

    def close(self):
        try:
            self.bus.shutdown()
        except Exception:
            pass
