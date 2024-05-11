from Tile import Tile
from settings import *

class Signal(Tile):
    def __init__(self, x, y, w, h, color, sprites):
        super().__init__(x, y, w, h, color, fill=False, sprites=sprites, frame_limit=4, timer_limit=500)
        self.signal_timer = 0
        self.recharge = False

    def show(self, time=0):
        screen.blit(self.sprites[self.frame], (self.rect.x, self.rect.y))
        self.update_anim(time)
