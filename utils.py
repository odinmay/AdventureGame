"""
This file will hold small userful functions that are used throughout the game logic
"""
from time import sleep
import os
import logging
from rich.panel import Panel
from settings import Settings
import json

logger = logging.getLogger(__name__)


class Utils:
    @staticmethod
    def transition():
        sleep(0.2)
        os.system(Settings.clear_cmd)
        logger.info("Screen cleared")

    @staticmethod
    def read_map_metadata(map_info_path: str) -> dict:
        with open(map_info_path, "r", encoding="utf-8") as json_file:
            # Dictionary of map_info.json data
            return json.load(json_file)



class Const:
    sidebar = Panel("")
