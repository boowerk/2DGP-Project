from pico2d import load_image, draw_rectangle, load_font

import game_framework
import game_world
from coin import Coin


class Wall:
    image = None

    def __init__(self, king):
        if Wall.image == None:
            Wall.image = load_image('wall.png')

        self.frame = 0
        self.level = 0
        self.hp = self.level
        self.x, self.y = 800, 310
        self.font = load_font('DeterminationSansK2.ttf', 20)
        self.king = king
        self.coin_spawned = False
        self.coin = None
        self.attacked = False
        self.attacked_timer = 0

    def draw(self):
        self.image.clip_draw(self.frame * 32, 0, 32, 64, self.x - self.king.camera_x, self.y, 64, 128)
        self.font.draw(self.x - self.king.camera_x - 10, self.y + 80, f'HP: {self.hp}', (255, 255, 255))
        pass

    def get_bb(self):
        # 충돌 박스 좌표 반환
        return self.x - self.king.camera_x - 20, self.y - 100, self.x - self.king.camera_x + 20, self.y

    def take_damage(self, damage):
        # 공격을 받을 때 호출
        self.hp -= damage
        self.attacked = True
        if self.hp <= 0:
            self.level = 0
            self.frame = 0

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

    def is_attacked(self):
        return self.attacked

    def update(self):
        # 충돌 영역 내 코인 리스트 가져오기
        coins_in_area = self.count_coins_in_area()

        self.attacked_timer += game_framework.frame_time
        if self.attacked_timer > 10.0:
            self.attacked = False
            self.hp = self.level
            self.attacked_timer = 0

        if len(coins_in_area) == 1 and not self.level == 4:
            self.hp = self.level + 1
            self.level += 1
            self.frame += 1
            # 충돌 영역 내 코인을 모두 삭제
            for coin in coins_in_area:
                game_world.remove_object(coin)

        if self.coin_spawned and self.coin is not None:
            game_world.remove_object(self.coin)
            self.coin = None  # 참조 제거
            self.coin_spawned = False

    def handle_collision(self, group, other):
        if group == 'king:wall' and not self.coin_spawned:
            self.coin = Coin(self.x, self.y + 100, other, 0.7)
            game_world.add_object(self.coin, 1)
            self.coin_spawned = True
        else:
            self.coin_spawned = False