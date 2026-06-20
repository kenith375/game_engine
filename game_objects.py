import pygame
import shared_tools as ST
from OpenGL.GL import *
class game_settings:
    def __init__(self):
        self.horiz_scale=1000
        self.vertic_scale=800
gs=game_settings()
class background(ST.game_object):
    def __init__(self, visible=True, does_this_object_perform_logic=False, physics=False):
        super().__init__(visible, 0, does_this_object_perform_logic, physics,0,0)
        self.texture=ST.load_texture("/kenith/Downloads/archUsersBeLike.png")
        self.dependencies=[]
    def display(self):
        self.display_image()
class funky_square(ST.game_object):
    def __init__(self, visible=True, does_this_object_perform_logic=False, physics=False):
        super().__init__(visible, -1, does_this_object_perform_logic, physics,0,0)
        self.dependencies=[]
    def display(self):
        a=ST.mask()
        a.remove_rect([-0.5,-0.5,1,1])
        a.remove_rect([.6,.6,0.3,0.3])
        for i in a.regions:
            glBegin(GL_QUADS)

            glColor3f(1.0, 0.0, 0.0)  # Red

            glVertex2f( i[0], i[1])
            glColor3f(1, 1, 0)
            glVertex2f( i[0]+i[2], i[1])
            glColor3f(1, 1, 1)
            glVertex2f( i[0]+i[2], i[1]+i[3])
            glColor3f(0, 1, 1)
            glVertex2f(i[0], i[1]+i[3])

            glEnd()
class wall(ST.game_object):
    def __init__(self, x,y,width,height,visible=True, does_this_object_perform_logic=False, physics=True):
        super().__init__(visible, 0, does_this_object_perform_logic, physics, x, y)
        self.width=width
        self.height=height
        self.dependencies=["player"]
        self.texture=ST.load_texture("a.png")
    def physics_frame(self,dep):
        if ST.do_rects_intersect(dep[0].get_bounds(),self.get_bounds()):
            dep[0].hit_ground()
    def get_bounds(self,dep=None):
        return [self.x_pos,self.y_pos,self.width,self.height]
    def display(self):
        self.display_image([self.x_pos/gs.horiz_scale,self.y_pos/gs.vertic_scale,self.width/gs.horiz_scale,self.height/gs.vertic_scale])
class player(ST.game_object):
    def __init__(self, x=0,y=0,width=20,height=50,visible=True, does_this_object_perform_logic=True, physics=False):
        super().__init__(visible, -2, does_this_object_perform_logic, physics, x, y, width, height)
        self.y_speed=0
        self.key="player"
        self.texture=ST.load_texture("a.png")
        self.dependencies=[]

    def logic_frame(self,x=None):
        self.y_pos-=self.y_speed
        self.y_speed+=.1
    def get_bounds(self,x=None):
        return [self.x_pos,self.y_pos,self.width,self.height]
    def display(self):
        self.display_image([self.x_pos/gs.horiz_scale,self.y_pos/gs.vertic_scale,self.width/gs.horiz_scale,self.height/gs.vertic_scale])