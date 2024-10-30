from pico2d import load_image, get_time

from state_machine import StateMachine


class Idle:
    @staticmethod
    def enter(king):
        king.dir = 0
        king.frame = 8

        king.start_time = get_time()
        pass

    @staticmethod
    def exit(king):
        pass

    @staticmethod
    def do(king):
        pass

    @staticmethod
    def draw(king):
        king.image.clip_draw(king.frame * 64, 0, 64, 64, king.x, king.y, 192, 192)
        pass

class Wait:
    @staticmethod
    def enter(king):
        pass

    @staticmethod
    def exit(king):
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
        self.image = load_image('king.png')

        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)

    def draw(self):
        self.state_machine.draw()
        pass

    def update(self):
        self.state_machine.update()
        pass