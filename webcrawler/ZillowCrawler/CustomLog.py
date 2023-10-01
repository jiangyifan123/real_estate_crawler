from functools import wraps
import logging
from datetime import datetime
import os

isDebug = True
filepath = 'logs/debug.log'
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

def logged(msg=""):
    """
    Add logging to a function. level is the logging
    level, name is the logger name, and message is the
    log message. If name and message aren't specified,
    they default to the function's module and name.
    """
    def decorate(fun):
        logging.basicConfig(filename=filepath, level=logging.DEBUG, format=LOG_FORMAT)
        @wraps(fun)
        def wrapper(*args, **kwargs):
            if isDebug: 
                logging.debug("start {name}, msg: {msg}".format(
                    name=fun.__name__,
                    msg=msg))
            ans = fun(*args, **kwargs)
            if isDebug:
                logging.debug("end {name}, msg: {msg}".format(
                    name=fun.__name__,
                    msg=msg))
            return ans
        return wrapper
    return decorate

def logError(msg=""):
    logging.basicConfig(filename=filepath, level=logging.ERROR, format=LOG_FORMAT)
    logging.error(msg)

def logDebug(msg=""):
    logging.basicConfig(filename=filepath, level=logging.DEBUG, format=LOG_FORMAT)
    logging.debug(msg)