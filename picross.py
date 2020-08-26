import pygame, sys
import numpy as np
author = 'JoshuaHM-p4'

SCREEN_SIZE = 512
class Pixel:
    global SCREEN_SIZE
    SIZE = 50
    mid = (SCREEN_SIZE // 2) - SIZE * 2.5
    LIGHT = (163, 210, 202)
    DARK = (5, 103, 118)
    ColorState = [LIGHT,DARK]

    def __init__(self,x,y):
        self.state = 0
        self.color = self.ColorState[self.state]
        self.relative_grid_pos = [x,y]
        self.pointlocation = [self.mid+ x*self.SIZE,self.mid+ y*self.SIZE]
        self.pixel_rect = pygame.Rect(
            (self.pointlocation),
            (self.SIZE,self.SIZE),
        )
    
    def render(self,screen):
        pygame.draw.rect(screen, self.color, self.pixel_rect)

    def fill(self):
        if self.state == 0:
            self.state = 1
            self.color = self.ColorState[self.state]
    
    def empty(self):
        if self.state == 1:
            self.state = 0
            self.color = self.ColorState[self.state]
    
    def cross(self):
        pass

    def __repr__(self):
        return str(self.state)

def makeGrid(columns = 5, rows = 5):
    grid = np.array([np.array([Pixel(x, y) for x in range(columns)]) for y in range(rows)], dtype = object)
    return grid

def draw(grid):
    for row in grid:
        for pix in row:
            pix.render(screen)

def check_collision(pos,mbutton):
    for row in pixel_grid:
        for pixel in row:
            if pixel.pixel_rect.collidepoint(pos):
                if mbutton == 'button1':
                    pixel.fill()
                elif mbutton == 'button2':
                    pixel.empty()

# def print2dArray(grid):
#    print([pixel for pixel in row] for row in grid])

def drawNumber(rows, columns = None):
    for i,n in enumerate(rows):
        pixel_pos = pixel_grid[i][0].pointlocation
        text_pos = (pixel_pos[0] - len(n.strip()), pixel_pos[1] + Pixel.SIZE//2)
        
        num_surface = game_font.render(str(n), True, (94, 170, 167))
        num_rect = num_surface.get_rect(midright = text_pos)
        screen.blit(num_surface, num_rect)

    for i,n in enumerate(columns):
        pixel_pos = pixel_grid[0][i].pointlocation
        vertical_text = n.strip()
        for y,num in enumerate(vertical_text):
            w = Pixel.SIZE
            text_pos = (pixel_pos[0] + Pixel.SIZE//2, 
            pixel_pos[1] - (-y * w *0.3) - (len(vertical_text)* (w * 0.3)) 
            )
            num_surface = game_font.render(str(num), True, (94, 170, 167))
            num_rect = num_surface.get_rect(center = text_pos)
            screen.blit(num_surface, num_rect)

def groupNum(line):
    ### Turn into string ###
    str_line = ''.join(map(str, line))
    ### Find length of ones ###
    ones = list(filter(None, str_line.split('0')))
    ones = list(map(len, ones))
    ### Turn back into string ###
    group_line = ' '.join(map(str,ones))
    if not group_line: return '0'
    return group_line

def getNumbers(grid):
    ######### ROWS #########
    rows = []
    for y in range(len(grid)):
        row = grid[y,:]
        str_row = groupNum(row)
        rows.append(str_row)    
    ######## COLUMNS ########
    columns = []
    for x in range(len(grid[0])):
        column = grid[:,x]
        str_column = groupNum(column)
        columns.append(str_column)
    return rows, columns


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_SIZE,SCREEN_SIZE))
pygame.display.set_caption("Pygame Picross")
BG = (232, 222, 210)
game_font = pygame.font.Font('mypicross/04B_19.TTF',30)

pixel_grid = makeGrid()
# guess_grid = makeGrid()
while True:
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif pygame.mouse.get_pressed()[0]:
            check_collision(pos,'button1')
        elif pygame.mouse.get_pressed()[2]:
            check_collision(pos,'button2')
        # elif pygame.mouse.get_pressed()[1]:
        #     print(pixel_grid)
        


    ###### <MAIN GAME LOOP> ######
    screen.fill(BG)
    draw(pixel_grid)

    rows, columns = getNumbers(pixel_grid)
    drawNumber(rows, columns)

    pygame.display.update()
    clock.tick(120)