from pico2d import load_image

import game_framework


class Poor:
    def __init__(self):
        self.x, self.y = 400, 356
        self.frame = 0
        self.frame_timer = 0
        self.run_image = load_image('npc_run_sprite.png')
        self.wait_image = load_image('npc_wait_sprite.png')
        self.walk_image = load_image('npc_walk_sprite.png')

    def draw(self):
        self.wait_image.clip_draw(self.frame * 128, 128, 128, 128, self.x, self.y, 100, 100)
        pass

    def update(self):
        self.frame_timer += game_framework.frame_time
        if self.frame_timer >= 0.2:  # 프레임 간격을 0.1초로 설정 (필요에 따라 조정 가능)
            self.frame = (self.frame + 6) % 36
            self.frame_timer = 0.0  # 타이머 리셋
        pass