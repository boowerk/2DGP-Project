from pico2d import load_image, get_time

import game_framework
from state_machine import StateMachine, time_out


class Idle:
    @staticmethod
    def enter(poor, e):
        poor.dir = 0    # 정지상태
        poor.frame = 0

        poor.start_time = get_time()
        pass

    @staticmethod
    def exit(poor, e):
        pass

    @staticmethod
    def do(poor):
        if get_time() - poor.start_time > 3:
            poor.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(poor):
        poor.wait_image.clip_draw(poor.frame * 128, 128, 128, 128, poor.x, poor.y, 100, 100)
        pass

class Wait:
    @staticmethod
    def enter(poor, e):
        poor.frame = 0
        poor.frame_col = 1
        poor.once = False
        pass

    @staticmethod
    def exit(poor, e):
        pass

    @staticmethod
    def do(poor):
        poor.frame_timer += game_framework.frame_time
        if poor.frame_timer >= 0.3 and poor.once == False:  # 프레임 간격을 0.1초로 설정 (필요에 따라 조정 가능)
            poor.frame = (poor.frame + 6) % 36
            poor.frame_timer = 0.0  # 타이머 리셋

            if poor.frame == 30:
                poor.frame_col = 0
                poor.frame = 0
                poor.once = True

        elif poor.frame_timer >= 0.3 and poor.once == True:
            poor.frame = (poor.frame + 6) % 18
            poor.frame_timer = 0.0  # 타이머 리셋

            if poor.frame == 12:
                poor.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(poor):
        poor.wait_image.clip_draw(poor.frame * 128, poor.frame_col * 128, 128, 128, poor.x, poor.y, 100, 100)
        pass

class Walk:
    @staticmethod
    def enter(poor, e):
        pass

    @staticmethod
    def exit(poor, e):
        pass

    @staticmethod
    def do(poor):
        pass

    @staticmethod
    def draw(poor):
        pass

class Poor:
    def __init__(self):
        self.x, self.y = 400, 356
        self.dir = 0
        self.frame = 0
        self.frame_timer = 0
        self.run_image = load_image('npc_run_sprite.png')
        self.wait_image = load_image('npc_wait_sprite.png')
        self.walk_image = load_image('npc_walk_sprite.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {time_out: Wait},
                Wait: {time_out: Idle}
            }
        )

    def draw(self):
        self.state_machine.draw()
        pass

    def update(self):
        self.state_machine.update()
        pass