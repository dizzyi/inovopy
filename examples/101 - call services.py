import time
from logging.config import dictConfig
from inovopy.util import LOGGING_CONFIG_CONSOLE
from inovopy.rosbridge import InovoRos


if __name__ == "__main__":
    dictConfig(LOGGING_CONFIG_CONSOLE)
    ros = InovoRos("192.168.1.122", "service")

    time.sleep(2)

    assert ros.estop_reset().success

    input("enter to reset safe stop . . .")
    assert ros.safe_stop_reset().success
    input("enter to reset estop . . .")
    assert ros.estop_reset().success
    input("enter to power on robot . . .")
    assert ros.power_on().success
    input("enter to enable robot . . .")
    assert ros.robot_enable().success

    input("enter to start runtime . . .")
    assert ros.runtime_start().success
    input("enter to pause runtime . . .")
    assert ros.runtime_pause().success
    input("enter to continue runtime . . .")
    assert ros.runtime_continue().success
    input("enter to stop runtime . . .")
    assert ros.runtime_stop().success

    input("enter to disable robot. . .")
    assert ros.robot_disable().success
    input("enter to power off robot. . .")
    assert ros.power_off().success
