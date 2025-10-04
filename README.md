# pupper_can_adapter
This reposetory is a project aimed to translate the servo rotation from the stanford pupper robot dog to can motors. THIS WAS MADE WITH AI. Im too stupid to make this shit in 2 days (This requierment is crazy bruh). The logic of translation the signals is mine. But the code is not. 
# pupper-can-adapter

Actuation Abstraction Layer (AAL) that lets you run the **Stanford Pupper** gait/walking stack on **CAN-based** smart actuators.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
# copy and edit the config
cp configs/robot.example.yaml configs/robot.yaml
# dry-run with simulator (no CAN frames sent)
pupper-can-run --config configs/robot.yaml --protocol sim
# scan CAN bus (Linux SocketCAN)
pupper-can-scan --channel can0
```

## Integrate with Pupper code
In your Pupper control loop:
```python
from pupper_can_adapter.aal import AAL
A = AAL(config_path="../pupper_can_adapter/configs/robot.yaml", hz=200)
A.start()
A.set_joint_angles(q_rad)  # list/np.ndarray of 12 radians in FR,FL,RR,RL × hip,thigh,knee
```

> ⚠️ **Safety**: The included `protocols/rmd.py` is a **skeleton**. Complete and test with wheels off the ground. Start with `--protocol sim`.
```


**LICENSE**
MIT License

Copyright (c) 2025 Oskar P ;3

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
