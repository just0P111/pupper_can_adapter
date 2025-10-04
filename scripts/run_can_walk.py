# Entry point: pupper-can-run
from __future__ import annotations
import argparse, time
import numpy as np
from pupper_can_adapter.aal import AAL

DEF_STAND = np.array([
    0.0, 0.7, -1.4,   # FR
    0.0, 0.7, -1.4,   # FL
    0.0, 0.7, -1.4,   # RR
    0.0, 0.7, -1.4,   # RL
])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--protocol", default="sim")
    ap.add_argument("--hz", type=int, default=200)
    args = ap.parse_args()

    # overwrite protocol at runtime by editing config dict on disk or here
    A = AAL(config_path=args.config, hz=args.hz)
    # Hack: override protocol field in loaded config
    A.cfg.protocol = args.protocol

    A.start()
    try:
        t0 = time.time()
        while True:
            # Simple breathing stand as a demo
            t = time.time() - t0
            q = DEF_STAND.copy()
            q[2::3] += 0.1 * np.sin(2*np.pi*0.25*t)  # move knees a bit
            A.set_joint_angles(q)
            time.sleep(1.0/args.hz)
    except KeyboardInterrupt:
        pass
    finally:
        A.stop()
