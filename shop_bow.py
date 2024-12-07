from pico2d import load_image, draw_rectangle

import game_world
from coin import Coin


class Shop_bow:
    image = None
    tool_bow = None

    def __init__(self, king, kingdom):
        if Shop_bow.image == None:
            Shop_bow.image = load_image("shop_bow.png")

        if Shop_bow.tool_bow == None:
            Shop_bow.tool_bow = load_image("tools_bow.png")
        self.king = king
        self.kingdom = kingdom
        self.x, self.y = 2100, 350
        self.tool_x, self.tool_y = 2160, 280
        self.coin_spawned = False
        self.coin = None
        self.tool_count = 0

    def draw(self):
        if self.kingdom.kingdom_level > 0:
            self.image.draw(self.x - self.king.camera_x, self.y)
        for i in range(self.tool_count):
            self.tool_bow.draw(self.tool_x + i * 20 - self.king.camera_x, self.tool_y, 48, 54)
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        # 충돌 박스 좌표 반환
        return self.x - self.king.camera_x - 50, self.y - 100, self.x - self.king.camera_x + 50, self.y - 50

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

    def update(self):
        # 충돌 영역 내 코인 리스트 가져오기
        coins_in_area = self.count_coins_in_area()

        if len(coins_in_area) == 1 and not self.tool_count == 3:
            self.tool_count += 1
            # 충돌 영역 내 코인을 모두 삭제
            for coin in coins_in_area:
                game_world.remove_object(coin)

        if self.coin_spawned and self.coin is not None:
            game_world.remove_object(self.coin)
            self.coin = None  # 참조 제거
            self.coin_spawned = False
        pass

    def handle_collision(self, group, other):
        if group == 'king:bow' and not self.coin_spawned:
            self.coin = Coin(self.x, self.y, other, 0.7)
            game_world.add_object(self.coin, 1)
            self.coin_spawned = True
        else:
            self.coin_spawned = False