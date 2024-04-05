"""
# Socket utils Module
This module provide an api class for listening tcp connection

## Classes
    - `SocketExecption` : An Excpetion Class for all socket related exception

## Function
    - `auto_detect_ips` : detect ip of local machine
"""

import socket
import platform
from inovopy.logger import Logger

class SocketException(Exception):
    pass

class EndOfCommunication(Exception):
    pass

def auto_detect_ips(logger: Logger) -> list[str]:
    """
    try to automatically detect local ip of this machine
    in all local networks

    ## Return:
        `list[str]` a list of ip

    ## Exception:
        `SocketException` if no local ip address is found
    """
    logger.info("No host provided, start detecting host. . .")

    hostname = socket.gethostname()
    if platform.system() == "Linux":
        logger.debug("....linux environmnet detected adding \".local\" suffix")
        hostname += ".local"
    logger.debug(f"....detected hostname : {hostname}")

    hosts = socket.gethostbyname_ex(hostname)
    logger.debug(f"....gethostbyname_ex : {hosts}")

    ips : list[str] = hosts[2]
    logger.info(f"detected ips : {ips}")

    if len(ips) == 0:
        logger.error("No local ip address found")
        raise SocketException("No local ip addresss found")

    if all("192.168" not in ip for ip in ips):
        logger.warn("No 192.168.X.X ip detected")
        logger.warn("device might not be connected to local network")

    return ips