from pico2d import load_image


class Treeline:
    image = None

    def __init__(self, king):
        if Treeline.image ==None:
            Treeline.image = load_image('treeline.png')
        self.x, self.y = 2750, 368
        self.king = king
        pass

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x - self.king.camera_x, self.y, 192, 320)
        pass