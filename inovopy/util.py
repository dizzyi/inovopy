"""
# Utils Module
This module provide utility functions and classes.

## Classes
`ConsoleHandler`: colorful python logging handler
`Loggable` : helper interface for logging class

## Functions
- `clean` : clean up all non visible character of a str
- `clamp` : clamp float
"""

import logging
import abc
import re


def clean(s: str) -> str:
    """clean up all non visible characters of a str"""
    return re.sub(r"[^ -~]", "", s)


def clamp(f: float, floor: float, ceil: float) -> float:
    """clamp a float between a floor and a ceil"""
    return min(max(f, floor), ceil)


class ConsoleHandler(logging.Handler):
    """
    A class for logging to console with color

    Base Class:
    - `logging.Handler`
    """

    class ConsoleColor:
        """
        a internal class for changing console display color
        """

        RED = "\033[31m"
        YELLOW = "\033[33m"
        GREEN = "\033[32m"
        RESET = "\033[0m"

    def __init__(self, level=0):
        super().__init__(level)

    def emit(self, record: logging.LogRecord):
        cc = ConsoleHandler.ConsoleColor

        l = record.levelno
        msg = self.format(record)

        if l >= 40:
            msg = f"{cc.RED}{msg}{cc.RESET}"
        elif l >= 30:
            msg = f"{cc.YELLOW}{msg}{cc.RESET}"
        elif l >= 20:
            msg = f"{cc.GREEN}{msg}{cc.RESET}"
        else:
            pass

        print(msg)


def get_package_logger() -> logging.Logger:
    """Get package logger"""
    return logging.getLogger("inovopy")


class Loggable(abc.ABC):
    """
    A simple interface baseclass for logging class

    Function:
    - `debug(*args, **kwargs)` : transparent to `logger.Logger.debug`
    - `info(*args, **kwargs)` : transparent to `logger.Logger.info`
    - `warning(*args, **kwargs)` : transparent to `logger.Logger.warning`
    - `error(*args, **kwargs)` : transparent to `logger.Logger.error`
    - `critical(*args, **kwargs)` : transparent to `logger.Logger.critical`
    """

    logger: logging.Logger | None = None

    @classmethod
    def get_class_logger(cls) -> logging.Logger:
        return get_package_logger().getChild(cls.__name__)

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        return cls.get_class_logger().getChild(name)

    def __init__(self, logger: logging.Logger | str | None = None):
        super().__init__()

        if isinstance(logger, logging.Logger):
            self.logger = logger
        elif isinstance(logger, str):
            self.logger = self.get_logger(logger)

    def debug(self, *args, **kwargs):
        """transparent to `logger.Logger.debug`"""
        if self.logger:
            self.logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        """transparent to `logger.Logger.info`"""
        if self.logger:
            self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        """transparent to `logger.Logger.warning`"""
        if self.logger:
            self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        """transparent to `logger.Logger.error`"""
        if self.logger:
            self.logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        """transparent to `logger.Logger.critical`"""
        if self.logger:
            self.logger.critical(*args, **kwargs)


# Default Logging Config
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
"""
A simple config for `logging`, console only

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
"""

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
"""
A simple config for `logging`, console + rotating file

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
"""