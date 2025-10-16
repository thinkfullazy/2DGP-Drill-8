from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDLK_LEFT, SDL_KEYUP

from state_machine import StateMachine

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
def time_out(e):
    return e[0] == 'TIME_OUT'
def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
class Idle:
    def __init__(self, boy):
        self.boy = boy
    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8
        # if get_time() - self.boy.wait_start_time > 2.0:
        #     self.boy.state_machine.handle_state_event(('TIME_OUT', None))
    def enter(self, e):
        self.boy.frame = 0
        # self.boy.wait_start_time = get_time()

    def exit(self, e):
        pass
    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_draw(self.boy.frame * 100, 300, 100, 100, self.boy.x, self.boy.y)
        else: # left
            self.boy.image.clip_draw(self.boy.frame * 100, 200, 100, 100, self.boy.x, self.boy.y)

class Run:
    def __init__(self, boy):
        self.boy = boy
    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8
        self.boy.x+= self.boy.dir * 5

    def enter(self, e):
        self.boy.frame = 0
        if right_down(e) or left_up(e):
            self.boy.dir = 1
            self.boy.face_dir = 1
        elif left_down(e) or right_up(e):
            self.boy.dir = -1
            self.boy.face_dir = -1

    def exit(self,e):
        pass
    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_draw(self.boy.frame * 100, 100, 100, 100, self.boy.x, self.boy.y)
        else: # left
            self.boy.image.clip_draw(self.boy.frame * 100, 0, 100, 100, self.boy.x, self.boy.y)

class Sleep:
    def __init__(self, boy):
        self.boy = boy
    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8
    def enter(self, e):
        self.boy.frame = 0
        self.boy.dir = 0
    def exit(self, e):
        pass
    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_composite_draw(self.boy.frame * 100, 300, 100, 100, 3.141592/2,'',  self.boy.x - 25, self.boy.y - 25, 100, 100)
        else: # left
            self.boy.image.clip_composite_draw(self.boy.frame * 100, 200, 100, 100, -3.141592/2,'', self.boy.x - 25, self.boy.y - 25, 100, 100)

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('animation_sheet.png')

        self.IDLE = Idle(self)
        # self.sleep = Sleep(self)
        self.RUN = Run(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                # self.sleep: {space_down: self.IDLE},
                self.IDLE:{right_down: self.RUN, left_down: self.RUN,right_up: self.RUN,left_up: self.RUN}, #time_out: self.sleep},
                self.RUN:{right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE}
            }
        )
    def update(self):
        self.state_machine.update()
    def draw(self):
        self.state_machine.draw()
    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT',event))

