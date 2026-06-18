import pygame
from OpenGL.GL import *
def load_texture(path):
    surface = pygame.image.load(path)
    texture_data = pygame.image.tostring(surface, "RGBA", True)
    width = surface.get_width()
    height = surface.get_height()
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        width,
        height,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        texture_data
    )
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return tex_id
def clipped_removed_section(rect,bounds=[-1,-1,2,2]):
    left = max(rect[0], bounds[0])
    top = max(rect[1], bounds[1])

    right = min(rect[0] + rect[2],
                bounds[0] + bounds[2])

    bottom = min(rect[1] + rect[3],
                 bounds[1] + bounds[3])

    if right <= left or bottom <= top:
        return None

    return [
        left,
        top,
        right - left,
        bottom - top
    ]
def do_rects_intersect(a,b):
    al=a[0]
    ar=a[0]+a[2]
    at=a[1]
    ab=a[1]+a[3]
    bl=b[0]
    br=b[0]+b[2]
    bt=b[1]
    bb=b[1]+b[3]
    return not(bl>=ar or bt>=ab or al>=br or at>=bb)
def section_is_covered_by_part_removed(a,b):
    al=a[0]
    ar=a[0]+a[2] #x position + width
    at=a[1]
    ab=a[1]+a[3] #y position + height
    bl=b[0]
    br=b[0]+b[2]
    bt=b[1]
    bb=b[1]+b[3]
    return al>=bl and br>=ar and at>=bt and bb>=ab

def cut_from(section,part_removed):
    if do_rects_intersect(section, part_removed):
        if section_is_covered_by_part_removed(section, part_removed):
            return []
        else:
            llos=[]#local list of sections
            part_removed_final_x=part_removed[0]+part_removed[2]
            part_removed_final_y=part_removed[1]+part_removed[3]
            section_final_x=section[0]+section[2]
            section_final_y=section[1]+section[3]
            is_left_rect=part_removed[0]>section[0]
            is_right_rect=part_removed_final_x<section_final_x
            is_top_rect=part_removed[1]>section[1]
            is_bottom_rect=part_removed_final_y<section_final_y
            if is_left_rect:
                llos.append([section[0],section[1],part_removed[0]-section[0],section[3]])
            if is_right_rect:
                llos.append([part_removed_final_x,section[1],section_final_x-part_removed_final_x,section[3]])
            if is_top_rect:
                llos.append([part_removed[0],section[1],part_removed_final_x-part_removed[0],part_removed[1]-section[1]])
            if is_bottom_rect:
                llos.append([part_removed[0],part_removed_final_y,part_removed_final_x-part_removed[0],section_final_y-part_removed_final_y])
            return llos
    else:
        return [section]

class mask:
    def __init__(self):
        self.regions=[[-1,-1, 2, 2]]
    def remove_rect(self,removed_section):
        new_sections=[]
        for section in self.regions:
            clipped=clipped_removed_section(removed_section,section)
            if clipped is None:
                new_sections.append(section)
            else:
                new_sections+=cut_from(section,clipped)
        self.regions=new_sections

class game_object:
    def __init__(self,visible=True,draw_layer=0,does_this_object_perform_logic=True,physics=False,object_pos_x=0,object_pos_y=0):
        self.is_visible=visible
        self.draw_layer=draw_layer
        self.is_active=does_this_object_perform_logic
        self.has_physics=physics
        if physics or visible:
            self.x_pos,self.y_pos=object_pos_x,object_pos_y
    def dump(self):
        print("Attributes:")
        for name, value in self.__dict__.items():
            print(f"  {name} = {value}")
    def display_image(self):
        glColor3f(1.0, 1.0, 1.0)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        glBegin(GL_QUADS)

        glTexCoord2f(0, 0)
        glVertex2f(-1, -1)

        glTexCoord2f(1, 0)
        glVertex2f(1, -1)

        glTexCoord2f(1, 1)
        glVertex2f(1, 1)

        glTexCoord2f(0, 1)
        glVertex2f(-1, 1)

        glEnd()

        glDisable(GL_TEXTURE_2D)
