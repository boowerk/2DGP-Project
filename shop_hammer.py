from pico2d import load_image


class Shop_hammer:
    def __init__(self, king):
        self.king = king
        self.image = load_image("shop_hammer.png")
        pass

    def draw(self):
        self.image.draw(1100 - self.king.camera_x, 350)
        pass

    def update(self):
        pass