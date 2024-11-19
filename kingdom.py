from pico2d import load_image


class Kingdom:
    def __init__(self, king):
        self.x, self.y = 1600, 297
        self.king = king
        self.kingdom_level = 0
        self.level0_kingdom = load_image("level0_base.png")
        self.level1_kingdom = load_image("level1_base.png")
        self.level2_kingdom = load_image("level2_base.png")
        self.level3_kingdom = load_image("level3_base.png")
        self.level4_kingdom = load_image("level4_base.png")
        self.level5_kingdom = load_image("level5_base.png")
        pass

    def draw(self):
        if self.kingdom_level == 0:
            self.level0_kingdom.draw(self.x - self.king.camera_x, self.y)
        pass

    def update(self):
        pass