from pico2d import load_image


class Portal:
    image = None

    def __init__(self, king):
        if Portal.image == None:
            Portal.image = load_image('portal.png')

        self.x, self.y = 100, 350
        self.king = king
        self.frame = 0
        self.col = 8

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.frame * 294, self.col * 204, 294, 204, self.x - self.king.camera_x, self.y)
        pass