from pico2d import load_image, get_time, load_font, draw_rectangle
from sdl2.examples.gfxdrawing import draw_circles

import game_framework
import game_world
from coin import Coin
from state_machine import StateMachine, time_out, right_down, left_up, left_down, right_up, space_down

# King Run Speed
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Idle:
    @staticmethod
    def enter(king, e):
        king.dir = 0    # 정지상태
        king.frame = 8

        king.start_time = get_time()
        pass

    @staticmethod
    def exit(king, e):
        if space_down(e):
            king.drop_coin()
        pass

    @staticmethod
    def do(king):
        if get_time() - king.start_time > 3:
            king.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(king):
        if king.last_dir == 1:
            king.image.clip_draw(king.frame * 64, 0, 64, 64, king.x - king.camera_x, king.y, 192, 192)
        else:
            king.image.clip_composite_draw(king.frame * 64, 0, 64, 64, 0, 'h', king.x - king.camera_x, king.y, 192, 192)

        pass

class Wait:
    @staticmethod
    def enter(king, e):
        king.frame = 8
        king.frame_step = 1
        king.frame_timer = 0
        pass

    @staticmethod
    def exit(king, e):
        king.frame = 8
        king.frame_step = 1

        if space_down(e):
            king.drop_coin()
        pass

    @staticmethod
    def do(king):
        king.frame_timer += 0.01

        if king.frame_timer >= king.frame_delay:
            king.frame_timer = 0

            if king.frame == 10:
                king.frame_step = -1
            elif king.frame == 8 and king.frame_step == -1:  # 애니메이션이 끝나면 Idle 상태로 전환
                king.state_machine.add_event(('TIME_OUT', 0))

            king.frame += king.frame_step
        pass

    @staticmethod
    def draw(king):
        if king.last_dir == 1:
            king.image.clip_draw(king.frame * 64, 0, 64, 64, king.x - king.camera_x, king.y, 192, 192)
        else:
            king.image.clip_composite_draw(king.frame * 64, 0, 64, 64, 0, 'h', king.x - king.camera_x, king.y, 192, 192)
        pass

class Walk:
    @staticmethod
    def enter(king, e):
        if right_down(e) or left_up(e):
            king.dir = 1
        elif left_down(e) or right_up(e):
            king.dir = -1

        king.last_dir = king.dir
        king.frame = 0
        king.frame_step = 1
        king.frame_timer = 0
        pass

    @staticmethod
    def exit(king, e):
        king.frame = 8
        if space_down(e):
            king.drop_coin()
        pass

    @staticmethod
    def do(king):
        if king.x > 600 + king.camera_x:
            king.camera_x = king.x - 600
            king.x += king.dir * RUN_SPEED_PPS * game_framework.frame_time
        elif king.x < 250 + king.camera_x:
            king.camera_x = king.x - 250
            king.x += king.dir * RUN_SPEED_PPS * game_framework.frame_time
        else:
            king.x += king.dir * RUN_SPEED_PPS * game_framework.frame_time

        # 프레임 속도 조절
        king.frame_timer += game_framework.frame_time
        if king.frame_timer >= 0.1:  # 프레임 간격을 0.1초로 설정 (필요에 따라 조정 가능)
            king.frame = (king.frame + 1) % 8
            king.frame_timer = 0.0  # 타이머 리셋
        pass

    @staticmethod
    def draw(king):
        if king.dir == 1:
            king.image.clip_draw(king.frame * 64, 0, 64, 64, king.x - king.camera_x, king.y, 192, 192)
        elif king.dir == -1:
            king.image.clip_composite_draw(king.frame * 64, 0, 64, 64, 0, 'h', king.x - king.camera_x, king.y, 192, 192)
        pass


class King:
    def __init__(self):
        self.x, self.y = 400, 356
        self.dir = 0
        self.last_dir = 1
        self.coin_count = 100
        self.frame = 8  # 정지 상태
        self.frame_step = 1 # 프레임의 증가 또는 감소
        self.frame_delay = 2.0  # 프레임 전환 간격
        self.image = load_image('king.png')
        self.font = load_font('DeterminationSansK2.ttf', 16)
        self.is_kingdom = False # 왕국에 있는가?
        self.camera_x = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Walk, left_down: Walk, left_up: Walk, right_up: Walk, time_out: Wait, space_down: Idle},
                Walk: {right_down: Idle, left_down: Idle, left_up: Idle, right_up: Idle, space_down: Walk},
                Wait: {right_down: Walk, left_down: Walk, left_up: Walk, right_up: Walk, time_out: Idle, space_down: Idle}
            }
        )

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x - self.camera_x, self.y + 50, f'{self.x}', (255, 255, 0))
        draw_rectangle(*self.get_bb())
        pass

    def update(self):
        self.state_machine.update()
        # print(f'king.x = {self.x}')
        pass

    def drop_coin(self):
        if self.coin_count > 0:
            self.coin_count -= 1
            coin = Coin(self.x, self.y - 80, self)
            game_world.add_object(coin, 1)

    def handle_event(self, event):
        self.state_machine.add_event(
            ('INPUT', event)
        )

    def get_camera_x(self):
        return self.camera_x

    def get_bb (self):
        return self.x - self.camera_x - 50, self.y - 80, self.x - self.camera_x + 50, self.y

    def handle_collision(self, group, other):
        if group == 'king:kingdom':
            pass
        elif group == 'king:shop_hammer':
            pass
        elif group == 'King:bow':
            pass
