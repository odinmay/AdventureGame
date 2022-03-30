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
        ################# Screens ##########################
        self.main_game_window = screen.ActiveGameDisplay()
        self.pause_menu_window = None
        self.options_window = None
        self.inv_window = None
        self.world_map_window = None
        self.local_map_window = None
        self.character_window = None
        self.splash_screen = screen.SplashScreen()
        self.main_menu = None
        ####################################################

        self.player_inv = go.Inventory()


# Initial console clear
os.system(Settings.clear_cmd)

# Initialize the main storage class
game = GameMem()

# """Test Items Remove"""
# ten_dollars = go.Item("10 Dollar Bill", "Cold Hard Cash", "0.1", "10")
# game.player_inv.add_item(ten_dollars, "1")
#
# weed_pen = go.Item("Weed Pen", "hittin' the pen!", "0.2", "50")
# game.player_inv.add_item(weed_pen, "1")
# game.player_inv.add_item(weed_pen, "12")
#
# shungite = go.Item("Shungite", "I think he's jail or something..", "2", "1000")
# game.player_inv.add_item(shungite, "10")
# """End Test Items"""


game.splash_screen.show()
game.main_menu = screen.MainMenu()
# MAIN GAME LOOP
while True:
    game.main_menu.show()
    usr_choice = game.main_menu.listen()
    if usr_choice == "1":

        # Main game window is drawn on instantiated on GameMem init
        # Then we listen for the returned key, this won't return until
        # a key match is pressed
        # game.main_game_window.show()
        game.main_game_window.load_map(go.Levels.NH1)
        usr_choice = game.main_game_window.listen()
        logger.info("Listening for input on main window")

        # In Main Game window
        if usr_choice == "esc":
            logger.debug("User pressed 'esc'")
            Utils.transition()
            game.pause_menu_window = screen.PauseDisplay()
            usr_choice = game.pause_menu_window.listen()

            # In Main Menu
            if usr_choice == "1":
                game.main_game_window.show()
            elif usr_choice == "2":
                game.options_window = screen.OptionsDisplay()
                game.options_window.show()
                usr_choice = game.options_window.listen()

                # In Options Menu
                if usr_choice == "1":
                    game.height_options = screen.HeightOptions()
                    game.height_options.show()
                    results = game.height_options.listen()

                    # TODO The console height is not changing because the obj is instantiated at creation and the console variable is set then | FIX: refresh the variable
                    if usr_choice == "1":
                        game.main_game_window.set_height(40)
                        game.main_game_window.show()
                    elif usr_choice == "2":
                        game.main_game_window.set_height(60)
                        game.main_game_window.show()
                    elif usr_choice == "3":
                        game.main_game_window.set_height(70)
                        game.main_game_window.show()
                    elif usr_choice == "4":
                        game.main_game_window.set_height(80)
                        game.main_game_window.show()

            # In Main Menu
            elif usr_choice == "4":
                game.main_game_window.show()

        # In MainGame Window, Clicked I for inventory
        elif usr_choice == "i":
            game.inv_window = screen.InventoryDisplay(game.player_inv.get_inv_table())
            game.inv_window.show()
            usr_choice = game.inv_window.listen()
            if usr_choice == "esc":
                game.main_game_window.show()

        # IN Main Game Window
        elif usr_choice == "m":
            game.world_map_window = screen.WorldMapDisplay()
            game.world_map_window.show()
            usr_choice = game.world_map_window.listen()
            if usr_choice == "l":
                game.local_map_window = screen.LocalMapDisplay()
                game.local_map_window.show()
                usr_choice = game.local_map_window.listen()
                if usr_choice == "m":
                    game.world_map_window.show()

            elif usr_choice == "esc" or usr_choice == "m":
                game.main_game_window.show()

        # In Char Menu
        elif usr_choice == "c":
            game.character_window = screen.CharacterStatus()
            game.character_window.show()
            usr_choice = game.character_window.listen()
            if usr_choice == "c":
                game.main_game_window.show()

    else:
        continue