from Tile import Tile
from settings import *

class Box(Tile):
    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h, color, fill=False, collider=True)
        self.vel = pygame.math.Vector2(0, 0)
        self.pushable = False
        self.push = False

    def move(self, x, y):
        self.pos.x = x*tile_size
        self.pos.y = y*tile_size
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def set_dir(self, dirx, diry):
        self.vel.update(dirx, diry)
