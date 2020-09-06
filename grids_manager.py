import pygame
import numpy as np
import os

directory = os.path.join(os.getcwd(),  'grids')
font = pygame.font.Font(os.path.join(os.getcwd(),'resources','04B_19.TTF'),15)
dark_color = (5, 102, 118)
light_color = (163, 210, 202)
if not os.path.exists(directory):
    os.mkdir(directory)

def save_to_dir(grid):
    filename = 'Grid'
    fullpath = os.path.join(directory, filename)

    i = 0
    while os.path.exists(fullpath + '.npy'):
        i += 1
        fullpath = os.path.join(directory, filename + '_' + str(i).zfill(2))

    np.save(fullpath, grid, allow_pickle = True)

def load_grid(filename):
    file = np.load(os.path.join(directory, filename), allow_pickle = True)
    return file

class Grid_Icon:
    length = 30
    size = (length, length)

    def __init__(self, number, filename):
        self.number = number
        self.label = font.render(str(number), True, dark_color)
        self.filename = filename

        self.x = self.length + self.number*self.length
        self.y = int(screen_height * 0.85)
        self.set_position()

    def set_position(self):  ## This repositions icons to the left ##
        self.rect = pygame.Rect([self.x, self.y], self.size)
        if self.number > 9:
            self.mid = (self.x + self.length//4, self.y + self.length//4) # if number is 0,1,2,3,...
        else:
            self.mid = (self.x + self.length//3, self.y + self.length//4) # if number is 10,11,12,13,...

    def draw(self, screen):
        pygame.draw.rect(screen, dark_color, (self.x-2,self.y-2,self.length+4,self.length+4))
        pygame.draw.rect(screen, light_color, self.rect)
        screen.blit(self.label, self.mid)

def icon_click(cursor_pos):
    if move_left_rect.collidepoint(cursor_pos):
        move_left()
    elif move_right_rect.collidepoint(cursor_pos):
        move_right()
    else:
        for icon in grid_icons:
            if icon.rect.collidepoint(cursor_pos):
                return icon.filename

def make_grids_list():
    global grid_icons, min_icon, max_icon, screen_height, font, move_right_rect, move_left_rect
    screen_width, screen_height = pygame.display.get_surface().get_size() 
    grid_icons = [Grid_Icon(num, grid_name) for num,grid_name in enumerate( sorted( os.listdir(directory) ) ) ]
    
    min_icon = 0
    max_icon = (screen_width - 30)//Grid_Icon.length - 1
    move_left_rect = pygame.Rect((0, screen_height * 0.85), (30,30))
    move_right_rect = pygame.Rect((screen_width-30, screen_height * 0.85), (30,30))

def show_grid_icons(screen):
    pygame.draw.rect(screen, dark_color, (move_left_rect.x-2,move_left_rect.y-2,Grid_Icon.length+4,Grid_Icon.length+4))
    pygame.draw.rect(screen, light_color, move_left_rect)
    screen.blit(font.render('<', True, dark_color), (move_left_rect.x + Grid_Icon.length//4, move_left_rect.y + Grid_Icon.length//4))
    
    if grid_icons:
        draw_limit = grid_icons[min_icon:max_icon]
        for icons in draw_limit:
            icons.draw(screen)

    pygame.draw.rect(screen, dark_color, (move_right_rect.x-2,move_right_rect.y-2,Grid_Icon.length+4,Grid_Icon.length+4))
    pygame.draw.rect(screen, light_color, move_right_rect)
    screen.blit(font.render('>', True, dark_color), (move_right_rect.x + Grid_Icon.length//3, move_right_rect.y + Grid_Icon.length//4))


def move_right():
    global max_icon, min_icon
    if max_icon < len(grid_icons):
        max_icon += 1
        min_icon += 1
        for icon in grid_icons:
            icon.x -= Grid_Icon.length # All icons will move to the right by one icon size
            icon.set_position()

def move_left():
    global max_icon, min_icon
    if min_icon > 0:
        min_icon -= 1
        max_icon -= 1
        for icon in grid_icons:
            icon.x += Grid_Icon.length # All icons will move to the left by one icon size
            icon.set_position()

