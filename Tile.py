import math

from settings import *


class Tile:
    def __init__(self, x, y, w, h, color, fill=True, collider=False, pushable=False, sprites=None, frame_limit=2,
                 timer_limit=300, hit_box=(5 * scale, 26 * scale), group=""):
        self.grid_pos = pygame.math.Vector2(x, y)
        self.pos = pygame.math.Vector2(x * tile_size, y * tile_size)
        self.size = pygame.math.Vector2(w, h)
        self.vel = pygame.math.Vector2(0, 0)
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.color = color
        self.fill = fill
        self.collider = collider
        self.pushable = pushable
        self.sprites = sprites
        self.use_img = bool(sprites)
        self.frame = 0
        self.frame_limit = frame_limit
        self.timer = 0
        self.timer_limit = timer_limit
        self.hit_box = hit_box
        self.group = group

    def show(self):
        pygame.draw.rect(screen, self.color, self.rect, 1 if self.fill else 0)

    def update_pos(self):
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        # self.update_grid_pos()

    def update_grid_pos(self):
        if self.pushable:
            x, y = self.grid_pos
            min_dist = 1000
            new_x, new_y = x, y
            for i in range(-1, 2):
                for j in range(-1, 2):
                    middle = ((x + j + 0.5) * tile_size, (y + i + 0.5) * tile_size)
                    tile_middle = (self.pos.x + self.size.x / 2, self.pos.y + self.size.y / 2)
                    # pygame.draw.line(screen, (0, 0, 255), middle, tile_middle)
                    distance = math.dist(middle, tile_middle)
                    if distance < min_dist:
                        min_dist = distance
                        new_x, new_y = x + j, y + i

            # pygame.draw.line(screen, (0, 255, 255), ((new_x + 0.5) * tile_size, (new_y + 0.5) * tile_size),
            #                  (self.pos.x + self.size.x / 2, self.pos.y + self.size.y / 2), 10)

    def update_anim(self, time):
        self.timer += time
        if self.timer > self.timer_limit:
            self.frame = (self.frame + 1) % self.frame_limit
            self.timer = 0

    def collide(self, other):
        return self.collider and other.collider and self.rect.colliderect(other.rect)
