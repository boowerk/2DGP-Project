from pico2d import load_image, get_time

from state_machine import StateMachine, time_out


class Idle:
    @staticmethod
    def enter(king, e):
        king.dir = 0    # 정지상태
        king.frame = 8

        king.start_time = get_time()
        pass

    @staticmethod
    def exit(king, e):
        pass

    @staticmethod
    def do(king):
        if get_time() - king.start_time > 3:
            king.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(king):
        king.image.clip_draw(king.frame * 64, 0, 64, 64, king.x, king.y, 192, 192)
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
        pass

    @staticmethod
    def do(king):
        king.frame_timer += 0.01

        if king.frame_timer >= king.frame_delay:
            king.frame_timer = 0

            if king.frame == 10:
                king.frame_step = -1
            elif king.frame == 8:
                king.frame_step = 1

            king.frame += king.frame_step
        pass

    @staticmethod
    def draw(king):
        king.image.clip_draw(king.frame * 64, 0, 64, 64, king.x, king.y, 192, 192)
        pass

class Walk:
    @staticmethod
    def enter(king, e):
        pass

    @staticmethod
    def exit(king, e):
        pass

    @staticmethod
    def do(king):
        pass

    @staticmethod
    def draw(king):
        pass


class King:
    def __init__(self):
        self.x, self.y = 400, 356
        self.dir = 0
        self.frame = 8  # 정지 상태
        self.frame_step = 1 # 프레임의 증가 또는 감소
        self.frame_delay = 0.1  # 프레임 전환 간격
        self.image = load_image('king.png')

        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {time_out: Wait}

            }
        )

    def draw(self):
        self.state_machine.draw()
        pass

    def update(self):
        self.state_machine.update()
        pass

    def handle_event(self, event):
        self.state_machine.add_event(
            ('INPUT', event)
        )