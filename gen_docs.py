import subprocess
import shutil
import os
from inovopy.logger import Logger

def gen_docs():
    logger = Logger.default("Gen-Docs")

    logger.info("Removing old /docs . . .")
    shutil.rmtree("./docs", ignore_errors=True)

    res = subprocess.run(["pdoc","--html","inovopy", "--force"], capture_output=True, text=True, check=False)

    for stdline in res.stdout.split('\n'):
        if stdline:
            logger.info(f"pdoc -- {stdline}")

    if res.stderr != "":
        logger.error(res.stderr)
        return
    
    logger.info("moving from /html/inovopy to /docs")
    shutil.copytree("./html/inovopy", "./docs")

    logger.info("Removing /html . . .")
    shutil.rmtree("./html", ignore_errors=True)

if __name__ == "__main__":
    gen_docs()