from Tile import Tile


class Water(Tile):
    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h, color, fill=False, collider=True)