import screen
from settings import Settings
import logging
from utils import Utils
import game_objects as go
import os

# Setting up root logger
logger = logging.getLogger(__name__)
logging.basicConfig(filename="game.log", filemode="w", level=logging.INFO, format='%(name)s:%(levelname)s:%(message)s:')
logger.info("Root logger initialized")

# Get OS
if os.name == "posix":
    logger.debug(f"Linux operating system identified. 'cls' command will be used.")
    Settings.clear_cmd = "clear"
elif os.name == "nt":
    logger.debug(f"Windows operating system identified. 'cls' command will be used.")
    Settings.clear_cmd = "cls"


# Class for holding obj states in memory
class GameMem:
    def __init__(self):
        logger.debug(f"{self.__class__} initialized.")
        logger.info("GameMem object has been created. Used for storing screens and other gamestate objects in memory")
        self.main_window = screen.ActiveGameDisplay()
        self.main_menu = None
        self.options = None
        self.inv_window = None

        self.player_inv = go.Inventory()


# Initial console clear
os.system(Settings.clear_cmd)

# Initialize the main storage class
game = GameMem()

"""Test Items Remove"""
ten_dollars = go.Item("10 Dollar Bill", "worth about $9.94 prolly", "0.1", "10")
game.player_inv.add_item(ten_dollars, "1")

weed_pen = go.Item("Weed Pen", "The good stuff, hittin the pen!", "0.2", "50")
game.player_inv.add_item(weed_pen, "1")
game.player_inv.add_item(weed_pen, "12")
"""End Test Items"""

# MAIN GAME LOOP
while True:
    # Main game window is drawn on instantiated on GameMem init
    # Then we listen for the returned key, this wont return until
    # a key match is pressed
    # game.main_window.show()
    usr_choice = game.main_window.listen()
    logger.info("Listening for input on main window")

    # In Main Game window
    if usr_choice == "esc":
        logger.debug("User pressed 'esc'")
        Utils.transition()
        game.main_menu = screen.PauseDisplay()
        usr_choice = game.main_menu.listen()

        # In Main Menu
        if usr_choice == "1":
            game.main_window.show()
        elif usr_choice == "2":
            game.options = screen.OptionsDisplay()
            game.options.show()
            usr_choice = game.options.listen()

            # In Options Menu
            if usr_choice == "1":
                game.height_options = screen.HeightOptions()
                game.height_options.show()
                results = game.height_options.listen()

                # TODO The console height is not changing because the obj is instantiated at creation and the console variable is set then | FIX: refresh the variable
                if usr_choice == "1":
                    Settings.console_height = 35
                elif usr_choice == "2":
                    Settings.console_height = 40
                elif usr_choice == "3":
                    Settings.console_height = 45
                elif usr_choice == "4":
                    Settings.console_height = 50

        # In Main Menu
        elif usr_choice == "4":
            game.main_window.show()

    # In MainGame Window, Clicked I for inventory
    elif usr_choice == "i":
        game.inv_window = screen.InventoryDisplay(game.player_inv.get_inv_table())
        game.inv_window.show()
        usr_choice = game.inv_window.listen()
        if usr_choice == "esc":
            game.main_window.show()
