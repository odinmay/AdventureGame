"""Runs main game loop and entire game. Main entry point"""
import logging
import os
from pprint import pprint
import level
import screen
from settings import Settings
from utils import Utils
import game_objects as go
import level as lvl
from time import sleep

# Setting up root logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="game.log",
    filemode="w",
    level=logging.DEBUG,
    format='%(name)s:%(levelname)s:%(message)s:'
)

logger.info("Root logger initialized")

lvl_loader = level.Loader()

# gas_station_lvl = lvl_loader.create_level("gas_station")
parking_lot_lvl = lvl_loader.create_level("parking_lot")


# Class for holding game object states in memory
class GameMem:
    """Game class which holds all active game objects"""

    def __init__(self):
        logger.debug(f"{self.__class__} initialized.")
        logger.info("GameMem object has been created. Used for storing screens and other "
                    "gamestate objects in memory")

        self.player = go.Player()

        #  TODO Instatiate all screen on boot, potentially multithread while splash screen shows
        ################# Screens ##########################
        self.active_game_window = screen.ActiveGameDisplay()
        self.pause_menu_window = None
        self.options_window = None
        self.inv_window = None
        self.world_map_window = None
        self.local_map_window = None
        self.character_window = None
        self.splash_screen = screen.SplashScreen()
        self.main_menu = None
        self.height_options = None
        self.item_popup_screen = None
        ####################################################

# Get OS info and set clear/cls command
if os.name == "posix":
    logger.debug("Linux operating system identified. 'cls' command will be used.")
    Settings.clear_cmd = "clear"
elif os.name == "nt":
    logger.debug("Windows operating system identified. 'cls' command will be used.")
    Settings.clear_cmd = "cls"

# Initial console clear
os.system(Settings.clear_cmd)

# Initialize the main storage class

game = GameMem()

weed_pen_details = Utils.load_art("weed_pen")

ten_dollars_details = Utils.load_art("10_dollar_bill")

shotgun_details = Utils.load_art("shotgun")

shungite_detais = Utils.load_art("shungite")

ten_dollars = go.Item("10 Dollar Bill", "Cold Hard Cash", 10, 0.1,
                   ten_dollars_details)  # Add another arg with item art
game.player.inv.add_item(ten_dollars, 1)

weed_pen = go.Item("Weed Pen", "hittin' the pen!", 50, 0.2, weed_pen_details)
game.player.inv.add_item(weed_pen, 1)
game.player.inv.add_item(weed_pen, 12)

shungite = go.Item("Shungite", "I think he's jail or something..", 1000, 2, shungite_detais)
game.player.inv.add_item(shungite, 10)

shotgun = go.Item("12GA Shotgun", "The classic pump.", 300, 9, shotgun_details)
game.player.inv.add_item(shotgun, 1)

# Show the splash Screen - its .show has 3 sec wait built in
game.splash_screen.show()

# Instantiate and show the main menu
game.main_menu = screen.MainMenu()
game.main_menu.show()
selection = game.main_menu.listen()  # Stay here and listen until a valid key press

# If New game selected, show main window and jump into MAIN GAME LOOP
if selection == "1":
    game.active_game_window.load_map(parking_lot_lvl)
    # START LOOP
    while True:
        # Begin listening on active game window
        key_pressed = game.active_game_window.listen()  # Get back what key was pressed on this menu

        # If Character Pauses with "esc"
        if key_pressed == "esc":
            # Log it, Transition, Instantiate, Display, Listen
            logger.debug("User pressed 'esc'")
            Utils.transition()
            game.pause_menu_window = screen.PauseDisplay()
            game.pause_menu_window.show()
            key_pressed = game.pause_menu_window.listen()

            # In Pause Menu
            if key_pressed == "1":  # Resume Game
                game.active_game_window.show()
            elif key_pressed == "2":  # Options
                game.options_window = screen.OptionsDisplay()
                game.options_window.show()
                key_pressed = game.options_window.listen()

                # In Options Menu
                if key_pressed == "1":
                    game.height_options = screen.HeightOptions()
                    game.height_options.show()
                    results = game.height_options.listen()

                    if key_pressed == "1":
                        Settings.console_height = 50
                        game.active_game_window.show()
                    elif key_pressed == "2":
                        Settings.console_height = 55
                        game.active_game_window.show()
                    elif key_pressed == "3":
                        Settings.console_height = 60
                        game.active_game_window.show()
                    elif key_pressed == "4":
                        Settings.console_height = 65
                        game.active_game_window.show()

            # In Main Menu
            elif key_pressed == "4":
                game.active_game_window.show()

            # In MainGame Window, Clicked I for inventory
        elif key_pressed == "i":
            game.inv_window = screen.InventoryDisplay(game.player.inv.get_inv_table())
            game.inv_window.show()
            while True:
                key_pressed = game.inv_window.listen()

                if key_pressed == "esc":
                    game.active_game_window.show()  # TODO Make this quit script
                    break
                #  Player presses up arrow in inventory
                if key_pressed == "up":
                    game.player.inv.move_selection("up")
                    game.inv_window.redraw_inv(game.player.inv.get_inv_table())
                #  Player presses down arrow in inventory
                if key_pressed == "down":
                    game.player.inv.move_selection("down")
                    game.inv_window.redraw_inv(game.player.inv.get_inv_table())
                #  Player selects an item
                if key_pressed == "enter":
                    game.player.inv.select_item()
                    game.item_popup_screen = screen.ItemOptions()
                    game.item_popup_screen.show()
                    key_pressed = game.item_popup_screen.listen


        # IN Main Game Window
        elif key_pressed == "m":
            game.world_map_window = screen.WorldMapDisplay()
            game.world_map_window.show()
            key_pressed = game.world_map_window.listen()
            if key_pressed == "l":
                game.local_map_window = screen.LocalMapDisplay()
                game.local_map_window.show()
                key_pressed = game.local_map_window.listen()
                if key_pressed == "m":
                    game.world_map_window.show()

            elif key_pressed in ["esc", "m"]:
                game.active_game_window.show()

        elif key_pressed == "c":  # Character Menu selected
            game.character_window = screen.CharacterStatus()
            game.character_window.show()
            key_pressed = game.character_window.listen()
            if key_pressed == "c":  # Return to game
                game.active_game_window.show()

        else:
            continue

# while True:
#     key_pressed = game.active_game_window.listen()
#     if key_pressed == "1":
#         # Main game window is drawn on instantiated on GameMem init
#         # Then we listen for the returned key, this won't return until
#         # a key match is pressed
#         # game.main_game_window.show()
#         game.active_game_window.load_map(go.Levels.NH1)
#         key_pressed = game.active_game_window.listen()
#         logger.info("Listening for input on main window")
