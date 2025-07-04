Module inovopy.socket.tcp_listener
==================================
# TCP Listener Module
This module provide an api class for listening tcp connection

## Classes
- `TcpListener` : a class for managing and listening connection

Variables
---------

`DEFAULT_PORT: int`
:   Default port to listen on if no poort are specified `50003`.

Classes
-------

`TcpListener(host: str | None = None, port: int = 50003, logger: logging.Logger | str | None = None)`
:   # TcpListener
    A class for listening to tcp connection
    
    ## Usage
    ```python
    from inovopy.socket import TcpListener
    
    example_listener = TcpListener()
    
    example_stream = example_listener.accept()
    ```
    
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

    ### Ancestors (in MRO)

    * inovopy.util.Loggable
    * abc.ABC

    ### Methods

    `accept(self, stream_logger: logging.Logger | str | None = None) ‑> inovopy.socket.tcp_stream.TcpStream`
    :   try accept a new tcp connection.
        
        ## Parameter:
        - `logger: logging.Logger | str | None` : logger of returned `TcpStream`
            - if `logger` is instance of `logging.Logger`, it will log with it;
            - if `logger` is `str`, new logger will be created with it as name
            - otherwise, no log
        
        ## Return:
        `TcpStream` : the accepted tcp connetion
        
        ## Exception:
        No exception, will continue to try to accept if encounter `OSError`