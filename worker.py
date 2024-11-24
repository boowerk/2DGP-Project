import random

from pico2d import load_image, get_time

import game_framework
import game_world
from coin import Coin
from game_world import remove_object
from state_machine import StateMachine, time_out, random_event, find_coin_event, miss_event

# worker Run Speed
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Idle:
    @staticmethod
    def enter(worker, e):
        worker.dir = 0    # 정지상태
        worker.frame = 1

        worker.start_time = get_time()
        pass

    @staticmethod
    def exit(worker, e):
        pass

    @staticmethod
    def do(worker):
        if get_time() - worker.start_time > 3:
            worker.state_machine.add_event(('TIME_OUT', 0))

        if random.random() < 0.01:
            worker.state_machine.add_event(('RANDOM', 0))
        pass

    @staticmethod
    def draw(worker):
        adjusted_x = worker.king.get_camera_x()
        if worker.last_dir == 1:  # 마지막 방향이 오른쪽일 때
            worker.wait_image.clip_draw(worker.frame * 128, 128, 128, 128, worker.x - adjusted_x, worker.y, 100, 100)
        elif worker.last_dir == -1:  # 마지막 방향이 왼쪽일 때
            worker.wait_image.clip_composite_draw(worker.frame * 128, 128, 128, 128, 0, 'h', worker.x - adjusted_x, worker.y, 100, 100)
        pass

class Wait:
    @staticmethod
    def enter(worker, e):
        worker.frame = 1
        worker.frame_col = 1
        worker.once = False

        worker.last_dir = worker.dir
        pass

    @staticmethod
    def exit(worker, e):
        pass

    @staticmethod
    def do(worker):
        worker.frame_timer += game_framework.frame_time
        if worker.frame_timer >= 0.3 and worker.once == False:  # 프레임 간격을 0.1초로 설정 (필요에 따라 조정 가능)
            worker.frame = (worker.frame + 6) % 36
            worker.frame_timer = 0.0  # 타이머 리셋

            if worker.frame == 31:
                worker.frame_col = 0
                worker.frame = 1
                worker.once = True

        elif worker.frame_timer >= 0.3 and worker.once == True:
            worker.frame = (worker.frame + 6) % 18
            worker.frame_timer = 0.0  # 타이머 리셋

            if worker.frame == 13:
                worker.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(worker):
        adjusted_x = worker.king.get_camera_x()
        if worker.last_dir == 1:  # 마지막 방향이 오른쪽일 때
            worker.wait_image.clip_draw(worker.frame * 128, worker.frame_col * 128, 128, 128, worker.x - adjusted_x, worker.y, 100, 100)
        elif worker.last_dir == -1:  # 마지막 방향이 왼쪽일 때
            worker.wait_image.clip_composite_draw(worker.frame * 128, worker.frame_col * 128, 128, 128, 0, 'h', worker.x - adjusted_x,
                                                worker.y, 100, 100)
        pass

class Walk:
    @staticmethod
    def enter(worker, e):
        worker.dir = random.choice([-1, 1])
        worker.frame = 1
        pass

    @staticmethod
    def exit(worker, e):
        worker.last_dir = worker.dir
        pass

    @staticmethod
    def do(worker):

        worker.x += worker.dir * RUN_SPEED_PPS * game_framework.frame_time

        worker.frame_timer += game_framework.frame_time
        if worker.frame_timer >= 0.1:
            worker.frame = (worker.frame + 6) % 36
            worker.frame_timer = 0

        if worker.x < 900:  # 화면 왼쪽 경계
            worker.x = 900
            worker.dir = 1
        elif worker.x > 2100:  # 화면 오른쪽 경계
            worker.x = 2100
            worker.dir = -1

        if random.random() < 0.001:
            worker.state_machine.add_event(('RANDOM', 0))
        pass

    @staticmethod
    def draw(worker):
        adjusted_x = worker.king.get_camera_x()
        if worker.dir == 1:
            worker.walk_image.clip_draw(worker.frame * 128, 0, 128, 128, worker.x - adjusted_x, worker.y, 100, 100)
        elif worker.dir == -1:
            worker.walk_image.clip_composite_draw(worker.frame * 128, 0, 128, 128, 0, 'h',worker.x - adjusted_x, worker.y, 100, 100)
        pass

class Run:
    @staticmethod
    def enter(worker, e):
        worker.frame = 3
        pass

    @staticmethod
    def exit(worker, e):
        worker.last_dir = worker.dir
        pass

    @staticmethod
    def do(worker):
        worker.x += worker.dir * RUN_SPEED_PPS * game_framework.frame_time

        worker.frame_timer += game_framework.frame_time
        if worker.frame_timer >= 0.1:
            worker.frame = (worker.frame + 6) % 36
            worker.frame_timer = 0

        if worker.x < 900:  # 화면 왼쪽 경계
            worker.x = 900
            worker.dir = 1
        elif worker.x > 2100:  # 화면 오른쪽 경계
            worker.x = 2100
            worker.dir = -1

        if random.random() < 0.001:
            worker.state_machine.add_event(('RANDOM', 0))
        pass

    @staticmethod
    def draw(worker):
        adjusted_x = worker.king.get_camera_x()
        if worker.dir == 1:
            worker.run_image.clip_draw(worker.frame * 128, 0, 128, 128, worker.x - adjusted_x, worker.y, 100, 100)
        elif worker.dir == -1:
            worker.run_image.clip_composite_draw(worker.frame * 128, 0, 128, 128, 0, 'h', worker.x - adjusted_x, worker.y, 100,
                                                100)
        pass

class Worker:
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
