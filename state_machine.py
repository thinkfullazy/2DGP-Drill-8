class StateMachine:
    def __init__(self, start_state):
        self.cur_state = start_state   #시작 상태
        self.cur_state.enter()          #시작상태 진입
        pass

    def update(self):
        self.cur_state.do()            #현재 상태 do 실행
        pass

    def draw(self):
        self.cur_state.draw()          #현재 상태 draw 실행
        pass


