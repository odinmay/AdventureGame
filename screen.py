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

# Set up the logger
logger = logging.getLogger(__name__)

# Handles drawing and Game Loop for the Main Menu
class MainMenuDisplay:
    resume = Panel(Align(text2art("1.     Resume", font=Settings.font), align="center", vertical="middle"))
    options = Panel(Align(text2art("2.     Options", font=Settings.font), align="center", vertical="middle"))
    stats = Panel(Align(text2art("3.     Stats", font=Settings.font), align="center", vertical="middle"))
    quit_game = Panel(Align(text2art("4.     Quit", font=Settings.font), align="center", vertical="middle"))

    def __init__(self):
        self.running = True

        self.con = Console()
        self.con.height = Settings.console_height

        self.twidth = os.get_terminal_size()[0]
        self.theight = os.get_terminal_size()[1]

        self.layout = Layout()
        self.layout.split_row(
            Layout(Const.sidebar, ratio=1),
            Layout(name="Center", ratio=2),
            Layout(Const.sidebar, ratio=1)
        )
        self.layout["Center"].split_column(
            Layout(MainMenuDisplay.resume),
            Layout(MainMenuDisplay.options),
            Layout(MainMenuDisplay.stats),
            Layout(MainMenuDisplay.quit_game)
        )
        self.con.print(self.layout)

    def options_menu(self):
        opt_menu = OptionsDisplay()
        opt_menu.display()
        del opt_menu

    def display(self):
        """
        When this function is called it will start the 'Game Loop' specific to the main menu
        """
        while self.running:
            current_x, current_y = os.get_terminal_size()

            if (current_x, current_y) != (self.twidth, self.theight):
                # update_screen(main_menu) Should do the below
                os.system(Settings.clear_cmd)
                self.con.print(self.layout)
                # sleep(0.2)

            # Wait for keyboard input
            key = keyboard.read_key()
            match key:
                case "esc":
                    return
                case "1":
                    return
                case "2":
                    os.system(Settings.clear_cmd)
                    self.options_menu()
                case "3":
                    pass
                case "4":
                    pass


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
        self.twidth = os.get_terminal_size()[0]
        self.theight = os.get_terminal_size()[1]

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

    def pause(self):
        main_menu = MainMenuDisplay()
        main_menu.display()
        del main_menu

    # Activate this Screens Game Loop
    def display(self):
        """
        When this function is called it will start the 'Game Loop' specific to the main menu
        """

        while self.running:
            current_x, current_y = os.get_terminal_size()

            if (current_x, current_y) != (self.twidth, self.theight):
                # update_screen(main_menu) Should do the below
                os.system(Settings.clear_cmd)
                self.con.print(self.layout)
                # sleep(0.2)

            # Wait for keyboard input
            key = keyboard.read_key()

            match key:
                case "esc":
                    Utils.transition() # Simply clears console and briefly sleeps to avoid double pressing buttons
                    self.pause()
                    os.system(Settings.clear_cmd)
                    self.con.print(self.layout)
                case "1":
                    pass
                case "2":
                    pass
                case "3":
                    pass
                case "4":
                    pass


class OptionsDisplay:
    height_opt = Panel(Align(text2art("1.     Console Height", font=Settings.font), align="center", vertical="middle"))
    font_opt = Panel(Align(text2art("2.     Font", font=Settings.font), align="center", vertical="middle"))
    ph1 = Panel(Align(text2art("3.     Placeholder", font=Settings.font), align="center", vertical="middle"))
    back = Panel(Align(text2art("4.     Back", font=Settings.font), align="center", vertical="middle"))

    def __init__(self):
        self.running = True

        self.con = Console()
        self.con.height = Settings.console_height

        self.twidth = os.get_terminal_size()[0]
        self.theight = os.get_terminal_size()[1]

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

    def console_height_menu(self):
        height = input("Please enter a new console height:\n")
        height = int(height)
        Settings.console_height = height

    def display(self):
        """
        When this function is called it will start the 'Game Loop' specific to the main menu
        """
        while self.running:
            current_x, current_y = os.get_terminal_size()

            if (current_x, current_y) != (self.twidth, self.theight):
                # update_screen(main_menu) Should do the below
                os.system(Settings.clear_cmd)
                self.con.print(self.layout)
                # sleep(0.2)

            # Wait for keyboard input
            key = keyboard.read_key()
            match key:
                case "esc":
                    return
                case "1":
                    Utils.transition()
                    self.console_height_menu()
                    Utils.transition()
                    self.con.print(self.layout)
                    return
                case "2":
                    pass
                case "3":
                    pass
                case "4":
                    pass