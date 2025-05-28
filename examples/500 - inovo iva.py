import time
from logging.config import dictConfig

from inovopy.util import LOGGING_CONFIG_CONSOLE
from inovopy.robot import InovoRobot
from inovopy.iva import RobotCommand, MotionMode
from inovopy.geometry.transform import Transform

if __name__ == "__main__":
    dictConfig(LOGGING_CONFIG_CONSOLE)

    bot = InovoRobot.default_iva("<PSU IP address>", "iva example")

    # Get Current
    print(bot.get_current_joint())
    print(bot.get_current_transform())

    # Motion
    bot.linear_relative(Transform.from_z(10.0))
    bot.joint(bot.get_current_joint().then_j1(10.0))

    # Set Motion Parameter
    bot.set_param(speed=10.0, accel=50.0, blend_linear=100.0, blend_angular=30.0)

    # Digital IO
    print(bot.get_io_beckhoff(0))
    print(bot.set_io_beckhoff(0, True))

    # Sequence
    seq = [
        RobotCommand.motion(MotionMode.LINEAR_RELATIVE, Transform.from_z(10.0)),
        RobotCommand.sleep(10),
        RobotCommand.set_parameter(speed=20.0, accel=5.0),
    ]
    bot.sequence(seq)
