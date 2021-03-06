"""Object definitions for the game"""
import logging
from typing import Tuple
from rich.table import Table
from rich.box import ASCII
from utils import Utils
import level as mf

logger = logging.getLogger(__name__)


class Game:
    """Game Class, may be deprecated by using game mem obj,
    I may split up gamemem object to further divide and silo objects"""
    def __init__(self):
        self.players_turn = True
        self.level_grid = None


class Actor:
    """Actors such as (Player, Enemy, Creature, vehicle)"""
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
    """Item object parent class with basic attrs"""
    def __init__(self, name, description, value, weight, info_panel):
        self.name = name
        self.description = description
        self.weight = weight
        self.value = value
        self.info_panel = info_panel
        # self.is_equipped = False use in a subclass object


class Attributes:
    """Player attribute container"""
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

    def increase_stat(self, stat: str, amount: int) -> None:
        """
        Increases the player stat by the desired amount

        :param stat: the stat to increase
        :param amount: amount to increase stat by
        :type stat: str
        :type amount: int
        :return: None
        """
        self.stats[stat] += amount

    def decrease_stat(self, stat: str, amount: int) -> None:
        """Decreases user stat unless it would go negative in which case it sets to 0"""
        if (self.stats[stat] - amount) < 0:
            self.stats[stat] = 0
        else:
            self.stats[stat] -= amount


class Player(Actor):
    """Player Actor class, will handle player actions and information"""
    def __init__(self):
        super(Actor).__init__()

        self.inv = Inventory()
        self.name = "Jack Bower"
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
    """Inventory class with methods for managing inventory Table"""
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

    def get_inv_table(self) -> Tuple[Table, list]:
        # Refresh inv table them return it
        self.refresh_inv_table()
        return self.inv_table, self._inv

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
            self.inv_table.add_row(*row[:-1])

    def add_item(self, item: Item, qty: int):
        """
        Adds item to the players inventory

        :param item: Item object to be added to inventory
        :param qty: int for the amount of the item to add
        :return: None
        """
        # If there is an item in the database already
        for row in self._inv:
            if item.name in row:
                # Find item in inventory
                old_qty = int(row[3])
                old_qty += qty
                return

        #  If this is the first item in players inv
        if len(self._inv) == 0:
            self._inv.append(
                ["-->", item.name, item.description, str(qty), str(item.value), str(item.weight), item.info_panel]
            )
        #  Else add a new item row to the inv
        else:
            self._inv.append(
                ["   ", item.name, item.description, str(qty), str(item.value), str(item.weight), item.info_panel]
            )
        logger.info(f"x{qty} {item.name} added to inventory.")
        self.refresh_inv_table()

    def remove_item(self, item: Item, qty: int):
        for item_row in self._inv:
            # Find matching item
            if item.name in item_row:
                # If new qty in negatives, just set at 0
                if int(item_row[3]) - qty < 0:
                    item_row[3] = 0
                # Else perform the subtraction
                else:
                    new_qty = int(item_row[3]) - qty
                    item_row[3] = new_qty
        logger.info(f"x{qty} {item.name} removed from inventory.")

    def move_selection(self, direction: str) -> None:
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
        # indx = Utils.find_index(self._inv)
        pass
        # self._inv[indx]


class Enemy(Actor):
    """Enemy actor, which will hold AI methods"""
    pass


class GameMap:
    """Object which holds specific maps as objects"""
    def __init__(self, map_path, info_path, intro_path):
        self.name = "Default Name"
        self.lvl_view = ""  # Computed view/read from file
        self.intro_view = ""
        self.map_path = map_path
        self.info_path = info_path
        self.intro_path = intro_path

        with open(self.intro_path, "r", encoding="utf-8") as intro_file:
            self.intro_view = intro_file.read()

        with open(self.map_path, "r", encoding="utf-8") as lvl_file:
            self.lvl_view = lvl_file.read()

        map_factory = mf.Loader()
        self.level_obj_grid = map_factory.get_map_strings(
            self.map_path,
            self.info_path
        )

    def get_map_str(self):
        for x in self.level_obj_grid:
            print(x)


# class Levels:
#     """This will hold all the loaded levels"""
#     NH1 = GameMap("Neighborhood House", "./levels/NH/NH1_intro.txt", "./levels/NH/NH1_map.txt")


