import math

from Tile import Tile
from settings import *
import pygame


class Box(Tile):
    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h, color, fill=False, collider=True, pushable=True)
        self.moving = False

    def update_pos(self, tiles=None):
        if self.moving:
            self.pos = self.pos.lerp(self.grid_pos * tile_size, 0.075)
            if math.dist(self.pos, self.grid_pos * tile_size) < 3:
                self.pos = self.grid_pos * tile_size
                self.moving = False
            elif math.dist(self.pos, self.grid_pos * tile_size) < 5:
                self.pos = self.pos.lerp(self.grid_pos * tile_size, 0.4)
            elif math.dist(self.pos, self.grid_pos * tile_size) < 15:
                self.pos = self.pos.lerp(self.grid_pos * tile_size, 0.2)
            elif math.dist(self.pos, self.grid_pos * tile_size) < 25:
                self.pos = self.pos.lerp(self.grid_pos * tile_size, 0.1)

        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        # self.update_grid_pos()

    def move(self, tiles, x, y):
        print(x, y)
        collided = False
        for tile in tiles:
            if self != tile and tile.collider:
                if tile.grid_pos.x == self.grid_pos.x + x and tile.grid_pos.y == self.grid_pos.y + y:
                    if type(tile) == Box:
                        if not tile.move(tiles, x, y):
                            collided = True
                    else:
                        collided = True
                    print(tile.grid_pos)
        if not collided:
            self.grid_pos.update(self.grid_pos.x + x, self.grid_pos.y + y)
            self.moving = True
            return True
        return False
