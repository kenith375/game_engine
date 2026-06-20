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
            self.object_names = json.load(jsonfile)
        self.objects_list={}
        for i in self.object_names["start_objects"]:
            new_game_object=getattr(game_objects, i)()
            self.objects_list[new_game_object.key]=new_game_object
        self.is_on_main_menu=None
    def set_preset(self,name="preset1"):
        self.delete_previous()
        for i in self.object_names[name]:
            new_game_object=getattr(game_objects, i[0])(i[1],i[2],i[3],i[4])
            self.objects_list[new_game_object.key]=new_game_object
    def delete_previous(self):
        pass
    def object_logic_frame(self):
        for item in self.objects_list.values():
            dep=[]
            try:
                for d in item.dependencies:
                    dep.append(self.objects_list[d])
            except:
                pass
            if item.is_active:
                item.logic_frame(dep)
            if item.has_physics:
                item.physics_frame(dep)
    def display_all_visible_objects(self):
        drawn_objects=[]
        for item in self.objects_list.values():
            if item.is_visible:
                drawn_objects.append(item)
        drawn_objects.sort(key=lambda x: x.draw_layer,reverse=True)      #The higher the draw layer, the later it is drawn, so a high draw layer is probably going to be on top
        for i in drawn_objects:
            i.display()
            
main=game()
main.set_preset()
i_zero=120000
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
    main.display_all_visible_objects()
    pygame.display.flip()
    clock.tick(settings["fps"])
    i+=1
    if i>i_zero:
        running=False
end = time.time()
print(i/(end-start))
pygame.quit()