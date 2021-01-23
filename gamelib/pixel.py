import pygame
import os 

class Pixel:
    screen = None
    LIGHT = (163, 210, 202)
    DARK = (5, 103, 118)
    ColorState = [LIGHT,DARK]
    font = pygame.font.Font('./resources/04B_19.TTF',30)
    cross_surface = font.render('x', True, (94, 170, 167))
    size = 50

    def __init__(self, pos = tuple, state = 0):
        self.state = state
        self.color = self.ColorState[self.state]
        self.crossed = False
        
        self.pos = pos
        self.align_pos(5)

    def align_pos(self, grid_size):
        w = pygame.display.get_surface().get_size()[0]
        offset = (w // 2) - self.size * grid_size//2
        self.x = offset + self.pos[0]*self.size
        self.y = offset + self.pos[1]*self.size
        self.pointlocation = [self.x, self.y]
        self.pixel_rect = pygame.Rect((self.pointlocation),(self.size,self.size),)

    def render(self):
        pygame.draw.rect(self.screen, self.DARK, (self.x-2,self.y-2,self.size+4,self.size+4),0)
        pygame.draw.rect(self.screen, self.color, self.pixel_rect)
        if self.crossed:
            self.displayCross()

    def displayCross(self):
        new_pos = (self.x + self.size//2, self.y + self.size//2)
        cross_rect = self.cross_surface.get_rect(center = (new_pos))
        self.screen.blit(self.cross_surface, cross_rect)

    ### Change Pixel State Methods ###
    def fill(self):
        if not self.state and not self.crossed:
            self.state = 1
            self.color = self.ColorState[self.state]

    def empty(self):
        if self.state == 1:
            self.state = 0
            self.color = self.ColorState[self.state]

    def cross(self):
        if self.state == 0 and not self.crossed:
            self.crossed = True

    def uncross(self):
        if self.state == 0 and self.crossed:
            self.crossed = False

    def __repr__(self):
        return str(int(self.state))

    def __eq__(self, p2):
        # 'Wrong' if the player fills a pixel where it shouldn't be 
        return 'Wrong' if self.state and not p2.state else self.state == p2.state