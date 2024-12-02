import random

from pico2d import load_image, get_time

import game_framework
import game_world
from coin import Coin
from game_world import remove_object
from state_machine import StateMachine, time_out, random_event, find_coin_event, miss_event, find_tool_event

# archer Run Speed
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Idle:
    @staticmethod
    def enter(archer, e):
        archer.dir = 0    # 정지상태
        archer.frame = 4

        archer.start_time = get_time()
        pass

    @staticmethod
    def exit(archer, e):
        pass

    @staticmethod
    def do(archer):
        if get_time() - archer.start_time > 3:
            archer.state_machine.add_event(('TIME_OUT', 0))

        if random.random() < 0.01:
            archer.state_machine.add_event(('RANDOM', 0))
        pass

    @staticmethod
    def draw(archer):
        adjusted_x = archer.king.get_camera_x()
        if archer.last_dir == 1:  # 마지막 방향이 오른쪽일 때
            archer.wait_image.clip_draw(archer.frame * 128, 128, 128, 128, archer.x - adjusted_x, archer.y, 100, 100)
        elif archer.last_dir == -1:  # 마지막 방향이 왼쪽일 때
            archer.wait_image.clip_composite_draw(archer.frame * 128, 128, 128, 128, 0, 'h', archer.x - adjusted_x, archer.y, 100, 100)
        pass

class Wait:
    @staticmethod
    def enter(archer, e):
        archer.frame = 4
        archer.frame_col = 1
        archer.once = False

        archer.last_dir = archer.dir
        pass

    @staticmethod
    def exit(archer, e):
        pass

    @staticmethod
    def do(archer):
        archer.frame_timer += game_framework.frame_time
        if archer.frame_timer >= 0.3 and archer.once == False:  # 프레임 간격을 0.1초로 설정 (필요에 따라 조정 가능)
            archer.frame = (archer.frame + 6) % 36
            archer.frame_timer = 0.0  # 타이머 리셋

            if archer.frame == 34:
                archer.frame_col = 0
                archer.frame = 4
                archer.once = True

        elif archer.frame_timer >= 0.3 and archer.once == True:
            archer.frame = (archer.frame + 6) % 18
            archer.frame_timer = 0.0  # 타이머 리셋

            if archer.frame == 16:
                archer.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(archer):
        adjusted_x = archer.king.get_camera_x()
        if archer.last_dir == 1:  # 마지막 방향이 오른쪽일 때
            archer.wait_image.clip_draw(archer.frame * 128, archer.frame_col * 128, 128, 128, archer.x - adjusted_x, archer.y, 100, 100)
        elif archer.last_dir == -1:  # 마지막 방향이 왼쪽일 때
            archer.wait_image.clip_composite_draw(archer.frame * 128, archer.frame_col * 128, 128, 128, 0, 'h', archer.x - adjusted_x,
                                                archer.y, 100, 100)
        pass

class Walk:
    @staticmethod
    def enter(archer, e):
        archer.dir = random.choice([-1, 1])
        archer.frame = 4
        pass

    @staticmethod
    def exit(archer, e):
        archer.last_dir = archer.dir
        pass

    @staticmethod
    def do(archer):

        archer.x += archer.dir * RUN_SPEED_PPS * game_framework.frame_time

        archer.frame_timer += game_framework.frame_time
        if archer.frame_timer >= 0.1:
            archer.frame = (archer.frame + 6) % 36
            archer.frame_timer = 0

        if archer.x < 900:  # 화면 왼쪽 경계
            archer.x = 900
            archer.dir = 1
        elif archer.x > 2100:  # 화면 오른쪽 경계
            archer.x = 2100
            archer.dir = -1

        if random.random() < 0.001:
            archer.state_machine.add_event(('RANDOM', 0))
        pass

    @staticmethod
    def draw(archer):
        adjusted_x = archer.king.get_camera_x()
        if archer.dir == 1:
            archer.walk_image.clip_draw(archer.frame * 128, 0, 128, 128, archer.x - adjusted_x, archer.y, 100, 100)
        elif archer.dir == -1:
            archer.walk_image.clip_composite_draw(archer.frame * 128, 0, 128, 128, 0, 'h',archer.x - adjusted_x, archer.y, 100, 100)
        pass

class Run:
    @staticmethod
    def enter(archer, e):
        archer.frame = 4
        pass

    @staticmethod
    def exit(archer, e):
        archer.last_dir = archer.dir
        pass

    @staticmethod
    def do(archer):

        archer.frame_timer += game_framework.frame_time
        if archer.frame_timer >= 0.1:
            archer.frame = (archer.frame + 6) % 36
            archer.frame_timer = 0

        if random.random() < 0.001:
            archer.state_machine.add_event(('RANDOM', 0))
        pass

    @staticmethod
    def draw(archer):
        adjusted_x = archer.king.get_camera_x()
        if archer.dir == 1:
            archer.run_image.clip_draw(archer.frame * 128, 0, 128, 128, archer.x - adjusted_x, archer.y, 100, 100)
        elif archer.dir == -1:
            archer.run_image.clip_composite_draw(archer.frame * 128, 0, 128, 128, 0, 'h', archer.x - adjusted_x, archer.y, 100,
                                                100)
        pass

class Fire:
    @staticmethod
    def enter(archer):
        pass

    @staticmethod
    def exit(archer, e):
        pass

    @staticmethod
    def do(archer):
        pass

    @staticmethod
    def draw(archer):
        pass

class Archer:
    def __init__(self, x, y, king):
        self.x, self.y = x, y
        self.dir = 0
        self.last_dir = 1
        self.frame = 0
        self.frame_timer = 0
        self.king = king
        self.run_image = load_image('npc_run_sprite.png')
        self.wait_image = load_image('npc_wait_sprite.png')
        self.walk_image = load_image('npc_walk_sprite.png')
        self.arrow = load_image('arrow.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {time_out: Wait, random_event: Walk},
                Wait: {time_out: Idle},
                Walk: {random_event: Wait, find_tool_event: Run},
                Run : {}
            }
        )

    def draw(self):
        self.state_machine.draw()
        pass

    def update(self):
        self.state_machine.update()
        pass