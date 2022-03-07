import logging
from datetime import datetime
from pathlib import Path

day = datetime.now().strftime("%y%m%d")
time = datetime.now().strftime("%H%M%S")
Path(f"../../log/{day}").mkdir(exist_ok=True)
logging.basicConfig(filename=f"../../log/{day}/{time}.log")


def log_error(e: Exception, problem_path: str):
    """Logs an exception raised while processing a problem in given path"""
    logging.error(f"{type(e)}: {e} in {problem_path}")
