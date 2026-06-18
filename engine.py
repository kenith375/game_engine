import game_objects
import pygame, math, numpy, time, json
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import shared_tools
pygame.init()
display = (1920, 1080)
Screen=pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
with open("settings.json", "r") as jsonfile: 
    settings = json.load(jsonfile)





class game:
    def __init__(self,debug=False):
        with open("list_of_game_objects.json", "r") as jsonfile: 
            object_names = json.load(jsonfile)
        self.objects_list=[]
        for i in object_names:
            self.objects_list.append(getattr(game_objects, i)())
        self.is_on_main_menu=True
    def object_logic_frame(self):
        for item in self.objects_list:
            if item.is_active:
                item.logic_frame()
            if item.has_physics:
                item.move_frame()
    def display_all_visible_objects(self,screen):
        drawn_objects=[]
        for item in self.objects_list:
            if item.is_visible:
                drawn_objects.append(item)
        drawn_objects.sort(key=lambda x: x.draw_layer)      #The higher the draw layer, the later it is drawn, so a high draw layer is probably going to be on top

        i=len(drawn_objects)
        while i>0:
            i-=1
            drawn_objects[i].display(screen)
            
main=game()
i_zero=1200
i=0
running = True
start = time.time()
clock=pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    main.object_logic_frame()
    glClear(GL_COLOR_BUFFER_BIT)
    main.display_all_visible_objects(Screen)
    pygame.display.flip()
    clock.tick(settings["fps"])
    i+=1
    if i>i_zero:
        running=False
end = time.time()
print(i/(end-start))
pygame.quit()