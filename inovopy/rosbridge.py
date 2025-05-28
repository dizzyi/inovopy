"""
# Ros Bridge Module
This module contain function and class for using rosbridge
api to command and get state from inovo arm

`inovopy.rosbridge.InovoRos`
"""

from contextlib import contextmanager
import logging
import typing
from enum import Enum

import inovopy.util
import roslibpy

# Topic
TOPIC_TCP_SPEED = "/default_move_group/tcp_speed"
TOPIC_TCP_POSE = "/default_move_group/tcp_pose"
TOPIC_JOINT_STATE = "/robot/joint_states"
TOPIC_POWER_STATUS = "/psu/status"
TOPIC_ROBOT_STATUS = "/robot/robot_state"
TOPIC_ESTOP_STATUS = "/psu/estop/state"
TOPIC_SAFE_STOP_STATUS = "/psu/safe_stop/state"
TOPIC_RUNTIME_STATE = "/sequence/runtime_state"
TOPIC_ARM_STATE = "/robot/arm_state"


TYPE_TCP_SPEED = "commander_msgs/SpeedStamped"
TYPE_TCP_POSE = "geometry_msgs/PoseStamped"
TYPE_JOINT_STATE = "sensor_msgs/JointState"
TYPE_POWER_STATUS = "psu_msgs/Status"
TYPE_ROBOT_STATUS = "arm_msgs/RobotState"
TYPE_ESTOP_STATUS = "psu_msgs/SafetyCircuitState"
TYPE_SAFE_STOP_STATUS = "psu_msgs/SafetyCircuitState"
TYPE_RUNTIME_STATE = "commander_msgs/RuntimeState"
TYPE_ARM_STATE = "arm_msgs/ArmState"

# Service
SERVICE_SAFE_STOP_RESET = "/psu/safe_stop/reset"
SERVICE_ESTOP_RESET = "/psu/estop/reset"
SERVICE_POWER_ON = "/psu/enable"
SERVICE_POWER_OFF = "/psu/disable"
SERVICE_ROBOT_ENABLE = "/robot/enable"
SERVICE_ROBOT_DISABLE = "/robot/disable"

SERVICE_SEQUENCE_START = "/sequence/start"
SERVICE_SEQUENCE_STOP = "/sequence/stop"
SERVICE_SEQUENCE_PAUSE = "/sequence/pause"
SERVICE_SEQUENCE_STEP = "/sequence/step"
SERVICE_SEQUENCE_DEBUG = "/sequence/debug"
SERVICE_SEQUENCE_CONTINUE = "/sequence/continue"
SERVICE_SEQUENCE_SET_VAR = "/sequence/set_var"
SERVICE_SEQUENCE_GET_VAR = "/sequence/get_var"


TYPE_TRIGGER = "std_srvs/Trigger"
TYPE_RUN_SEQUENCE = "commander_msgs/RunSequence"
TYPE_SET_VAR = "commander_msgs/set_var"
TYPE_GET_VAR = "commander_msgs/get_var"

# Publish Service
TOPIC_CARTESIAN_JOG = "/default_move_group/cartesian_jog"
TYPE_CARTESIAN_JOG_DEMAND = "commander_msgs/CartesianJogDemand"


class RuntimeState(Enum):
    Idle = 0
    Running = 1
    Paused = 2
    PausedOnError = 3


class Variable:
    name: str
    dtype: str
    value: str

    def __init__(self, name: str, dtype: str, value: str):
        self.name = name
        self.dtype = dtype
        self.value = value

    @classmethod
    def from_message(cls, message) -> "Variable":
        return Variable(message["name"], message["type"], message["value"])


class JointState:
    age: int = 0
    current: float = 0
    drive_temp: float = 0
    ff_torque: float = 0

    joint_temp: float = 0
    motor_temp: float = 0
    output_gain: float = 0
    position: float = 0

    state: int = 0
    status: int = 0

    target_position: float = 0
    torque: float = 0
    velocity: float = 0

    @classmethod
    def attr_list(cls) -> list[str]:
        return [
            "age",
            "current",
            "drive_temp",
            "ff_torque",
            "joint_temp",
            "motor_temp",
            "output_gain",
            "position",
            "state",
            "status",
            "target_position",
            "torque",
            "velocity",
        ]

    def __init__(self):
        pass

    @classmethod
    def from_message(cls, message) -> "JointState":
        js = JointState()

        for a in JointState.attr_list():
            setattr(js, a, message[a])

        return js

    def __str__(self):
        return str(dict((a, getattr(self, a)) for a in JointState.attr_list()))


class InovoServiceResponse:
    """
    Response when calling service

    Field:
    - `success : bool` : whether the service call success
    - `message : str` : message from service call, usually error message
    - `value : str | None` : extra information from response, used in `runtime_get_var`
    """

    success: bool
    message: str
    value: str | None

    def __init__(self, message: dict):
        self.success = message["success"]
        self.message = message["message"]
        self.value = message.get("value")

    def __str__(self):
        return str(
            {"success": self.success, "message": self.message, "value": self.value}
        )

    @classmethod
    def from_message(cls, message) -> "InovoServiceResponse":
        return InovoServiceResponse(message)


class InovoRos(inovopy.util.Loggable):
    """
    # RosBridge
    A class managing rosbridge api communication

    ## Usage
    ```python
    from inovopy.rosbridge import InovoRos

    ros = InovoRos("192.168.1.1")

    ros.estop_reset()
    ```
    """

    # Ros
    ros: roslibpy.Ros
    """connection manager to ROS server (`roslibpy.Ros`)"""

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

    def __init__(self, host: str, logger: logging.Logger | str | None = None):
        """
        initalize `InovoRos`

        ## Args
        - `host : str` : host of psu, preferably in form of `192.168.x.x`
        - `logger: logging.Logger | str | None` :
            - if `logger` is instance of `logging.Logger`, it will log with it;
            - if `logger` is `str`, new logger will be created with it as name
            - otherwise, no log
        """
        super().__init__(logger)

        self.host: str = host

        self.info(f"ros bridge initalized with host : {self.host}")
        if not "192.168" in self.host:
            self.warning("host is not in form of 192.168.x.x")
            self.warning("this might cause networking latency")

        self.ros = roslibpy.Ros(host, 9090)
        self.ros.run()

        build_list = [
            (self.__tcp_speed, TOPIC_TCP_SPEED, TYPE_TCP_SPEED),
            (self.__tcp_pose, TOPIC_TCP_POSE, TYPE_TCP_POSE),
            (self.__joint_state, TOPIC_JOINT_STATE, TYPE_JOINT_STATE),
            (self.__power_status, TOPIC_POWER_STATUS, TYPE_POWER_STATUS),
            (self.__robot_status, TOPIC_ROBOT_STATUS, TYPE_ROBOT_STATUS),
            (self.__estop_status, TOPIC_ESTOP_STATUS, TYPE_ESTOP_STATUS),
            (self.__safe_stop_status, TOPIC_SAFE_STOP_STATUS, TYPE_SAFE_STOP_STATUS),
            (self.__runtime_state, TOPIC_RUNTIME_STATE, TYPE_RUNTIME_STATE),
            (self.__arm_state, TOPIC_ARM_STATE, TYPE_ARM_STATE),
        ]

        self.subscribers: dict[str, roslibpy.Topic] = {}

        for cb, name, message_type in build_list:
            self.info(f"Subscribing to topic: {name}, type : {message_type}")
            sub = roslibpy.Topic(self.ros, name, message_type)
            sub.subscribe(cb)
            self.subscribers[name] = sub

    # Topic Call Back
    def __tcp_speed(self, message):
        self.tcp_speed_lin = message["speed"]["linear"]
        self.tcp_speed_ang = message["speed"]["angular"]

    def __tcp_pose(self, message):
        vec = message["pose"]["position"]
        self.tcp_pose_vec = (vec["x"], vec["y"], vec["z"])

        quat = message["pose"]["orientation"]
        self.tcp_pose_quat = (
            quat["x"],
            quat["y"],
            quat["z"],
            quat["w"],
        )

    def __joint_state(self, message):
        self.joint_pos = message["position"]
        self.joint_vel = message["velocity"]
        self.joint_eff = message["effort"]

    def __power_status(self, message):
        self.power_status = message["state"]
        self.voltage = message["voltage"]
        self.current = message["current"]

    def __robot_status(self, message):
        self.driver_state = message["driver_state"]
        self.drives_powered = message["drives_powered"]

    def __estop_status(self, message):
        self.estop_active = message["active"]
        self.estop_circuit = message["circuit_complete"]

    def __safe_stop_status(self, message):
        self.safe_stop_active = message["active"]
        self.safe_stop_circuit = message["circuit_complete"]

    def __runtime_state(self, message):
        self.active_blocks = message["active_blocks"]
        self.current_block_progress = message["current_block_progress"]
        self.runtime_status = RuntimeState(message["state"])
        self.variables = []

        for v in message["variables"]:
            self.variables.append(Variable.from_message(v))

    def __arm_state(self, message):
        self.enabled = message["enabled"]
        self.state = message["state"]
        self.joint_states = []

        for j in message["joint_states"]:
            self.joint_states.append(JointState.from_message(j))

    # Service

    # PSU/Robot
    def safe_stop_reset(self) -> InovoServiceResponse:
        req = roslibpy.ServiceRequest()
        res = roslibpy.Service(self.ros, SERVICE_SAFE_STOP_RESET, TYPE_TRIGGER).call(
            req
        )
        return InovoServiceResponse.from_message(res)

    def estop_reset(self) -> InovoServiceResponse:
        req = roslibpy.ServiceRequest()
        res = roslibpy.Service(self.ros, SERVICE_ESTOP_RESET, TYPE_TRIGGER).call(req)
        return InovoServiceResponse.from_message(res)

    def power_on(self) -> InovoServiceResponse:
        req = roslibpy.ServiceRequest()
        res = roslibpy.Service(self.ros, SERVICE_POWER_ON, TYPE_TRIGGER).call(req)
        return InovoServiceResponse.from_message(res)

    def power_off(self) -> InovoServiceResponse:
        req = roslibpy.ServiceRequest()
        res = roslibpy.Service(self.ros, SERVICE_POWER_OFF, TYPE_TRIGGER).call(req)
        return InovoServiceResponse.from_message(res)

    def robot_enable(self) -> InovoServiceResponse:
        req = roslibpy.ServiceRequest()
        res = roslibpy.Service(self.ros, SERVICE_ROBOT_ENABLE, TYPE_TRIGGER).call(req)
        return InovoServiceResponse.from_message(res)

    def robot_disable(self) -> InovoServiceResponse:
        req = roslibpy.ServiceRequest()
        res = roslibpy.Service(self.ros, SERVICE_ROBOT_DISABLE, TYPE_TRIGGER).call(req)
        return InovoServiceResponse.from_message(res)

    # Runtime
    def runtime_start(self, procedure_name: str | None = None) -> InovoServiceResponse:
        """
        start a sequence in runtime

        ## Args:
        - `procedure_name : str | None`:
            - if `None`, will start from start block
            - if `str`, will try to start function with respected name
        """

        payload = {}

        if procedure_name:
            payload["procedure_name"] = procedure_name

        req = roslibpy.ServiceRequest(payload)
        res = roslibpy.Service(
            self.ros, SERVICE_SEQUENCE_START, TYPE_RUN_SEQUENCE
        ).call(req)
        return InovoServiceResponse.from_message(res)

    def runtime_stop(self) -> InovoServiceResponse:
        req = roslibpy.ServiceRequest()
        res = roslibpy.Service(self.ros, SERVICE_SEQUENCE_STOP, TYPE_TRIGGER).call(req)
        return InovoServiceResponse.from_message(res)

    def runtime_pause(self) -> InovoServiceResponse:
        req = roslibpy.ServiceRequest()
        res = roslibpy.Service(self.ros, SERVICE_SEQUENCE_PAUSE, TYPE_TRIGGER).call(req)
        return InovoServiceResponse.from_message(res)

    def runtime_step(self) -> InovoServiceResponse:
        req = roslibpy.ServiceRequest()
        res = roslibpy.Service(self.ros, SERVICE_SEQUENCE_STEP, TYPE_TRIGGER).call(req)
        return InovoServiceResponse.from_message(res)

    def runtime_debug(self) -> InovoServiceResponse:
        req = roslibpy.ServiceRequest()
        res = roslibpy.Service(self.ros, SERVICE_SEQUENCE_DEBUG, TYPE_TRIGGER).call(req)
        return InovoServiceResponse.from_message(res)

    def runtime_continue(self) -> InovoServiceResponse:
        req = roslibpy.ServiceRequest()
        res = roslibpy.Service(self.ros, SERVICE_SEQUENCE_CONTINUE, TYPE_TRIGGER).call(
            req
        )
        return InovoServiceResponse.from_message(res)

    def runtime_get_var(self, name: str) -> InovoServiceResponse:
        req = roslibpy.ServiceRequest({"name": name})
        res = roslibpy.Service(self.ros, SERVICE_SEQUENCE_GET_VAR, TYPE_GET_VAR).call(
            req
        )
        return InovoServiceResponse.from_message(res)

    def runtime_set_var(self, name: str, value: typing.Any) -> InovoServiceResponse:
        req = roslibpy.ServiceRequest({"name": name, "value": str(value)})
        res = roslibpy.Service(self.ros, SERVICE_SEQUENCE_SET_VAR, TYPE_SET_VAR).call(
            req
        )
        return InovoServiceResponse.from_message(res)

    @contextmanager
    def jog(self):
        """
        Enter a context of jog command mode. Advertise when enter context
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
        """

        top = roslibpy.Topic(self.ros, TOPIC_CARTESIAN_JOG, TYPE_CARTESIAN_JOG_DEMAND)
        top.advertise()

        publisher = JogPublisher(top)

        yield publisher

        publisher.publisher.unadvertise()
        del publisher

    # Destruction
    def unsubscribe_all(self):
        for n, sub in self.subscribers.items():
            self.info(f"unsubscribing topic : {n}")
            sub.unsubscribe()

    def resubscribe_all(self):
        for n, sub in self.subscribers.items():
            self.info(f"resubscribing topic : {n}")
            sub.subscribe()

    def __del__(self):
        self.ros.close()


class JogPublisher:
    """
    context manager for jog

    automatically unadvertise when `del`
    """

    publisher: roslibpy.Topic

    def __init__(self, publisher: roslibpy.Topic):
        self.publisher = publisher

        self.publisher.advertise()

    def jog(
        self,
        x: float = 0,
        y: float = 0,
        z: float = 0,
        rx: float = 0,
        ry: float = 0,
        rz: float = 0,
    ):
        """
        Send a cartesian jog twist demand

        Args:
        - `x : float`: target linear velocity x. Defaults to 0.
        - `y : float`: target linear velocity y. Defaults to 0.
        - `z : float`: target linear velocity z. Defaults to 0.
        - `rx : float`: target angular velocity rx. Defaults to 0.
        - `ry : float`: target angular velocity ry. Defaults to 0.
        - `rz : float`: target angular velocity ry. Defaults to 0.
        """
        self.publisher.publish(
            roslibpy.Message(
                {
                    "twist": {
                        "linear": {
                            "x": x,
                            "y": y,
                            "z": z,
                        },
                        "angular": {
                            "x": rx,
                            "y": ry,
                            "z": rz,
                        },
                    }
                }
            )
        )

    def __del__(self):
        self.publisher.unadvertise()
