from pico2d import load_image


class Portal:
    def __init__(self, x, y, king):
        self.x, self.y = x, y
        self.king = king
        self.image = load_image('portal.png')

    def update(self):
        pass

    def draw(self):
        pass