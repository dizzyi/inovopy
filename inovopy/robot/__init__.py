from contextlib import contextmanager
import json
import re

from inovopy.logger import Logger
from inovopy.robridge import RosBridge
from inovopy.socket import TcpListener, TcpStream
from inovopy.geometry.jointcoord import JointCoord
from inovopy.geometry.transform import Transform, rad_to_deg
from inovopy.iva import *
from inovopy.utils import clean

class IvaException(Exception):
    """
    # Iva Exception
    """

class InovoRobot:

    def __init__(
            self,
            tcp_stream : TcpStream,
            ros_bridge : RosBridge,
            logger : Logger | None = None
        ):
        self.tcp_stream : TcpStream = tcp_stream
        self.ros_bridge : RosBridge = ros_bridge
        self.logger : Logger = \
                logger if logger else Logger.default(f"InooRobot {tcp_stream.ip}")

    @classmethod
    def default_iva(cls, host:str)->'InovoRobot':
        listener = TcpListener()
        ros_bridge : RosBridge = RosBridge(host=host)
        ros_bridge.start_seq("iva")
        tcp_stream: TcpStream = listener.accept()
        del(listener)
        bot : InovoRobot = InovoRobot(tcp_stream=tcp_stream, ros_bridge=ros_bridge)
        return bot

    def read(self) -> str:
        return self.tcp_stream.read()
    
    def write(self, instruction : dict[str, str|float]):
        msg = json.dumps(instruction)
        self.tcp_stream.write(msg)

    def assert_res_ok(self):
        res = self.read()
        if res != "OK":
            raise IvaException(f"Expect resopnse to be \"OK\", but recieve {res}")

    def execute(self, robot_command: RobotCommand, enter_context: bool = False):
        self.write(execute(robot_command=robot_command, enter_context=enter_context))
        self.assert_res_ok()

    def sleep(self, second: float):
        self.execute(RobotCommand.sleep(second=second))
    
    def enqueue(self, robot_command: RobotCommand):
        self.write(enqueue(robot_command=robot_command))
        self.assert_res_ok()

    def dequeue(self, enter_context: bool = False):
        self.write(dequeue(enter_context=enter_context))
        self.assert_res_ok()
    
    def sequence(self, sequence: list[RobotCommand], enter_context: bool = False):
        for step in sequence:
            self.enqueue(step)
        self.dequeue(enter_context=enter_context)

    def pop(self):
        self.write(pop())
        self.assert_res_ok()

    def io(self, io_command : IOCommand):
        self.write(io(io_command=io_command))

    def get_io_beckhoff(self, port: int) -> bool:
        self.io(IOCommand.get_digital(target="beckhoff",port=port))
        return self.read() == "True"
    def get_io_wrist(self, port: int) -> bool:
        self.io(IOCommand.get_digital(target="wrist", port=port))
        return self.read() == "True"
    def set_io_beckhoff(self, port: int, state: bool):
        self.io(IOCommand.set_digital(target="beckhoff",port=port, state=state))
        self.assert_res_ok()
    def set_io_wrist(self, port: int, state: bool):
        self.io(IOCommand.set_digital(target="wrist", port=port, state=state))
        self.assert_res_ok()

    def gipper_activate(self):
        self.write(GripperCommand.activate())
        self.assert_res_ok()
    def gripper_get(self)->float:
        self.write(GripperCommand.get())
        return float(self.read()) * 100
    def gripper_set(self, label: str):
        self.write(GripperCommand.set(label=label))
        self.assert_res_ok()

    def get_current_transform(self) -> Transform:
        self.write(get_current("transform"))
        return Transform.from_robot(self.read())

    def get_current_joint(self) -> JointCoord:
        self.write(get_current("joint_coord"))
        return JointCoord.from_robot(self.read())
    
    def get_data(self,key : str) -> str:
        self.write(get_data(key=key))
        return self.read()

    @contextmanager
    def context(self, robot_command: RobotCommand):
        self.execute(robot_command=robot_command, enter_context=True)
        try:
            yield
        finally:
            self.pop()

    @contextmanager
    def context_sequence(self, sequence: list[RobotCommand]):
        self.sequence(sequence=sequence, enter_context=True)
        try:
            yield
        finally:
            self.pop()