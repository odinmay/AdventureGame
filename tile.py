import logging
from random import choice
from utils import Utils
import game_objects as go

logger = logging.getLogger(__name__)


# Types of tiles:subclasses Door Wall Furniture Hazard Waypoint
class Tile:
    def __init__(self):
        # initialize with its position potentially
        self.name = "generic_tile"
        self.view = " "
        self._position = None
        self.bullet_passthrough = True
        self.player_passthrough = True
        self.can_cover = False
        # Slippery?

    def __str__(self):
        return self.view

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position


class SolidTile(Tile):
    def __init__(self):
        super(SolidTile, self).__init__()

        self.player_passthrough = False
        self.bullet_passthrough = False
        self.can_cover = True


class StorageObjectTile(SolidTile):
    def __init__(self):
        super(SolidTile, self).__init__()

        self.loot_table = []
    #  TODO: def func for Random choice from loot table, maybe based on skill


class Wall(SolidTile):
    """
    This is a wall, it provides cover
    Depending on its material it may be able to be shot through,
    if the shot hits it can damage the player but won't damage them as much
    """

    def __init__(self, material="wood"):
        """Initialize Tile Parent Object"""
        super(Wall, self).__init__()
        self.name = "Wall"
        self.view = "#"
        self.material = material
        self.health = None

        # Setting Wall Health
        match self.material:
            case "wood":
                self.health = 100
                self.bullet_passthrough = True
            case "drywall":
                self.health = 50
                self.bullet_passthrough = True
            case "concrete":
                self.health = 300
                self.bullet_passthrough = False
            case "glass":
                self.health = 25
                self.bullet_passthrough = True

    # def __repr__(self):
    # return " ".join(self.__dict__.values())
    def __str__(self):
        return self.view


class Door(SolidTile):
    def __init__(self):
        super(Door, self).__init__()

        self.name = "Door"
        self.view = "D"

    def open(self):
        self.view = "d"
        print("You have opened the door")


class Car(StorageObjectTile):
    def __init__(self):
        super(Car, self).__init__()

        self.name = "Car"
        self.view = "C"
        self.loot_table = [(
            "Shotgun",
            go.Item("12GA Shotgun", "The classic pump.", 300, 9, Utils.load_art("shotgun")))]
        self.actions = {"Search Trunk": self.search_trunk}

    def search_trunk(self, player):
        item = choice(self.loot_table)
        print(f"You have found a {item[0]}")


class Tree(SolidTile):
    def __init__(self):
        super(Tree, self).__init__()

        self.name = "Tree"
        self.view = "T"

    def cut_wood(self):
        print("You are cutting wood.")


class Workbench(StorageObjectTile):
    def __init__(self):
        super(Workbench, self).__init__()

        self.name = "Workbench"
        self.loot_table = [(
            "Shotgun",
            go.Item("12GA Shotgun", "The classic pump.", 300, 9, Utils.load_art("shotgun")))]
        self.view = "B"

        self.actions = {"Search Workbench": self.search_workbench}

    def search_workbench(self, player):
        item = choice(self.loot_table)
        print(f"You have found a {item[0]}")


class Window(SolidTile):
    def __init__(self):
        super(Window, self).__init__()

        self.name = "Window"
        self.view = "W"
        self.bullet_passthrough = True
        self.can_cover = False
        self.player_passthrough = False

    @staticmethod
    def break_window(self):
        print("Player broke the window")

