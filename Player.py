from Tile import Tile
from settings import *


class Player(Tile):
    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h, color, fill=False, collider=True, sprites=player_img, frame_limit=2,
                         timer_limit=300)
        self.control = True
        self.direction = 3
        self.moving = 1

    def show(self):
        if not self.transmit:
            if self.frame == 1 and self.direction in [0, 2] and self.moving == 0:
                screen.blit(self.sprites[self.moving][self.direction][self.frame], (self.pos.x, self.pos.y + 3 * scale))
            elif self.direction == 3:
                if self.moving == 1 and self.frame == 0:
                    screen.blit(self.sprites[self.moving][self.direction][self.frame],
                                (self.pos.x, self.pos.y + 5 * scale))
                else:
                    screen.blit(self.sprites[self.moving][self.direction][self.frame],
                                (self.pos.x, self.pos.y + 3 * scale))
            elif self.moving == 1 and self.direction in [0, 2]:
                if self.frame == 0:
                    screen.blit(self.sprites[self.moving][self.direction][self.frame],
                                (self.pos.x + (4 if self.direction == 2 else 0), self.pos.y + 3 * scale))
                else:
                    screen.blit(self.sprites[self.moving][self.direction][self.frame],
                                (self.pos.x, self.pos.y + 1 * scale))
            elif self.moving == 1 and self.direction == 1:
                if self.frame == 1:
                    screen.blit(self.sprites[self.moving][self.direction][self.frame],
                                (self.pos.x, self.pos.y - 2 * scale))
                else:
                    screen.blit(self.sprites[self.moving][self.direction][self.frame],
                                (self.pos.x, self.pos.y + 1 * scale))
                screen.blit(self.sprites[self.moving][self.direction][self.frame],
                            (self.pos.x, self.pos.y + 1000 * scale))
            else:
                screen.blit(self.sprites[self.moving][self.direction][self.frame], self.pos)
        else:
            screen.blit(self.sprites[2][self.frame], (self.pos.x, self.pos.y))
        # pygame.draw.rect(screen, self.color, self.rect, 1 if self.fill else 0)

    def update_pos(self):
        self.rect = pygame.Rect(self.pos.x + self.hit_box[0], self.pos.y + self.hit_box[1], self.size.x, self.size.y)

    def update(self, tiles, time=0):
        if self.vel.magnitude() == 0:
            future_rect = pygame.Rect(self.pos.x + self.hit_box[0] + (self.vel.x * 6),
                                      self.pos.y + self.hit_box[1] + (self.vel.y * 6),
                                      self.size.x, self.size.y)
            for tile in tiles:
                if tile.tile_type == "signal" and future_rect.x < tile.rect.x + tile.rect.width - future_rect.width and future_rect.x + future_rect.width > tile.rect.x + future_rect.width and \
                        tile.rect.y + tile.rect.height > future_rect.y + future_rect.height > tile.rect.y:
                    if not self.transmit:
                        self.transmit = True
                        tile.signal_timer = 3000

                    tile.signal_timer -= time
                    if tile.signal_timer < 0:
                        print("yayyy")

            self.update_anim(time)
            self.update_pos()
            return

        future_rect = pygame.Rect(self.pos.x + self.hit_box[0] + (self.vel.x * 6),
                                  self.pos.y + self.hit_box[1] + (self.vel.y * 6),
                                  self.size.x, self.size.y)

        move = [True, True]
        for tile in tiles:
            if future_rect.colliderect(tile.rect):
                if tile.collider:
                    print("www")
                    future_rect_x = pygame.Rect(self.pos.x + self.hit_box[0] + (self.vel.x * 6),
                                                self.pos.y + self.hit_box[1],
                                                self.size.x, self.size.y)
                    future_rect_y = pygame.Rect(self.pos.x + self.hit_box[0],
                                                self.pos.y + self.hit_box[1] + (self.vel.y * 6),
                                                self.size.x, self.size.y)

                    if future_rect_x.colliderect(tile.rect):
                        while future_rect_x.colliderect(tile.rect):
                            future_rect_x.x -= 1 if self.rect.x < tile.rect.x else -1
                        self.pos.x = future_rect_x.x - self.hit_box[0]
                        move[0] = False
                        print(tile)
                        if tile.pushable:
                            if not tile.moving:
                                tile.move(tiles, 1 if self.rect.x < tile.rect.x else -1, 0)

                    if future_rect_y.colliderect(tile.rect):
                        while future_rect_y.colliderect(tile.rect):
                            future_rect_y.y -= 1 if self.rect.y < tile.rect.y else -1
                        self.pos.y = future_rect_y.y - self.hit_box[1]
                        move[1] = False
                        if tile.pushable:
                            if not tile.moving:
                                tile.move(tiles, 0, 1 if self.rect.y < tile.rect.y else -1)
                if tile.tile_type == "signal":
                    self.transmit = False
                    self.frame = 0

            if tile.tile_type == "signal":
                if future_rect.x < tile.rect.x + tile.rect.width - future_rect.width and future_rect.x + future_rect.width > tile.rect.x + future_rect.width and \
                        future_rect.y + future_rect.height < tile.rect.y + tile.rect.height:
                    self.transmit = False
                    self.frame = 0
                if self.transmit:
                    self.transmit = False
                    self.frame = 0
                    print("NO WAY")

        if move[0]:
            self.pos.x += (self.vel.normalize() * 6).x
        if move[1]:
            self.pos.y += (self.vel.normalize() * 6).y

        self.update_anim(time)
        self.update_pos()
        # pygame.draw.rect(screen, (50, 50, 200), self.rect, 1 if self.fill else 0)

    def set_dir(self, dir_x, dir_y):
        self.vel.update(dir_x, dir_y)
