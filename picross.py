import pygame, sys, os

author = 'JoshuaHM-p4'
# WIP Checklist 
# Level Grid Icons Wrapping
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
    game_text = game_font.render(message, True, color_dark)
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

    cross = False
    timer_started = False
    start_time = 0
    passed_time = 0

    def __init__(self):
        self.state = 'create'
        self.player_grid = Grid()

    def state_manager(self):
        if self.state == 'create':
            self.create()
        if self.state == 'solve':
            self.solve()        
   
    def create(self):
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0]:
                self.player_grid.change_pixel(pos,'fill')
                if resize_rect.collidepoint(pos):
                    self.resized = not self.resized
                    self.resize_everything()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if settings_rect.collidepoint(pos):
                    self.menu_visible = not self.menu_visible
                elif play_rect.collidepoint(pos) and self.menu_visible:
                    self.hidden_grid = self.player_grid 
                    self.player_grid = Grid()
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
                else: 
                    self.menu_visible = False
                    self.load_icons_visible = False 
            if pygame.mouse.get_pressed()[2]:
                self.player_grid.change_pixel(pos,'empty')

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
        
        # < Toggle Scale Button > #
        pygame.draw.rect(screen, color_light, resize_rect)
        if not self.resized:
            screen.blit(resize_icon_1, (resize_rect.x - 3, resize_rect.y - 3))
        else:
            screen.blit(resize_icon_2, (resize_rect.x + 5, resize_rect.y + 5))


        pygame.display.update()
        ##############################################################     


    def solve(self):
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.key.get_pressed()[pygame.K_x]:  #checking pressed keys
                self.cross = True
            if event.type == pygame.KEYUP:
                self.cross = False
            if pygame.mouse.get_pressed()[0]:
                if resize_rect.collidepoint(pos):
                    self.resized = not self.resized
                    self.resize_everything()
                if not self.cross:
                    self.player_grid.change_pixel(pos,'fill')
                if self.cross:
                    self.player_grid.change_pixel(pos, 'cross')
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cross_rect.collidepoint(pos):
                    self.cross = not self.cross
                elif settings_rect.collidepoint(pos):
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
                    self.player_grid = Grid()
                    self.just_loaded = True
                    self.message_timer = 100
                    self.timer_started = not self.timer_started
                    if self.timer_started:
                        self.start_time = pygame.time.get_ticks()
                else:
                    self.menu_visible = False
                    self.load_icons_visible = False
            if self.cross and pygame.mouse.get_pressed()[2]:
                self.player_grid.change_pixel(pos,'uncross')
           

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

        # < Cross Button > #
        pygame.draw.rect(screen, color_light, cross_rect)
        if self.cross:
            screen.blit(cross_active, (cross_rect.x + 17, cross_rect.y + 10))
        else:
            screen.blit(cross_inactive, (cross_rect.x + 17, cross_rect.y + 10))
        
        # < Toggle Scale Button > #
        pygame.draw.rect(screen, color_light, resize_rect)
        if not self.resized:
            screen.blit(resize_icon_1, (resize_rect.x - 3, resize_rect.y - 3))
        else:
            screen.blit(resize_icon_2, (resize_rect.x + 5, resize_rect.y + 5))
            
        # < Timer > #
        if self.timer_started:
            self.passed_time = pygame.time.get_ticks() - self.start_time
        time_text = game_font.render(str(self.passed_time/1000), True, color_mid)
        screen.blit(time_text, (screen_width//2 -30, screen_height//10))
        if self.player_grid == self.hidden_grid:
            self.timer_started = False

        pygame.display.update()
        #########################################################################

    def resize_everything(self):
        global screen, screen_height, screen_width, cross_rect, resize_rect
        if self.resized:
            screen_width = 760
            screen_height = 760
            screen = pygame.display.set_mode((screen_width, screen_height))
            Pixel.SIZE = 76      
        elif not self.resized:
            screen_width = 500
            screen_height = 500
            screen = pygame.display.set_mode((screen_width, screen_height))
            Pixel.SIZE = 50
        self.player_grid.realign()
        cross_rect = pygame.Rect((screen_width-100,screen_height//2), (50,50))
        resize_rect = pygame.Rect((screen_width-100,(screen_height//2 - 70)), (50,50))


    def show_Menu(self):
        if self.menu_visible:
            if self.state == 'create':
                # Play button
                pygame.draw.rect(screen, color_light, play_rect)
                screen.blit(play_text, (play_rect.x + 12, play_rect.y + 12))

                # Save Button
                pygame.draw.rect(screen, color_light, save_rect)
                screen.blit(save_text, (save_rect.x + 12, save_rect.y + 12))
            elif self.state == 'solve':
                # Edit button
                pygame.draw.rect(screen, color_light, edit_rect)
                screen.blit(edit_text, (edit_rect.x + 12, edit_rect.y + 12))

                # Create Button
                pygame.draw.rect(screen, color_light, create_rect)
                screen.blit(create_text, (create_rect.x + 8, create_rect.y + 17))

            # Load Button
            pygame.draw.rect(screen, color_light, load_rect)
            screen.blit(load_text, (load_rect.x + 12, load_rect.y + 12))
                

def recolor_surface(surface, color):
    """Fill all pixels of the surface with color, preserve transparency. Taken from StackOverflow """
    w, h = surface.get_size()
    r, g, b = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))


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
game_font_s =  pygame.font.Font(os.path.join(location,'resources','04B_19.TTF'),25)

cross_rect = pygame.Rect((screen_width-100,screen_height//2), (50,50))
cross_active = game_font.render('x', True, color_dark)
cross_inactive = game_font.render('x', True, color_mid)

settings_hidden = pygame.Rect((0,0),(60,60))
settings_surface = pygame.image.load(os.path.join(location, 'resources', 'icons','gear.png')).convert_alpha()
settings_surface = pygame.transform.scale(settings_surface, (50,50))
recolor_surface(settings_surface, color_dark)
settings_rect = settings_surface.get_rect(topleft = (0,0))

resize_rect = pygame.Rect((screen_width-100,(screen_height//2 - 70)), (50,50))
resize_icon_1 = pygame.image.load(os.path.join(location, 'resources', 'icons', 'resize-1.png')).convert_alpha()
resize_icon_2 = pygame.image.load(os.path.join(location, 'resources', 'icons', 'resize-2.png')).convert_alpha()
resize_icon_1 = pygame.transform.scale(resize_icon_1, (55,55))
resize_icon_2 = pygame.transform.scale(resize_icon_2, (40,40))
recolor_surface(resize_icon_1, color_dark)
recolor_surface(resize_icon_2, color_dark)
# text_1x = game_font_s.render('1x', True, color_bg) 
# text_2x = game_font_s.render('2x', True, color_bg)

play_rect = pygame.Rect((0, 100), (100, 50))
play_text = game_font.render('Play', True, color_dark)

edit_rect = pygame.Rect((0, 100), (100, 50))
edit_text = game_font.render('Edit', True, color_dark) 

save_rect = pygame.Rect((0, 150), (100, 50))
save_text = game_font.render('Save', True, color_dark)

create_rect = pygame.Rect((0, 150), (100, 50))
create_text = game_font_s.render('Create', True, color_dark)

load_rect = pygame.Rect((0, 200), (100, 50))
load_text = game_font.render('Load', True, color_dark)

############################### < MAIN GAME LOOP > ####################################
game_state = GameState()
while True:
    game_state.state_manager()
    clock.tick(120)
#######################################################################################