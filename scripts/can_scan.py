# Entry point: pupper-can-scan
from __future__ import annotations
import argparse, time
import can

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--channel", default="can0")
    args = ap.parse_args()

    bus = can.interface.Bus(bustype="socketcan", channel=args.channel)
    print(f"Listening on {args.channel}… (Ctrl+C to stop)")
    try:
        while True:
            msg = bus.recv(timeout=1.0)
            if msg:
                print(msg)
    except KeyboardInterrupt:
        pass
