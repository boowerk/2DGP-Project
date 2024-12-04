from pico2d import load_image, get_time, draw_rectangle

import game_world


class Arrow:
    def __init__(self, x, y, dir, king):
        self.x, self.y = x, y
        self.dir = dir
        self.king = king
        self.image = load_image('arrow.png')
        self.to_remove = False
        self.creation_time = get_time()  # 화살 생성 시간 기록

    def update(self):
        self.x += self.dir * 5  # 화살 이동 속도 조정
        if get_time() - self.creation_time > 2.0:
            game_world.remove_object(self)

        # 플래그가 설정된 경우 삭제
        if self.to_remove:
            game_world.remove_object(self)

    def get_bb(self):
        # 충돌 박스 좌표 반환
        return self.x - self.king.camera_x - 20, self.y - 8, self.x - self.king.camera_x + 20, self.y + 8

    def draw(self):
        self.image.draw(self.x - self.king.camera_x, self.y, 32, 32)
        draw_rectangle(*self.get_bb())

    def handle_collision(self, group, other):
        if group == 'troll:arrow':
            self.to_remove = True
            pass