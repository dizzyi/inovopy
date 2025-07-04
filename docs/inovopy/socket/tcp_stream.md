Module inovopy.socket.tcp_stream
================================
# TCP Stream Module
This module provide an api class for managing tcp connection

## Class
- `TcpStream` : a class for managing tcp connection

Classes
-------

`TcpStream(conn: socket.socket, logger: logging.Logger | str | None = None)`
:   # TcpStream
    A class for managing tcp connetion
    
    ## Usage
    ```python
    from inovopy.socket import TcpListener, TcpStream
    
    example_listener : TcpListener = TcpListener()
    
    example_stream : TcpStream = example_listener.accept()
    
    example_stream.write("send a message")
    
    read_message = example_stream.read()
    ```
    
    initalize the stream
    
    ## Parameter
    - `conn : socket.socket` : the socket connection
    - `logger: logging.Logger | str | None` :
        - if `logger` is instance of `logging.Logger`, it will log with it;
        - if `logger` is `str`, new logger will be created with it as name
        - otherwise, no log

    ### Ancestors (in MRO)

    * inovopy.util.Loggable
    * abc.ABC

    ### Static methods

    `connect(ip: str | None = None, port: int = 50003, logger: logging.Logger | str | None = None) ‑> inovopy.socket.tcp_stream.TcpStream`
    :   Try to connect to an socket address
        
        ## Parameter
        - `ip : str`: if `None`, will try local machine
        - `port: int` : port to connect to
        - `logger: Logger`: logger for the resulted `TcpStream`
        
        ## Return
        `TcpStream` the resulted connection
        
        ## Exception:
        `SocketException`
        - if no network interface found

    ### Instance variables

    `ip: str`
    :   get the local ip of the socket

    ### Methods

    `read(self) ‑> str`
    :   read a message form the connection
        
        maximum byte : `4096`
        
        ## Return:
        `str` the message read
        
        ## Exception:
        `SocketException`:
        - if the read failed
        - if `EOF` character is read

    `try_read(self, timeout: float = 1.0) ‑> str | None`
    :   try to read a message from the socket
        ## Parameter
        - `timout : float = 1.0` : time out for the reading
        
        ## Return
        `str` : read message; or
        `None` : if no message is recived

    `write(self, msg: str)`
    :   write a message to the connection
        
        ## Parameter:
        - `msg : str` : string message to send