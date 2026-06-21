import pygame,math
import shared_tools as ST
from OpenGL.GL import *
import numpy as np
class game_settings:
    def __init__(self):
        self.res_x=1920
        self.res_y=1080
        self.horiz_scale=1000
        self.vertic_scale=1000*self.res_y/self.res_x
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
            dep[0].hit_ground(self)
    def get_bounds(self,dep=None):
        return [self.x_pos,self.y_pos,self.width,self.height]
    def display(self):
        self.display_image([self.x_pos/gs.horiz_scale,self.y_pos/gs.vertic_scale,self.width/gs.horiz_scale,self.height/gs.vertic_scale])

class player(ST.game_object):
    def __init__(self, x=0,y=0,width=50,height=50,visible=True, does_this_object_perform_logic=True, physics=False):
        super().__init__(visible, -2, does_this_object_perform_logic, physics, x, y, width, height)
        self.y_speed=0
        self.key="player"
        self.texture=ST.load_texture("a.png")
        self.dependencies=[]
        self.sub_hit_boxes={}
        self.sub_hit_boxes["feet"]=[0,0,50,10]
        self.sub_hit_boxes["head"]=[0,40,50,10]
        self.sub_hit_boxes["left"]=[0,5,5,40]
        self.sub_hit_boxes["right"]=[45,5,5,40]
        self.spin=100
    def hit_ground(self,wall):
        hit_regions=[]
        for region in ["head","feet","left","right"]:
            hit_regions.append(ST.do_rects_intersect(np.add(self.sub_hit_boxes[region],[self.x_pos,self.y_pos,0,0]),wall.get_bounds()))
        head=hit_regions[0]
        feet=hit_regions[1]
        left=hit_regions[2]
        right=hit_regions[3]
        if left:
            self.x_pos=wall.x_pos+wall.width
        elif right:
            self.x_pos=wall.x_pos-self.width
        elif head:
            self.y_pos=wall.y_pos-self.height
            self.y_speed=0
        elif feet:
            self.y_pos=wall.y_pos+wall.height
            self.y_speed=-math.floor(abs(self.y_speed)*5)/20
    def logic_frame(self,x,k):
        if k[pygame.K_LEFT]:
            self.x_pos-=1
        if k[pygame.K_RIGHT]:
            self.x_pos+=1
        self.y_pos-=self.y_speed
        self.y_speed+=.1
    def get_bounds(self,x=None):
        return [self.x_pos,self.y_pos,self.width,self.height]
    def display(self):
        self.display_image([self.x_pos/gs.horiz_scale,self.y_pos/gs.vertic_scale,self.width/gs.horiz_scale,self.height/gs.vertic_scale])