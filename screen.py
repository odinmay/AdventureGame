import os
import logging
from rich.panel import Panel
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.prompt import IntPrompt
from art import text2art
from settings import Settings
import keyboard
from utils import Utils, Const
from shutil import get_terminal_size
from time import sleep

# Set up the logger
logger = logging.getLogger(__name__)


class MenuWindow:
    def __init__(self, opt1, opt2, opt3, opt4):
        self.opt1 = Panel(Align(text2art(f"1.  {opt1}", font=Settings.font), align="center", vertical="middle"))
        self.opt2 = Panel(Align(text2art(f"2.  {opt2}", font=Settings.font), align="center", vertical="middle"))
        self.opt3 = Panel(Align(text2art(f"3.  {opt3}", font=Settings.font), align="center", vertical="middle"))
        self.opt4 = Panel(Align(text2art(f"4.  {opt4}", font=Settings.font), align="center", vertical="middle"))

        self.con = Console()
        self.con.height = Settings.console_height
        self.twidth = get_terminal_size()[0]
        self.theight = get_terminal_size()[1]

        self.layout = Layout()
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

        self.con.print(self.layout)

    def show(self):
        Utils.transition()
        self.con.print(self.layout)

    def listen(self):
        """
        Listen for window resize and returns the matched key pressed as a string
        """
        while True:
            # Resize window
            current_x, current_y = get_terminal_size()
            if (current_x, current_y) != (self.twidth, self.theight):
                os.system(Settings.clear_cmd)
                self.con.print(self.layout)

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
class MainMenuDisplay(MenuWindow):
    def __init__(self):
        super(MainMenuDisplay, self).__init__("Resume", "Options", "Stats", "Quit Game")


class OptionsDisplay(MenuWindow):
    def __init__(self):
        super(OptionsDisplay, self).__init__("Height", "Font", "Color", "Credits")


class HeightOptions(MenuWindow):
    def __init__(self):
        super(HeightOptions, self).__init__("35", "40", "45", "50")

class ActiveGameDisplay:
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
        logger.info("Setting up Game Display..")
        # Set variables
        self.running = True
        self.twidth = get_terminal_size()[0]
        self.theight = get_terminal_size()[1]

        # Instantiate Layout and Console Object
        self.layout = Layout()
        self.con = Console(height=Settings.console_height)

        # Set up the layout of the screen
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

        self.con.print(self.layout)
        logger.info("Main Display successfully setup")

    def show(self):
        Utils.transition()
        self.con.print(self.layout)

    # Activate this Screens Game Loop
    def listen(self):
        """
        Listen for window resize and returns the matched key pressed as a string
        """

        while True:
            current_x, current_y = get_terminal_size()

            if (current_x, current_y) != (self.twidth, self.theight):
                # update_screen(main_menu) Should do the below
                os.system(Settings.clear_cmd)
                self.con.print(self.layout)
                # sleep(0.2)

            # Wait for keyboard input
            key = keyboard.read_key()

            match key:
                case "esc":
                    return key
                    # Utils.transition()  # Simply clears console and briefly sleeps to avoid double pressing buttons
                    # self.pause()
                    # os.system(Settings.clear_cmd)
                    # self.con.print(self.layout)
                case "1":
                    return key
                case "2":
                    return key
                case "3":
                    return key
                case "4":
                    return key


class OptionsDisplay:
    height_opt = Panel(Align(text2art("1.  Console Height", font=Settings.font), align="center", vertical="middle"))
    font_opt = Panel(Align(text2art("2.  Font", font=Settings.font), align="center", vertical="middle"))
    ph1 = Panel(Align(text2art("3.  Placeholder", font=Settings.font), align="center", vertical="middle"))
    back = Panel(Align(text2art("4.  Back", font=Settings.font), align="center", vertical="middle"))

    def __init__(self):
        self.running = True

        self.con = Console()
        self.con.height = Settings.console_height

        self.twidth = get_terminal_size()[0]
        self.theight = get_terminal_size()[1]

        self.layout = Layout()
        self.layout.split_row(
            Layout(Const.sidebar, ratio=1),
            Layout(name="Center", ratio=2),
            Layout(Const.sidebar, ratio=1)
        )
        self.layout["Center"].split_column(
            Layout(OptionsDisplay.height_opt),
            Layout(OptionsDisplay.font_opt),
            Layout(OptionsDisplay.ph1),
            Layout(OptionsDisplay.back)
        )
        self.con.print(self.layout)

    def show(self):
        Utils.transition()
        self.con.print(self.layout)

    def listen(self):
        """
        Listen for window resize and returns the matched key pressed as a string
        """
        while self.running:
            current_x, current_y = get_terminal_size()

            if (current_x, current_y) != (self.twidth, self.theight):
                # update_screen(main_menu) Should do the below
                os.system(Settings.clear_cmd)
                self.con.print(self.layout)
                # sleep(0.2)

            # Wait for keyboard input
            key = keyboard.read_key(suppress=True)

            match key:
                case "esc":
                    return
                case "1":
                    Utils.transition()
                    # Console height sub-menu
                    Utils.transition()
                    self.con.print(self.layout)
                    return
                case "2":
                    pass
                case "3":
                    pass
                case "4":
                    pass









