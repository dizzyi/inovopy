Module inovopy.iva
==================
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

Functions
---------

`custom(custom_command: dict[str, str | float]) ‑> dict[str, str | float]`
:   generate jsonable `dict[str,str|float]` for custom command
    
    ## Parameter
    - `custom_command : dict[str,str|float]` : custom command to execute

`dequeue(enter_context: bool = False) ‑> dict[str, str | float]`
:   generate jsonable `dict[str,str|float]` for dequeue command
    
    ## Parameter
    - `enter_context : bool` : whether or not to push to the context stack

`enqueue(robot_command: RobotCommand) ‑> dict[str, str | float]`
:   generate jsonable `dict[str,str|float]` for enqueue command
    
    ## Parameter
    - `robot_command : RobotCommand` : the robot command to enqueue

`execute(robot_command: RobotCommand, enter_context: bool = False) ‑> dict[str, str | float]`
:   generate jsonable `dict[str,str|float]` for execute command
    
    ## Parameter
    - `robot_command : RobotCommand` : the robot command to execute
    - `enter_context : bool` : whether or not to push to the context stack

`get_current(target: Literal['transform', 'joint_coord']) ‑> dict[str, str | float]`
:   generate jsonable `dict[str,str|float]` for get command
    
    ## Parameter
    - `transform : bool` : whether to get the current transform or joint

`get_data(key: str) ‑> dict[str, str | float]`
:   generate jsonable `dict[str,str|float]` for get data command
    
    ## Parameter
    - `key : str` : key of the data to get from the robot

`gripper(gripper_command: GripperCommand) ‑> dict[str, str | float]`
:   generate jsonable `dict[str,str|float]` for gripper command
    
    ## Parameter
    - `gripper_command : GripperCommand` : gripper command to execute

`io(io_command: IOCommand) ‑> dict[str, str | float]`
:   generate jsonable `dict[str,str|float]` for io command
    
    ## Parameter
    - `io_command : IOCommand` : io command to execute

`pop() ‑> dict[str, str | float]`
:   generate jsonable `dict[str,str|float]` for pop command

Classes
-------

`GripperCommand(argument: dict[str, str | float])`
:   # Gripper Command
    A class for constructing gripper command
    
    ## Class Method
    - `activate`
    - `set`
    - `get`

    ### Static methods

    `activate() ‑> inovopy.iva.GripperCommand`
    :   return a gripper command for activating the gripper

    `get() ‑> inovopy.iva.GripperCommand`
    :   return a gripper command for getting the state of the robot

    `set(label: str) ‑> inovopy.iva.GripperCommand`
    :   return a gripper command for setting the gripper
        
        # Parameter
        - `label : str` : the label to set the gripper to

    ### Methods

    `to_dict(self) ‑> dict[str, str | float]`
    :   return `dict[str,str|float]` representation of the command

`IOCommand(argument: dict[str, str | float])`
:   # IO Command
    A class for constructing IO Command
    
    ## Class Method
    - `set_beckhoff`
    - `get_beckhoff`
    - `set_wrist`
    - `get_wrist`

    ### Static methods

    `get_digital(target: Literal['beckhoff', 'wrist'], port: int) ‑> inovopy.iva.IOCommand`
    :   return a command for getting the digital input
        
        ## Parameter
        - `port : int` : port to set

    `set_digital(target: Literal['beckhoff', 'wrist'], port: int, state: bool) ‑> inovopy.iva.IOCommand`
    :   return a command for setting the digital output
        
        ## Parameter
        - `port : int` : port to set
        - `state : bool` : state to set

    ### Methods

    `to_dict(self) ‑> dict[str, str | float]`
    :   return a `dict[str,str|float]` representation of the io command

`MotionMode(*args, **kwds)`
:   # MotionMode
    An str-enum class for different robot motion's
    interpolation mode and specify whether is relative move
    
    ## Enum
    - `LINEAR`
    - `LINEAR_RELATIVE`
    - `JOINT`
    - `JOINT_RELATIVE`

    ### Ancestors (in MRO)

    * builtins.str
    * enum.Enum

    ### Class variables

    `JOINT`
    :

    `JOINT_RELATIVE`
    :

    `LINEAR`
    :

    `LINEAR_RELATIVE`
    :

    ### Methods

    `to_arg(self) ‑> str`
    :

`RobotCommand(argument: dict[str, str | float])`
:   # RobotCommand
    a class for constructing robot command
    
    ## Class Method
    - `synchronize` : command to break blending
    - `sleep` : command to robot to sleep
    - `set_parameter` : command to set motion parameter of robot
    - `motion` : command to move the robot

    ### Static methods

    `motion(motion_mode: MotionMode, target: inovopy.geometry.jointcoord.JointCoord | inovopy.geometry.transform.Transform) ‑> inovopy.iva.RobotCommand`
    :   Return a `RobotCommand` for robot motion
        
        ## Parameter
        - `motion_mode : MotionMode`, specify the motion mode
        - `target` : target of the motion, either transform or joint coord

    `set_parameter(speed: float | None = None, accel: float | None = None, blend_linear: float | None = None, blend_angular: float | None = None, tcp_speed_linear: float | None = None, tcp_speed_angular: float | None = None) ‑> inovopy.iva.RobotCommand`
    :   Return a `RobotCommand` for setting the robot motion parameter
        
        ## Parameter
        - `speed : float`, in percent, range from `1` to `100`
        - `accel : float`, in precent, range from `1` to `100`
        - `blend_linear : float`, in mm, range from `1` to `1000`
        - `blend_angular : float`, in degree, range from `1` to `360`
        - `tcp_speed_linear : float`, in mm, range from `1` to `999`
        - `tcp_speed_angular : float`, in degree, range from `1` to `360`

    `sleep(second: float) ‑> inovopy.iva.RobotCommand`
    :   Return a `RobotCommand` for the robot to sleep
        
        ## Parameter
        - `second : float` : specify the lenght of sleep in seconds

    `synchronize() ‑> inovopy.iva.RobotCommand`
    :   Return a `RobotCommand` for synchronizing/breaking blending

    ### Methods

    `to_dict(self) ‑> dict[str, str | float]`
    :   return `dict[str,str|float]` representation of the command