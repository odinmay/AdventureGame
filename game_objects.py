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
from utils import Utils


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
