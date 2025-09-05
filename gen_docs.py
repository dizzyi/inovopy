"""generate docs for inovopy"""

import subprocess
import shutil
import os
import logging
from logging.config import dictConfig
from inovopy.util import LOGGING_CONFIG_CONSOLE


def gen_docs():
    """generate docs for inovopy"""
    logger = logging.getLogger("GEN DOC")

    logger.info("Removing old /docs . . .")
    shutil.rmtree("./docs", ignore_errors=True)

    logger.info("generating docs . . .")
    res = subprocess.run(
        ["pdoc", "--html", "-o", "./docs", "inovopy"],
        capture_output=True,
        text=True,
        check=False,
    )

    for stdline in res.stdout.split("\n"):
        if stdline:
            logger.info(f"pdoc -- {stdline}")

    if res.stderr != "":
        logger.error(res.stderr)
        return


if __name__ == "__main__":
    dictConfig(LOGGING_CONFIG_CONSOLE)
    gen_docs()
