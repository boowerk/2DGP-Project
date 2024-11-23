from pico2d import load_image, draw_rectangle

import game_world
from coin import Coin


class Kingdom:
    def __init__(self, king):
        self.x, self.y = 1600, 297
        self.king = king
        self.kingdom_level = 0
        self.coin_spawned = False
        self.coin = None
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

    def count_coins_in_area(self):
        # 현재 충돌 영역 내의 코인 개수를 셈
        left, bottom, right, top = self.get_bb()
        coins = game_world.find_objects(Coin)
        count = 0

        for coin in coins:
            coin_left, coin_bottom, coin_right, coin_top = coin.get_bb()
            if coin_left < right and coin_right > left and coin_bottom < top and coin_top > bottom:
                count += 1

        return count

    def handle_collision(self, group, other):
        if group == 'king:kingdom':
            if self.kingdom_level == 0 and not self.coin_spawned:
                self.coin = Coin(1600, 500, other, 0.5)
                game_world.add_object(self.coin, 1)
                self.coin_spawned = True
        else:
            self.coin_spawned = False


    def update(self):
        # 충돌 영역 내 코인 개수를 출력
        coin_count = self.count_coins_in_area()
        print(f'Coins in area: {coin_count}')

        if self.coin_spawned and self.coin is not None:
            game_world.remove_object(self.coin)  # 게임 월드에서 코인 제거
            self.coin = None  # 참조 제거
            self.coin_spawned = False
        pass