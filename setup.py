"""
setup script for inovopy
"""
from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'Inovo Robot Arm API'
LONG_DESCRIPTION = \
"""
A package that provide a simple python socket based api for controlling inovo robot arms.
"""

# Setting up
setup(
    name="inovopy",
    version=VERSION,
    author="Alan Chung",
    author_email="deeralan827@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'websockets', 'asyncio', 'nest-asyncio'],
    keywords=['python', 'robotics', 'inovo robotics', 'inovo robot arm', 'motion', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
