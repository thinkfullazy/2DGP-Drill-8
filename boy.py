from pico2d import load_image

from state_machine import StateMachine


class Idle:
    def __init__(self, boy):
        self.boy = boy
    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8
        pass
    def enter(self):
        self.boy.frame = 0
        pass
    def exit(self):
        pass
    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_draw(self.boy.frame * 100, 300, 100, 100, self.boy.x, self.boy.y)
        else: # left
            self.boy.image.clip_draw(self.boy.frame * 100, 200, 100, 100, self.boy.x, self.boy.y)



class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.image = load_image('animation_sheet.png')

        self.IDLE = Idle(self)
        self.state_machine = StateMachine(self.IDLE)
    def update(self):
        self.state_machine.update()
    def draw(self):
        self.state_machine.draw()
