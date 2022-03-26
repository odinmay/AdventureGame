import screen
from settings import Settings
import logging
import os

# Get OS
if os.name == "posix":
    Settings.clear = "clear"
elif os.name == "nt":
    Settings.clear = "cls"

# Set up logger
logger = logging.getLogger(__name__)


# Class for holding class states in memory
class GameMem:
    def __init__(self):
        self.main_window = screen.ActiveGameDisplay()

# Initialize the main storage class
game_memory = GameMem()
game_memory.main_window.display()

