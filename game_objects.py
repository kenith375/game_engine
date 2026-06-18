import pygame
import shared_tools as ST
from OpenGL.GL import *
class background(ST.game_object):
    def __init__(self, visible=True, does_this_object_perform_logic=False, physics=False):
        super().__init__(visible, 0, does_this_object_perform_logic, physics,0,0)
        self.texture=ST.load_texture("/kenith/Downloads/archUsersBeLike.png")
    def display(self, screen):
        self.display_image()
class funky_square(ST.game_object):
    def __init__(self, visible=True, does_this_object_perform_logic=False, physics=False):
        super().__init__(visible, -1, does_this_object_perform_logic, physics,0,0)
    def display(self, screen):
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