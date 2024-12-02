from pico2d import load_image, get_time

import game_world


class Arrow:
    def __init__(self, x, y, dir):
        self.x, self.y = x, y
        self.dir = dir
        self.image = load_image('arrow.png')
        self.creation_time = get_time()  # 화살 생성 시간 기록

    def update(self):
        self.x += self.dir * 10  # 화살 이동 속도 조정
        if get_time() - self.creation_time > 2.0:
            game_world.remove_object(self)

    def draw(self):
        self.image.draw(self.x, self.y)