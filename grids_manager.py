import pygame
import numpy as np
import os

directory = os.path.join(os.getcwd(),  'grids')
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
    font = pygame.font.Font(os.path.join(os.getcwd(),'resources','04B_19.TTF'),15)
    dark_color = (5, 102, 118)
    light_color = (163, 210, 202)

    def __init__(self, pos, number, filename):
        self.filename = filename
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.rect = pygame.Rect(pos, self.size)
        self.label = self.font.render(str(number), True, self.dark_color)
        if number > 9:
            self.mid = (pos[0] + self.length//4, pos[1] + self.length//4)
        else:
            self.mid = (pos[0] + self.length//3, pos[1] + self.length//4)

    def draw(self, screen):
        pygame.draw.rect(screen, self.dark_color, (self.x-2,self.y-2,self.length+4,self.length+4))
        pygame.draw.rect(screen, self.light_color, self.rect)
        screen.blit(self.label, self.mid)

def make_grids_list():
    global grid_icons
    grid_icons = []
    # grids = [os.path.splitext(file)[0] for file in os.listdir(directory)]
    for num,grid_name in enumerate(sorted(os.listdir(directory))):
        print(grid_name)
        x_pos = 30 + num*30
        y_pos = int(pygame.display.get_surface().get_size()[1] * 0.85)
        ## Icon Wrapping Here ##
        grid_icons.append(Grid_Icon((x_pos, y_pos), num, grid_name))

def show_grid_icons(screen): 
    for icon in grid_icons:
        icon.draw(screen)

def grid_click(cursor_pos):
    for icon in grid_icons:
        if icon.rect.collidepoint(cursor_pos):
            return icon.filename


