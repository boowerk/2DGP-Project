from pico2d import load_image, load_font

import game_framework
import game_world
from troll import Troll


class Portal:
    image = None
    font = None

    def __init__(self, king):
        if Portal.image == None:
            Portal.image = load_image('portal.png')
        if Portal.font is None:
            Portal.font = load_font('DeterminationSansK2.ttf', 24)  # 폰트 파일과 크기 설정

        self.x, self.y = -300, 350
        self.king = king
        self.frame = 0
        self.col = 8
        self.frame_timer = 0
        self.distance = 0

        # Troll 소환을 위한 타이머
        self.spawn_timer = 0
        self.spawn_interval = 60.0  # 60초
        self.wave = 0

    def update(self):
        self.distance = abs(self.king.x - self.x)

        if self.distance <= 600:
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

        # Troll 소환 타이머 처리
        self.spawn_timer += game_framework.frame_time
        if self.spawn_timer >= self.spawn_interval:  # 60초가 지났다면
            self.wave += 1
            self.spawn_troll()  # Troll 소환
            self.spawn_timer = 0  # 타이머 리셋

    def spawn_troll(self):
        # Troll 생성 및 game_world에 추가
        for i in range(self.wave):
            new_troll = Troll(self.x + i * 50, self.king)  # 약간의 위치 차이를 주어 생성
            game_world.add_object(new_troll, 1)  # 1번 레이어에 추가 (적절한 레이어 설정 필요)
        print("Troll spawned at Portal!")

    def draw(self):
        # 남은 시간 계산 및 화면에 출력
        remaining_time = max(0, self.spawn_interval - self.spawn_timer)  # 0 이하로는 표시되지 않도록
        text = f"Next spawn in: {remaining_time:.1f}s"
        Portal.font.draw(0, 590, text, (255, 255, 255))  # 화면 중앙(400, 300)에 텍스트 표시

        self.image.clip_draw(self.frame * 294, self.col * 204, 294, 204, self.x - self.king.camera_x, self.y)
        pass