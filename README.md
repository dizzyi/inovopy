# Inovopy 
[![Static Badge](https://img.shields.io/badge/PyPI-inovopy-blue)](https://pypi.org/project/inovopy/)
[![Static Badge](https://img.shields.io/badge/docs-page-red)](https://dizzyi.github.io/inovopy/)
[![Static Badge](https://img.shields.io/badge/github-inovopy-green)](https://github.com/dizzyi/inovopy)


## Introduction
A package that provide a simple python socket based api for controlling inovo robot arms.

## Installation
```bash
pip install inovopy
```
### [Documentation](https://dizzyi.github.io/inovopy/) 


## Usage

see [examples](https://github.com/dizzyi/inovopy/tree/main/examples)


### Ros
inovopy provide ros based api to interact with inovo robot arm.

#### Example
```python
from inovopy.rosbridge import InovoRos

ros = InovoRos("192.168.1.122", "Test")
```

All fields are sync to the live robot state through RosBridge
```python
class InovoRos(inovopy.util.Loggable):
    # Ros
    ros: roslibpy.Ros

    # Tcp Speed
    tcp_speed_lin: float = 0
    tcp_speed_ang: float = 0

    # Tcp Pose
    tcp_pose_vec: tuple[float, float, float] = (0, 0, 0)
    tcp_pose_quat: tuple[float, float, float, float] = (0, 0, 0, 0)

    # Joint State
    joint_pos: list[float] = []
    joint_vel: list[float] = []
    joint_eff: list[float] = []

    # Power Status
    voltage: float = 0
    current: float = 0
    power_status: str = 0

    # Robot Status
    driver_state: str = ""
    drive_powered: bool = False

    # EStop Status
    estop_active: bool = False
    estop_circuit: bool = False

    # Safe Stop Status
    safe_stop_active: bool = False
    safe_stop_circuit: bool = False

    # Runtime State
    active_blocks: list[str] = []
    current_block_progress: float = 0
    runtime_status: RuntimeState = 0
    variables: list[Variable] = []

    # Arm State
    enable: bool = False
    state: int = 0
    joint_states: list[JointState] = []
```

APIs:
```python
ros.safe_stop_reset()
ros.estop_reset()
ros.power_on()
ros.robot_enable()

ros.runtime_start()
ros.runtime_pause()
ros.runtime_step()
ros.runtime_continue()
ros.runtime_get_var("a")
ros.runtime_set_var("a", 32)
ros.runtime_stop()
ros.runtime_start("do something")

ros.robot_disable()
ros.power_off()
```

### iva
To enact more precise and dynmaic control of robot, you can use [`iva`](https://github.com/dizzyi/inovo-iva), a message framework design to interact with inovo robot arms.

1. Download latest release of [iva.isq](https://github.com/dizzyi/inovo-iva/releases)
2. Import the project to inovo robot psu
3. look for the socket connect block and change the target ip to robot control server's ip address
4. use `inovopy.robot.InovoRobot` to control the robot

[example](https://github.com/dizzyi/inovopy/blob/main/examples/500%20-%20inovo%20iva.py)

```python
from inovopy.robot import InovoRobot
from inovopy.iva import RobotCommand, MotionMode
from inovopy.geometry.transform import Transform


bot = InovoRobot.default_iva("<PSU IP address>", "iva example")

# Get Current
print(bot.get_current_joint())
print(bot.get_current_transform())

# Motion
bot.linear_relative(Transform.from_z(10.0))
bot.joint(bot.get_current_joint().then_j1(10.0))

# Set Motion Parameter
bot.set_param(speed=10.0, accel=50.0, blend_linear=100.0, blend_angular=30.0)

# Digital IO
print(bot.get_io_beckhoff(0))
print(bot.set_io_beckhoff(0, True))

# Sequence
seq = [
    RobotCommand.motion(MotionMode.LINEAR_RELATIVE, Transform.from_z(10.0)),
    RobotCommand.sleep(10),
    RobotCommand.set_parameter(speed=20.0, accel=5.0),
]
bot.sequence(seq)
```