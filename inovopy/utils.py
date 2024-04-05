"""
# Utils Module
This module provide useful functions

## Functions
    - `clean` : clean up all non visible character of a str
    - `now_str` : return formatted str of current datetime
    - `clamp` : clamp float
"""
import re
import datetime

def clean(s:str) -> str:
    """clean up all non visible characters of a str"""
    return re.sub(r"[^ -~]", "", s)

def now_str() -> str:
    """
    return a readable string of current time in format of YYYY-MM-DD HH:MM:SS

    e.g. '2024-01-01 12:00:00'
    """
    return datetime.datetime.now().strftime(r"%Y-%m-%d %Z")

def clamp(f:float, floor:float, ceil:float) -> float:
    """clamp a float between a floor and a ceil"""
    return min(max(f,floor),ceil)
