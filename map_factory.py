"""
Where the tiles are made
"""
import json
import os
from pprint import pprint
import game_objects as go
from utils import Utils


class MapFactory:
    """Build created maps with process_map_file function"""

    def process_map_file(self, map_path, map_info_path):
        map_rows = []

        with open(map_path, "r", encoding="utf-8") as f:
            # Read past the first two lines - they are the reference lines
            f.readline()
            f.readline()
            # read in all lines but the last, again cutting out reference lines from editor
            for line in f.readlines()[:-1]:
                # Remove start and end line boundaries from level editor
                line = line[1:-2]
                # Split it into a list and add it to map_rows
                map_rows.append(list(line))

        self._update_tile_list(map_info_path)

        return self._build_map(map_rows, map_info_path)

    def _build_map(self, map_row: list, map_info_path: str):
        """Builds the object row list and str list for display and returns both"""
        obj_list = []
        for line in map_row:
            obj_row = []
            for tile in line:
                match tile:
                    case "door":
                        obj_row.append(go.Door())
                    case "pool":
                        obj_row.append(go.Pool())
                    case "window":
                        obj_row.append(go.Window())
                    case "wall":
                        obj_row.append(go.Wall("wood"))
                    case "car":
                        obj_row.append(go.Car())
                    case " ":
                        obj_row.append(go.Tile())

    @staticmethod
    def _update_tile_list(self, map_info_path):
        """Update the tile_list.txt master list with map_tiles keys"""

        # Open map_info file to gather map_tiles list
        map_info = Utils.read_map_metadata(map_info_path)

        # For ea. tile in 'map_tiles' keys, if its not in item_list.txt add it.
        for tile in map_info["map_tiles"].values():
            # Open tile_list.txt and read it
            f = open('tile_list.txt', "r+", encoding="utf-8")
            file_data = f.read()
            # Append to file if not already in it
            if tile not in file_data:
                f.write(f"{tile}\n")
            # Close file for cleanup
            f.close()


factory = MapFactory()
factory.process_map_file("./levels/ExampleMap/example_map.txt", "./levels/ExampleMap/example_info.json")
