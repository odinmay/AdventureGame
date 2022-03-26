"""Object definitions for the game"""
import os
import keyboard
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align
from rich.prompt import Prompt,Confirm
from art import text2art
from time import sleep


class Utils:
    @staticmethod
    def transition():
        os.system('clear')
        sleep(0.25)


class Settings:
    font = "big"
    console_height = 40
    empty_str = ""
    # THEME ???


class Game:
    def __init__(self):
        self.players_turn = True
        self.current_level = "Level Object"


class Map:
    def __init__(self):
        self.layout = []
        self.map_name = "Map Name Placeholder"
        self.map_path = "Path To Map Location"
        # Item and enemy spawn locaions?


# Actors such as (Player, Enemy, Creature, vehicle)
class Actor:
    def __init__(self):
        self._position = None

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    def current_tile(self):
        """compute current tile based on position attr.
        ex. enemy.current_tile.cover_value
        """
        # Return the tile object that is in this actors position
        pass


class Item:
    def __init__(self):
        self.name = "Name Placeholder"
        self.description = "Generic Description of item"
        self.weight = 0
        self.value = 0
        # self.is_equipped = False use in a subclass object


class Attributes:
    def __init__(self):
        self.stats = {
            "aim": 0,
            "strength": 0,
            "dexterity": 0,
            "intelligence": 0,
            "charisma": 0,
            "luck": 0
        }

        self.skills = {
            "Sacred Scrounger": ("You sometimes find extra things.", False),
            "Lethal Shot": ("More likely to get critical hits with guns.", False),
        }

        self.injuries = {
            "Broken Leg": ("Your leg is broken", False),
        }

        self.buffs = {
            "Coffee": ("You are feeling alert", False),
        }

    def increase_stat(self, stat, amount):
        self.stats[stat] += amount


class Player(Actor):
    pass


class Enemy(Actor):
    pass


# Types of tiles:subclasses Door Wall Furniture Hazard Waypoint
class Tile:
    def __init__(self):
        # initialize with its position potentially
        self.name = "The Omega Tile"
        self.contents = None
        self._position = [1, 4]
        self.bullet_passthrough = True
        self.player_passthrough = True
        self.can_cover = False
        # Slippery?

    def __str__(self):
        return self.name

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position


class Wall(Tile):
    """
    This is a wall, it provides cover
    Depending on its material it may be able to be shot through,
    if the shot hits it can damage the player but won't damage them as much
    """

    def __init__(self):
        """Initialize Tile Parent Object"""
        super(Wall, self).__init__()
        self.can_cover = True
        self.player_passthrough = False
        self.material = "Wood"
        self.health = None

        # Setting Wall Health
        match self.material:
            case "Wood":
                self.health = 100
                self.bullet_passthrough = True
            case "drywall":
                self.health = 50
                self.bullet_passthrough = True
            case "Concrete":
                self.health = 300
                self.bullet_passthrough = False


#### Game Loops #####
class MainMenuLoop:
    resume = Panel(Align(text2art("1.     Resume", font=Settings.font), align="center", vertical="middle"))
    options = Panel(Align(text2art("2.     Options", font=Settings.font), align="center", vertical="middle"))
    stats = Panel(Align(text2art("3.     Stats", font=Settings.font), align="center", vertical="middle"))
    quit_game = Panel(Align(text2art("4.     Quit", font=Settings.font), align="center", vertical="middle"))
    SIDEBAR = Panel(Settings.empty_str)

    def __init__(self):
        self.running = True

        self.con = Console()
        self.con.height = 40

        self.twidth = os.get_terminal_size()[0]
        self.theight = os.get_terminal_size()[1]

        self.layout = Layout()
        self.layout.split_row(
            Layout(MainMenuLoop.SIDEBAR, ratio=1),
            Layout(name="Center", ratio=2),
            Layout(MainMenuLoop.SIDEBAR, ratio=1)
        )
        self.layout["Center"].split_column(
            Layout(MainMenuLoop.resume),
            Layout(MainMenuLoop.options),
            Layout(MainMenuLoop.stats),
            Layout(MainMenuLoop.quit_game)
        )
        self.con.print(self.layout)

    def activate(self):
        """
        When this function is called it will start the 'Game Loop' specific to the main menu
        """
        while self.running:
            current_x, current_y = os.get_terminal_size()

            if (current_x, current_y) != (self.twidth, self.theight):
                # update_screen(main_menu) Should do the below
                os.system('clear')
                self.con.print(self.layout)
                # sleep(0.2)

            # Wait for keyboard input
            key = keyboard.read_key()
            match key:
                case "esc":
                    self.running = False
                case "1":
                    self.running = False
                case "2":
                    pass
                case "3":
                    pass
                case "4":
                    pass

        """
        The layout needs updated initially and sidebars need added as well. then format text and set keybinds to it
        , creat other screens(should the be methods or their own classes?)
        """


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

    sidebar = " "

    def __init__(self):
        os.system('clear')
        self.running = True
        self.layout = Layout()
        self.con = Console()
        self.con.height = Settings.console_height

        self.twidth = os.get_terminal_size()[0]
        self.theight = os.get_terminal_size()[1]


        self.layout.split_row(
            Layout(Panel(ActiveGameDisplay.sidebar), ratio=1),
            Layout(name="Center", ratio=2),
            Layout(Panel(ActiveGameDisplay.sidebar), ratio=1)
        )
        # Split the center to a Map on top and HUD/UI on the bottom
        self.layout["Center"].split_column(
            Layout(Panel(ActiveGameDisplay.game_map, title_align="center", title=f"4th St. Library", padding=0),
                   name="MAP", ratio=2),
            Layout(Panel(ActiveGameDisplay.hud, title=f"Buster Scruggs: Level 12", title_align="center"), name="HUD",
                   size=8)
        )
        self.con.print(self.layout)

    def activate(self):
        """
        When this function is called it will start the 'Game Loop' specific to the main menu
        """
        while self.running:
            current_x, current_y = os.get_terminal_size()

            if (current_x, current_y) != (self.twidth, self.theight):
                # update_screen(main_menu) Should do the below
                os.system('clear')
                self.con.print(self.layout)
                # sleep(0.2)



            # Wait for keyboard input
            key = keyboard.read_key()

            match key:
                case "esc":
                    self.running = False
                    Utils.transition()  # Simply clears console and briefly sleeps to avoid double pressing buttons
                    mm = MainMenuLoop()
                    mm.activate()
                case "1":
                    pass
                case "2":
                    pass
                case "3":
                    pass
                case "4":
                    pass



while True:
    main = ActiveGameDisplay()
    main.activate()
