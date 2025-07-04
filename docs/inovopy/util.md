Module inovopy.util
===================
# Utils Module
This module provide utility functions and classes.

## Classes
`ConsoleHandler`: colorful python logging handler
`Loggable` : helper interface for logging class

## Functions
- `clean` : clean up all non visible character of a str
- `clamp` : clamp float

Variables
---------

`LOGGING_CONFIG`
:   A simple config for `logging`, console + rotating file
    
    Usage:
    ```python
    from logging.config import dictConfig
    from inovopy.util import LOGGING_CONFIG
    
    dictConfig(LOGGING_CONFIG)
    ```
    Value: 
    ```python
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simpleformatter": {
                "format": "%(name)-10s %(levelname)-7s %(message)s",
            },
            "detailformatter": {
                "format": "%(asctime)s %(name)-10s %(levelname)-7s %(funcName)s() L%(lineno)-4d %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "rotatehandler": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "detailformatter",
                "filename": "logging/master_log.log",
                "maxBytes": 50 * 1000 * 1000,
                "backupCount": 3,
            },
            "consolehandler": {
                "()": "inovopy.util.ConsoleHandler",
                "formatter": "simpleformatter",
                "level": "INFO",
            },
        },
        "loggers": {
            "root": {
                "handlers": ["consolehandler", "rotatehandler"],
                "level": "DEBUG",
                "propagate": True,
            }
        },
    }
    ```

`LOGGING_CONFIG_CONSOLE`
:   A simple config for `logging`, console only
    
    Usage:
    ```python
    from logging.config import dictConfig
    from inovopy.util import LOGGING_CONFIG_CONSOLE
    
    dictConfig(LOGGING_CONFIG_CONSOLE)
    ```
    
    Value:
    ```python
    LOGGING_CONFIG_CONSOLE = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simpleformatter": {
                "format": "%(name)-10s %(levelname)-7s %(message)s",
            },
        },
        "handlers": {
            "consolehandler": {
                "()": "inovopy.util.ConsoleHandler",
                "formatter": "simpleformatter",
                "level": "INFO",
            },
        },
        "loggers": {
            "root": {
                "handlers": ["consolehandler"],
                "level": "DEBUG",
                "propagate": True,
            }
        },
    }
    ```

Functions
---------

`clamp(f: float, floor: float, ceil: float) ‑> float`
:   clamp a float between a floor and a ceil

`clean(s: str) ‑> str`
:   clean up all non visible characters of a str

`get_package_logger() ‑> logging.Logger`
:   Get package logger

Classes
-------

`ConsoleHandler(level=0)`
:   A class for logging to console with color
    
    Base Class:
    - `logging.Handler`
    
    Initializes the instance - basically setting the formatter to None
    and the filter list to empty.

    ### Ancestors (in MRO)

    * logging.Handler
    * logging.Filterer

    ### Class variables

    `ConsoleColor`
    :   a internal class for changing console display color

    ### Methods

    `emit(self, record: logging.LogRecord)`
    :   Do whatever it takes to actually log the specified logging record.
        
        This version is intended to be implemented by subclasses and so
        raises a NotImplementedError.

`Loggable(logger: logging.Logger | str | None = None)`
:   A simple interface baseclass for logging class
    
    Function:
    - `debug(*args, **kwargs)` : transparent to `logger.Logger.debug`
    - `info(*args, **kwargs)` : transparent to `logger.Logger.info`
    - `warning(*args, **kwargs)` : transparent to `logger.Logger.warning`
    - `error(*args, **kwargs)` : transparent to `logger.Logger.error`
    - `critical(*args, **kwargs)` : transparent to `logger.Logger.critical`

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * inovopy.robot.InovoRobot
    * inovopy.rosbridge.InovoRos
    * inovopy.socket.tcp_listener.TcpListener
    * inovopy.socket.tcp_stream.TcpStream

    ### Class variables

    `logger: logging.Logger | None`
    :

    ### Static methods

    `get_class_logger() ‑> logging.Logger`
    :

    `get_logger(name: str) ‑> logging.Logger`
    :

    ### Methods

    `critical(self, *args, **kwargs)`
    :   transparent to `logger.Logger.critical`

    `debug(self, *args, **kwargs)`
    :   transparent to `logger.Logger.debug`

    `error(self, *args, **kwargs)`
    :   transparent to `logger.Logger.error`

    `info(self, *args, **kwargs)`
    :   transparent to `logger.Logger.info`

    `warning(self, *args, **kwargs)`
    :   transparent to `logger.Logger.warning`