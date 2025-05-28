"""
# TCP Listener Module
This module provide an api class for listening tcp connection

## Classes
- `TcpListener` : a class for managing and listening connection
"""

import socket
import select
import logging

from inovopy.socket import SocketException, detect_interfaces
from inovopy.socket.tcp_stream import TcpStream
from inovopy.util import Loggable

DEFAULT_PORT: int = 50003
"""Default port to listen on if no poort are specified `50003`."""


class TcpListener(Loggable):
    """
    # TcpListener
    A class for listening to tcp connection

    ## Usage
    ```python
    from inovopy.socket import TcpListener

    example_listener = TcpListener()

    example_stream = example_listener.accept()
    ```
    """

    def __init__(
        self,
        host: str | None = None,
        port: int = DEFAULT_PORT,
        logger: logging.Logger | str | None = None,
    ):
        """
        initalize the tcp listener

        do not specify the host if you wish to listen at all
        of the host in your machine.

        specify the host if you wish to listen at a specific
        network in you machine

        ## Parameter
        - `host : str | None` : local ip
        - `port : int` : port to listen to
        - `logger: logging.Logger | str | None` :
            - if `logger` is instance of `logging.Logger`, it will log with it;
            - if `logger` is `str`, new logger will be created with it as name
            - otherwise, no log

        ## Exception:
        `SocketException`:
        - if no network interface found
        - if not vaild socket are created
        """
        super().__init__(logger)

        self.debug("creating TcpListener . . .")

        if host is None:
            self.info("host not supplied, detecting networks . . .")
            ips = detect_interfaces()
            """a list of ip to bind socket to and listen to"""

            if len(ips) == 0:
                self.error("No interface found")
                raise SocketException(
                    "No Network Interfaces, please make sure device is connected to network"
                )
        else:
            ips = [host]

        self.info("creating sockets . . .")

        self.__sockets: list[socket.socket] = []
        """a list of socket to listen to"""

        for ip in ips:
            self.debug(f"Listening @ ip {ip}")
            soc: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.debug("....setting socket option")
            soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.debug("....trying to bind . . .")
            try:
                soc.bind((ip, port))
                self.debug("....socket binding successful.")
            except OSError as e:
                self.warning(f"Failed to bind @ {ip}:{port}")
                self.warning(f"Error: {e}")
                continue

            self.debug("....trying to listen . . .")
            try:
                soc.listen()
                self.debug("....socket start listening . . .")
            except OSError as e:
                self.warning(f"Failed to listen @ {ip}:{port}")
                self.warning(f"{e}")
                continue

            soc.setblocking(False)

            self.info(f"Finished setting up socket @ {ip}:{port}")
            self.__sockets.append(soc)

        if len(self.__sockets) == 0:
            self.error("No vaild socket created.")
            raise SocketException("No vaild socket created.")

    def accept(self, stream_logger: logging.Logger | str | None = None) -> TcpStream:
        """
        try accept a new tcp connection.

        ## Parameter:
        - `logger: logging.Logger | str | None` : logger of returned `TcpStream`
            - if `logger` is instance of `logging.Logger`, it will log with it;
            - if `logger` is `str`, new logger will be created with it as name
            - otherwise, no log

        ## Return:
        `TcpStream` : the accepted tcp connetion

        ## Exception:
        No exception, will continue to try to accept if encounter `OSError`
        """
        self.info("Start accepting . . .")

        self.debug("waiting for connection . . .")
        while True:
            readables, _, _ = select.select(self.__sockets, [], [], 1)

            for soc in readables:
                soc: socket.socket = soc

                if soc not in self.__sockets:
                    self.warning("....readables not in self.__sockets")
                    continue

                (ip, port) = soc.getsockname()

                self.info(f"trying to accept connection at {ip}:{port}")

                try:
                    accept = soc.accept()
                    conn: socket.socket = accept[0]
                    peer_ip, peer_port = accept[1]
                    self.info(f"Accepting connect successful to {peer_ip}:{peer_port}")
                except OSError as e:
                    self.warning("Accepting connection failed")
                    self.warning(f"{e}")
                    continue

                stream = TcpStream(conn, stream_logger)
                return stream

    def __del__(self):
        for soc in self.__sockets:
            try:
                (ip, port) = soc.getsockname()
                self.debug(f"shutting down socket @ {ip}:{port}")
                soc.close()
            except OSError as e:
                self.error("Failed to shut down socket!")
                self.error(f"{e}")
                continue
