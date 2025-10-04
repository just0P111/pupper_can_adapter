from pupper_can_adapter.mapper import JointMapper
import numpy as np

def test_limits_and_signs():
    cfg = [{"id": i+1, "sign": 1 if i % 2 == 0 else -1, "zero": 0.1, "min": -1.0, "max": 1.0} for i in range(12)]
    m = JointMapper(cfg)
    q = np.linspace(-2.0, 2.0, 12)
    targets = m.joint_to_motor_targets(q)
    assert len(targets) == 12
    # Check clamping applied
    for (mid, cmd), qv in zip(targets, q):
        assert -1.0001 <= cmd <= 1.0001
