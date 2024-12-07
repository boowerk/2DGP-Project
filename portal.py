from pico2d import load_image

import game_framework


class Portal:
    image = None

    def __init__(self, king):
        if Portal.image == None:
            Portal.image = load_image('portal.png')

        self.x, self.y = 100, 350
        self.king = king
        self.frame = 0
        self.col = 8
        self.frame_timer = 0
        self.distance = 0

    def update(self):
        self.distance = abs(self.king.x - self.x)

        if self.distance <= 400:
            self.frame_timer += game_framework.frame_time
            if self.frame_timer >= 0.1:  # 프레임 간격을 0.1초로 설정 (필요에 따라 조정 가능)
                self.frame = (self.frame + 1) % 5
                self.frame_timer = 0.0  # 타이머 리셋
                if self.frame == 4:
                    self.frame = 0

                    if self.col == 4:
                        self.col = 6
                        self.frame = 0
                    else:
                        self.col -= 1
        else:
            self.frame = 0
            self.col = 8



        pass

    def draw(self):
        self.image.clip_draw(self.frame * 294, self.col * 204, 294, 204, self.x - self.king.camera_x, self.y)
        pass