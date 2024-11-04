from pico2d import load_image

width, height = 381, 96


class Map:
    def __init__(self, x, king):
        self.grass_tile = load_image('tiles.png')
        self.x = x
        self.king = king

    def draw(self):
        self.grass_tile.clip_draw(232, 0, 127, 32, self.x - self.king.camera_x, 225, width, height)

    def update(self):
        pass