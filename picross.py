import pygame, sys
import numpy as np
import os
import pickle

author = 'JoshuaHM-p4'

##### OPTIONS BUTTON WIP ######

# new_surface = pygame.transform.rotozoom(surface, -i*6, 1)
# new_surface.centerx -= i
# screen.blit(new_surface , settings_rect)


def isOver(rect, pos, function):
    if rect.collidepoint(pos):
        function()

def animation_slide(surface, pos):
    if settings_rect.collidepoint(pos) and settings_rect.centerx <= 25:
        settings_rect.centerx += 2
    elif not settings_rect.collidepoint(pos) and settings_rect.centerx > 1:
        settings_rect.centerx -= 2
    surface = pygame.transform.rotozoom(surface, -settings_rect.centerx*2, 1)
    # surface = pygame.transform.rotate(surface, settings_rect.centerx*2)
    return surface

class GameState:
    def __init__(self):
        self.state = 'create'
        self.player_grid = Grid()
        
    def create_and_save(self):
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0]:
                self.player_grid.check_collision(pos,'button1')
                isOver(settings_rect, pos, self.switch_to_solve)
            if pygame.mouse.get_pressed()[2]:
                self.player_grid.check_collision(pos,'button2')
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         self.switch_to_solve()

        screen.fill(color_bg)
        rotated_surface = animation_slide(settings_surface, pos)
        screen.blit(rotated_surface, settings_rect)

        self.show_gamestate()
        self.player_grid.draw()
        rows, columns = self.player_grid.getNumbers()
        self.player_grid.drawNumbers(rows, columns)

        ##### FILL CROSS BUTTONS #####

        
        pygame.display.update()



    def load_and_solve(self):
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0]:
                self.player_grid.check_collision(pos,'button1')
                isOver(settings_rect, pos, self.switch_to_create)
            if pygame.mouse.get_pressed()[2]:
                self.player_grid.check_collision(pos,'button2')
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.switch_to_create()

        screen.fill(color_bg)
        rotated_surface = animation_slide(settings_surface, pos)
        screen.blit(rotated_surface, settings_rect)

        self.show_gamestate()
        self.player_grid.draw()
        rows, columns = self.hidden_grid.getNumbers()
        self.player_grid.drawNumbers(rows, columns)

        ##### FILL CROSS BUTTONS #####

        ##### TIMER #####

        pygame.display.update()

    def state_manager(self):
        if self.state == 'create':
            self.create_and_save()
            

        if self.state == 'solve':
            self.load_and_solve()

    def switch_to_solve(self):
        # del self.player_grid
        self.player_grid = Grid(solve = True)
        self.hidden_grid = Grid(player = False, array = [[0,1,0,0,1],[0,1,0,0,1],[0,1,0,0,1],[0,1,0,0,1],[0,1,0,0,1]])
        self.state = 'solve'
        self.load_and_solve()

    def switch_to_create(self):
        # del self.player_grid, self.hidden_grid
        self.player_grid = Grid(solve = False)
        self.state = 'create'
        self.create_and_save()

    def show_gamestate(self):
        w,h = pygame.display.get_surface().get_size()
        game_text = game_font.render(self.state, True, color_mid)
        text_rect = game_text.get_rect(center = (w//2,h*0.05))
        screen.blit(game_text, text_rect)



# General Setup
pygame.init()
clock = pygame.time.Clock()

from pixel import Pixel
from grid import Grid

# Game Screen Variables
screen_width = 512
screen_height = 512
screen = pygame.display.set_mode((screen_width,screen_height))
Pixel.screen = screen
Grid.screen = screen

pygame.display.set_caption("Pygame Picross")
color_bg = (232, 222, 210)
color_light = (163, 210, 202)
color_mid = (94, 170, 168)
color_dark = (5, 102, 118)
location = os.path.dirname(__file__)
game_font =  pygame.font.Font(os.path.join(location,'resources','04B_19.TTF'),30)

settings_surface = pygame.image.load(os.path.join(location, 'resources', 'gear.png')).convert_alpha()
settings_surface = pygame.transform.scale(settings_surface, (50,50))
settings_rect = settings_surface.get_rect(topleft = (-25,0))

# pygame.display.set_icon(icon)

###### < MAIN GAME LOOP > ######
game_state = GameState()
while True:
    game_state.state_manager()
    clock.tick(120)