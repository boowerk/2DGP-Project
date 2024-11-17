from pico2d import load_image

import game_framework


class Coin:
    image = None

    def __init__(self, x, y, king):
        if Coin.image == None:
            Coin.image = load_image("coin.png")
        self.x, self.y = x, y
        self.king = king
        self.frame_timer = 0
        self.frame = 0

    def draw(self):
        self.image.clip_draw(self.frame * 10, 0, 10, 10, self.x - self.king.camera_x, self.y, 20, 20)
        pass

    def update(self):
        self.frame_timer += game_framework.frame_time
        if self.frame_timer >= 0.1:  # 프레임 간격을 0.1초로 설정 (필요에 따라 조정 가능)
            self.frame = (self.frame + 1) % 8
            self.frame_timer = 0.0  # 타이머 리셋
        pass