from pico2d import load_image


class Portal:
    image = None

    def __init__(self, x, y, king):
        if Portal.image == None:
            Portal.image = load_image('portal.png')

        self.x, self.y = x, y
        self.king = king
        self.frame = 0

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.frame * 424, 0, 424, 272, self.x - self.king.camera_x, self.y)
        pass