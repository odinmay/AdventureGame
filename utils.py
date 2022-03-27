"""
This file will hold small userful functions that are used throughout the game logic
"""
from time import sleep
import os
import logging
from rich.panel import Panel
from settings import Settings

logger = logging.getLogger(__name__)


class Utils:
    @staticmethod
    def transition():
        sleep(0.2)
        os.system(Settings.clear_cmd)
        logger.info("Screen cleared")


class Const:
    sidebar = Panel("")
