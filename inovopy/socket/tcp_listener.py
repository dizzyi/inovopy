"""
# TCP Listener Module
This module provide an api class for listening tcp connection

## Classes
    - `TcpListener` : a class for managing and listening connection
"""
import socket
import select

from inovopy.socket.utils import SocketException, auto_detect_ips
from inovopy.socket.tcp_stream import TcpStream
from inovopy.logger import Logger

class TcpListener:
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

    DEFAULT_PORT : int = 50003
    """Default port to listen on if no poort are specified"""

    def __init__(
            self,
            host: str | None = None,
            port: int | None = None,
            logger : Logger | None = None,
        ):
        """
        initalize the tcp listener

        do not specify the host if you wish to listen at all
        of the host in your machine.

        specify the host if you wish to listen at a specific
        network in you machine

        ## Parameter
            - `host : str | None` : local ip
            - `port : int | None` : port to listen to
            - `logger : Logger | None` : logger for logging

        ## Exception:
        `SocketException`:
            - if not local ip address are found
            - if not vaild socket are created
        """
        port : int = port or TcpListener.DEFAULT_PORT

        if logger is None:
            self.logger : Logger = Logger.default(f"TcpListener-{port}")
            """logger for logging"""
        else:
            self.logger : Logger = logger


        self.logger.debug("creating TcpListener . . .")

        if host is None:
            ips = auto_detect_ips(self.logger)
            """a list of ip to bind socket to and listen to"""
        else:
            ips = [host]


        self.logger.info("Creating Socket . . .")

        self.__sockets : list[socket.socket] = []
        """a list of socket to listen to"""

        for ip in ips:
            self.logger.debug(f"ip : {ip}")
            soc : socket.socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.logger.debug("....setting socket option")
            soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.logger.debug("....trying to bind . . .")
            try:
                soc.bind((ip,port))
                self.logger.debug("....socket binding successful.")
            except OSError as e:
                self.logger.warn(f"Failed to bind @ {ip}:{port}")
                self.logger.warn(f"Error: {e}")
                continue

            self.logger.debug("....trying to listen . . .")
            try:
                soc.listen()
                self.logger.debug("....socket start listening . . .")
            except OSError as e:
                self.logger.warn(f"Failed to listen @ {ip}:{port}")
                self.logger.warn(f"{e}")
                continue

            soc.setblocking(False)

            self.logger.info(f"Finished setting up socket @ {ip}:{port}")
            self.__sockets.append(soc)


        if len(self.__sockets) == 0:
            self.logger.error("No vaild socket created.")
            raise SocketException("No vaild socket created.")

    def accept(self, stream_logger : Logger | None = None) -> TcpStream:
        """
        try accept a new tcp connection

        ## Parameter:
            `stream_logger : Logger` : logger of returned TcpStream
        
        ## Return:
            `TcpStream` : the accepted tcp connetion

        ## Exception:
            No exception, will continue to try to accept if encounter `OSError`
        """
        self.logger.info("Start accepting . . .")

        self.logger.debug("waiting for connection . . .")
        while True:
            readables, _, _ = select.select(self.__sockets,[],[],1)

            for soc in readables:
                if soc not in self.__sockets:
                    self.logger.debug("....readables not in self.__sockets")
                    continue

                (ip,port) = soc.getsockname()

                self.logger.info(f"trying to accept connection at {ip}:{port}")

                try:
                    accept = soc.accept()
                    conn : socket.socket = accept[0]
                    peer_ip, peer_port = accept[1]
                    self.logger.info(f"Accepting connect successful to {peer_ip}:{peer_port}")
                except OSError as e:
                    self.logger.warn("Accepting connection failed")
                    self.logger.warn(f"{e}")
                    continue

                stream = TcpStream(conn, stream_logger)
                return stream


    def __del__(self):
        for soc in self.__sockets:
            try:
                (ip,port) = soc.getsockname()
                self.logger.debug(f"shutting down socket @ {ip}:{port}")
                soc.close()
            except OSError as e:
                self.logger.error("Failed to shut down socket!")
                self.logger.error(f"{e}")
                continue
