import logging
import os
from datetime import datetime

now = datetime.now().strftime("%y%m%d_%H%M%S")
os.mkdir(f"../../log/{now}")
logging.basicConfig(filename=f"../../log/{now}/errors.log")


def log_error(e: Exception, problem_path: str):
    """Logs an exception raised while processing a problem in given path"""
    logging.error(f"{type(e)}: {e} in {problem_path}")
