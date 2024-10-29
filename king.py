from pico2d import load_image


class King:
    def __init__(self):
        self.x, self.y = 400, 356
        self.frame = 8
        self.image = load_image('king.png')
        pass

    def draw(self):
        self.image.clip_draw(self.frame * 64, 0, 64, 64, self.x, self.y, 192, 192)
        pass

    def update(self):
        self.frame = (self.frame + 1) % 8
        pass
