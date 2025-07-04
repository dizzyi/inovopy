"""
setup script for inovopy
"""

from setuptools import setup, find_packages
from pathlib import Path

VERSION = "1.0.1"
DESCRIPTION = "Inovo Robot Arm API"
LONG_DESCRIPTION = (Path(__file__).parent / "README.md").read_text()

# Setting up
setup(
    name="inovopy",
    version=VERSION,
    author="Alan Chung",
    author_email="deeralan827@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["numpy", "roslibpy"],
    keywords=[
        "python",
        "robotics",
        "inovo robotics",
        "inovo robot arm",
        "motion",
        "sockets",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
