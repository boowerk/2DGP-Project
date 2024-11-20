from pico2d import load_image, draw_rectangle

import game_world
from coin import Coin


class Kingdom:
    def __init__(self, king):
        self.x, self.y = 1600, 297
        self.king = king
        self.kingdom_level = 0
        self.coin_spawned = False
        self.level0_kingdom = load_image("level0_base.png")
        self.level1_kingdom = load_image("level1_base.png")
        self.level2_kingdom = load_image("level2_base.png")
        self.level3_kingdom = load_image("level3_base.png")
        self.level4_kingdom = load_image("level4_base.png")
        self.level5_kingdom = load_image("level5_base.png")
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        if self.kingdom_level == 0:
            self.level0_kingdom.draw(self.x - self.king.camera_x, self.y)
        pass

    def get_bb(self):
        return self.x - self.king.camera_x - 50, self.y - 60, self.x - self.king.camera_x + 50, self.y

    def handle_collision(self, group, other):
        if group == 'king:kingdom':
            if self.kingdom_level == 0 and not self.coin_spawned:
                coin = Coin(1600, 500, other)
                game_world.add_object(coin, 1)
                self.coin_spawned = True

    def update(self):
        pass