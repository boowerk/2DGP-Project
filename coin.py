from pico2d import load_image


class Coin:
    image = None

    def __init__(self, x, y):
        if Coin.image == None:
            Coin.image = load_image("coin.png")
        self.x, self.y = x, y
        self.frame = 0
        pass

    def draw(self):
        self.image.clip_draw(self.frame * 10, 0, 10, 10, self.x, self.y)
        pass

    def update(self):
        self.frame = (self.frame + 1) % 8
        pass