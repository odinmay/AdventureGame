import os
import logging
from rich.panel import Panel
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from art import text2art
from settings import Settings
import keyboard
from utils import Utils, Const
from shutil import get_terminal_size

# Set up the logger
logger = logging.getLogger(__name__)


class Screen:
    def __init__(self):
        self.con = Console()
        self.layout = Layout()
        self.con.height = Settings.console_height
        self.twidth = get_terminal_size()[0]
        self.theight = get_terminal_size()[1]
        logger.info(f"{self.__class__} initialized")

    def show(self):
        Utils.transition()
        self.con.print(self.layout)

    def resize_if_needed(self):
        current_x, current_y = get_terminal_size()
        if (current_x, current_y) != (self.twidth, self.theight):
            os.system(Settings.clear_cmd)
            self.con.print(self.layout)


class MenuWindow(Screen):
    def __init__(self, opt1, opt2, opt3, opt4):
        super(MenuWindow, self).__init__()
        self.opt1 = Panel(Align(text2art(f"1.  {opt1}", font=Settings.font), align="center", vertical="middle"))
        self.opt2 = Panel(Align(text2art(f"2.  {opt2}", font=Settings.font), align="center", vertical="middle"))
        self.opt3 = Panel(Align(text2art(f"3.  {opt3}", font=Settings.font), align="center", vertical="middle"))
        self.opt4 = Panel(Align(text2art(f"4.  {opt4}", font=Settings.font), align="center", vertical="middle"))

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
        self.show()
        logger.debug(f"{self.__class__} initialized")

    def listen(self):
        # Listen for user input and if it matches a key, return it
        while True:
            # Resize window
            self.resize_if_needed()

            # Wait for keyboard input
            key = keyboard.read_key(suppress=True)

            match key:
                case "esc":
                    return key
                case "1":
                    return key
                case "2":
                    return key
                case "3":
                    return key
                case "4":
                    return key


# Main Menu Display Class
class PauseDisplay(MenuWindow):
    def __init__(self):
        super(PauseDisplay, self).__init__("Resume", "Options", "Stats", "Quit Game")
        logger.debug(f"{self.__class__} initialized")


class OptionsDisplay(MenuWindow):
    def __init__(self):
        super(OptionsDisplay, self).__init__("Height", "Font", "Color", "Back")


class HeightOptions(MenuWindow):
    def __init__(self):
        super(HeightOptions, self).__init__("35", "40", "45", "50")


class ActiveGameDisplay(Screen):
    hud = f"""
       Cover: 60                                           Actions: O O O
       Health: 100                                         Movement: 2
       Ammo: 6/28                                          Enemies Visible: 2
       Armor: 23                                           Concealed: Y
       Inventory: 'I'  |  Character: 'I'  |  Help: 'H'  |  Line of Sight: 'S'
       """

    game_map = """
            A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R  S  T  U
        1  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
        2  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
        3  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
        4  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
        5  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
        6  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
        7  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
        8  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
        9  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
       10  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
    """

    def __init__(self):
        super(ActiveGameDisplay, self).__init__()

        # Split to three rows
        self.layout.split_row(
            Layout(Const.sidebar, ratio=1),
            Layout(name="Center", ratio=2),
            Layout(Const.sidebar, ratio=1)
        )
        # Split the center into 2. Map on top and HUD on the bottom
        self.layout["Center"].split_column(
            Layout(Panel(ActiveGameDisplay.game_map, title_align="center", title=f"4th St. Library", padding=0),
                   name="MAP", ratio=2),
            Layout(Panel(ActiveGameDisplay.hud, title=f"Buster Scruggs: Level 12", title_align="center"), name="HUD",
                   size=8)
        )
        self.show()

    def listen(self):
        # Listen for user input and if it matches a key, return it
        while True:
            # Resize window
            self.resize_if_needed()

            # Wait for keyboard input
            key = keyboard.read_key(suppress=True)

            match key:
                case "esc":
                    return key
                case "1":
                    return key
                case "2":
                    return key
                case "3":
                    return key
                case "4":
                    return key
                case "i":
                    return key


class InventoryDisplay(Screen):
    def __init__(self, inv_table):
        super(InventoryDisplay, self).__init__()

        self.layout.split_row(
            Layout(Const.sidebar, ratio=1),
            Layout(Panel(inv_table, title_align="center", title=f"Inventory", expand=True, padding=1),
                   name="INV", ratio=2),
            Layout(Const.sidebar, ratio=1)
        )

        self.show()

    def listen(self):
        # Listen for user input and if it matches a key, return it
        while True:
            # Resize window
            self.resize_if_needed()

            # Wait for keyboard input
            key = keyboard.read_key(suppress=True)

            match key:
                case "esc":
                    return key
                case "1":
                    return key
                case "2":
                    return key
                case "3":
                    return key
                case "4":
                    return key
                case "i":
                    return key
