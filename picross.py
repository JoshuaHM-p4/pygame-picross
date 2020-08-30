import pygame, sys
import numpy as np
import os
import pickle

author = 'JoshuaHM-p4'
# WIP Checklist 
# Fill and Cross Buttons (Solve)
# Level Grid Icons Wrapping
# Resizing Feature
# Deleting Editing Levels

def settings_animation(surface, pos):
    if settings_hidden.collidepoint(pos) and settings_rect.centerx <= 25:
        settings_rect.centerx += 1
    elif settings_rect.centerx >= -30:
        settings_rect.centerx -= 1
    surface = pygame.transform.rotozoom(surface, -settings_rect.centerx*5, 1)
    # surface = pygame.transform.rotate(surface, -settings_rect.centerx*2)
    return surface

def top_text(message: str):
        game_text = game_font.render(message, True, color_mid)
        text_rect = game_text.get_rect(center = (screen_width//2,screen_height//20))
        screen.blit(game_text, text_rect)

def bottom_text(message: str):
    message_text = game_font.render(str(message), True, color_dark)
    message_rect = message_text.get_rect(center = (screen_width//2 - len(message)//2, int(screen_height*0.95)))
    screen.blit(message_text, message_rect)

class GameState:
    resized = False
    menu_visible = False
    load_icons_visible = False

    grid_filename = None

    just_loaded = False
    just_saved = False
    message_timer = 0

    def __init__(self):
        self.state = 'create'
        self.player_grid = Grid()
    
    def create(self):
        global screen
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0]:
                self.player_grid.check_collision(pos,'button1')
                if settings_rect.collidepoint(pos):
                    self.menu_visible = not self.menu_visible
                elif play_rect.collidepoint(pos) and self.menu_visible:
                    self.hidden_grid = self.player_grid 
                    self.player_grid = Grid(solve = True)
                    self.state = 'solve'
                    self.solve()
                elif save_rect.collidepoint(pos) and self.menu_visible:
                    if self.player_grid.grid_states().any():
                        grids_manager.save_to_dir(self.player_grid.grid)
                        grids_manager.make_grids_list()
                        self.just_saved = True
                        self.message_timer = 100
                elif load_rect.collidepoint(pos) and self.menu_visible:
                    self.load_icons_visible = not self.load_icons_visible
                    grids_manager.make_grids_list()
                elif self.load_icons_visible and grids_manager.grid_click(pos):
                    self.grid_filename = grids_manager.grid_click(pos)
                    self.player_grid.grid = grids_manager.load_grid(self.grid_filename)
                    self.just_loaded = True
                    self.message_timer = 100
                elif resize_rect.collidepoint(pos) and self.menu_visible:
                    self.resized = not self.resized
                    if self.resized:
                        screen = pygame.display.set_mode((screen_width*2, screen_height*2))
                    else:
                        screen = pygame.display.set_mode((screen_width, screen_height))
                else: 
                    self.menu_visible = False
                    self.load_icons_visible = False 
            elif pygame.mouse.get_pressed()[2]:
                self.player_grid.check_collision(pos,'button2')

        ################ < Main Screen Elements > ################
        screen.fill(color_bg)
        top_text(self.state.title())

        # < Main Grid Board Draw > #
        self.player_grid.draw()
        rows, columns = self.player_grid.getNumbers()
        self.player_grid.drawNumbers(rows, columns)

        # < Options > #
        rotated_surface = settings_animation(settings_surface, pos)
        screen.blit(rotated_surface, settings_rect)

        if self.menu_visible:
            self.show_Menu()
        if self.load_icons_visible:
            grids_manager.show_grid_icons(screen)

        # < Message > #
        if self.message_timer >= 1:
            if self.just_loaded:
                bottom_text(f"Loaded \"{self.grid_filename}\"")
            if self.just_saved:
                bottom_text('Saved')
            self.message_timer -= 1
        else:
            self.just_loaded = False
            self.just_saved = False


        pygame.display.update()
        ###########################################################       


    def solve(self):
        global screen
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0]:
                self.player_grid.check_collision(pos,'button1')
                if settings_rect.collidepoint(pos):
                    self.menu_visible = not self.menu_visible
                elif edit_rect.collidepoint(pos) and self.menu_visible:
                    self.player_grid = self.hidden_grid
                    self.state = 'create'
                    self.create()
                elif create_rect.collidepoint(pos) and self.menu_visible:
                    self.player_grid = Grid()
                    self.state = 'create'
                    self.create()
                elif load_rect.collidepoint(pos) and self.menu_visible:
                    self.load_icons_visible = not self.load_icons_visible
                    grids_manager.make_grids_list()
                elif self.load_icons_visible and grids_manager.grid_click(pos):
                    self.grid_filename = grids_manager.grid_click(pos)
                    self.hidden_grid.grid = grids_manager.load_grid(self.grid_filename)
                    self.player_grid = Grid(solve = True)
                    self.just_loaded = True
                    self.message_timer = 100
                elif resize_rect.collidepoint(pos) and self.menu_visible:
                    self.resized = not self.resized
                    if self.resized:
                        screen = pygame.display.set_mode((screen_width*2, screen_height*2))
                    else:
                        screen = pygame.display.set_mode((screen_width, screen_height))
                else:
                    self.menu_visible = False
                    self.load_icons_visible = False
            elif pygame.mouse.get_pressed()[2]:
                self.player_grid.check_collision(pos,'button2')
           

        ################ < Main Screen Elements > ################
        screen.fill(color_bg)
        top_text(self.state.title())

        # < Main Grid Board Draw > 
        self.player_grid.draw()
        rows, columns = self.hidden_grid.getNumbers()
        self.player_grid.drawNumbers(rows, columns)

        # < Options Menu > #
        rotated_surface = settings_animation(settings_surface, pos)
        screen.blit(rotated_surface, settings_rect)     
           
        if self.menu_visible:
            self.show_Menu()
        if self.load_icons_visible:
            grids_manager.show_grid_icons(screen)

        # < Message > #
        if self.message_timer >= 1:
            if self.just_loaded:
                bottom_text(f"Loaded \"{self.grid_filename}\"")
            self.message_timer -= 1
        elif self.just_loaded:
            self.just_loaded = False

        ##### FILL CROSS BUTTONS #####

        ##### TIMER #####

        pygame.display.update()
        ###########################################################

    def show_Menu(self):
        if self.menu_visible:
            if self.state == 'create':
                # Play button
                pygame.draw.rect(screen, color_mid, play_rect)
                screen.blit(play_text, (play_rect.x + 12, play_rect.y + 12))

                # Save Button
                pygame.draw.rect(screen, color_mid, save_rect)
                screen.blit(save_text, (save_rect.x + 12, save_rect.y + 12))
            elif self.state == 'solve':
                # Edit button
                pygame.draw.rect(screen, color_mid, edit_rect)
                screen.blit(edit_text, (edit_rect.x + 12, edit_rect.y + 12))

                # Create Button
                pygame.draw.rect(screen, color_mid, create_rect)
                screen.blit(create_text, (create_rect.x + 8, create_rect.y + 17))

            # Load Button
            pygame.draw.rect(screen, color_mid, load_rect)
            screen.blit(load_text, (load_rect.x + 12, load_rect.y + 12))

            # Toggle Scale Button
            pygame.draw.rect(screen, color_mid, resize_rect)
            if not self.resized:
                screen.blit(text_2x, (resize_rect.x + resize_rect.width//3, resize_rect.y + int(resize_rect.height*0.25)))
            else:
                screen.blit(text_1x, (resize_rect.x + resize_rect.width//3, resize_rect.y + int(resize_rect.height*0.25)))

    def state_manager(self):
        if self.state == 'create':
            self.create()
        if self.state == 'solve':
            self.solve()        






##################################### General Setup #################################
pygame.init()
clock = pygame.time.Clock()

from pixel import Pixel
from grid import Grid
import grids_manager

# Game Screen Variables
screen_width = 500
screen_height = 500
screen = pygame.display.set_mode((screen_width,screen_height))
# pygame.display.set_icon(icon)


Pixel.screen = screen
Grid.screen = screen

pygame.display.set_caption("Pygame Picross")
color_bg = (232, 222, 210)
color_light = (163, 210, 202)
color_mid = (94, 170, 168)
color_dark = (5, 102, 118)
location = os.getcwd()
game_font =  pygame.font.Font(os.path.join(location,'resources','04B_19.TTF'),30)
small_game_font =  pygame.font.Font(os.path.join(location,'resources','04B_19.TTF'),25)

settings_hidden = pygame.Rect((0,0),(60,60))
settings_surface = pygame.image.load(os.path.join(location, 'resources', 'gear.png')).convert_alpha()
settings_surface = pygame.transform.scale(settings_surface, (50,50))
settings_rect = settings_surface.get_rect(topleft = (0,0))

play_rect = pygame.Rect((0, 70), (100, 50))
play_text = game_font.render('Play', True, color_bg)

edit_rect = pygame.Rect((0, 70), (100, 50))
edit_text = game_font.render('Edit', True, color_bg) 

save_rect = pygame.Rect((0, 120), (100, 50))
save_text = game_font.render('Save', True, color_bg)

create_rect = pygame.Rect((0, 120), (100, 50))
create_text = small_game_font.render('Create', True, color_bg)

load_rect = pygame.Rect((0, 170), (100, 50))
load_text = game_font.render('Load', True, color_bg)

resize_rect = pygame.Rect((0,220), (100,50))
text_1x = game_font.render('1x', True, color_bg) 
text_2x = game_font.render('2x', True, color_bg)

############################### < MAIN GAME LOOP > ####################################
game_state = GameState()
while True:
    game_state.state_manager()
    clock.tick(120)
#######################################################################################