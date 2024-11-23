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

    @staticmethod
    def check_collision(bb1, bb2):
        # 충돌 여부를 확인하는 함수
        left1, bottom1, right1, top1 = bb1
        left2, bottom2, right2, top2 = bb2
        return not (right1 < left2 or left1 > right2 or top1 < bottom2 or bottom1 > top2)

    def count_coins_in_area(self):
        # 현재 충돌 범위에 있는 모든 Coin 객체를 반환
        coins = game_world.find_objects(Coin)
        my_bb = self.get_bb()
        coins_in_area = []

        for coin in coins:
            coin_bb = coin.get_bb()
            if self.check_collision(my_bb, coin_bb):
                coins_in_area.append(coin)

        return coins_in_area

    def handle_collision(self, group, other):
        if group == 'king:kingdom':
            if self.kingdom_level == 0 and not self.coin_spawned:
                self.coin = Coin(1600, 500, other, 0.5)
                game_world.add_object(self.coin, 1)
                self.coin_spawned = True
        else:
            self.coin_spawned = False


    def update(self):
        # 충돌 영역 내 코인 리스트 가져오기
        coins_in_area = self.count_coins_in_area()

        if len(coins_in_area) == 1 and self.kingdom_level == 0:
            self.kingdom_level += 1
            # 충돌 영역 내 코인을 모두 삭제
            for coin in coins_in_area:
                game_world.remove_object(coin)

        print(f'Coins in area: {len(coins_in_area)}')

        if self.coin_spawned and self.coin is not None:
            game_world.remove_object(self.coin)  # 게임 월드에서 코인 제거
            self.coin = None  # 참조 제거
            self.coin_spawned = False
        pass