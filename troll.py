import random

from pico2d import load_image, get_time

import game_framework
import game_world
import shop_hammer
from coin import Coin
from game_world import remove_object
from state_machine import StateMachine, time_out, random_event, find_coin_event, miss_event

# troll Run Speed
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Idle:
    @staticmethod
    def enter(troll, e):
        troll.dir = 0    # 정지상태
        troll.frame = 3

        troll.start_time = get_time()
        pass

    @staticmethod
    def exit(troll, e):
        pass

    @staticmethod
    def do(troll):
        if get_time() - troll.start_time > 3:
            troll.state_machine.add_event(('TIME_OUT', 0))

        if random.random() < 0.01:
            troll.state_machine.add_event(('RANDOM', 0))
        pass

    @staticmethod
    def draw(troll):
        adjusted_x = troll.king.get_camera_x()
        if troll.last_dir == 1:  # 마지막 방향이 오른쪽일 때
            troll.wait_image.clip_draw(troll.frame * 128, 128, 128, 128, troll.x - adjusted_x, troll.y, 100, 100)
        elif troll.last_dir == -1:  # 마지막 방향이 왼쪽일 때
            troll.wait_image.clip_composite_draw(troll.frame * 128, 128, 128, 128, 0, 'h', troll.x - adjusted_x, troll.y, 100, 100)
        pass

class Wait:
    @staticmethod
    def enter(troll, e):
        troll.frame = 3
        troll.frame_col = 1
        troll.once = False

        troll.last_dir = troll.dir
        pass

    @staticmethod
    def exit(troll, e):
        pass

    @staticmethod
    def do(troll):
        troll.frame_timer += game_framework.frame_time
        if troll.frame_timer >= 0.3 and troll.once == False:  # 프레임 간격을 0.1초로 설정 (필요에 따라 조정 가능)
            troll.frame = (troll.frame + 6) % 36
            troll.frame_timer = 0.0  # 타이머 리셋

            if troll.frame == 33:
                troll.frame_col = 0
                troll.frame = 3
                troll.once = True

        elif troll.frame_timer >= 0.3 and troll.once == True:
            troll.frame = (troll.frame + 6) % 18
            troll.frame_timer = 0.0  # 타이머 리셋

            if troll.frame == 15:
                troll.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(troll):
        adjusted_x = troll.king.get_camera_x()
        if troll.last_dir == 1:  # 마지막 방향이 오른쪽일 때
            troll.wait_image.clip_draw(troll.frame * 128, troll.frame_col * 128, 128, 128, troll.x - adjusted_x, troll.y, 100, 100)
        elif troll.last_dir == -1:  # 마지막 방향이 왼쪽일 때
            troll.wait_image.clip_composite_draw(troll.frame * 128, troll.frame_col * 128, 128, 128, 0, 'h', troll.x - adjusted_x,
                                                troll.y, 100, 100)
        pass

class Walk:
    @staticmethod
    def enter(troll, e):
        troll.dir = random.choice([-1, 1])
        troll.frame = 3
        pass

    @staticmethod
    def exit(troll, e):
        troll.last_dir = troll.dir
        pass

    @staticmethod
    def do(troll):

        troll.x += troll.dir * RUN_SPEED_PPS * game_framework.frame_time

        troll.frame_timer += game_framework.frame_time
        if troll.frame_timer >= 0.1:
            troll.frame = (troll.frame + 6) % 36
            troll.frame_timer = 0

        if troll.x < 900:  # 화면 왼쪽 경계
            troll.x = 900
            troll.dir = 1
        elif troll.x > 2100:  # 화면 오른쪽 경계
            troll.x = 2100
            troll.dir = -1

        if random.random() < 0.001:
            troll.state_machine.add_event(('RANDOM', 0))
        pass

    @staticmethod
    def draw(troll):
        adjusted_x = troll.king.get_camera_x()
        if troll.dir == 1:
            troll.walk_image.clip_draw(troll.frame * 128, 0, 128, 128, troll.x - adjusted_x, troll.y, 100, 100)
        elif troll.dir == -1:
            troll.walk_image.clip_composite_draw(troll.frame * 128, 0, 128, 128, 0, 'h',troll.x - adjusted_x, troll.y, 100, 100)
        pass

class Run:
    @staticmethod
    def enter(troll, e):
        troll.frame = 3
        pass

    @staticmethod
    def exit(troll, e):
        troll.last_dir = troll.dir
        pass

    @staticmethod
    def do(troll):
        troll.x += troll.dir * RUN_SPEED_PPS * game_framework.frame_time

        troll.frame_timer += game_framework.frame_time
        if troll.frame_timer >= 0.1:
            troll.frame = (troll.frame + 6) % 36
            troll.frame_timer = 0

        if troll.x < 900:  # 화면 왼쪽 경계
            troll.x = 900
            troll.dir = 1
        elif troll.x > 2100:  # 화면 오른쪽 경계
            troll.x = 2100
            troll.dir = -1

        if random.random() < 0.001:
            troll.state_machine.add_event(('RANDOM', 0))
        pass

    @staticmethod
    def draw(troll):
        adjusted_x = troll.king.get_camera_x()
        if troll.dir == 1:
            troll.run_image.clip_draw(troll.frame * 128, 0, 128, 128, troll.x - adjusted_x, troll.y, 100, 100)
        elif troll.dir == -1:
            troll.run_image.clip_composite_draw(troll.frame * 128, 0, 128, 128, 0, 'h', troll.x - adjusted_x, troll.y, 100,
                                                100)
        pass

class Troll:
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
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {time_out: Wait, random_event: Walk},
                Wait: {time_out: Idle},
                Walk: {random_event: Wait, find_coin_event: Run},
                Run : {}
            }
        )

    def draw(self):
        self.state_machine.draw()
        pass

    def update(self):
        self.state_machine.update()
        pass
