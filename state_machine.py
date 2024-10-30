class StateMachine:

    def __init__(self, obj):
        self.obj = obj
        pass

    def start(self, state):
        self.cur_state = state
        pass

    def update(self):
        self.cur_state.do(self.obj)
        pass

    def draw(self):
        self.cur_state.draw(self.obj)
        pass