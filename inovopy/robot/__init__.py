"""
# Robot Module
This module provide a simple api for controlling inovo robot arm with
predefinded `iva` protocal.

## Class
- `InovoRobot`: A class for interfacing with inovo robot arm

## Example
```python
from inovopy.robot import InovoRobot

bot = InovoRobot.default_iva("psu000")


```
"""

import logging
from contextlib import contextmanager
import json

from inovopy.util import Loggable
from inovopy.rosbridge import InovoRos
from inovopy.socket import TcpListener, TcpStream
from inovopy.geometry.jointcoord import JointCoord
from inovopy.geometry.transform import Transform
from inovopy.iva import *


class IvaException(Exception):
    """
    # Iva Exception
    """


class InovoRobot(Loggable):
    """
    # InovoRobot
    An API class for controlling and access information from inovo robot arm system.

    # Usage
    ```python
    from inovopy.robot import InovoRobot

    bot = InovoRobot.default_iva("psu000")

    print(bot.get_current_transform())
    print(bot.get_current_jointcoord())
    ```
    """

    def __init__(
        self,
        tcp_stream: TcpStream,
        inovo_ros: InovoRos,
        logger: logging.Logger | str | None = None,
    ):
        super().__init__(logger)
        self.tcp_stream: TcpStream = tcp_stream
        self.inovo_ros: InovoRos = inovo_ros

    @classmethod
    def default_iva(
        cls, host: str, logger: logging.Logger | str | None = None
    ) -> "InovoRobot":
        """
        start the iva protocal by

        - start up a tcp listener
        - start a sequence on psu via rosbridge
        - accept a connection

        ## Parameter:
        - `host: str` : remote host to start sequence, aka psu's address

        ## Return:
        `InovoRobot` : the resulted api class
        """
        listener = TcpListener()

        inovo_ros: InovoRos = InovoRos(host=host)
        inovo_ros.runtime_start("iva")

        tcp_stream: TcpStream = listener.accept()
        del listener

        bot: InovoRobot = InovoRobot(
            tcp_stream=tcp_stream, inovo_ros=inovo_ros, logger=logger
        )
        return bot

    def read(self) -> str:
        """read a line"""
        return self.tcp_stream.read()

    def write(self, instruction: dict[str, str | float]):
        """
        write an instruction as str

        ## Parameter:
        - `instruction : dict[str, str|float]` : jsonable instruction dict
        """
        msg = json.dumps(instruction)
        self.tcp_stream.write(msg)

    def assert_res_ok(self):
        """read a message and assert that it is `OK`"""
        res = self.read()
        if res != "OK":
            raise IvaException(f'Expect resopnse to be "OK", but recieve {res}')

    def execute(self, robot_command: RobotCommand, enter_context: bool = False):
        """
        instruct the robot to execute a `inovopy.iva.RobotCommand`

        ## Parameter:
        - `robot_command: inovopy.iva.RobotCommand`: command to execute
        - `enter_context: bool`: whether the execution of command create a pop-able context

        ## Exception:
        `IvaException` raise if response is not `OK`
        """
        self.write(execute(robot_command=robot_command, enter_context=enter_context))
        self.assert_res_ok()

    def sleep(self, second: float):
        """
        instruct the robot to sleep for a specified time

        ## Parameter:
        - `second: float` : second to sleep
        """
        self.execute(RobotCommand.sleep(second=second))

    def set_param(
        self,
        speed: float | None = None,
        accel: float | None = None,
        blend_linear: float | None = None,
        blend_angular: float | None = None,
        tcp_speed_linear: float | None = None,
        tcp_speed_angular: float | None = None,
    ):
        """
        set the motion parameter of the robot

        ## Parameter
        - `speed : float`, in percent, range from `1` to `100`
        - `accel : float`, in precent, range from `1` to `100`
        - `blend_linear : float`, in mm, range from `1` to `1000`
        - `blend_angular : float`, in degree, range from `1` to `360`
        - `tcp_speed_linear : float`, in mm, range from `1` to `999`
        - `tcp_speed_angular : float`, in degree, range from `1` to `360`
        """
        robot_command = RobotCommand.set_parameter(
            speed=speed,
            accel=accel,
            blend_linear=blend_linear,
            blend_angular=blend_angular,
            tcp_speed_linear=tcp_speed_linear,
            tcp_speed_angular=tcp_speed_angular,
        )

        self.execute(robot_command=robot_command)

    def linear(self, target: Transform | JointCoord):
        """linear move to a target"""
        self.execute(target.as_linear())

    def linear_relative(self, target: Transform | JointCoord):
        """linear relative move to a target"""
        self.execute(target.as_linear_relative())

    def joint(self, target: Transform | JointCoord):
        """joint move to a target"""
        self.execute(target.as_joint())

    def joint_relative(self, target: Transform | JointCoord):
        """joint relative move to a target"""
        self.execute(target.as_joint_relative())

    def enqueue(self, robot_command: RobotCommand):
        """
        instruct the robot to enqueue a command

        ## Parameter
        - `robot_command: inovopy.iva.RobotCommand`: the command to enqueue
        """
        self.write(enqueue(robot_command=robot_command))
        self.assert_res_ok()

    def dequeue(self, enter_context: bool = False):
        """
        instruct the robot to dequeue all enqueued command

        ## Parameter
        - `enter_context: bool`: whether enter a context with the sequence or not
        """
        self.write(dequeue(enter_context=enter_context))
        self.assert_res_ok()

    def sequence(self, sequence: list[RobotCommand], enter_context: bool = False):
        """
        perform a sequence of `inovopy.iva.RobotCommand`

        ## Parameter
        - `enter_context: bool`: whether enter a context with the sequence or not
        """
        for step in sequence:
            self.enqueue(step)
        self.dequeue(enter_context=enter_context)

    def pop(self):
        """
        exit a context
        """
        self.write(pop())
        self.assert_res_ok()

    def io(self, io_command: IOCommand):
        """
        instruct the robot to perform a `inovopy.iva.IOCommand`

        ## Parameter
        - `io_command: inovopy.iva.IOCommand`: io commmand to perform

        ## Return
        `str` the respons
        """
        self.write(io(io_command=io_command))
        return self.read()

    def get_io_beckhoff(self, port: int) -> bool:
        """
        get beckhoff input port

        ## Parameter
        - `port: int`: input port to get, default `0-7`

        ## Return
        `bool` state of io
        """
        return self.io(IOCommand.get_digital(target="beckhoff", port=port)) == "True"

    def get_io_wrist(self, port: int) -> bool:
        """
        get wrist input port

        ## Parameter
        - `port: int`: input port to get, default `0-1`

        ## Return
        `bool` state of io
        """
        return self.io(IOCommand.get_digital(target="wrist", port=port)) == "True"

    def set_io_beckhoff(self, port: int, state: bool):
        """
        set beckhoff output port

        ## Parameter
        - `port: int`: output port to set, default `0-7`
        - `state: bool`: target state of the output
        """
        res = self.io(IOCommand.set_digital(target="beckhoff", port=port, state=state))
        assert res == "OK"

    def set_io_wrist(self, port: int, state: bool):
        """
        set wrist output port

        ## Parameter
        - `port: int`: output port to set, default `0-7`
        - `state: bool`: target state of the output
        """
        res = self.io(IOCommand.set_digital(target="wrist", port=port, state=state))
        assert res == "OK"

    def gripper(self, gripper_command: GripperCommand):
        self.write(gripper(gripper_command))

    def gipper_activate(self):
        """activate the gripper"""
        self.gripper(GripperCommand.activate())
        self.assert_res_ok()

    def gripper_get(self) -> float:
        """
        get the gripper width

        ## Return
        `float` in percentage
        """
        self.gripper(GripperCommand.get())
        return float(self.read()) * 100

    def gripper_set(self, label: str):
        """
        set a gripper to a predefine label


        #Parameter
        - `label: str`: the label to set to
        """
        self.gripper(GripperCommand.set(label=label))
        self.assert_res_ok()

    def get_current_transform(self) -> Transform:
        """
        get the current transform

        ## Return:
        `inovopy.geometry.transform.Transform` : current tranform
        """
        self.write(get_current("transform"))
        return Transform.from_robot(self.read())

    def get_current_joint(self) -> JointCoord:
        """
        get the current joint coordinate

        ## Return:
        `inovopy.geometry.jointcoord.JointCoord`: current joint coordinate
        """
        self.write(get_current("joint_coord"))
        return JointCoord.from_robot(self.read())

    def get_data(self, key: str) -> str:
        """
        get data with a key

        ## Parameter:
        - `key : str` : key for the data

        ## Return:
        - `str` value of the data
        - `str` containing `Error` will return if the key is not found
        """
        self.write(get_data(key=key))
        return self.read()

    @contextmanager
    def context(self, robot_command: RobotCommand):
        """
        enter a context with a robot command

        ## Parameter
        - `robot_command: inovopy.iva.RobotCommand` : the command to execute

        ## Context Manager
        when exit context `InovoRobot.pop` the context
        """
        self.execute(robot_command=robot_command, enter_context=True)
        try:
            yield
        finally:
            self.pop()

    @contextmanager
    def context_sequence(self, sequence: list[RobotCommand]):
        """
        enter a context with a robot command

        ## Parameter
        - `sequence: list[inovopy.iva.RobotCommand]` : the sequence to execute

        ## Context Manager
        when exit context `InovoRobot.pop` the context
        """
        self.sequence(sequence=sequence, enter_context=True)
        try:
            yield
        finally:
            self.pop()
