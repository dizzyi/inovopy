Module inovopy.robot
====================
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

Classes
-------

`InovoRobot(tcp_stream: inovopy.socket.tcp_stream.TcpStream, inovo_ros: inovopy.rosbridge.InovoRos, logger: logging.Logger | str | None = None)`
:   # InovoRobot
    An API class for controlling and access information from inovo robot arm system.
    
    # Usage
    ```python
    from inovopy.robot import InovoRobot
    
    bot = InovoRobot.default_iva("psu000")
    
    print(bot.get_current_transform())
    print(bot.get_current_jointcoord())
    ```

    ### Ancestors (in MRO)

    * inovopy.util.Loggable
    * abc.ABC

    ### Static methods

    `default_iva(host: str, logger: logging.Logger | str | None = None) ‑> inovopy.robot.InovoRobot`
    :   start the iva protocal by
        
        - start up a tcp listener
        - start a sequence on psu via rosbridge
        - accept a connection
        
        ## Parameter:
        - `host: str` : remote host to start sequence, aka psu's address
        
        ## Return:
        `InovoRobot` : the resulted api class

    ### Methods

    `assert_res_ok(self)`
    :   read a message and assert that it is `OK`

    `context(self, robot_command: inovopy.iva.RobotCommand)`
    :   enter a context with a robot command
        
        ## Parameter
        - `robot_command: inovopy.iva.RobotCommand` : the command to execute
        
        ## Context Manager
        when exit context `InovoRobot.pop` the context

    `context_sequence(self, sequence: list[inovopy.iva.RobotCommand])`
    :   enter a context with a robot command
        
        ## Parameter
        - `sequence: list[inovopy.iva.RobotCommand]` : the sequence to execute
        
        ## Context Manager
        when exit context `InovoRobot.pop` the context

    `dequeue(self, enter_context: bool = False)`
    :   instruct the robot to dequeue all enqueued command
        
        ## Parameter
        - `enter_context: bool`: whether enter a context with the sequence or not

    `enqueue(self, robot_command: inovopy.iva.RobotCommand)`
    :   instruct the robot to enqueue a command
        
        ## Parameter
        - `robot_command: inovopy.iva.RobotCommand`: the command to enqueue

    `execute(self, robot_command: inovopy.iva.RobotCommand, enter_context: bool = False)`
    :   instruct the robot to execute a `inovopy.iva.RobotCommand`
        
        ## Parameter:
        - `robot_command: inovopy.iva.RobotCommand`: command to execute
        - `enter_context: bool`: whether the execution of command create a pop-able context
        
        ## Exception:
        `IvaException` raise if response is not `OK`

    `get_current_joint(self) ‑> inovopy.geometry.jointcoord.JointCoord`
    :   get the current joint coordinate
        
        ## Return:
        `inovopy.geometry.jointcoord.JointCoord`: current joint coordinate

    `get_current_transform(self) ‑> inovopy.geometry.transform.Transform`
    :   get the current transform
        
        ## Return:
        `inovopy.geometry.transform.Transform` : current tranform

    `get_data(self, key: str) ‑> str`
    :   get data with a key
        
        ## Parameter:
        - `key : str` : key for the data
        
        ## Return:
        - `str` value of the data
        - `str` containing `Error` will return if the key is not found

    `get_io_beckhoff(self, port: int) ‑> bool`
    :   get beckhoff input port
        
        ## Parameter
        - `port: int`: input port to get, default `0-7`
        
        ## Return
        `bool` state of io

    `get_io_wrist(self, port: int) ‑> bool`
    :   get wrist input port
        
        ## Parameter
        - `port: int`: input port to get, default `0-1`
        
        ## Return
        `bool` state of io

    `gipper_activate(self)`
    :   activate the gripper

    `gripper(self, gripper_command: inovopy.iva.GripperCommand)`
    :

    `gripper_get(self) ‑> float`
    :   get the gripper width
        
        ## Return
        `float` in percentage

    `gripper_set(self, label: str)`
    :   set a gripper to a predefine label
        
        
        #Parameter
        - `label: str`: the label to set to

    `io(self, io_command: inovopy.iva.IOCommand)`
    :   instruct the robot to perform a `inovopy.iva.IOCommand`
        
        ## Parameter
        - `io_command: inovopy.iva.IOCommand`: io commmand to perform
        
        ## Return
        `str` the respons

    `joint(self, target: inovopy.geometry.transform.Transform | inovopy.geometry.jointcoord.JointCoord)`
    :   joint move to a target

    `joint_relative(self, target: inovopy.geometry.transform.Transform | inovopy.geometry.jointcoord.JointCoord)`
    :   joint relative move to a target

    `linear(self, target: inovopy.geometry.transform.Transform | inovopy.geometry.jointcoord.JointCoord)`
    :   linear move to a target

    `linear_relative(self, target: inovopy.geometry.transform.Transform | inovopy.geometry.jointcoord.JointCoord)`
    :   linear relative move to a target

    `pop(self)`
    :   exit a context

    `read(self) ‑> str`
    :   read a line

    `sequence(self, sequence: list[inovopy.iva.RobotCommand], enter_context: bool = False)`
    :   perform a sequence of `inovopy.iva.RobotCommand`
        
        ## Parameter
        - `enter_context: bool`: whether enter a context with the sequence or not

    `set_io_beckhoff(self, port: int, state: bool)`
    :   set beckhoff output port
        
        ## Parameter
        - `port: int`: output port to set, default `0-7`
        - `state: bool`: target state of the output

    `set_io_wrist(self, port: int, state: bool)`
    :   set wrist output port
        
        ## Parameter
        - `port: int`: output port to set, default `0-7`
        - `state: bool`: target state of the output

    `set_param(self, speed: float | None = None, accel: float | None = None, blend_linear: float | None = None, blend_angular: float | None = None, tcp_speed_linear: float | None = None, tcp_speed_angular: float | None = None)`
    :   set the motion parameter of the robot
        
        ## Parameter
        - `speed : float`, in percent, range from `1` to `100`
        - `accel : float`, in precent, range from `1` to `100`
        - `blend_linear : float`, in mm, range from `1` to `1000`
        - `blend_angular : float`, in degree, range from `1` to `360`
        - `tcp_speed_linear : float`, in mm, range from `1` to `999`
        - `tcp_speed_angular : float`, in degree, range from `1` to `360`

    `sleep(self, second: float)`
    :   instruct the robot to sleep for a specified time
        
        ## Parameter:
        - `second: float` : second to sleep

    `write(self, instruction: dict[str, str | float])`
    :   write an instruction as str
        
        ## Parameter:
        - `instruction : dict[str, str|float]` : jsonable instruction dict

`IvaException(*args, **kwargs)`
:   # Iva Exception

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException