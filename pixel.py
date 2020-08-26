import pygame
class Pixel:
    SIZE = 50
    LIGHT = (163, 210, 202)
    DARK = (5, 103, 118)
    ColorState = [LIGHT,DARK]
    font = pygame.font.Font('mypicross/04B_19.TTF',30)

    def __init__(self,screen,x,y):
        self.screen = screen
        self.state = 0
        self.color = self.ColorState[self.state]
        self.relative_grid_pos = [x,y]
        w, h = pygame.display.get_surface().get_size()
        self.mid = (w // 2) - self.SIZE * 2.5
        self.x = self.mid+ x*self.SIZE
        self.y = self.mid+ y*self.SIZE
        self.pointlocation = [self.x, self.y]
        self.pixel_rect = pygame.Rect(
            (self.pointlocation),
            (self.SIZE,self.SIZE),
        )
        self.crossed = False
        
    
    def render(self):
        pygame.draw.rect(self.screen, self.DARK, (self.x-2,self.y-2,self.SIZE+4,self.SIZE+4),0)
        pygame.draw.rect(self.screen, self.color, self.pixel_rect)
        if self.crossed: 
            self.displayCross()

    def displayCross(self):
        x_surface = self.font.render('x', True, (94, 170, 167))
        new_pos = (self.x + self.SIZE//2, self.y + self.SIZE//2)
        x_rect = x_surface.get_rect(center = (new_pos))
        self.screen.blit(x_surface, x_rect)

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
        if not self.state and not self.crossed:
            self.crossed = True
        
    def uncross(self):
        if self.state == 0 and self.crossed:
            self.crossed = False

    def __repr__(self):
        return str(self.state)