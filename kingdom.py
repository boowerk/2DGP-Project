from pico2d import load_image, draw_rectangle, load_wav

import game_world
import king
from coin import Coin


class Kingdom:
    upgrade_sound_1 = None
    upgrade_sound_2 = None
    upgrade_sound_3 = None
    upgrade_sound_4 = None
    upgrade_sound_5 = None

    def __init__(self, king):
        if not Kingdom.upgrade_sound_1:
            Kingdom.upgrade_sound_1 = load_wav('castle_upgrade_1.wav')
            Kingdom.upgrade_sound_1.set_volume(32)

        if not Kingdom.upgrade_sound_2:
            Kingdom.upgrade_sound_2 = load_wav('castle_upgrade_2.wav')
            Kingdom.upgrade_sound_2.set_volume(32)

        if not Kingdom.upgrade_sound_3:
            Kingdom.upgrade_sound_3 = load_wav('castle_upgrade_3lp.wav')
            Kingdom.upgrade_sound_3.set_volume(32)

        if not Kingdom.upgrade_sound_4:
            Kingdom.upgrade_sound_4 = load_wav('castle_upgrade_4.wav')
            Kingdom.upgrade_sound_4.set_volume(32)

        if not Kingdom.upgrade_sound_5:
            Kingdom.upgrade_sound_5 = load_wav('castle_upgrade_5.wav')
            Kingdom.upgrade_sound_5.set_volume(32)

        self.x, self.y = 1600, 297
        self.king = king
        self.kingdom_level = 0
        self.coin_spawned = False
        self.coin = None
        self.spawned_coins = []  # 생성된 코인을 저장할 리스트
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
        elif self.kingdom_level == 1:
            self.level1_kingdom.draw(self.x - self.king.camera_x, self.y)
        elif self.kingdom_level == 2:
            self.level2_kingdom.draw(self.x - self.king.camera_x, self.y + 60)
        elif self.kingdom_level == 3:
            self.level3_kingdom.draw(self.x - self.king.camera_x, self.y + 60)
        elif self.kingdom_level == 4:
            self.level4_kingdom.draw(self.x - self.king.camera_x, self.y + 100)
        elif self.kingdom_level == 5:
            self.level5_kingdom.draw(self.x - self.king.camera_x, self.y + 100)

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
        if group == 'king:kingdom' and not self.coin_spawned:

            # 현재 레벨에 따라 코인 위치 설정
            coin_positions = {
                0: [1600],
                1: [1600, 1650],
                2: [1550, 1600, 1650],
                3: [1550, 1600, 1650, 1700],
                4: [1500, 1550, 1600, 1650, 1700],
            }
            if self.kingdom_level in coin_positions:
                self.spawned_coins = [Coin(x, 500, other, 0.5) for x in coin_positions[self.kingdom_level]]
                for coin in self.spawned_coins:
                    game_world.add_object(coin, 1)
        else:
            self.coin_spawned = False


    def update(self):
        coins_in_area = self.count_coins_in_area()

        # 현재 레벨에서 코인 조건 충족 시 레벨 업 및 코인 제거
        if len(coins_in_area) == self.kingdom_level + 1 and not self.kingdom_level == 5:
            self.kingdom_level += 1
            for coin in coins_in_area:
                game_world.remove_object(coin)

                # 레벨 업 사운드 재생
            if self.kingdom_level == 1:
                Kingdom.upgrade_sound_1.play()
            elif self.kingdom_level == 2:
                Kingdom.upgrade_sound_2.play()
            elif self.kingdom_level == 3:
                Kingdom.upgrade_sound_3.play()
            elif self.kingdom_level == 4:
                Kingdom.upgrade_sound_4.play()
            elif self.kingdom_level == 5:
                Kingdom.upgrade_sound_5.play()

        # print(f'Coins in area: {len(coins_in_area)}')

        if self.coin_spawned and self.coin is not None:
            game_world.remove_object(self.coin)  # 게임 월드에서 코인 제거
            self.coin = None  # 참조 제거
            self.coin_spawned = False
        pass