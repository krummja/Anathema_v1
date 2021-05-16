from __future__ import annotations
from functools import wraps
import logging


def log_init(cls):
    cls__init__ = cls.__init__

    def __init__(self, *args, **kwargs):
        logging.info("Starting " + self.__class__.__name__)
        cls__init__(self, *args, **kwargs)

    cls.__init__ = __init__
    return cls
