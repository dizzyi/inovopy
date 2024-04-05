"""
# TCP Stream Module
This module provide an api class for managing tcp connection

## Class
- `TcpStream` : a class for managing tcp connection
"""
import socket
import select

from inovopy.socket.utils import SocketException, auto_detect_ips
from inovopy.utils import clean
from inovopy.logger import Logger

class TcpStream:
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
    def __init__(
            self,
            conn: socket.socket,
            logger : Logger | None = None
        ):
        """
        initalize the stream

        ## Parameter
        - `conn : socket.socket` : the socket connection
        - `logger` : if it's `None`, a logger with default setting will be created
        """
        self.__conn : socket.socket = conn
        if logger:
            self.logger : Logger = logger
        else:
            ip,port = self.__conn.getsockname()
            peer_ip, _ = self.__conn.getpeername()
            name : str = f"TcpStream-{ip}-{port}-{peer_ip}"
            self.logger : Logger = Logger.default(name)

    @classmethod
    def connect(
            cls,
            ip : str | None = None,
            port : int = 50003,
            logger : Logger | None = None
        ) -> 'TcpStream':
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
        """
        if not ip:
            ip = "localhost"
        if not logger:
            name = f"TcpClient {ip}-{port}"
            logger = Logger.default(name)
        if ip == "localhost":
            ip = auto_detect_ips(logger)[0]

        logger.info("Start connecting . . .")
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((ip,port))
            logger.info(f"Successfully connected to {ip}:{port}")
            return TcpStream(conn=conn, logger=logger)
        except OSError as e:
            logger.warn("Failed to connect")
            logger.warn(f"{e}")
            raise SocketException("Failed to connect") from e

    @property
    def ip(self)->str:
        """get the local ip of the socket"""
        return self.__conn.getsockname()[0]

    def try_read(self,timeout: float = 1.0) -> str | None:
        """
        try to read a message from the socket
        ## Parameter
        - `timout : float = 1.0` : time out for the reading
        
        ## Return
        `str` : read message; or
        `None` : if no message is recived
        """
        ready_socket, _, _ = select.select([self.__conn],[],[],timeout)
        if not ready_socket:
            return None
        return self.read()


    def read(self) -> str:
        """
        read a message form the connection

        maximum byte : `2048`

        ## Return:
        `str` the message read

        ## Exception:
        `SocketException`:
        - if the read failed
        - if `EOF` character is read
        """
        try:
            self.__conn.setblocking(True)
            data = self.__conn.recv(2048)
        except OSError as e:
            self.logger.error("Error occur during socket read!")
            self.logger.error(f"{e}")
            raise SocketException("Read Error") from e

        if not data:
            self.__conn.close()
            self.logger.error("Read Error : EOF detected")
            raise SocketException("Read Error : EOF detected")

        s = clean(data.decode("UTF-8"))
        self.logger.debug(f"....{s}")

        return s

    def write(self, msg: str):
        """
        write a message to the connection

        ## Parameter:
        - `msg : str` : string message to send
        """
        try:
            self.logger.debug(f"{msg}")
            msg = f"{msg}\n"
            self.__conn.send(msg.encode())
        except Exception as e:
            self.logger.error("Error occur during socket write!")
            self.logger.error(f"{e}")
            raise SocketException("Write Error") from e

    def __del__(self):
        try:
            self.logger.debug("closing socket")
            self.__conn.shutdown(socket.SHUT_RDWR)
            self.__conn.close()
        except OSError as e:
            try:
                self.logger.error("Failed to shut down socket!")
                self.logger.error(f"{e}")
            except OSError:
                pass
