import math

from Tile import Tile
from Water import Water
from settings import *
import pygame


class Box(Tile):
    def __init__(self, x, y, w, h, color, group="", sprite=None):
        super().__init__(x, y, w, h, color, fill=False, collider=True, pushable=True, hit_box=(0, 0), group=group, sprites=sprite)
        self.moving = False
        self.leader = False

    def show(self):
        screen.blit(self.sprites[1 if (not self.collider and not self.moving) else 0], (self.rect.x, self.rect.y))

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
        group_tiles = [self]
        for tile in tiles:
            if tile.group != "" and tile.group == self.group and tile != self:
                group_tiles.append(tile)
        print(group_tiles)
        collided = False
        count_wet = 0
        water_tiles = []
        if self.collider:
            for tile in tiles:
                if tile not in group_tiles and tile.collider:
                    any_col = False
                    for g_t in group_tiles:
                        if tile.grid_pos.x == g_t.grid_pos.x + x and tile.grid_pos.y == g_t.grid_pos.y + y:
                            any_col = True
                    if any_col:
                        if type(tile) == Box:
                            if not tile.move(tiles, x, y):
                                collided = True
                        elif type(tile) == Water:
                            count_wet += 1
                            water_tiles.append(tile)
                            # self.collider = False
                            # tile.collider = False
                        else:
                            collided = True
                        print(tile.grid_pos)

            if count_wet == len(group_tiles):
                print("aaa")
                for i in range(len(group_tiles)):
                    group_tiles[i].collider = False
                    water_tiles[i].collider = False
            if not collided:
                for g_t in group_tiles:
                    g_t.grid_pos.update(g_t.grid_pos.x + x, g_t.grid_pos.y + y)
                    g_t.moving = True
                return True
            return False
