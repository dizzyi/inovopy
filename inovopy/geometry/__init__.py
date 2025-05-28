"""
# Geometry Module
This module provide geometric data structure class for robot control

## Modules
- `transform` : Functions and Class for 3D spatial transform
- `jointcoord` : 6D joint space representation
"""

import numpy
from abc import ABC
from inovopy.iva import MotionMode, RobotCommand


def deg_to_rad(deg: float) -> float:
    """translate degree to radian"""
    return deg / 180 * numpy.pi


def rad_to_deg(rad: float) -> float:
    """translate radion to degree"""
    return rad / numpy.pi * 180


class IntoRobotCommand(ABC):
    """
    # IntoRobotCommand
    An interface for all class that can be turn into robot command

    ## Method
    - `as_motion`
    - `as_linear`
    - `as_linear_relative`
    - `as_joint`
    - `as_joint_relative`
    """

    # @abstractmethod
    def as_motion(self, motion_mode: MotionMode) -> RobotCommand:
        """construct a new motion command from the `self`"""
        return RobotCommand.motion(motion_mode=motion_mode, target=self)

    # @abstractmethod
    def as_linear(self) -> RobotCommand:
        """construct a new linear motion command from the `self`"""
        return self.as_motion(motion_mode=MotionMode.LINEAR)

    # @abstractmethod
    def as_linear_relative(self) -> RobotCommand:
        """construct a new linear relative motion command from the `self`"""
        return self.as_motion(motion_mode=MotionMode.LINEAR_RELATIVE)

    # @abstractmethod
    def as_joint(self) -> RobotCommand:
        """construct a new joint motion command from the `self`"""
        return self.as_motion(motion_mode=MotionMode.JOINT)

    # @abstractmethod
    def as_joint_relative(self) -> RobotCommand:
        """construct a new joint relative motion command from the `self`"""
        return self.as_motion(motion_mode=MotionMode.JOINT_RELATIVE)


from inovopy.geometry.transform import Transform
from inovopy.geometry.jointcoord import JointCoord
