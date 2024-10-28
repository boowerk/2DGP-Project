from pico2d import load_image

width, height = 254, 64

class Map:
    def __init__(self, x):
        self.grass_tile = load_image('tiles.png')
        self.x = x

    def draw(self):
        self.grass_tile.clip_draw(232, 0, 127, 32, self.x, 150, width, height)

    def update(self):
        pass