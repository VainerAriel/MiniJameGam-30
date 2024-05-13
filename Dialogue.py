import random

import pygame

from settings import *


class Dialogue:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.display = False
        self.images = None
        self.timer = 0
        self.image = 0
        self.time_limit = 5000
        self.skip_timer = 0

    def trigger(self, images):
        self.display = True
        self.images = images
        self.image = 0
        self.timer = self.time_limit

    def show(self, time, keys, click):
        if self.display:
            if self.timer > 4500:
                screen.blit(self.images[self.image], (self.pos.x + random.randint(-3, 3), self.pos.y))
            else:
                screen.blit(self.images[self.image],
                            self.pos)
            self.timer -= time
            self.skip_timer -= time

            if self.timer < 0 or (self.skip_timer < 0 and (keys[pygame.K_SPACE] or click)):
                if self.image < len(self.images)-1:
                    self.image += 1
                    self.timer = self.time_limit
                else:
                    self.display = False
                if keys[pygame.K_SPACE] or click:
                    self.skip_timer = 500
