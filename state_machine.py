from event_to_string import event_to_string


class StateMachine:
    def __init__(self, start_state, rules):
        self.cur_state = start_state   #시작 상태
        self.cur_state.enter('start')  #시작상태 진입
        self.rules = rules

    def update(self):
        self.cur_state.do()            #현재 상태 do 실행
        pass

    def draw(self):
        self.cur_state.draw()          #현재 상태 draw 실행
        pass

    def handle_state_event(self, state_event): #상태 전환
        for check_event in self.rules[self.cur_state].keys():
            if check_event(state_event):
                self.next_state = self.rules[self.cur_state][check_event]
                self.cur_state.exit(state_event)
                self.next_state.enter(state_event)
                print(f'{self.cur_state.__class__.__name__} - {event_to_string(state_event)} -> {self.next_state.__class__.__name__}')
                self.cur_state = self.next_state
                return
        print(f'처리되지 않은 이벤트 {event_to_string(state_event)}')


