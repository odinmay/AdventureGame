"""Object definitions for the game"""
import logging
from rich.table import Table

logger = logging.getLogger(__name__)


class Game:
    def __init__(self):
        self.players_turn = True
        self.current_level = "Level Object"


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
    def __init__(self, name, description, weight, value):
        self.name = name
        self.description = description
        self.weight = weight
        self.value = value
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

    def decrease_stat(self, stat, amount):
        pass


class Player(Actor):
    pass


class Inventory:
    def __init__(self):
        # Dict for storing inv data
        self._inv = {}

        # Setup visual inv repr Table object
        self.player_inv = Table(title="Items", expand=True)
        self.player_inv.add_column("Quantity", justify="center")
        self.player_inv.add_column("Name", justify="right")
        self.player_inv.add_column("Weight", justify="right")
        self.player_inv.add_column("Value", justify="right")

    def get_inv_table(self) -> Table:
        # Refresh inv table them return it
        self.refresh_inv_table()
        return self.player_inv

    def refresh_inv_table(self):
        # Recreate Table object (empty)
        self.player_inv = Table(title="Items", expand=True)
        self.player_inv.add_column("Quantity", justify="center")
        self.player_inv.add_column("Name", justify="right")
        self.player_inv.add_column("Weight", justify="right")
        self.player_inv.add_column("Value", justify="right")

        # Rebuild the table using the _inv data
        for item in self._inv.values():
            row_str = ",".join(item)
            self.player_inv.add_row(*row_str.split(','))

    def add_item(self, item: Item, qty: str):
        # If there is an item in the database already
        if self._inv.get(item.name):
            # TODO: Add error checking on this type cast. It will error eventually
            new_qty = int(self._inv[item.name][0]) + int(qty)
            self._inv[item.name][0] = str(new_qty)

        else:
            self._inv[item.name] = [qty, item.name, item.weight, item.value]

        self.refresh_inv_table()

    # TODO Implement item removal function
    def remove_item(self, item: Item, qty: int):
        logger.info(f"x{qty} {item.name} removed from inventory.")


class Enemy(Actor):
    pass


class GameMap:
    def __init__(self, name, intro_path, lvl_path):
        self.name = name
        self.lvl_view = ""  # Computed view/read from file
        self.intro_view = ""
        self.lvl_path = lvl_path
        self.intro_path = intro_path

        with open(self.intro_path, "r", encoding="utf-8") as f:
            self.intro_view = f.read()

        with open(self.lvl_path, "r", encoding="utf-8") as f:
            self.lvl_view = f.read()


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


class Levels:
    NH1 = GameMap("Neighborhood House", "./levels/NH/NH1_intro.txt", "./levels/NH/NH1_map.txt")
