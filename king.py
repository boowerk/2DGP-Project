from pico2d import load_image, get_time

from state_machine import StateMachine, time_out, right_down, left_up, left_down, right_up


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
        pass

    @staticmethod
    def exit(king, e):
        king.frame = 8
        pass

    @staticmethod
    def do(king):

        if king.x > 400:
            king.camera_x = king.x - 400
            king.x += king.dir * 5
        else:
            king.x += king.dir * 5
        king.frame = (king.frame + 1) % 8
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
        self.x, self.y = 300, 356
        self.dir = 0
        self.last_dir = 1
        self.frame = 8  # 정지 상태
        self.frame_step = 1 # 프레임의 증가 또는 감소
        self.frame_delay = 0.1  # 프레임 전환 간격
        self.image = load_image('king.png')

        self.camera_x = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Walk, left_down: Walk, left_up: Walk, right_up: Walk, time_out: Wait},
                Walk: {right_down: Idle, left_down: Idle, left_up: Idle, right_up: Idle},
                Wait: {right_down: Walk, left_down: Walk, left_up: Walk, right_up: Walk, time_out: Idle}
            }
        )

    def draw(self):
        self.state_machine.draw()
        pass

    def update(self):
        self.state_machine.update()

        print(f'king.x = {self.x}')
        pass

    def handle_event(self, event):
        self.state_machine.add_event(
            ('INPUT', event)
        )