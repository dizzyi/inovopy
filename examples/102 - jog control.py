import time
from logging.config import dictConfig
from inovopy.util import LOGGING_CONFIG_CONSOLE
from inovopy.rosbridge import InovoRos


if __name__ == "__main__":
    dictConfig(LOGGING_CONFIG_CONSOLE)

    ros = InovoRos("<PSU IP addresss>", "jog")

    time.sleep(2)

    # Enter context of live controlling robot
    with ros.jog() as j:

        for i in range(100):
            # specify target twist (linear + angular velocity)
            j.jog(z=-0.01)
            # some delay time
            time.sleep(0.01)

        for i in range(100):
            j.jog(z=0.01)
            time.sleep(0.01)
