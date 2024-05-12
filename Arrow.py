import math

from Tile import Tile
from settings import *


class Arrow(Tile):
    def __init__(self, x, y, w, h, color, tile_type="arrow", direction=0, shoot_timer_limit=1000, bullet_sprites=None):
        super().__init__(x, y, w, h, color, tile_type=tile_type, fill=False, collider=True, rotation=direction)
        self.arrows = []
        self.shoot_timer = 10000
        self.shoot_timer_limit = shoot_timer_limit
        self.bullet_sprites = bullet_sprites

    def shoot(self, time, tiles, player):
        self.shoot_timer += time
        if self.shoot_timer > self.shoot_timer_limit:
            self.shoot_timer = 0
            # 16*7
            if self.rotation % 2 == 0:
                w, h = 14 * scale*1.25, 6 * scale*1.25
                x, y = self.pos.x + tile_size / 2 - w / 2, self.pos.y + tile_size / 2 - h / 2
            else:
                w, h = 6 * scale*1.25, 14 * scale*1.25
                x, y = self.pos.x + tile_size / 2 - w / 2, self.pos.y + tile_size / 2 - h / 2

            self.arrows.append(Bullet(x, y, w, h, (255, 0, 0), self.rotation, self.bullet_sprites))

            pygame.draw.rect(screen, (255, 255, 0), (x, y, w, h))

        for i in range(len(self.arrows) - 1, -1, -1):
            bullet = self.arrows[i]
            visibile = False
            immune = False
            for tile in tiles:
                if tile.tile_type in ["wall", "box"] and not (tile.tile_type == "box" and not tile.collider):
                    # if tile.rect.x < bullet.rect.x < tile.rect.x + tile.rect.width - bullet.rect.width and tile.rect.y + tile.rect.height - bullet.rect.height > bullet.rect.y > tile.rect.y:
                    if math.dist((bullet.rect.x + bullet.rect.width / 2, bullet.rect.y + bullet.rect.height / 2), (tile.rect.x + tile.rect.width / 2, tile.rect.y + tile.rect.height / 2)) < tile_size / 4:
                        try:
                            self.arrows.remove(bullet)
                        except ValueError:
                            pass
                # if tile.tile_type == "box":
                #     if math.dist((player.rect.x + player.rect.width / 2, player.rect.y + player.rect.height / 2), (
                #     tile.rect.x + tile.rect.width / 2, tile.rect.y + tile.rect.height / 2)) < 3*tile_size:
                #         immune = True
            if player.rect.colliderect(bullet.rect) and not immune:
                player.dead = True
                self.arrows.remove(bullet)
            bullet.update()
            bullet.update_pos()
            bullet.update_anim(time)

    def show(self, time=0):
        for bullet in self.arrows:
            bullet.show(time)


class Laser(Tile):
    def __init__(self, x, y, w, h, color, tile_type="laser", direction=0):
        super().__init__(x, y, w, h, color, tile_type=tile_type, fill=False, collider=True, rotation=direction)

        self.laser_parts = []

    def setup_laser(self, tiles):
        self.laser_parts = []

        if self.rotation in [0, 2]:
            latest = None
            for tile in tiles:
                if tile.tile_type in ["wall", "box"]:
                    if tile.grid_pos.y == self.grid_pos.y:
                        if (tile.grid_pos.x < self.grid_pos.x) if not self.rotation else (
                                tile.grid_pos.x > self.grid_pos.x):
                            if latest is None:
                                latest = tile.grid_pos
                            if (tile.grid_pos.x > latest.x) if not self.rotation else (tile.grid_pos.x < latest.x):
                                latest = tile.grid_pos
            if not self.rotation:
                for i in range(int(latest.x) + 1, int(self.grid_pos.x)):
                    self.laser_parts.append((i, self.grid_pos.y))
            else:
                for i in range(int(self.grid_pos.x) + 1, int(latest.x)):
                    self.laser_parts.append((i, self.grid_pos.y))
        else:
            latest = None
            for tile in tiles:
                if tile.tile_type in ["wall", "box"]:
                    if tile.grid_pos.x == self.grid_pos.x:
                        if (tile.grid_pos.y < self.grid_pos.y) if not (self.rotation - 1) else (
                                tile.grid_pos.y > self.grid_pos.y):
                            if latest is None:
                                latest = tile.grid_pos
                            if (tile.grid_pos.y > latest.y) if not (self.rotation - 1) else (
                                    tile.grid_pos.y < latest.y):
                                latest = tile.grid_pos
            if not (self.rotation - 1):
                for i in range(int(latest.y) + 1, int(self.grid_pos.y)):
                    self.laser_parts.append((self.grid_pos.x, i))
            else:
                for i in range(int(self.grid_pos.y) + 1, int(latest.y)):
                    self.laser_parts.append((self.grid_pos.x, i))

    def show(self, time=0, player=None):
        pygame.draw.rect(screen, self.color, self.rect, 1 if self.fill else 0)
        if self.rotation == 0:
            pygame.draw.rect(screen, (0, 0, 0), (self.rect.x, self.rect.y + self.rect.height / 2 - 10, 20, 20))
        elif self.rotation == 1:
            pygame.draw.rect(screen, (0, 0, 0), (self.rect.x + self.rect.height / 2 - 10, self.rect.y, 20, 20))
        elif self.rotation == 2:
            pygame.draw.rect(screen, (0, 0, 0),
                             (self.rect.x + self.rect.width - 20, self.rect.y + self.rect.height / 2 - 10, 20, 20))
        elif self.rotation == 3:
            pygame.draw.rect(screen, (0, 0, 0),
                             (self.rect.x + self.rect.height / 2 - 10, self.rect.y + self.rect.height - 20, 20, 20))
        for laser in self.laser_parts:
            pygame.draw.rect(screen, (255, 0, 0),
                             (laser[0] * tile_size, laser[1] * tile_size, tile_size, tile_size))
            if player.rect.colliderect(pygame.Rect(laser[0] * tile_size, laser[1] * tile_size, tile_size, tile_size)):
                player.dead = True


class Bullet(Tile):
    def __init__(self, x, y, w, h, color, direction=0, sprites=None):
        super().__init__(x, y, w, h, color, tile_type="bullet", fill=False, collider=True, rotation=direction, sprites=sprites, frame_limit=3, timer_limit=200)
        self.pos = pygame.math.Vector2(x, y)
        self.update_pos()
        if self.rotation % 2 == 0:
            self.vel.x = -7*magic_pixel if not self.rotation else 7*magic_pixel
        else:
            self.vel.y = -7*magic_pixel if not (self.rotation - 1) else 7*magic_pixel

    def show(self, time=0):
        # pygame.draw.rect(screen, self.color, self.rect, 1 if self.fill else 0)
        screen.blit(self.sprites[3 if self.rotation%2==0 else 4], (self.rect.x, self.rect.y))
        screen.blit(self.sprites[self.frame], (self.rect.x, self.rect.y))

    def update(self):
        self.pos += self.vel
        return
