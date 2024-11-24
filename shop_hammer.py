from pico2d import load_image, draw_rectangle


class Shop_hammer:
    def __init__(self, king):
        self.king = king
        self.x, self.y = 1100, 350
        self.image = load_image("shop_hammer.png")
        pass

    def draw(self):
        self.image.draw(self.x - self.king.camera_x, self.y)
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        # 충돌 박스 좌표 반환
        return self.x - self.king.camera_x - 50, self.y - 100, self.x - self.king.camera_x + 50, self.y

    def update(self):
        pass