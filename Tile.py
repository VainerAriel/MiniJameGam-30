from settings import *


# floor, wall, water, signal

class Tile:
    def __init__(self, x, y, w, h, color, fill=True, collider=False, pushable=False, sprites=None, frame_limit=2,
                 timer_limit=300, hit_box=(0, 0), group="", transmit=False, tile_type="floor", rotation=4, value=None):
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
        self.transmit = transmit
        self.signal_timer = 0
        self.rotation = rotation
        self.open = False
        self.active = True
        self.anim = True
        self.loop = True
        self.value = value
        self.pressed = False
        if tile_type == "code block":
            self.anim = False
        if tile_type == "door":
            self.anim = False
            self.loop = False

        self.tile_type = tile_type

    def show(self, time=0):
        if self.tile_type not in ["signal", "bullet", "door", "code block", "pressure plate"]:
            pygame.draw.rect(screen, self.color, self.rect, 1 if self.fill else 0)
        elif self.tile_type == "code block":
            screen.blit(self.sprites[self.frame], (self.rect.x+tile_size/4, self.rect.y+tile_size/4))
        else:
            # pygame.draw.rect(screen, self.color, self.rect, 1 if self.fill else 0)
            screen.blit(self.sprites[self.frame], (self.rect.x, self.rect.y))

    def update_button(self, tiles):
        if self.tile_type == "pressure plate" and self.group=="leader":
            group = [self]
            for tile in tiles:
                if tile.tile_type == "pressure plate" and self!=tile:
                    group.append(tile)
            # print(group)
            count = 0
            for member in group:
                for tile in tiles:
                    if tile.tile_type=="box" and member.grid_pos == tile.grid_pos and member!=tile:
                        count += 1

            if count==4:
                for m in group:
                    m.pressed = True
            else:
                for m in group:
                    m.pressed = False

    def update_pos(self):
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def update_grid_pos(self):
        pass
        # if self.pushable:
        #     x, y = self.grid_pos
        #     min_dist = 1000
        #     new_x, new_y = x, y
        #     for i in range(-1, 2):
        #         for j in range(-1, 2):
        #             middle = ((x + j + 0.5) * tile_size, (y + i + 0.5) * tile_size)
        #             tile_middle = (self.pos.x + self.size.x / 2, self.pos.y + self.size.y / 2)
        #             # pygame.draw.line(screen, (0, 0, 255), middle, tile_middle)
        #             distance = math.dist(middle, tile_middle)
        #             if distance < min_dist:
        #                 min_dist = distance
        #                 new_x, new_y = x + j, y + i

        # pygame.draw.line(screen, (0, 255, 255), ((new_x + 0.5) * tile_size, (new_y + 0.5) * tile_size),
        #                  (self.pos.x + self.size.x / 2, self.pos.y + self.size.y / 2), 10)

    def update_anim(self, time):
        if self.anim:
            self.timer += time
            if self.timer > self.timer_limit:
                if self.loop:
                    self.frame = (self.frame + 1) % (self.frame_limit if not self.transmit else 3)
                else:
                    if self.frame < self.frame_limit:
                        self.frame += 1
                self.timer = 0
