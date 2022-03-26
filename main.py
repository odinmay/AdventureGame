import screen
from settings import Settings
import logging
from utils import Utils
import os

# Get OS
if os.name == "posix":
    Settings.clear_cmd = "clear"
elif os.name == "nt":
    Settings.clear_cmd = "cls"

# Set up logger
logger = logging.getLogger(__name__)


# Class for holding class states in memory
class GameMem:
    def __init__(self):
        self.main_window = screen.ActiveGameDisplay()
        self.main_menu = None
        self.options = None

os.system(Settings.clear_cmd)
# Initialize the main storage class
game = GameMem()

# MAIN GAME LOOP
while True:
    # Main game window is drawn on instantiated on GameMem init
    # Then we listen for the returned key, this wont return until
    # a key match is pressed
    result = game.main_window.listen()

    # In Main Game window
    if result == "esc":
        Utils.transition()
        game.main_menu = screen.MainMenuDisplay()
        result = game.main_menu.listen()

        # In Main Menu
        if result == "2":
            Utils.transition()
            game.options = screen.OptionsDisplay()
            result = game.options.listen()

            # In Options Menu
            if result == "1":
                Utils.transition()
                game.height_options = screen.HeightOptions()
                results = game.height_options.listen()

                if result == "1":
                    Settings.console_height = 35
                elif result == "2":
                    Settings.console_height = 40
                elif result == "3":
                    Settings.console_height = 45
                elif result == "4":
                    Settings.console_height = 50

        # In Main Menu
        elif result == "4":
            game.main_window.show()



