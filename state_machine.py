from tabnanny import check


def start_evnet(e):
    return e[0] == 'START'

def time_out(e):
    return e[0] == 'TIME_OUT'


class StateMachine:

    def __init__(self, obj):
        self.obj = obj
        self.event_q = []

    def start(self, state):
        self.cur_state = state
        self.cur_state.enter(self.obj, ('START', 0))
        print(f'Enter into {state}')
        pass

    def update(self):
        self.cur_state.do(self.obj)

        if self.event_q:
            e = self.event_q.pop(0)
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e):
                    print(f'Exit from {self.cur_state}')
                    self.cur_state.exit(self.obj, e)

                    self.cur_state = next_state
                    print(f'Enter into {next_state}')

                    self.cur_state.enter(self.obj, e)
                    return
            print(f'        WARING: {e} not handled at state {self.cur_state}')


    def draw(self):
        self.cur_state.draw(self.obj)
        pass

    def add_event(self, e):
        print(f'    DEBUG: add event {e}')
        self.event_q.append(e)
        pass

    def set_transitions(self, transitions):
        self.transitions = transitions