"""Object definitions for the game"""
import logging
from rich.table import Table
from rich.box import ASCII
from utils import Utils

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
    def __init__(self, name, description, value, weight):
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
    def __init__(self):
        super(Actor).__init__()

        self.name = "PLACEHOLDER"
        self.level = 1
        self.attributes = Attributes()
        self.health = 100
        self.armor_value = 0
        self.actions = []
        self.concealed = True
        self.ammo = {
            "9mm": "0",
            ".45": "0",
            ".22": "0"
        }

    def reload(self):
        pass

    def use_consumable(self, item: Item):
        pass

    def equip_item(self, item: Item):
        pass


class Inventory:
    def __init__(self):
        # Dict for storing inv data
        self._inv = []
        # Name Description qty val(total) weight(total)
        # Setup visual inv repr Table object
        self.inv_table = Table(box=ASCII, expand=True)
        self.inv_table.add_column("Active", justify="center")
        self.inv_table.add_column("Name", justify="center")
        self.inv_table.add_column("Description", justify="left")
        self.inv_table.add_column("Qty", justify="center")
        self.inv_table.add_column("Value", justify="right")
        self.inv_table.add_column("Weight", justify="right")

    def get_inv_table(self) -> Table:
        # Refresh inv table them return it
        self.refresh_inv_table()
        return self.inv_table

    def refresh_inv_table(self):
        # Recreate Table object (empty)
        del self.inv_table
        self.inv_table = Table(box=ASCII, expand=True)
        self.inv_table.add_column("Active", justify="center")
        self.inv_table.add_column("Name", justify="center")
        self.inv_table.add_column("Description", justify="left")
        self.inv_table.add_column("Qty", justify="center")
        self.inv_table.add_column("Value", justify="right")
        self.inv_table.add_column("Weight", justify="right")

        # Rebuild the table using the current self._inv data
        for row in self._inv:
            self.inv_table.add_row(*row)

    def add_item(self, item: Item, qty: int):
        # If there is an item in the database already
        for row in self._inv:
            if item.name in row:  # TODO Test to see if items with similar names effects this 'gun' and 'gun barrel'
                # Item in table already
                old_qty = int(row[3])
                old_qty += qty
                return

        #  If this is the first item in players inv
        if len(self._inv) == 0:
            self._inv.append(["-->", item.name, item.description, str(qty), str(item.value), str(item.weight)])

        else:
            self._inv.append(["   ", item.name, item.description, str(qty), str(item.value), str(item.weight)])

        self.refresh_inv_table()

    # TODO Implement item removal function
    def remove_item(self, item: Item, qty: int):
        logger.info(f"x{qty} {item.name} removed from inventory.")

    def move_selection(self, direction):
        """Handles moving the active item arrow in the Item table"""

        if direction == "up":
            #  Find which index the active item is at
            indx = Utils.find_index(self._inv)
            #  If it's the first item, move to the bottom
            if indx < 1:
                self._inv[-1][0] = "-->"
                self._inv[indx][0] = "   "
            #  Else move up one row
            else:
                self._inv[indx][0] = "   "
                self._inv[indx - 1][0] = "-->"

        elif direction == "down":
            #  Find which index the active item is at
            indx = Utils.find_index(self._inv)
            #  If it's the last item, move to the top
            if len(self._inv) - 1 == indx:
                self._inv[0][0] = "-->"
                self._inv[-1][0] = "   "
            #  Else move down one row
            else:
                self._inv[indx][0] = "   "
                self._inv[indx + 1][0] = "-->"

        # Redraw the table with the updated row data
        self.refresh_inv_table()

    def select_item(self):
        # Find active item index
        indx = Utils.find_index(self._inv)

        # self._inv[indx]


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


class Levels:
    NH1 = GameMap("Neighborhood House", "./levels/NH/NH1_intro.txt", "./levels/NH/NH1_map.txt")
