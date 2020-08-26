import pygame, sys
import numpy as np
author = 'JoshuaHM-p4'

##### OPTIONS BUTTON WIP ######

# General Setup
pygame.init()
clock = pygame.time.Clock()

from pixel import Pixel
from grid import Grid

# Game Screen
screen_width = 512
screen_height = 512
screen = pygame.display.set_mode((screen_width,screen_height))
Pixel.screen = screen
pygame.display.set_caption("Pygame Picross")
BG = (232, 222, 210)
game_font = pygame.font.Font('mypicross/04B_19.TTF',30)

## Create game ##
pixel_grid = Grid(screen, creating = False)
# guess_grid = makeGrid()


while True:
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif pygame.mouse.get_pressed()[0]:
            pixel_grid.check_collision(pos,'button1')
        elif pygame.mouse.get_pressed()[2]:
            pixel_grid.check_collision(pos,'button2')

    ###### <MAIN GAME LOOP> ######
    screen.fill(BG)
    pixel_grid.draw()

    rows, columns = pixel_grid.getNumbers()
    pixel_grid.drawNumbers(rows, columns)

    pygame.display.update()
    clock.tick(120)