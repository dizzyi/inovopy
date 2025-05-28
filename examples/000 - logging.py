from inovopy.util import *

import logging
from logging.config import dictConfig

# exit(0)

if __name__ == "__main__":
    dictConfig(LOGGING_CONFIG_CONSOLE)

    logger = logging.getLogger("main")

    logger.debug("logger started")
    logger.info("logger started")
    logger.warning("logger started")
    logger.error("logger started")
