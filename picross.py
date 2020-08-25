import pygame, sys
import numpy as np
author = 'JoshuaHM-p4"

SCREEN_SIZE = 512
BG = (232, 222, 210)


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_SIZE,SCREEN_SIZE))
pygame.display.set_caption("Picross")
screen.fill(BG)

class Pixel:
    global SCREEN_SIZE
    size = 50
    mid = (SCREEN_SIZE // 2) - size * 2.5
    LIGHT = (163, 210, 202)
    DARK = (5, 103, 118)

    def __init__(self,x,y):
        self.status = self.LIGHT
        self.gridpos = [x,y]
        self.pixel_rect = pygame.Rect(
            (self.mid+ x*self.size,self.mid+ y*self.size),
            (self.size,self.size)
        )
        
    def fill(self):
        if self.status == self.LIGHT:
            self.status = self.DARK
    
    def delete(self):
        if self.status == self.DARK:
            self.status = self.LIGHT
    

def makeGrid(columns = 5, rows = 5):
    new_array = [[Pixel(column, row) for row in range(rows)] for column in range(columns)]
    return new_array

def draw(grid):
    for row in grid:
        for pix in row:
            pygame.draw.rect(screen, pix.status, pix.pixel_rect)

def check_collision(pos,mbutton):
    for i in pixel_grid:
        for pixel in i:
            if pixel.pixel_rect.collidepoint(pos):
                if mbutton == 'button1':
                    pixel.fill()
                elif mbutton == 'button2':
                    pixel.delete()



pixel_grid = makeGrid()
# guess_grid = makeGrid()
held = False

while True:
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif pygame.mouse.get_pressed()[0]:
            check_collision(pos,'button1')
        elif pygame.mouse.get_pressed()[2]:
            check_collision(pos,'button2')
    ### <MAIN GAME LOOP> ###
    draw(pixel_grid)

    pygame.display.update()
    clock.tick(120)