from Tile import Tile
from settings import *

class Wall(Tile):
    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h, color, fill=False, collider=True)
