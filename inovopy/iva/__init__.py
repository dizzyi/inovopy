"""
# IVA Module
This module provide class and function for
message generation of IVA communication protocal to inovo robots

## Functions
- `execute` : generate `dict` for `execute` message for robot
- `enqueue` : generate `dict` for `enqueue` message for robot
- `dequeue` : generate `dict` for `dequeue` message for robot
- `pop` : generate `dict` for `pop` message for robot
- `io` : generate `dict` for `io` message for robot
- `gripper` : generate `dict` for `gripper` message for robot
- `get_current` : generate `dict` for `get` current message for robot
- `get_data` : generate `dict` for `get` data message for robot
- `custom` : generate `dict` for `custom` message for robot

## Class
- `RobotCommand` ; class for constructing robot command
- `IOCommand` ; class for constructing IO command
- `GripperCommand` ; class for constructing gripper command

## Interface, Abstract Base Class
- `IntoRobotCommand` : interface for class to constructing robot command
"""

from typing import Literal
from enum import Enum
import numpy
from inovopy.util import clamp
import inovopy


def execute(
    robot_command: "RobotCommand", enter_context: bool = False
) -> dict[str, str | float]:
    """
    generate jsonable `dict[str,str|float]` for execute command

    ## Parameter
    - `robot_command : RobotCommand` : the robot command to execute
    - `enter_context : bool` : whether or not to push to the context stack
    """
    return {
        "op_code": "execute",
        "enter_context": 1 if enter_context else 0,
        **robot_command.to_dict(),
    }


def enqueue(robot_command: "RobotCommand") -> dict[str, str | float]:
    """
    generate jsonable `dict[str,str|float]` for enqueue command

    ## Parameter
    - `robot_command : RobotCommand` : the robot command to enqueue
    """
    return {"op_code": "enqueue", **robot_command.to_dict()}


def dequeue(enter_context: bool = False) -> dict[str, str | float]:
    """
    generate jsonable `dict[str,str|float]` for dequeue command

    ## Parameter
    - `enter_context : bool` : whether or not to push to the context stack
    """
    return {"op_code": "dequeue", "enter_context": 1 if enter_context else 0}


def pop() -> dict[str, str | float]:
    """
    generate jsonable `dict[str,str|float]` for pop command
    """
    return {
        "op_code": "pop",
    }


def gripper(gripper_command: "GripperCommand") -> dict[str, str | float]:
    """
    generate jsonable `dict[str,str|float]` for gripper command

    ## Parameter
    - `gripper_command : GripperCommand` : gripper command to execute
    """
    return {"op_code": "gripper", **gripper_command.to_dict()}


def io(io_command: "IOCommand") -> dict[str, str | float]:
    """
    generate jsonable `dict[str,str|float]` for io command

    ## Parameter
    - `io_command : IOCommand` : io command to execute
    """
    return {"op_code": "io", **io_command.to_dict()}


def get_current(target: Literal["transform", "joint_coord"]) -> dict[str, str | float]:
    """
    generate jsonable `dict[str,str|float]` for get command

    ## Parameter
    - `transform : bool` : whether to get the current transform or joint
    """
    return {
        "op_code": "get",
        "target": "transform" if target == "transform" else "joint_coord",
    }


def get_data(key: str) -> dict[str, str | float]:
    """
    generate jsonable `dict[str,str|float]` for get data command

    ## Parameter
    - `key : str` : key of the data to get from the robot
    """
    return {"op_code": "get", "target": "data", "key": key}


def custom(custom_command: dict[str, str | float]) -> dict[str, str | float]:
    """
    generate jsonable `dict[str,str|float]` for custom command

    ## Parameter
    - `custom_command : dict[str,str|float]` : custom command to execute
    """
    return {"op_code": "custom", **custom_command}


class RobotCommand:
    """
    # RobotCommand
    a class for constructing robot command

    ## Class Method
    - `synchronize` : command to break blending
    - `sleep` : command to robot to sleep
    - `set_parameter` : command to set motion parameter of robot
    - `motion` : command to move the robot
    """

    def __init__(self, argument: dict[str, str | float]):
        self.argument: dict[str, str | float] = argument

    def to_dict(self) -> dict[str, str | float]:
        """return `dict[str,str|float]` representation of the command"""
        return self.argument

    @classmethod
    def synchronize(cls) -> "RobotCommand":
        """Return a `RobotCommand` for synchronizing/breaking blending"""
        return RobotCommand(
            {
                "action": "synchronize",
            }
        )

    @classmethod
    def sleep(cls, second: float) -> "RobotCommand":
        """
        Return a `RobotCommand` for the robot to sleep

        ## Parameter
        - `second : float` : specify the lenght of sleep in seconds
        """
        return RobotCommand({"action": "sleep", "second": second})

    @classmethod
    def set_parameter(
        cls,
        speed: float | None = None,
        accel: float | None = None,
        blend_linear: float | None = None,
        blend_angular: float | None = None,
        tcp_speed_linear: float | None = None,
        tcp_speed_angular: float | None = None,
    ) -> "RobotCommand":
        """
        Return a `RobotCommand` for setting the robot motion parameter

        ## Parameter
        - `speed : float`, in percent, range from `1` to `100`
        - `accel : float`, in precent, range from `1` to `100`
        - `blend_linear : float`, in mm, range from `1` to `1000`
        - `blend_angular : float`, in degree, range from `1` to `360`
        - `tcp_speed_linear : float`, in mm, range from `1` to `999`
        - `tcp_speed_angular : float`, in degree, range from `1` to `360`
        """

        speed = clamp(speed / 100, 0.01, 1) if speed else 0

        accel = clamp(accel / 100, 0.01, 1) if accel else 0

        blend_linear = clamp(blend_linear / 1000, 0.001, 1) if blend_linear else 0

        blend_angular = (
            clamp(
                inovopy.geometry.transform.deg_to_rad(blend_angular),
                0.001,
                2 * numpy.pi,
            )
            if blend_angular
            else 0
        )

        tcp_speed_linear = (
            clamp(tcp_speed_linear / 1000, 0.001, 0.999) if tcp_speed_linear else 0
        )

        tcp_speed_angular = (
            clamp(
                inovopy.geometry.transform.deg_to_rad(tcp_speed_angular),
                0.001,
                2 * numpy.pi,
            )
            if tcp_speed_angular
            else 0
        )

        return RobotCommand(
            {
                "action": "set_parameter",
                "speed": speed,
                "accel": accel,
                "blend_linear": blend_linear,
                "blend_angular": blend_angular,
                "tcp_speed_linear": tcp_speed_linear,
                "tcp_speed_angular": tcp_speed_angular,
            }
        )

    @classmethod
    def motion(
        cls,
        motion_mode: "MotionMode",
        target: "inovopy.geometry.jointcoord.JointCoord | inovopy.geometry.transform.Transform",
    ) -> "RobotCommand":
        """
        Return a `RobotCommand` for robot motion

        ## Parameter
        - `motion_mode : MotionMode`, specify the motion mode
        - `target` : target of the motion, either transform or joint coord
        """
        return RobotCommand(
            {
                "action": "motion",
                "motion_mode": motion_mode.to_arg(),
                **target.to_dict(),
            }
        )


class MotionMode(str, Enum):
    """
    # MotionMode
    An str-enum class for different robot motion's
    interpolation mode and specify whether is relative move

    ## Enum
    - `LINEAR`
    - `LINEAR_RELATIVE`
    - `JOINT`
    - `JOINT_RELATIVE`
    """

    LINEAR = "linear"
    LINEAR_RELATIVE = "linear_relative"
    JOINT = "joint"
    JOINT_RELATIVE = "joint_relatve"

    def to_arg(self) -> str:
        return str(self).split(".")[1].lower()


class IOCommand:
    """
    # IO Command
    A class for constructing IO Command

    ## Class Method
    - `set_beckhoff`
    - `get_beckhoff`
    - `set_wrist`
    - `get_wrist`
    """

    def __init__(self, argument: dict[str, str | float]):
        self.argument = argument

    def to_dict(self) -> dict[str, str | float]:
        """return a `dict[str,str|float]` representation of the io command"""
        return self.argument

    @classmethod
    def set_digital(
        cls, target: Literal["beckhoff", "wrist"], port: int, state: bool
    ) -> "IOCommand":
        """
        return a command for setting the digital output

        ## Parameter
        - `port : int` : port to set
        - `state : bool` : state to set
        """
        return IOCommand(
            {
                "action": "set",
                "target": "beckhoff" if target == "beckhoff" else "wrist",
                "port": port,
                "state": 1 if state else 0,
            }
        )

    @classmethod
    def get_digital(
        cls, target: Literal["beckhoff", "wrist"], port: int
    ) -> "IOCommand":
        """
        return a command for getting the digital input

        ## Parameter
        - `port : int` : port to set
        """
        return IOCommand(
            {
                "action": "get",
                "target": "beckhoff" if target == "beckhoff" else "wrist",
                "port": port,
            }
        )


class GripperCommand:
    """
    # Gripper Command
    A class for constructing gripper command

    ## Class Method
    - `activate`
    - `set`
    - `get`
    """

    def __init__(self, argument: dict[str, str | float]):
        self.argument = argument

    def to_dict(self) -> dict[str, str | float]:
        """return `dict[str,str|float]` representation of the command"""
        return self.argument

    @classmethod
    def activate(cls) -> "GripperCommand":
        """return a gripper command for activating the gripper"""
        return GripperCommand({"action": "activate"})

    @classmethod
    def set(cls, label: str) -> "GripperCommand":
        """
        return a gripper command for setting the gripper

        # Parameter
        - `label : str` : the label to set the gripper to
        """
        return GripperCommand({"action": "set", "label": label})

    @classmethod
    def get(cls) -> "GripperCommand":
        """return a gripper command for getting the state of the robot"""
        return GripperCommand({"action": "get"})
