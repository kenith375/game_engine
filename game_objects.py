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
class ramp(ST.game_object):
    def __init__(self, rotation=0, x=-950,y=-500,width=250,height=250,visible=True, does_this_object_perform_logic=False, physics=True):
        super().__init__(visible, 0, does_this_object_perform_logic, physics, x, y)
        self.rotation=rotation
        self.width=width
        self.height=height
        self.dependencies=["player"]
        self.texture=ST.load_texture("ramp.png")
    def display(self):
        self.display_image([self.x_pos/gs.horiz_scale,self.y_pos/gs.vertic_scale,self.width/gs.horiz_scale,self.height/gs.vertic_scale])
    def physics_frame(self,dep):
        if ST.do_rects_intersect(dep[0].get_bounds(),self.get_bounds()):
            dep[0].touch_ramp(self)
    def get_bounds(self):
        return [self.x_pos,self.y_pos,self.width,self.height]
class player(ST.game_object):
    def __init__(self, x=0,y=0,width=50,height=50,visible=True, does_this_object_perform_logic=True, physics=False):
        super().__init__(visible, -2, does_this_object_perform_logic, physics, x, y, width, height)
        self.x_speed=0
        self.y_speed=0
        self.jump_dir=.5*math.pi
        self.on_ground=False
        self.key="player"
        self.texture=ST.load_texture("ball.png")
        self.dependencies=[]
        self.sub_hit_boxes={}
        self.sub_hit_boxes["feet"]=[10,0,30,10]
        self.sub_hit_boxes["head"]=[10,40,30,10]
        self.sub_hit_boxes["left"]=[0,5,5,40]
        self.sub_hit_boxes["right"]=[45,5,5,40]
        self.stored_spin=100
        self.temp_spin=4
    def touch_ramp(self,ramp):
        rel_x=ramp.x_pos-self.x_pos
        rel_y=ramp.y_pos+ramp.height-self.y_pos
        dist=rel_x**2+rel_y**2
        if dist>(ramp.width**2):
            self.y_pos=math.sqrt((ramp.width**2)-rel_x**2)+ramp.y_pos
            self.y_speed=0
            self.on_ground=True
        if ramp.rotation==0:
            if self.y_speed<0:
                pass

    def hit_ground(self,wall):
        hit_regions=[]
        for region in ["head","feet","left","right"]:
            hit_regions.append(ST.do_rects_intersect(np.add(self.sub_hit_boxes[region],[self.x_pos,self.y_pos,0,0]),wall.get_bounds()))
        head=hit_regions[0]
        feet=hit_regions[1]
        left=hit_regions[2]
        right=hit_regions[3]
        if left:
            self.x_speed=max(0,self.x_speed)
            self.x_pos=wall.x_pos+wall.width-1
            self.jump_dir=0
            if abs(self.temp_spin)>5:
                self.y_speed=-self.temp_spin
        elif right:
            self.x_speed=min(0,self.x_speed)
            self.x_pos=wall.x_pos-self.width+1
            self.y_speed=self.temp_spin
            self.jump_dir=math.pi
        else:
            self.jump_dir=0.5*math.pi
        if head:
            self.y_pos=wall.y_pos-self.height
            self.y_speed=max(self.y_speed,0)
        elif feet:
            self.y_pos=wall.y_pos+wall.height
            self.y_speed=-math.floor(abs(self.y_speed)*5)/20
            self.on_ground=True
    def logic_frame(self,x,k):
        l_in=k[pygame.K_LEFT]
        r_in=k[pygame.K_RIGHT]
        if l_in:
            self.temp_spin-=.04
        if r_in:
            self.temp_spin+=.04
        if self.on_ground:
            self.temp_spin*=.995
            self.x_speed+=self.temp_spin*0.01
            self.x_speed*=0.98
        else:
            self.temp_spin*=.9995
            self.x_speed*=.998
        self.x_pos+=self.x_speed
        
        if k[pygame.K_SPACE]and self.on_ground:
            self.on_ground=False
            self.y_speed+=2*math.sin(self.jump_dir)
            self.x_pos+=2*math.cos(self.jump_dir)
        self.y_pos+=self.y_speed
        self.y_speed-=.01
    def get_bounds(self,x=None):
        return [self.x_pos,self.y_pos,self.width,self.height]
    def display(self):
        self.display_image([self.x_pos/gs.horiz_scale,self.y_pos/gs.vertic_scale,self.width/gs.horiz_scale,self.height/gs.vertic_scale])