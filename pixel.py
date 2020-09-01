import pygame
import os
## This is script is used for rendering grids onto the screen only ##    

class Pixel:
    screen = None
    SIZE = 50
    LIGHT = (163, 210, 202)
    DARK = (5, 103, 118)
    ColorState = [LIGHT,DARK]
    font = pygame.font.Font(os.path.join(os.getcwd(),'resources','04B_19.TTF'),int(SIZE*0.6))
    cross_surface = font.render('x', True, (94, 170, 167))

    def __init__(self, pos, state = 0):
        self.state = state
        self.color = self.ColorState[self.state]
        self.crossed = False

        self.pos = pos
        self.align_pos()

    def align_pos(self):
        w = pygame.display.get_surface().get_size()[0]
        self.offset = (w // 2) - self.SIZE * 2.5
        self.x = self.offset + self.pos[0]*self.SIZE
        self.y = self.offset + self.pos[1]*self.SIZE
        self.pointlocation = [self.x, self.y]
        self.pixel_rect = pygame.Rect(
            (self.pointlocation),
            (self.SIZE,self.SIZE),
        )

    def render(self):
        pygame.draw.rect(self.screen, self.DARK, (self.x-2,self.y-2,self.SIZE+4,self.SIZE+4),0)
        pygame.draw.rect(self.screen, self.color, self.pixel_rect)
        if self.crossed:
            self.displayCross()

    def displayCross(self):
        new_pos = (self.x + self.SIZE//2, self.y + self.SIZE//2)
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
    