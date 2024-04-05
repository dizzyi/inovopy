"""
# Logger Module
This module provide a simple logging framework, 
which allow a single logger to log to multiple different target
with different level of verbosity

## Classes
- `LogLevel` : An enum representing different level of logging
- `LogTarget` : An interface for logger to log message to
- `Logger` : A class for managing multiple log target
- `ConsoleTarget` : A class for logging message to console
- `RollingFileTarget` : A class for logging message to rolling files

## Example
```python
from inovopy.logger import Logger
example_logger = Logger.default("Example")
example_logger.trace("This is a tracing level message.")
example_logger.debug("This is a debug level message.")
example_logger.info("This is a info level message.")
example_logger.warn("This is a warn level message.")
example_logger.error("This is a error level message.")
```
"""
import os
from typing import Optional, IO, cast
from abc import ABC, abstractmethod
from enum import IntEnum

class LogLevel(IntEnum):
    """
    # LogLevel
    LogLevel is an enum class representing different of logging verbosity

    ## Levels
    The different logging level are 
    
    - `TRACE = 0`, for detail tracing, highest level of verbosity 
    - `DEBUG = 1`, for debug information
    - `INFO  = 2`, for general information
    - `WARN  = 3`, for recoverable error
    - `ERROR = 4`, for irrecoverable error
    - `NOLOG = 5`, no logging at all
    """
    TRACE = 0
    DEBUG = 1
    INFO  = 2
    WARN  = 3
    ERROR = 4
    NOLOG = 5

    def to_str(self) -> str:
        """
        ## Return
        `str`: a string representation of the log level
        """
        match self:
            case LogLevel.TRACE:
                return "TRACE"
            case LogLevel.DEBUG:
                return "DEBUG"
            case LogLevel.INFO:
                return "INFO"
            case LogLevel.WARN:
                return "WARN"
            case LogLevel.ERROR:
                return "ERROR"
            case _:
                return ""

class LogTarget(ABC):
    """
    # LogTarget
    This is an interface for logger to log message into

    ## Usage
    You can make you own class implement this interface 
    for custom logging targets
    
    ```python
    class MyTarget(LogTarget):
        def __init__(self):
            self.log_level = LogLevel.INFO
        def log_to_target(self, msg: str, log_level: LogLevel):
            ## your own implementation
            return
        def get_log_level(self) -> LogLevel:
            return self.log_level
    ```

    Then you can make add this target to the logger

    ```python
    example_logger : Logger = Logger.default("Example")
    example_logger.add_target(MyTarget())
    ```
    """
    @abstractmethod
    def log_to_target(self, msg:str, log_level: LogLevel):
        """
        log message to target with a specific log level.

        ## Parameters:
        - `msg : str` : the message to log
        - `log_level : LogLevel` : log level of the message 
        """
    @abstractmethod
    def get_log_level(self) -> LogLevel:
        """
        getter for the target current log level
        
        ## Return:
        `LogLevel`: the log level of the target
        """


class Logger:
    """
    # Logger
    A class for managing different logging target.

    Allow you to log to different logging target with only one line.

    ## Example
    ```python
    from inovopy.logger import Logger
    example_logger = Logger.default()
    example_logger = Logger.default("Example")
    example_logger.trace("This is a tracing level message.")
    example_logger.debug("This is a debug level message.")
    example_logger.info("This is a info level message.")
    example_logger.warn("This is a warn level message.")
    example_logger.error("This is a error level message.")
    ```
    """
    def __init__(self):
        """
        initalize the logger with no logging target
        """
        self.__targets : list[LogTarget] = []

    def log(self, msg: str, log_level: LogLevel):
        """
        log a message with a specified log level to all of logger's target

        the input message will be tag with its log level

        e.g. a message `abc` with level `DEBUG` will be formatted as  `DEBUG  | abc`

        the message will only log to the target if the target's log level
        if smaller than the message logging level

        ## Parameter:
        - `msg : str` : message to log
        - `log_level` : log level of the message
        """
        msg = f"{log_level.to_str(): <6} | {msg}"
        for target in self.__targets:
            if target.get_log_level() <= log_level:
                target.log_to_target(msg, log_level)

    def add_target(self, target: LogTarget):
        """
        add a logging target to the logger

        ## Parameter
        - `target: LogTarget` : an object that implement `LogTarget`
        """
        self.__targets.append(target)

    @classmethod
    def default(cls, name:str) -> 'Logger':
        """
        construct an default logger for command usage

        it contain a console target, and a rolling files targets.

        ## Parameters:
        - `name : str` : the name to initalize the target with

        ## Return:
        `Logger` : the constructed logger
        """
        logger = Logger()
        logger.add_default_target(name)
        return logger

    def add_default_target(self, name: str):
        """
        add default target to a logger

        it contain a console target, and a rolling files targets.

       ## Parameters:
        - `name : str` : the name to initalize the target with
        """
        self.add_target(ConsoleTarget(name=name))
        self.add_target(RollingFileTarget(name=name))

    def trace(self, msg: str):
        """
        log a message with `TRACE` level

        ## Parameter:
        - `msg : str` : message to log
        """
        return self.log(msg, LogLevel.TRACE)

    def debug(self, msg: str):
        """
        log a message with `DEBUG` level

        ## Parameter:
        - `msg : str` : message to log
        """
        return self.log(msg, LogLevel.DEBUG)

    def info(self, msg: str):
        """
        log a message with `INFO` level

        ## Parameter:
        - `msg : str` : message to log
        """
        return self.log(msg, LogLevel.INFO)

    def warn(self, msg: str):
        """
        log a message with `WARN` level

        ## Parameter:
        - `msg : str` : message to log
        """
        return self.log(msg, LogLevel.WARN)

    def error(self, msg: str):
        """
        log a message with `ERROR` level

        ## Parameter:
        - `msg : str` : message to log
        """
        return self.log(msg, LogLevel.ERROR)


class ConsoleTarget(LogTarget):
    """
    # ConsoleTarget
    A class for printing log message to console

    it will print:
    - `INFO` message as green 
    - `WARN` message as yellow 
    - `ERROR` message as red 
    """

    NAME_PAD_SIZE = 10
    """static class variable for the name pad size of the console target"""

    class ConsoleColor:
        """
        a internal class for changing console display color
        """
        RED = '\033[31m'
        YELLOW = '\033[33m'
        GREEN = '\033[32m'
        RESET = '\033[0m'


    def __init__(self, name:str, log_level: LogLevel= LogLevel.INFO):
        """
        initalize a logger with a name and log level

        ## Parameters:
        - `name : str` : name of the console target
        - `log_level : LogLevel` : log level of the console target
        """
        self.name : str = name
        self.log_level : LogLevel = log_level
        ConsoleTarget.NAME_PAD_SIZE = min(max(len(self.name), ConsoleTarget.NAME_PAD_SIZE),30)

    def get_log_level(self) -> LogLevel:
        return self.log_level

    def log_to_target(self, msg: str, log_level: LogLevel):

        msg = f"{self.name.ljust(ConsoleTarget.NAME_PAD_SIZE)} | {msg}"

        cc = ConsoleTarget.ConsoleColor
        match log_level:
            case LogLevel.INFO:
                msg = f"{cc.GREEN}{msg}{cc.RESET}"
            case LogLevel.WARN:
                msg = f"{cc.YELLOW}{msg}{cc.RESET}"
            case LogLevel.ERROR:
                msg = f"{cc.RED}{msg}{cc.RESET}"
            case _:
                pass
        print(msg)

class RollingFileTarget(LogTarget):
    """
    # RollingFileTarget
    A class for storing log message to rolling files

    ## Field
    - `name : str` : name of the target
    - `log_level` : log level of the target
    - `max_roll` : number of max files in rolling
    - `max_size` : max size of the files before rolling

    ## Usage 
    Rolling file targets are not enabled by default,
    to enabled rolling file targets you can:
    - ### Set Environment Variables
    set environment variable `INOVO_LOG_DIR` to desire directory for storing logs files
    - ### Set Class Variable of `RollingFileTarget`
    ```python
    RollingFileTarget.ROOT_DIR = "./your/desire/logging/path"
        ```
    
    ## Rolling Files
    ### Directory & Files
    when the `ROOT_DIR` is set,
    it will create sub-directory of its `name`, and a `ROOT_DIR/name/name.0.log`
    and write to the file.
    ```
    ROOT_DIR
        L name
            L name.0.log
    ```
    ### Rolling
    after the file size of the log file exceed the `max_size`
    it will rolling the file `name.0.log -> name.1.log` and create a new `name.0.log`
    ```
    ROOT_DIR
        L name
            L name.0.log  <- current writing
            L name.1.log  <- history
    ```
    ### Rolling Limit
    `max_roll` specify the max number of file in rolling, 
    if the number of file exceed `max_roll` the oldest file will be discarded.
    thus keeping the all the log file never exceed a predeterminated size
    """
    ROOT_DIR : Optional[str] = os.environ.get("INOVO_LOG_DIR")
    """root directory of all log"""

    def __init__(
            self,
            name: str,
            log_level: LogLevel = LogLevel.TRACE,
            max_roll: int = 10,
            max_size: int =  1_000_000,
        ):
        """
        initalize the logger
        ## Parameter
        - `name : str` : name of the target
        - `log_level` : log level of the target
        - `max_roll` : number of max files in rolling
        - `max_size` : max size of the files before rolling
        """
        self.name : str = name
        self.log_level : LogLevel = log_level
        self.max_roll : int = max_roll
        self.max_size : int = max_size
        self.__f : Optional[IO] = None

    @property
    def log_dir(self)->str:
        """
        get the log sub directoy of the logger
        """
        root_dir : str = cast(str, RollingFileTarget.ROOT_DIR)
        return os.path.join(root_dir, self.name)

    def get_log_level(self) -> LogLevel:
        return self.log_level

    def log_to_target(self, msg: str, log_level: LogLevel):
        if RollingFileTarget.ROOT_DIR is None:
            return

        if self.__f is None:
            self.roll()

        f : IO = cast(IO, self.__f)

        f.write(f"{msg}\n")
        f.flush()

        if os.path.getsize(os.path.join(self.log_dir, f"{self.name}.0.log")) > self.max_size:
            f.close()
            self.__f = None

    def roll(self):
        """
        roll all the log files
        """
        if RollingFileTarget.ROOT_DIR is None:
            return

        if not os.path.isdir(self.log_dir):
            os.makedirs(self.log_dir)

        for i in reversed(range(self.max_roll)):
            try:
                os.replace(
                    os.path.join(self.log_dir, f"{self.name}.{i}.log"),
                    os.path.join(self.log_dir, f"{self.name}.{i+1}.log")
                )
            except FileNotFoundError:
                pass

        self.__f = open(os.path.join(self.log_dir, f"{self.name}.0.log"), "w", encoding="utf-8")

    def __del__(self):
        self.__f = None
