"""
This file will hold small userful functions that are used throughout the game logic
"""

from time import sleep
import os
import logging

# Setting up root logger
logger = logging.getLogger(__name__)
logging.basicConfig(filename="game.log",filemode="w", level=logging.INFO, format='%(name)s:%(levelname)s:%(message)s:')
logger.info("Root logger has been instantiated")


class Utils:
    @staticmethod
    def transition():
        os.system('clear')
        sleep(0.25)
