"""
This file will hold small userful functions that are used throughout the game logic
"""
from time import sleep
import os
import logging

import keyboard
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

    @staticmethod
    def clear_input(self):
        for i in range(100):
            keyboard.send("backspace")

    # def find_index(self, ):
    @staticmethod
    def find_index(item_row):
        counter = 0
        for row in item_row:
            if "-->" in row:
                return counter
            counter += 1
        return counter

    @staticmethod
    def load_art(filename):
        with open("./art/item_details/" + filename + ".txt", "r") as file:
            return file.read()

class Const:
    sidebar = Panel("")
