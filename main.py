import screen
import logging

# Set up logger
logger = logging.getLogger(__name__)


# Class for holding class states in memory
class GameMem:
    def __init__(self):
        self.main_window = screen.ActiveGameDisplay()

# Initialize the main storage class
game_memory = GameMem()
game_memory.main_window.display()

