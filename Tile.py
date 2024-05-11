from settings import *


class Tile:
    def __init__(self, x, y, w, h, color, fill=True, collider=False, sprites=None):
        self.pos = pygame.math.Vector2(x, y)
        self.size = pygame.math.Vector2(w, h)
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.color = color
        self.fill = fill
        self.collider = collider
        self.sprites = sprites
        self.use_img = bool(sprites)
        self.frame = 0
        self.timer = 0

    def show(self, direction=0, moving=0, time=0):
        if not self.use_img:
            pygame.draw.rect(screen, self.color, self.rect, 1 if self.fill else 0)
        else:
            # pygame.draw.rect(screen, self.color, self.rect, 1 if self.fill else 0)

            if self.frame == 1 and direction in [0, 2] and moving == 0:
                screen.blit(self.sprites[moving][direction][self.frame], (self.pos.x, self.pos.y+3*scale))
            elif direction == 3:
                if moving == 1 and self.frame == 0:
                    screen.blit(self.sprites[moving][direction][self.frame], (self.pos.x, self.pos.y+5*scale))
                else:
                    screen.blit(self.sprites[moving][direction][self.frame], (self.pos.x, self.pos.y+3*scale))
            elif moving == 1 and direction in [0, 2]:
                if self.frame == 0:
                    screen.blit(self.sprites[moving][direction][self.frame], (self.pos.x + (4 if direction == 2 else 0), self.pos.y + 3 * scale))
                else:
                    screen.blit(self.sprites[moving][direction][self.frame], (self.pos.x, self.pos.y + 1 * scale))
            elif moving == 1 and direction == 1:
                if self.frame == 1:
                    screen.blit(self.sprites[moving][direction][self.frame], (self.pos.x, self.pos.y - 2 * scale))
                else:
                    screen.blit(self.sprites[moving][direction][self.frame], (self.pos.x, self.pos.y + 1 * scale))
                screen.blit(self.sprites[moving][direction][self.frame], (self.pos.x, self.pos.y + 1000 * scale))

            else:
                screen.blit(self.sprites[moving][direction][self.frame], self.pos)
            self.timer += time
            if self.timer > 300:
                self.frame = (self.frame + 1) % len(self.sprites[moving][direction])
                self.timer = 0

    def collide(self, other):
        return self.collider and other.collider and self.rect.colliderect(other.rect)