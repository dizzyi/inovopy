"""
# TCP Stream Module
This module provide an api class for managing tcp connection

## Class
- `TcpStream` : a class for managing tcp connection
"""

import socket
import select
import logging

from inovopy.socket import SocketException, EndOfCommunication, detect_interfaces
from inovopy.util import clean
from inovopy.util import Loggable


class TcpStream(Loggable):
    """
    # TcpStream
    A class for managing tcp connetion

    ## Usage
    ```python
    from inovopy.socket import TcpListener, TcpStream

    example_listener : TcpListener = TcpListener()

    example_stream : TcpStream = example_listener.accept()

    example_stream.write("send a message")

    read_message = example_stream.read()
    ```
    """

    def __init__(self, conn: socket.socket, logger: logging.Logger | str | None = None):
        """
        initalize the stream

        ## Parameter
        - `conn : socket.socket` : the socket connection
        - `logger: logging.Logger | str | None` :
            - if `logger` is instance of `logging.Logger`, it will log with it;
            - if `logger` is `str`, new logger will be created with it as name
            - otherwise, no log
        """
        super().__init__(logger)
        self.__conn: socket.socket = conn

    @classmethod
    def connect(
        cls,
        ip: str | None = None,
        port: int = 50003,
        logger: logging.Logger | str | None = None,
    ) -> "TcpStream":
        """
        Try to connect to an socket address

        ## Parameter
        - `ip : str`: if `None`, will try local machine
        - `port: int` : port to connect to
        - `logger: Logger`: logger for the resulted `TcpStream`

        ## Return
        `TcpStream` the resulted connection

        ## Exception:
        `SocketException`
        - if no network interface found
        """
        logger = TcpStream.get_class_logger()

        if not ip:
            ip = "localhost"

        if ip == "localhost":
            ips = detect_interfaces()
            if len(ips) == 0:
                logger.error("No interface found")
                raise SocketException(
                    "No Network Interfaces, please make sure device is connected to network"
                )

        logger.debug("Start connecting . . .")
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((ip, port))
            logger.debug(f"Successfully connected to {ip}:{port}")
            return TcpStream(conn=conn, logger=logger)
        except OSError as e:
            logger.warning("Failed to connect")
            logger.warning(f"{e}")
            raise SocketException("Failed to connect") from e

    @property
    def ip(self) -> str:
        """get the local ip of the socket"""
        return self.__conn.getsockname()[0]

    def try_read(self, timeout: float = 1.0) -> str | None:
        """
        try to read a message from the socket
        ## Parameter
        - `timout : float = 1.0` : time out for the reading

        ## Return
        `str` : read message; or
        `None` : if no message is recived
        """
        ready_socket, _, _ = select.select([self.__conn], [], [], timeout)
        if not ready_socket:
            return None
        return self.read()

    def read(self) -> str:
        """
        read a message form the connection

        maximum byte : `4096`

        ## Return:
        `str` the message read

        ## Exception:
        `SocketException`:
        - if the read failed
        - if `EOF` character is read
        """
        try:
            self.__conn.setblocking(True)
            data = self.__conn.recv(4096)
        except OSError as e:
            self.error("Error occur during socket read!")
            self.error(f"{e}")
            raise SocketException("Read Error") from e

        if not data:
            self.__conn.close()
            self.error("Read Error : EOF detected")
            raise EndOfCommunication()

        s = clean(data.decode("UTF-8"))
        self.debug(f"...{s}")

        return s

    def write(self, msg: str):
        """
        write a message to the connection

        ## Parameter:
        - `msg : str` : string message to send
        """
        try:
            self.debug(f"{msg}")
            msg = f"{msg}\n"
            self.__conn.send(msg.encode())
        except Exception as e:
            self.error("Error occur during socket write!")
            self.error(f"{e}")
            raise SocketException("Write Error") from e

    def __del__(self):
        try:
            self.debug("closing socket")
            self.__conn.close()
        except OSError as e:
            try:
                self.error("Failed to shut down socket!")
                self.error(f"{e}")
            except OSError:
                pass
