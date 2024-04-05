"""
# Ros Bridge Module
This module contain function and class for using rosbridge 
api to command and get state from inovo arm

## Class
    - `RosBridge` : for handling rosbridge communication

## Functions
    - `run_time_json` : construct rosbridge message for reading runtime state
    - `arm_state_json` : construct rosbridge message for reading arm state
    - `stop_seq_json` : construct rosbridge messagee for stopping sequence
    - `start_seq_json` : construct rosbridge messsage for starting sequence

## Exception
    - `RosBridgeExcpetion` : all ros bridge related exception
"""
import json
import socket
import asyncio
import websockets
import nest_asyncio

from inovopy.logger import Logger

def run_time_json()->str:
    """construct rosbridge message for reading runtime state"""
    return json.dumps({
        "op": "subscribe",
        "topic": "/sequence/runtime_state",
        "type": "commander_msgs/RuntimeState",
    })

def arm_state_json()->str:
    """construct rosbridge message for reading arm state"""
    return json.dumps({
            "op": "subscribe",
            "topic": "/robot/arm_state",
            "type": "arm_msgs/ArmState",
    })

def stop_seq_json() -> str:
    """construct rosbridge messagee for stopping sequence"""
    return json.dumps({
        "op" : "call_service",
        "service": "/sequence/stop",
        "id": "call_service:/sequence/stop",
        "type": "std_srvs/Trigger",
        "args": {}
    })

def start_seq_json(sequence: str) -> str:
    """
    construct rosbridge messsage for starting sequence

    ## Parameter
        - sequence: str` : name of sequence(function name) in inovo blocky run time to start
    """
    return json.dumps({
        "op": "call_service",
        "service": "/sequence/start",
        "id": "sequencer/RunSequence",
        "args": {
            "procedure_name" : sequence
        }
    })

class RosBridgeException(Exception):
    """
    ROS Bridge related exception
    """

class RosBridge:
    """
    # RosBridge
    A class managing rosbridge api communication

    ## Usage
    ```python
    from inovopy.rosbrige import RosBridge

    my_ros_bridge = RosBridge("192.168.1.2")

    run_time_state = my_ros_bridge.get_run_time_state()
    arm_state = my_ros_bridge.get_arm_state()

    my_ros_bridge.start_seq("my function")
    my_ros_bridge.stop_seq()
    ```
    """
    def __init__(
            self,
            host: str,
            logger: Logger | None = None
        ):
        """
        initalize `RosBridge`

        ## Parameter
            - `host : str` : host of psu, preferably in form of `192.168.x.x`
            - `logger: Logger | None` : logger, if default if None
        """
        nest_asyncio.apply()
        self.url : str = f"ws://{host}:9090/"
        self.logger: Logger = logger if logger else Logger.default(f"RosBridge {host}")
        self.logger.info(f"ros bridge initalized with url : {self.url}")
        if not "192.168" in self.url:
            self.logger.warn("host is not in form of 192.168.x.x")
            self.logger.warn("this might cause networking errors")

    async def __websocket(self, req: str) -> dict:
        """
        async routine for creating a websocket, 
        sending message and get response

        ## Parameter:
            - `req : str` : json message to send

        ## Return:
            `dict` response parse into dict
        """
        self.logger.debug("........trying to connect to websocket . . .")
        try:
            async with websockets.connect(self.url) as websocket:
                self.logger.debug("........connection successful, sending message . . .")
                await websocket.send(req)

                self.logger.debug("........reading message . . .")
                res = await websocket.recv()
                res = json.loads(res)
                return res
        except (ConnectionRefusedError, socket.gaierror) as e:
            self.logger.error(f"Cannot Connect Websocket due to connection refused error : {e}")
            self.logger.error("this error might be cause by host name not being not a ip address")
            self.logger.error("please retry with 192.168.x.x form ip as host")
            raise RosBridgeException("Websocket Connection Error") from e
        

    def websocket(self, req: str) -> dict:
        """
        sending message and get response

        ## Parameter:
            - `req : str` : json message to send

        ## Return:
            `dict` response parse into dict
        """
        self.logger.debug(f"....req : {req}")
        res = asyncio.get_event_loop().run_until_complete(self.__websocket(req))
        self.logger.debug(f"....res : {res}")
        return res
    
    def get_run_time_state(self) -> dict:
        """
        get the runtime state
        
        ## Return:
            `dict` return message representing runtime state
        """
        self.logger.info("getting run time state . . .")
        return self.websocket(run_time_json())

    def get_arm_state(self) -> dict:
        """
        get the arm state
        
        ## Return:
            `dict` return message representing arm state
        """
        self.logger.info("getting arm state . . .")
        return self.websocket(arm_state_json())

    def stop_seq(self):
        """stop sequence"""
        self.logger.info("stopping robot sequence . . .")
        if not self.websocket(stop_seq_json())["values"]["success"]:
            self.logger.error("failed to stop robot sequence")
            raise RosBridgeException("Failed to stop sequence")

    def start_seq(self,seq:str):
        """
        start a sequence

        ## Parameter:
            - `seq: str` : name of the function to call
        """
        self.logger.info(f"starting robot sequence {seq} . . .")
        if not self.websocket(start_seq_json(seq))["values"]["success"]:
            self.logger.error("failed to start robot sequence")
            raise RosBridgeException("Failed to start sequence")
