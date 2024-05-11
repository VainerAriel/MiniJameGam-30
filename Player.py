from Tile import Tile
from settings import *


class Player(Tile):
    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h, color, fill=False, collider=True, sprites=player_img)
        self.vel = pygame.math.Vector2(0, 0)

    def move(self, axis, reverse=False, col_scale=1):
        if self.vel.magnitude() != 0:
            if axis == "x":
                self.pos.x += (self.vel.normalize() * 6 * col_scale).x * (-1 if reverse else 1)
            elif axis == "y":
                self.pos.y += (self.vel.normalize() * 6 * col_scale).y * (-1 if reverse else 1)
            self.rect = pygame.Rect(self.pos.x+2*scale, self.pos.y+20*scale, self.size.x, self.size.y)

    def set_dir(self, dirx, diry):
        self.vel.update(dirx, diry)


