"""
Where the tiles are made
"""
import json
import logging
import os
from pprint import pprint
from time import sleep
import tile
from utils import Utils

logger = logging.getLogger(__name__)


class Level:
    def __init__(self):
        self.name = None
        self.level_view = None
        self.intro_view = None
        self.obj_grid = None
        self.spawn_point = None
        self.str_border = [
            [" ", " ", " ", "A", " ", "B", " ", "C", " ", "D", " ", "E", " ", "F", " ", "H", " ",
             "I", " ", "J", " ", "K", " ", "L", " ", "M", " ", "N", " ", "O", " ", "P", " ", "Q",
             " ", "R", " ", "S", " ", "T", " ", "U", " ", "V", " ", "W", " ", "X", " ", "Y", " ",
             "Z", " ", "a", " ", "b", " ", "c", "" ", d", " ", "e", " ", "f", " ", "g", " ", "h",
             " ", "i", " ", "j", " ", "k", " ", "k", " ", "l"],
            [" ", " ", "v", "_", "v", "_", "v", "_", "v", "_", "v", "_", "v", "_", "v", "_", "v",
             "_", "v", "_", "v", "_", "v", "_", "v", "_", "v", "_", "v", "_", "v", "_", "v", "_",
             "v", "_", "v", "_", "v", "_", "v", "_", "v", "_", "v", "_", "v", "_", "v", "_", "v",
             "_", "v", "_", "v", "_", "v", "_", "v", "_", "v", "_", "v", "_", "v", "_", "v", "_",
             "v", "_", "v", "_", "v", "_", "v", "_", "v", "_", "v"],
            ["01", "|"],
            ["02", "|"],
            ["03", "|"],
            ["04", "|"],
            ["05", "|"],
            ["06", "|"],
            ["07", "|"],
            ["08", "|"],
            ["09", "|"],
            ["10", "|"],
            ["11", "|"],
            ["12", "|"],
            ["13", "|"],
            ["14", "|"],
            ["15", "|"],
            ["16", "|"],
            ["17", "|"],
            ["18", "|"],
            ["19", "|"],
            ["20", "|"],
            ["21", "|"],
            ["22", "|"],
            [" ", " ", "|", "^", "_", "^", "_", "^", "_", "^", "_", "^", "_", "^", "_", "^", "_",
             "^", "_", "^", "_", "^", "_", "^", "_", "^", "_", "^", "_", "^", "_", "^", "_", "^",
             "_", "^", "_", "^", "_", "^", "_", "^", "_", "^", "_", "^", "_", "^", "_", "^", "_",
             "^", "_", "^", "_", "^", "_", "^", "_", "^", "_", "^", "_", "^", "_", "^", "_", "^",
             "_", "^", "_", "^", "_", "^", "_", "^", "_", "^", "_", "|"],
            [" ", " ", " ", "A", "B", "C", "D", "E", "F", "H", "I", "J", "K", "L", "M", "N", "O",
             "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f",
             "g", "h", "i", "j", "k", "k", "l"]
        ]
        logger.info(f"{self.__class__.__name__} has been instantiated")

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def add_border(self, obj_grid):
        """Connect the object grid str's to the _str_border list use list.extend()"""
        for line in zip(obj_grid, self.str_border[2:-2]):
            print()

    def redraw_map(self, obj):
        """Redraw the map from the obj list, obj list should already be updated"""
        pass

def get_tile(tile_name: str):
    """Gets object from a dict of objects"""
    if tile_name == " ":
        return tile.Tile()
    tiles = {
        "#": tile.Wall,
        "D": tile.Door,
        "W": tile.Window,
        "T": tile.Tree,
        "C": tile.Car,
        "B": tile.Workbench,
    }

    return tiles[tile_name]()


class Loader:  # Maybe call it Loader  <---   LevelFactory
    """Build created maps with process_map_file function"""

    def __init__(self):
        pass

    def create_level(self, name: str):
        """Checks specific sub folder and builds a Level object using its functions and returns it"""
        #  Call all build methods and set vars, Build level obj and return it
        level = Level()
        level.name = name
        level = self._build_level_view(name, level)
        level = self._build_intro_view(name, level)
        level = self._build_obj_grid(name, level)
        self._update_tile_list(name)
        return level

    def _build_level_view(self, name, lvl):
        """Creates the level view variable for the Level object"""
        with open(f"./levels/{name}/{name}_map.txt") as file:
            lvl.level_view = file.read()
            return lvl

    def _build_intro_view(self, name, lvl):
        """Creates the level intro view variable for the Level object"""
        with open(f"./levels/{name}/{name}_intro.txt") as file:
            lvl.intro_view = file.read()
            return lvl

    def _build_spawn_point(self, name):
        """Map Metadata to select spawn point"""
        metadata = Utils.read_map_metadata(f"./levels/{name}/{name}_info.txt")
        spawn = metadata['spawn_point']

    def _build_legend(self, name):
        """Use metadata to build legend string RIGHT PANE active game window"""
        metadata = Utils.read_map_metadata(f"./levels/{name}/{name}_info.txt")
        legend = metadata['legend']

    def _get_str_codes(self, name):
        map_rows = []

        with open(f"./levels/{name}/{name}_map.txt", "r",
                  encoding="utf-8") as f:
            # Read past the first two lines - they are the reference lines
            f.readline()
            f.readline()
            # read in all lines but the last, again cutting out reference lines from editor
            for line in f.readlines()[:-2]:
                # Remove start and end line boundaries from level editor
                line = line[3:-2]
                # Split it into a list and add it to map_rows
                map_rows.append(list(line))

        return map_rows

    def _build_obj_grid(self, name, lvl):
        """Builds the object row list and str list for display and returns both"""
        map_rows = self._get_str_codes(name)

        obj_list = []
        for line in map_rows:
            obj_row = []
            for tile_name in line:
                obj_row.append(get_tile(tile_name))
            obj_list.append(obj_row)

        lvl.obj_grid = obj_list
        return lvl

    def _update_tile_list(self, name):
        """Update the tile_list.txt master list with map_tiles keys"""

        # Open map_info file to gather map_tiles list
        map_info = Utils.read_map_metadata(f"./levels/{name}/{name}_info.json")

        # For ea. tile in 'map_tiles' keys, if its not in item_list.txt add it.
        for tile_name in map_info["map_tiles"].values():
            # Open tile_list.txt and read it
            f = open('tile_list.txt', "r+", encoding="utf-8")
            file_data = f.read()
            # Append to file if not already in it
            if tile_name not in file_data:
                f.write(f"{tile_name}\n")
            # Close file for cleanup
            f.close()


if __name__ == "__main__":
    lvl = Level()
    print(len(lvl.str_border))
    for line in lvl.str_border:
        # print("".join(line))
        print(line)
