import time
from logging.config import dictConfig
from inovopy.util import LOGGING_CONFIG_CONSOLE
from inovopy.rosbridge import InovoRos


if __name__ == "__main__":
    dictConfig(LOGGING_CONFIG_CONSOLE)
    
    ros = InovoRos("<PSU IP addresss>", "rosbridge")

    time.sleep(2)

    print("All field is sync to PSU via ROS, update automatically")
    print(ros.tcp_pose_vec)
