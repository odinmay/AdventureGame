from shutil import get_terminal_size
from time import sleep
import logging
import os
from typing import Tuple
from rich.panel import Panel
from rich.align import Align
from rich.table import Table
from rich.console import Console
from rich.layout import Layout
from art import text2art
from settings import Settings
import keyboard
from utils import Utils, Const
import game_objects

# Set up the logger
logger = logging.getLogger(__name__)

test_art = (r'''
#####################|
####################/
###################|       ___________
##################/_______/```````````\______________
#############___/`````````````````````````````"""""""|
############/  ``````````````````````""""""""""""""" |
############|```````````````"""""""""""""""""""   __/
###########_/\_____```````"""""""________________/
##########/       \____________/
#######/
##/

                                   
            ~
   ~  ~   ~                   ~         ~
 ~      ~                         ~

__
``\__       ~   ~               ##    
`````|       ~                 #####  
"___/           ~              #### # #
                                 #####
                                #  ###
                                  ##  #
                                    ## #
                                      #
                                       #
                                      _||
                 ,                 ._/  /---+-\_
               #=\  #             /#_,/~~~     |\.
          ,___    \/ /#          /   /_ __ __ /#'|
            # \__#/ /___#       /      |   __   __\
              /  \\/# \*`      / [][ ] |  /  | |  ##
              ` /==|\          |       | T__ | \._/|
               #  /|*\        =L  _ _ _|__  \_     |
                  |*| `       /_______/|  `,__./==\|
                  |#|        ||=======||\___ __._ _|
________    _____/##|________||=======|| \  `  _`   \
 |/|=|=|=* #=|/|/###\|*|=|==|||=======|| |    | |    |
      .                           `                   
   "        `       ,     "            `   "        ' 
                                '                '    ''')


class Screen:
    def __init__(self):
        self.con = Console(style="yellow on black")
        self.layout = Layout()
        self.con.height = Settings.console_height
        self.twidth = get_terminal_size()[0]
        self.theight = get_terminal_size()[1]
        logger.info(f"{self.__class__.__name__} initialized")

    def show(self):
        Utils.transition()
        # Set to current height in settings
        self.con.height = Settings.console_height
        logger.info(f'Drawing {self.__class__.__name__}')
        self.con.print(self.layout)

    def resize_if_needed(self):
        current_x, current_y = get_terminal_size()
        if (current_x, current_y) != (self.twidth, self.theight):
            os.system(Settings.clear_cmd)
            self.con.print(self.layout)


class MenuWindow(Screen):
    def __init__(self, opt1: str, opt2: str, opt3: str, opt4: str):
        super(MenuWindow, self).__init__()
        self.opt1 = Panel(
            Align(text2art(f"1.  {opt1}", font=Settings.font), align="center", vertical="middle"))
        self.opt2 = Panel(
            Align(text2art(f"2.  {opt2}", font=Settings.font), align="center", vertical="middle"))
        self.opt3 = Panel(
            Align(text2art(f"3.  {opt3}", font=Settings.font), align="center", vertical="middle"))
        self.opt4 = Panel(
            Align(text2art(f"4.  {opt4}", font=Settings.font), align="center", vertical="middle"))

        self.layout.split_row(
            Layout(Const.sidebar, ratio=1),
            Layout(name="Center", ratio=2),
            Layout(Const.sidebar, ratio=1)
        )
        self.layout["Center"].split_column(
            Layout(self.opt1),
            Layout(self.opt2),
            Layout(self.opt3),
            Layout(self.opt4)
        )

    def listen(self) -> str:
        logger.info(f"{self.__class__.__name__} Listening for user input")

        # Listen for user input and if it matches a key, return it
        while True:
            # Resize window
            self.resize_if_needed()

            # Wait for keyboard input
            key = keyboard.read_key(suppress=True)

            usable_keys = ["esc", "1", "2", "3", "4"]
            if key in usable_keys:
                logger.debug(f"User pressed {key}")
                return key


class PauseDisplay(MenuWindow):
    def __init__(self):
        super(PauseDisplay, self).__init__("Resume", "Options", "Stats", "Quit Game")


class OptionsDisplay(MenuWindow):
    def __init__(self):
        super(OptionsDisplay, self).__init__("Height", "Font", "Color",
                                             "Back")  # Pass in menu options any MenuWindow subclass


class HeightOptions(MenuWindow):
    def __init__(self):
        super(HeightOptions, self).__init__("50", "55", "60",
                                            "65")  # Pass in menu options any MenuWindow subclass


class ItemOptions(MenuWindow):
    def __init__(self):
        super(ItemOptions, self).__init__("Use Item", "Drop Item", "Item Info", "Back")


class ActiveGameDisplay(Screen):
    hud = f"""
       Cover: 60                                           Actions: O O O
       Health: 100                                         Movement: 2
       Ammo: 6/28                                          Enemies Visible: 2
       Armor: 23                                           Concealed: Y
       Inventory: 'I'  |  Character: 'I'  |  Help: 'H'  |  Line of Sight: 'S'
       """

    game_map = ""

    def __init__(self):
        super(ActiveGameDisplay, self).__init__()

        # Split to three rows
        self.layout.split_row(
            Layout(Const.sidebar, ratio=1),
            Layout(name="Center", ratio=2),
            Layout(Const.sidebar, ratio=1)
        )
        # Split the center into 2. GameMap on top and HUD on the bottom
        self.layout["Center"].split_column(
            Layout(Panel(Align(
                ActiveGameDisplay.game_map, align="center", vertical="top"),
                title_align="center", title=f"4th St. Library", padding=2), name="MAP", ratio=2),
            Layout(Panel(ActiveGameDisplay.hud, title=f"Buster Scruggs: Level 12",
                         title_align="center"), name="HUD",
                   size=8)
        )

    def listen(self) -> str:
        logger.info(f"{self.__class__.__name__}lassname Listening for user input")

        # Listen for user input and if it matches a key, return it
        while True:
            # Resize window
            self.resize_if_needed()

            # Wait for keyboard input
            key = keyboard.read_key(suppress=True)

            usable_keys = ["esc", "1", "2", "3", "4", "i", "m", "c"]
            if key in usable_keys:
                logger.debug(f"User pressed {key}")
                return key

    def load_map(self, level):
        """Loads map intro file, sleeps, then loads the actual map file"""
        self.layout["MAP"].update(
            Panel(Align(level.intro_view, align="center", vertical="middle"), title_align="center",
                  title=f"{level.name}",
                  padding=2))
        self.show()
        sleep(5)
        self.layout["MAP"].update(
            Panel(Align(level.level_view, align="center", vertical="middle"), title_align="center",
                  title=f"{level.name}", padding=2))
        self.show()


class InventoryDisplay(Screen):
    def __init__(self, table_data: Tuple[Table, list]):  #  TODO Type hint tuple
        super(InventoryDisplay, self).__init__()
        for item_row in table_data[1]:
            if "-->" in item_row:
                item_panel = Panel(item_row[-1], padding=1)

        self.layout.split_row(
            Layout(item_panel, ratio=1),
            Layout(
                Panel(table_data[0], title_align="center", title=f"Inventory", expand=True, padding=1),
                name="INV", ratio=2),
            Layout(Const.sidebar, ratio=1)
        )

    def redraw_inv(self, table_data: Tuple[Table, list]):
        for item_row in table_data[1]:
            if "-->" in item_row:
                item_panel = Panel(item_row[-1], padding=1)

        logger.info("Redrawing inventory table")
        self.layout.split_row(
            Layout(item_panel, ratio=1),
            Layout(Panel(table_data[0], title_align="center", title=f"Inventory", expand=True, padding=1),
                   name="INV", ratio=2),
            Layout(Const.sidebar, ratio=1)
        )
        self.show()

    def listen(self) -> str:
        logger.info(f"{self.__class__.__name__} Listening for user input")

        # Listen for user input and if it matches a key, return it
        while True:
            # Resize window
            self.resize_if_needed()

            # Wait for keyboard input
            key = keyboard.read_key(suppress=True)

            usable_keys = ["esc", "1", "2", "3", "4", "i", "up", "down", "enter"]
            if key in usable_keys:
                logger.debug(f"User pressed {key}")
                return key


class WorldMapDisplay(Screen):
    """Add map: GameMap obj to init"""

    def __init__(self):
        super(WorldMapDisplay, self).__init__()

        self.layout.split_row(
            Layout(
                Panel(
                    Align(f"[white]{text2art('World GameMap', font='big')}[/white]", align="center",
                          vertical="middle")),
                ratio=4),
            Layout(Panel(Align(f"[white]{text2art('LOC', font='big')}[/white]", align="center")),
                   ratio=1)
        )

    def listen(self) -> str:
        logger.info(f"{self.__class__.__name__} Listening for user input")

        # Listen for user input and if it matches a key, return it
        while True:
            # Resize window
            self.resize_if_needed()

            # Wait for keyboard input
            key = keyboard.read_key(suppress=True)

            usable_keys = ["esc", "m", "l"]
            if key in usable_keys:
                logger.debug(f"User pressed {key}")
                return key


class LocalMapDisplay(Screen):
    def __init__(self):
        super(LocalMapDisplay, self).__init__()

        self.layout.split_row(
            Layout(Panel(
                Align(f"[white]{text2art('Local Area GameMap', font='big')}[/white]",
                      align="center",
                      vertical="middle")),
                ratio=4),
            Layout(Panel(Align(f"[white]{text2art('LOC', font='big')}[/white]", align="center")),
                   ratio=1)
        )

    def listen(self) -> str:
        logger.info(f"{self.__class__.__name__} Listening for user input")

        # Listen for user input and if it matches a key, return it
        while True:
            # Resize window
            self.resize_if_needed()

            # Wait for keyboard input
            key = keyboard.read_key(suppress=True)

            usable_keys = ["esc", "m", "l"]
            if key in usable_keys:
                logger.debug(f"User pressed {key}")
                return key


class CharacterStatus(Screen):
    def __init__(self):
        super(CharacterStatus, self).__init__()

        self.layout.split_column(
            Layout(Panel("Top"), ratio=1, name="Top"),
            Layout(Panel("Character Status/Level info"), ratio=4, name="Bottom")
        )

        self.layout["Top"].split_row(
            Layout(
                Panel(Align(f"[white]{text2art('Loadout', font='big')}[/white]", align="center")),
                ratio=1,
                name="TopLeft"),
            Layout(Panel(Align(f"[white]{text2art('Status', font='big')}[/white]", align="center")),
                   ratio=1,
                   name="TopRight"),
        )

        self.layout["Bottom"].split_row(
            Layout(Panel("Left"), ratio=1, name="Left"),
            Layout(Panel("Right"), ratio=1, name="Right")
        )

        self.layout["Left"].split_row(
            Layout(Panel("Player Picture Here"), ratio=1),
            Layout(Panel("Equipment"), ratio=1)
        )

        self.layout["Right"].split_row(
            Layout(Panel("Health\nStam\nStr\nDex"), ratio=1),
            Layout(Panel("Budds/Debuffs"), ratio=1)
        )

    def listen(self) -> str:
        logger.info(f"{self.__class__.__name__} Listening for user input")

        # Listen for user input and if it matches a key, return it
        while True:
            # Resize window
            self.resize_if_needed()

            # Wait for keyboard input
            key = keyboard.read_key(suppress=True)

            usable_keys = ["esc", "c"]
            if key in usable_keys:
                logger.debug(f"User pressed {key}")
                return key


class SplashScreen(Screen):
    def __init__(self):
        super(SplashScreen, self).__init__()

        self.layout.split_column(
            Layout(Panel(
                Align(text2art("*=*      Wasted   Lands      *=*", font="big"), align="center")),
                ratio=1, name="Top"),
            Layout(Panel(Align(text2art(
                f"Produced     by     Aldo\nCreated     by     Odin\nPublished     by     GWA",
                font='big'), align="center")), ratio=4, name="Bottom")
        )

    def show(self):
        Utils.transition()
        logger.info(f"Drawing {self.__class__.__name__}")
        self.con.print(self.layout)
        sleep(3)
        return


class MainMenu(Screen):
    def __init__(self):
        super(MainMenu, self).__init__()

        self.layout.split_row(
            Layout(Panel(test_art), ratio=1),
            Layout(Panel(""), name="Middle", ratio=2),
            Layout(Panel(test_art), ratio=1)
        )

        self.layout["Middle"].split_column(
            Layout(Panel(Align(text2art("Wasted    Lands", font="big"), align="center")), ratio=1,
                   name="Top"),
            Layout(Panel(""), ratio=4, name="Bottom")
        )

        self.layout["Bottom"].split_column(
            Layout(Panel(Align(text2art("New Game", font="big"), align="center"))),
            Layout(Panel(Align(text2art("Load Game", font="big"), align="center"))),
            Layout(Panel(Align(text2art("Options", font="big"), align="center"))),
            Layout(Panel(Align(text2art("Quit Game", font="big"), align="center")))
        )

    def listen(self) -> str:
        logger.info(f"{self.__class__.__name__} Listening for user input")

        # Listen for user input and if it matches a key, return it
        while True:
            # Resize window
            self.resize_if_needed()

            # Wait for keyboard input
            key = keyboard.read_key(suppress=True)

            usable_keys = ["esc", "1", "2", "3", "4"]
            if key in usable_keys:
                logger.debug(f"User pressed {key}")
                return key
