Module inovopy.rosbridge
========================
# Ros Bridge Module
This module contain function and class for using rosbridge
api to command and get state from inovo arm

`inovopy.rosbridge.InovoRos`

Classes
-------

`InovoRos(host: str, logger: logging.Logger | str | None = None)`
:   # RosBridge
    A class managing rosbridge api communication
    
    ## Usage
    ```python
    from inovopy.rosbridge import InovoRos
    
    ros = InovoRos("192.168.1.1")
    
    ros.estop_reset()
    ```
    
    initalize `InovoRos`
    
    ## Args
    - `host : str` : host of psu, preferably in form of `192.168.x.x`
    - `logger: logging.Logger | str | None` :
        - if `logger` is instance of `logging.Logger`, it will log with it;
        - if `logger` is `str`, new logger will be created with it as name
        - otherwise, no log

    ### Ancestors (in MRO)

    * inovopy.util.Loggable
    * abc.ABC

    ### Class variables

    `active_blocks: list[str]`
    :

    `current: float`
    :

    `current_block_progress: float`
    :

    `drive_powered: bool`
    :

    `driver_state: str`
    :

    `enable: bool`
    :

    `estop_active: bool`
    :

    `estop_circuit: bool`
    :

    `joint_eff: list[float]`
    :

    `joint_pos: list[float]`
    :

    `joint_states: list[inovopy.rosbridge.JointState]`
    :

    `joint_vel: list[float]`
    :

    `power_status: str`
    :

    `ros: roslibpy.ros.Ros`
    :   connection manager to ROS server (`roslibpy.Ros`)

    `runtime_status: inovopy.rosbridge.RuntimeState`
    :

    `safe_stop_active: bool`
    :

    `safe_stop_circuit: bool`
    :

    `state: int`
    :

    `tcp_pose_quat: tuple[float, float, float, float]`
    :

    `tcp_pose_vec: tuple[float, float, float]`
    :

    `tcp_speed_ang: float`
    :

    `tcp_speed_lin: float`
    :

    `variables: list[inovopy.rosbridge.Variable]`
    :

    `voltage: float`
    :

    ### Methods

    `estop_reset(self) ‑> inovopy.rosbridge.InovoServiceResponse`
    :

    `jog(self)`
    :   Enter a context of jog command mode. Advertise when enter context
        and automatically unadvertise when exit.
        
        ## Yields:
        - `JogPublisher`: api for jog command
        
        ## Example:
        ```python
        import time
        from inovopy.rosbridge import InovoRos
        
        ros = InovoRos("192.168.1.122", "Jog")
        
        with ros.jog() as j:
            for _ in range(1000):
                j.jog(z=-0.01)
                time.sleep(0.01)
            for _ in range(1000):
                j.jog(z=0.01)
                time.sleep(0.01)
        ```

    `power_off(self) ‑> inovopy.rosbridge.InovoServiceResponse`
    :

    `power_on(self) ‑> inovopy.rosbridge.InovoServiceResponse`
    :

    `resubscribe_all(self)`
    :

    `robot_disable(self) ‑> inovopy.rosbridge.InovoServiceResponse`
    :

    `robot_enable(self) ‑> inovopy.rosbridge.InovoServiceResponse`
    :

    `runtime_continue(self) ‑> inovopy.rosbridge.InovoServiceResponse`
    :

    `runtime_debug(self) ‑> inovopy.rosbridge.InovoServiceResponse`
    :

    `runtime_get_var(self, name: str) ‑> inovopy.rosbridge.InovoServiceResponse`
    :

    `runtime_pause(self) ‑> inovopy.rosbridge.InovoServiceResponse`
    :

    `runtime_set_var(self, name: str, value: Any) ‑> inovopy.rosbridge.InovoServiceResponse`
    :

    `runtime_start(self, procedure_name: str | None = None) ‑> inovopy.rosbridge.InovoServiceResponse`
    :   start a sequence in runtime
        
        ## Args:
        - `procedure_name : str | None`:
            - if `None`, will start from start block
            - if `str`, will try to start function with respected name

    `runtime_step(self) ‑> inovopy.rosbridge.InovoServiceResponse`
    :

    `runtime_stop(self) ‑> inovopy.rosbridge.InovoServiceResponse`
    :

    `safe_stop_reset(self) ‑> inovopy.rosbridge.InovoServiceResponse`
    :

    `unsubscribe_all(self)`
    :

`InovoServiceResponse(message: dict)`
:   Response when calling service
    
    Field:
    - `success : bool` : whether the service call success
    - `message : str` : message from service call, usually error message
    - `value : str | None` : extra information from response, used in `runtime_get_var`

    ### Class variables

    `message: str`
    :

    `success: bool`
    :

    `value: str | None`
    :

    ### Static methods

    `from_message(message) ‑> inovopy.rosbridge.InovoServiceResponse`
    :

`JogPublisher(publisher: roslibpy.core.Topic)`
:   context manager for jog
    
    automatically unadvertise when `del`

    ### Class variables

    `publisher: roslibpy.core.Topic`
    :

    ### Methods

    `jog(self, x: float = 0, y: float = 0, z: float = 0, rx: float = 0, ry: float = 0, rz: float = 0)`
    :   Send a cartesian jog twist demand
        
        Args:
        - `x : float`: target linear velocity x. Defaults to 0.
        - `y : float`: target linear velocity y. Defaults to 0.
        - `z : float`: target linear velocity z. Defaults to 0.
        - `rx : float`: target angular velocity rx. Defaults to 0.
        - `ry : float`: target angular velocity ry. Defaults to 0.
        - `rz : float`: target angular velocity ry. Defaults to 0.

`JointState()`
:   

    ### Class variables

    `age: int`
    :

    `current: float`
    :

    `drive_temp: float`
    :

    `ff_torque: float`
    :

    `joint_temp: float`
    :

    `motor_temp: float`
    :

    `output_gain: float`
    :

    `position: float`
    :

    `state: int`
    :

    `status: int`
    :

    `target_position: float`
    :

    `torque: float`
    :

    `velocity: float`
    :

    ### Static methods

    `attr_list() ‑> list[str]`
    :

    `from_message(message) ‑> inovopy.rosbridge.JointState`
    :

`RuntimeState(*args, **kwds)`
:   Create a collection of name/value pairs.
    
    Example enumeration:
    
    >>> class Color(Enum):
    ...     RED = 1
    ...     BLUE = 2
    ...     GREEN = 3
    
    Access them by:
    
    - attribute access::
    
    >>> Color.RED
    <Color.RED: 1>
    
    - value lookup:
    
    >>> Color(1)
    <Color.RED: 1>
    
    - name lookup:
    
    >>> Color['RED']
    <Color.RED: 1>
    
    Enumerations can be iterated over, and know how many members they have:
    
    >>> len(Color)
    3
    
    >>> list(Color)
    [<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]
    
    Methods can be added to enumerations, and members can have their own
    attributes -- see the documentation for details.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `Idle`
    :

    `Paused`
    :

    `PausedOnError`
    :

    `Running`
    :

`Variable(name: str, dtype: str, value: str)`
:   

    ### Class variables

    `dtype: str`
    :

    `name: str`
    :

    `value: str`
    :

    ### Static methods

    `from_message(message) ‑> inovopy.rosbridge.Variable`
    :