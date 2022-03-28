import logging

logger = logging.getLogger(__name__)


# Types of tiles:subclasses Door Wall Furniture Hazard Waypoint
class Tile:
    def __init__(self):
        # initialize with its position potentially
        self.name = "generic_tile"
        self.view = "~"
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

        self.actions = {
            #"Search": self.rng_loot # Function gets called when getting value
        }

    #TODO: def func for Random choice from loot table, maybe based on skill


class Wall(Tile):
    """
    This is a wall, it provides cover
    Depending on its material it may be able to be shot through,
    if the shot hits it can damage the player but won't damage them as much
    """

    def __init__(self, material, name="unnamed wall"):
        """Initialize Tile Parent Object"""
        super(Wall, self).__init__()
        self.name = name
        self.view = "#"
        self.can_cover = True
        self.player_passthrough = False
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

        print(list(self.__dict__.values())[0])
    # def __repr__(self):
    #     return " ".join(self.__dict__.values())
